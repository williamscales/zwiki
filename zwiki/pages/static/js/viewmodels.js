function PageViewModel(slug) {
    var self = this;

    self.STATUS_OWNED = "owned";
    self.STATUS_UNLOCKED = "unlocked";
    self.STATUS_LOCKED = "locked";
    self.STATUS_EXPIRED = "expired";

    self.title = ko.observable();
    self.slug = ko.observable();
    self.datePublished = ko.observable();
    self.editSummary = ko.observable();
    self.content = ko.observable();
    self.displayMode = ko.observable("view");
    self.lockState = ko.observable();

    self.fetchPage = function () {
        $.ajax({
            url: "/page/" + slug,
            type: "GET",
        }).done(function (page) {
            self.title(page.title);
            self.slug(page.slug);
            self.datePublished(page.date_published);
            self.editSummary(page.edit_summary);
            self.content(page.content);
        });
    };

    self.acquireLock = function (success, failure) {
        var checkLockResponse = function (response) {
            if ((response.state === self.STATUS_OWNED)) {
                success(response.state);
            } else {
                failure(response.state);
            };
        };

        var checkStatus = function (response) {
            self.lockState(response.state);
            if ((response.state === self.STATUS_OWNED) || (response.state === self.STATUS_UNLOCKED) || (response.state === self.STATUS_EXPIRED)) {
                var csrftoken = $.cookie('csrftoken');
                $.ajax({
                    url: "/page/status/" + slug,
                    type: "PUT",
                    contentType: "application/json; charset=UTF-8",
                    data: JSON.stringify({ state: self.STATUS_LOCKED }),
                    headers: { "X-CSRFToken": csrftoken }
                }).done(checkLockResponse);
            } else if (response.state === self.STATUS_LOCKED) {
                failure(response.state);
            };
        };

        $.ajax({
            url: "/page/status/" + slug,
            type: "GET",
        }).done(checkStatus);
    }

    self.addPage = function (page) {
        self.myobjects.push(page);
    };

    self.removePage = function (page) {
        self.myobjects.remove(page);
    };

    self.editPage = function (page) {
        var success = function (state) {
            self.displayMode("edit");
        };
        var failure = function (state) {
            alert("Couldn't lock page for editing. Response: '"+ state +"'");
        };
        self.acquireLock(success, failure);
    };

    self.cancelEdit = function (page) {
        self.fetchPage();
        self.displayMode("view");
        self.unlock();
    };

    self.unlock = function () {
        var csrftoken = $.cookie('csrftoken');
        $.ajax({
            url: "/page/status/" + slug,
            type: "PUT",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify({ state: self.STATUS_UNLOCKED }),
            headers: { "X-CSRFToken": csrftoken },
        }).done(alert('Unlocked page'));
    };

    self.commitEdit = function (formElement) {
        var success = function (state) {
            var csrftoken = $.cookie('csrftoken');
            $.ajax({
                url: "/page/" + slug,
                type: "PUT",
                contentType: "application/json; charset=UTF-8",
                data: ko.toJSON(self),
                headers: { "X-CSRFToken": csrftoken },
            }).done(function (response) {
                alert("Saved page!");
                self.unlock();
            });
            self.displayMode("view");
        };
        var failure = function (state) {
            alert("Couldn't lock page to commit edit");
        };
        self.acquireLock(success, failure);
    };
}

home_page = new PageViewModel("home");
home_page.fetchPage();
ko.applyBindings(home_page);
