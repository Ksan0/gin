var GIN = {
    AjaxErrors: {
        NONE: "OK",
        BAD_METHOD: "BAD_METHOD",
        BAD_FORM: "BAD_FORM",
        BAD_SESSION: "BAD_SESSION",
        BAD_LOGIN_OR_PASSWORD: "BAD_LOGIN_OR_PASSWORD",
        INTERNAL_ERROR: "INTERNAL_ERROR",

        get_error: function (data) {
            return data.status;
        }
    },

    Dialog: null
};