function Message(title, message) {
    var self = this;

    self.title = ko.observable(title);
    self.message = ko.observable(message);
};


function MessagesViewModel(messages) {
    var self = this;

    self.messages = ko.observableArray(messages);

    self.addMessage = function (message) {
        self.messages.push(message);
        // Set a jquery timer here to eventually call removeMessage and clean it
        // up.
        // Avoid a memory leak though
    };

    self.removeMessage = function (message) {
        self.messages.remove(message);
    };
};


function PageHistoryViewModel() {
    var self = this;

    self.history = ko.observableArray();
    self.displayMode = ko.observable("hidden");
    self.currentTitle = ko.observable();

    self.add = function (data) {
        self.history.push(data);
    };

    self.removeAll = function () {
        self.history.removeAll();
    };
};


// Corresponds to zwiki.pages.models.Page
function PageViewModel(slug, messages) {
    var self = this;

    STATUS_OWNED = "owned";
    STATUS_UNLOCKED = "unlocked";
    STATUS_LOCKED = "locked";
    STATUS_EXPIRED = "expired";

    self.title = ko.observable();
    self.slug = ko.observable();
    self.date_published = ko.observable();
    self.edit_summary = ko.observable();
    self.content = ko.observable();
    self.html = ko.observable();
    self.displayMode = ko.observable("view");
    self.lockState = ko.observable();
    self.pageHistory = new PageHistoryViewModel();

    // Fetches the page data from the server using AJAX and populates the
    // PageViewModel
    self.fetchPage = function () {
        $.ajax({
            url: "/page/" + slug + "/",
            type: "GET",
        }).done(function (page) {
            self.updatePageValues(page);
        });
    };

    self.updatePageValues = function (page) {
        self.title(page.title);
        self.pageHistory.currentTitle(page.title);
        self.slug(page.slug);
        self.date_published(page.date_published);
        self.edit_summary(page.edit_summary);
        self.content(page.content);
        self.html(page.html);
    };

    // Tries to lock the page for editing. Success and failure are callbacks
    // which will be run if the request succeeds or fails. They receive an
    // object containing a status and possibly a message.
    self.acquireLock = function (success, failure) {
        var checkLockResponse = function (response) {
            if ((response.state === STATUS_OWNED)) {
                success(response.state);
            } else {
                failure(response.state);
            };
        };

        var checkStatus = function (response) {
            self.lockState(response.state);
            if ((response.state === STATUS_OWNED) || (response.state === STATUS_UNLOCKED) || (response.state === STATUS_EXPIRED)) {
                var csrftoken = $.cookie('csrftoken');
                $.ajax({
                    url: "/page/status/" + slug + "/",
                    type: "PUT",
                    contentType: "application/json; charset=UTF-8",
                    data: JSON.stringify({ state: STATUS_LOCKED }),
                    headers: { "X-CSRFToken": csrftoken }
                }).done(checkLockResponse);
            } else {
                failure(response.state);
            };
        };

        $.ajax({
            url: "/page/status/" + slug + "/",
            type: "GET",
        }).done(checkStatus);
    }

    // Tries to unlock the page so that others can edit it.
    self.releaseLock = function () {
        var csrftoken = $.cookie('csrftoken');
        $.ajax({
            url: "/page/status/" + slug + "/",
            type: "PUT",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify({ state: STATUS_UNLOCKED }),
            headers: { "X-CSRFToken": csrftoken },
        }).done(function (response) {
            if (! response.state === STATUS_UNLOCKED) {
                messages.addMessage(new Message("There was a problem unlocking the page.", "Page lock state: " + state));
            };
        });
    };

    // Puts the page into edit mode after locking it
    self.editPage = function () {
        var success = function (state) {
            messages.addMessage(new Message("Locked for editing", "Until ..."));
            if (self.pageHistory.displayMode() === "history") {
                self.hideHistory();
            }
            self.displayMode("edit");
        };
        var failure = function (state) {
            messages.addMessage(new Message("Couldn't lock page for editing", "Page lock state: " + state));
        };
        self.acquireLock(success, failure);
    };

    // Discards the edit-in-progress and unlocks the page
    self.cancelEdit = function (page) {
        self.fetchPage();
        self.displayMode("view");
        self.releaseLock();
        messages.addMessage(new Message("Canceled edit.", "The page is no longer locked for editing"));
    };

    // Sends the edited page to the server and unlocks the page.
    self.commitEdit = function (formElement) {
        var success = function (state) {
            var csrftoken = $.cookie('csrftoken');
            $.ajax({
                url: "/page/" + slug + "/",
                type: "PUT",
                contentType: "application/json; charset=UTF-8",
                // We don't need to send the page HTML to the server (it will be
                // re-generated automatically), so we exclude it:
                data: ko.toJSON(self, function (k,v) {
                    return (k == "html" ? undefined : v);
                }),
                headers: { "X-CSRFToken": csrftoken },
            }).done(function (data) {
                messages.addMessage(new Message("Saved page!", ""));
                self.updatePageValues(data);
                self.releaseLock();
            });
            self.displayMode("view");
        };
        var failure = function (state) {
            messages.addMessage(new Message("Couldn't lock page to commit edit.", "Page lock state: " + state));
        };
        self.acquireLock(success, failure);
    };

    // Fetches the page history using AJAX
    self.fetchHistory = function () {
        $.ajax({
            url: "/page/history/" + slug + "/",
            type: "GET",
        }).done(function (data) {
            self.pageHistory.removeAll();
            for (var i=0; i<data.length; i++) {
                self.pageHistory.add(data[i]);
            };
        });
    };

    self.viewHistory = function () {
        self.fetchHistory();
        self.displayMode("hidden");
        self.pageHistory.displayMode("history");
        $("#view_history_link").hide();
        $("#view_page_link").show();
    };

    self.hideHistory = function () {
        self.pageHistory.displayMode("hidden");
        self.displayMode("view");
        $("#view_history_link").show();
        $("#view_page_link").hide();
    };
}

messages = new MessagesViewModel([]);
home_page = new PageViewModel("home", messages);
home_page.fetchPage();
ko.applyBindings(home_page, $("#page")[0]);
ko.applyBindings(home_page, $("#sidebar")[0]);
ko.applyBindings(home_page.pageHistory, $("#page_history")[0]);
ko.applyBindings(messages, $("#messages")[0]);
