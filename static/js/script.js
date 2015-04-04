False = false;
True = true;

var GIN = {
    AjaxResponseKeys: {
        FIELDS_ERRORS: "fields_errors",
        REDIRECT: "redirect",
        CREATION_ID: "creation_id",
        CREATION_DATA: "creation_data",
        CREATION_DATE: "creation_date"
    },

    RegForm: null
};


GIN.RegForm = function(form_id, method, url, on_ctrl_enter, send_on_init, f_success, f_error) {
    var form = $("#" + form_id);

    var f_send = function () {
        form.find(".form_error").html("");
        $.ajax({
            method: method,
            url: url,
            data: form.serialize(),
            success: function (data, textStatus, jqXHR) {
                var fields_errors = data[GIN.AjaxResponseKeys.FIELDS_ERRORS];
                if (fields_errors) {
                    for(var field in fields_errors) {
                        form.find("." + field + "_error").html(fields_errors[field]);
                    }
                } else if (f_success) {
                    f_success(data, textStatus, jqXHR, form);
                }
                var redirect = data[GIN.AjaxResponseKeys.REDIRECT];
                if (redirect) {
                    window.location.replace(redirect);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (f_error) {
                    f_error(jqXHR, textStatus, errorThrown);
                }
            }
        });
        return false;
    };

    form.find(".form_submit_button").on("click", function () {
        return f_send();
    });
    if (on_ctrl_enter) {
        form.on("keydown", function (event) {
            if (event.keyCode == 13 && event.ctrlKey) {
                return f_send();
            }
        });
    }
    if (send_on_init) {
        f_send();
    }
};