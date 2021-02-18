$(function() {
    'use strict';
    var signUpForm = () => {
        $("#signUpForm").submit(function(e) {
            e.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.attr("data-validation"),
                data: form.serialize(),
                type: 'post',
                context: form,
                dataType: 'json',
                success: function(data) {
                    //console.log(data);
                    if (data.errors) {
                        //$("form input[type='text']").removeClass("is-invalid is-valid");
                        $(".invalid-feedback").remove();
                        $.each(data, function(k, v) {
                            if (k != "errors") {
                                // console.log(data[k].is_valid)
                                if (data[k].is_valid) {
                                    $("#" + k).removeClass("is-valid is-invalid");
                                    $("#" + k).addClass("is-valid");
                                    if (k == 'password') {

                                        $("input[type='password']").removeClass("is-valid is-invalid");
                                        $("input[type='password']").addClass("is-valid");
                                    }

                                } else {
                                    $("#" + k).removeClass("is-valid is-invalid");
                                    $("#" + k).addClass("is-invalid").after("<div class='invalid-feedback'>" + data[k].msg + "</div>");
                                    if (k == 'password') {
                                        $("input[type='password']").removeClass("is-valid is-invalid");
                                        $("input[type='password']").addClass("is-invalid").after("<div class='invalid-feedback'>" + data[k].msg + "</div>");
                                    }
                                }
                            }
                        });
                    } else {
                        this.off('submit');
                        this.submit();
                    }

                },
                error: function(jqXHR, textStatus, errorThrown) {
                    Swal.fire(
                        jqXHR.status + "",
                        textStatus + " : " + errorThrown,
                        'error'
                    )
                }
            });
        });
    }

    $(function() {
        signUpForm()
    });
});