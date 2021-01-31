$(function() {
    'use strict';

    var adminSideBar = function() {
        $('#sidebarCollapse').on('click', function() {
            $('#sidebar').toggleClass('active');
            $(this).toggleClass('active');
        });
    };

    var logoutSwal = function() {
        $('.logout').on('click', function() {
            // swal({
            //     title: "Are you sure?",
            //     icon: "warning",
            //     buttons: ["No", "Yes"],
            //     dangerMode: true,
            // }).then((willDelete) => {
            //     if (willDelete) {
            //         $.ajax({
            //             url: "/admin/logout/",
            //             success: function(result) { location.reload(); }
            //         });
            //     } else {}
            // });
            Swal.fire({
                title: 'Are you sure?',
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: "/admin/logout/",
                        success: function(result) { location.reload(); }
                    });
                }
            })
        });
    };

    var sidebarCollapse = function() {
        let loc = window.location.pathname;

        $('a[href="' + loc + '"]').css({ "opacity": "1" }).parent().parent().addClass("show").prev().css({ "opacity": "1" });
    };

    var tableManager = function() {
        $('.tablemanager').tablemanager({
            firstSort: [
                [1, 0],
                [2, 0],
                [3, 0],
                [4, 0],
            ],
            // disable: ["last"],
            appendFilterby: true,
            dateFormat: [
                [5, "mm-dd-yyyy"]
            ],
            debug: false,
            vocabulary: {
                voc_filter_by: 'Search By',
                voc_type_here_filter: 'Search...',
                voc_show_rows: 'Rows Per Page'
            },
            pagination: false,
            showrows: [5, 10, 20, 50, 100],
            // disableFilterBy: [1]
        });
    }
    var loadMoreRows = function() {
        let i;
        for (i = 0; i < 5; i++) { $('.tablemanager').find("tbody tr").eq(i).addClass('active'); }

        $('#loadmore-btn').on("click", function() {
            var rows = $('.tablemanager').find("tbody tr"),
                rlen = rows.length;

            var $rows = $('.tablemanager').find("tbody tr")
            var last = $rows.filter('.active:last').index();

            if ((last + 1) == rlen) {
                Swal.fire("All Records loaded");
            } else {
                $rows.filter(':lt(' + (last + 10) + ')').addClass('active').css({ "display": "" });

            }
        });
    }
    var disableBtn = function() {
        $('.disable-btn').on("click", function() {

            Swal.fire({
                title: 'Are you sure?',
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: "",
                        success: function(data) {
                            if (true) {
                                Swal.fire("User disabled successfully.", "", "success");
                            }
                        }
                    });
                }
            })

            // .then(name => {
            //     if (!name) throw null;

            //     //return fetch(`url`);
            //     return true;

            // })
            // .then(results => {
            //     if (results)
            //         Swal.fire("User disabled successfully.", {
            //             icon: "success",
            //         });
            //     else {

            //         Swal.fire("Oh no!", "The AJAX request failed!", "error");
            //         Swal.close();
            //     }

            // })
            // .catch(err => {
            //     if (err) {
            //         swal("Oh no!", "The AJAX request failed!", "error");
            //     } else {
            //         swal.stopLoading();
            //         swal.close();
            //     }
            // });
        });

    }

    var dyanmicBreads = function() {
        let loc = window.location.pathname;
        var $this = $("#sidebar").find('a[href="' + loc + '"]');
        if (loc != "/admin/") {
            $this.parents('li').each(function(n, li) {
                var $a = $(li).children('a').clone();
                var url = $(li).children('a').attr('href').split('=').toString();
                if ($a.hasClass = ("collapse")) {
                    $a.removeClass();
                }
                if (url == loc) {
                    $('.breadcrumb').prepend('<li class="breadcrumb-item active">' + $a.get(0).innerHTML + '</li>');
                } else {
                    $('.breadcrumb').prepend('<li class="breadcrumb-item">' + $a.get(0).outerHTML + '</li>');
                }
            });

            $('.breadcrumb').prepend('<li class="breadcrumb-item"><a href="/admin/">Dashboard</a></li>');
        } else {
            //$('.breadcrumb').html('<a href="/admin/">DASHBOARD /</a>');
        }
    }


    var userViewDets = function() {
        $(".userViewDets").on("click", function() {
            $.ajax({
                url: $(this).attr("data-view-url"),
                datatype: JSON,
                success: function(data) {
                    var details = "Bank Name : " + data.bankName + "\n" +
                        "Bank IFSC CODE : " + data.bankifscCode + "\n" +
                        "Account Number : " + data.accNo + "\n" +
                        "Account Holder Name : " + data.accName + "\n" +
                        "Pan No : " + data.panNo + "\n" +
                        "Pan Name : " + data.panName;

                    Swal.fire(
                        'User Verification Details',
                        loopValues(data),
                        // "<div class=''><div class='row'><span class='col'></span><span class='col'></span></div></div>",
                    )


                }
            });
        });

        function loopValues(data) {
            var userDetails = "";
            var label = ['Bank Name : ', 'Bank IFSC CODE : ', 'Account Number : ', 'Account Holder : ', 'Pan No : ', 'Pan Name : '];
            let i = 0;
            for (var val in data) {
                userDetails += "<div class='row'><span class='col text-right'>" + label[i++] + "</span><span class='col text-left'>" + data[val] + "</span></div>"
            }
            return userDetails;
        }
    }

    // var userDocuDownload = function() {
    //     $("#userDocuDownload").on("click", function() {
    //         $.ajax({
    //             url: $(this).attr("data-url"),
    //             datatype: JSON,
    //             success: function(data) {}
    //         });
    //     });
    // }

    var verifyChk = function() {
        $(".verifyChk").on("click", function() {
            $.ajax({
                url: $(this).attr("data-verify-url"),
                datatype: JSON,
                success: function(data) {
                    if (data.is_verified) {
                        Swal.fire({
                            title: 'Are you sure?',
                            icon: 'warning',
                            showCancelButton: true,
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                Swal.fire("User Verified", "", "success");
                            }
                        })
                    }
                }
            });
        });
    }


    var addBadgesInput = function() {
        $('#addBadge').on("click", function() {
            swal("Enter the badge name :", {
                    content: "input",
                })
                .then((value) => {
                    swal(`${value} Badge Added`);
                });
        });
    }
    var badgeDelete = function() {
        $('#badge').on("click", function() {
            swal({
                title: "Are you sure you want to delete this badge?",
                text: "You will not be able to see the badge entries of this anymore!",
                icon: "warning",
                buttons: [
                    'No, cancel it!',
                    'Yes, I am sure!'
                ],
                dangerMode: true,
            }).then(function(isConfirm) {
                if (isConfirm) {
                    swal({
                        title: 'Deleted',
                        text: 'The Badge is deleted success fully',
                        icon: 'success'
                    }).then(function() {
                        form.submit();
                    });
                } else {
                    swal("Cancelled", "The Badge is safe :)", "error");
                }
            });
        });
    }

    /////////////// CREATIVE CATEGORIES ///////////////
    var addMainCrtCat = function() {
        $("#add-main-crt-cat").on("click", function() {
            CatOps("Add Category", "Main Creative Item Category", "Enter category", $(this).attr("data-add-mainCrtCat"), "crt_category_name");

        });
    };


    var addSubCrtCat = function() {
        $("#add-sub-crt-cat").on("click", function() {
            CatOps("Add Sub Category", "Sub Creative Item Category", "Enter category", $(this).attr("data-add-subCrtCat"), "crt_sub_category_name");
        });
    };

    var editMainCrtCat = function() {
            $(".edit-main-crt-cat").on("click", function() {

                const url = $(this).attr("data-edit-mainCrtCat");
                $.ajax({
                    type: "GET",
                    url: url,
                    datatype: 'json',
                    success: function(response) {
                        if (response != null) {
                            CatOps("Edit Category", "Main Creative Item Category", "Edit category", url, "crt_category_name", response.crt_category_name);
                        } else {
                            Swal.fire(
                                'Error',
                                `Some error occured, Try Again..`,
                                'error'
                            )
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
        // 
    var editSubCrtCat = function() {
        $(".edit-sub-crt-cat").on("click", function() {
            const url = $(this).attr("data-edit-subCrtCat");
            $.ajax({
                type: "GET",
                url: url,
                datatype: 'json',
                success: function(response) {
                    if (response != null) {
                        CatOps("Edit Category", "Sub Creative Item Category", "Edit Sub category", url, "crt_sub_category_name", response.crt_sub_category_name);
                    } else {
                        Swal.fire(
                            'Error',
                            `Some error occured, Try Again..`,
                            'error'
                        )
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
    var delCrtCat = function() {
        $(".del-each-crt-cat").on("click", function() {

            Swal.fire({
                title: 'Are you sure?',
                text: "Once done action cannot be revert!!",
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.isConfirmed) {
                    delCat($(this).attr("data-del"));
                }
            })


        });
    };
    /////////////// SCRAP CATEGORIES ///////////////


    var addMainScpCat = function() {
        $("#add-main-scp-cat").on("click", function() {
            CatOps("Add Category", "Main Scrap Item Category", "Enter category", $(this).attr("data-add-mainScpCat"), "scp_category_name");

        });
    };


    var addSubScpCat = function() {
        $("#add-sub-scp-cat").on("click", function() {
            CatOps("Add Sub Category", "Sub Scrap Item Category", "Enter category", $(this).attr("data-add-subScpCat"), "scp_sub_category_name");
        });
    };

    var editMainScpCat = function() {
            $(".edit-main-scp-cat").on("click", function() {

                const url = $(this).attr("data-edit-mainScpCat");
                $.ajax({
                    type: "GET",
                    url: url,
                    datatype: 'json',
                    success: function(response) {
                        if (response != null) {
                            CatOps("Edit Category", "Main Scrap Item Category", "Edit category", url, "scp_category_name", response.scp_category_name);
                        } else {
                            Swal.fire(
                                'Error',
                                `Category name not found, Try Again..`,
                                'error'
                            )
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
        // 
    var editSubScpCat = function() {
        $(".edit-sub-scp-cat").on("click", function() {
            const url = $(this).attr("data-edit-subScpCat");
            $.ajax({
                type: "GET",
                url: url,
                datatype: 'json',
                success: function(response) {
                    if (response != null) {
                        CatOps("Edit Category", "Sub Scrap Item Category", "Edit Sub category", url, "scp_sub_category_name", response.scp_sub_category_name);
                    } else {
                        Swal.fire(
                            'Error',
                            `Category name not found, Try Again..`,
                            'error'
                        )
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
    var delScpCat = function() {
        $(".del-each-scp-cat").on("click", function() {

            Swal.fire({
                title: 'Are you sure?',
                text: "Once done action cannot be revert!!",
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.isConfirmed) {
                    delCat($(this).attr("data-del"));
                }
            })


        });
    };
    var disableProdBtn = function() {
        $('.prod-disable').on("click", function() {

            Swal.fire({
                title: 'Are you sure?',
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: "",
                        success: function(data) {
                            if (true) {
                                Swal.fire("Product disabled successfully.", "", "success");
                            }
                        }
                    });
                }
            })
        });
    }

    /* SEND EMAILS */
    var selectUserEmail = function() {

        let values = [];
        let $inputTag = $("#user-email");
        //let email = [];
        let i = 0

        $(".tablemanager.select-email").tablemanager({
            disable: ['first'],
        })

        $('#selectAll').click(function(e) {
            $(this).closest('table').find('td input:checkbox').prop('checked', this.checked);
        });

        $("#addEmails").click(function(e) {
            //   let dbEmail = [];
            $.each($("td input:checked").closest("tr").find("td:last-child"),
                function() {
                    const email = $(this).text();
                    if (validateEmail(email)) {
                        values.push(email);
                    } else {
                        $('.inputTag').before('<span class="invalid-email-chip"><span class="content">' + email + '</span><a class="email-remove">×</a></span>');
                    }

                });


            $('input:checked').prop('checked', false);
            $('#addEmailModal').modal("hide");

            addEmails(values);
            //alert("val---" + values.join(", "));

        });


        $inputTag.keydown(function(e) {
            $inputTag.css('border', '')
            if (e.keyCode === 13 || e.keyCode === 32 || e.keyCode === 188) {
                let getEmail = $inputTag.val();
                e.preventDefault();
                if (validateEmail(getEmail)) {
                    if (!values.includes(getEmail)) {
                        $('.inputTag').before('<span class="email-chip"><span class="content">' + getEmail + '</span><a class="email-remove">×</a></span>');
                        $inputTag.val('');

                        //email[i++] = getEmail
                        values.push(getEmail);
                        // console.log(email);
                        $("#user-email-list").val(values)
                    } else {
                        Swal.fire("Email already exists in the list");
                    }
                } else {
                    $inputTag.css('border', '1px solid red')
                }

            }

        });

        function addEmails(data) {
            if (data) {
                var newEmail = [];
                // $.each(values, (k, v) => {
                //     newEmail.push(v);
                // });
                $("#user-email-list").val('');
                $(".inputTag").siblings().remove('.email-chip');
                $.each(data, function(key, val) {
                    if (validateEmail(val)) {
                        $('.inputTag').before('<span class="email-chip"><span class="content">' + val + '</span><a class="email-remove">×</a></span>');
                        $inputTag.val('');

                        newEmail.push(val);
                        $("#user-email-list").val(newEmail)
                    } else {
                        $('.inputTag').before('<span class="invalid-email-chip"><span class="content">' + val + '</span><a class="email-remove">×</a></span>');
                        $(".invalid-email").css('border', '1px solid red')
                    }
                })

            }

        }

        function updateInputEmails(data) {
            if (data) {
                var updatedEmails = [];
                // console.log(data)
                $("#user-email-list").val('');
                $.each(data, function(key, val) {
                    if (validateEmail(val)) {
                        updatedEmails.push(val)
                        $("#user-email-list").val(updatedEmails)
                    }
                })

            }
        }

        function validateEmail(val) {
            return /^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,6}$/.test(val);
        }




        $(document).on("click", '.email-remove', function(e) {
            var rmEmail = $(this).siblings().text();
            if ($(this).parent().hasClass("email-chip")) {
                values.splice(values.indexOf(rmEmail), 1);
            }
            $(this).parent().slice(values.indexOf(rmEmail)).remove();
            // console.log(values);
            updateInputEmails(values);

        });



    }


    $(function() {
        adminSideBar();
        logoutSwal();
        sidebarCollapse();
        tableManager();
        loadMoreRows();
        disableBtn();
        dyanmicBreads();
        userViewDets();
        // userDocuDownload();
        verifyChk();
        addBadgesInput();
        badgeDelete();
        // deleteAssignedBadge();
        addMainCrtCat();
        addSubCrtCat();
        editMainCrtCat();
        editSubCrtCat();
        delCrtCat();

        addMainScpCat();
        addSubScpCat();
        editMainScpCat();
        editSubScpCat();
        delScpCat();

        disableProdBtn();

        selectUserEmail();



    });

    /////////////// CREATIVE CATEGORIES ///////////////
    function delCat(url) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function(response) {
                if (response.saved) {
                    Swal.fire(response.itemName + ' deleted', "", "success");
                    setTimeout(function() { location.reload() }, 2000);

                } else {
                    Swal.fire(
                        'Error',
                        response.itemName + 'not deleted. \n' + response.message + ', Try Again..',
                        'error'
                    )
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                Swal.fire(
                    jqXHR.status + "",
                    textStatus + " : " + errorThrown,
                    'error'
                )
            }

        })

    };

    function CatOps(titl, inLbl, inPlace, url, field, inVal) {
        (async() => {
            const { value: crtCat } = await Swal.fire({
                title: titl,
                input: "text",
                inputLabel: inLbl,
                inputPlaceholder: inPlace,
                inputValue: inVal || "",
                inputValidator: (value) => {
                    if (!value) {
                        return 'You need to write something!'
                    }
                }
            })
            if (crtCat) {
                Swal.fire({
                    title: 'Are you sure?',
                    icon: 'warning',
                    showCancelButton: true,
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes',

                }).then((result) => {
                    if (result.isConfirmed) {
                        let postDataObj = {
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                            action: 'post',
                        };
                        postDataObj[field] = `${crtCat}`;

                        $.ajax({
                            type: "POST",
                            url: url,
                            dataType: 'json',
                            data: postDataObj,
                            success: function(response) {
                                if (response.saved) {
                                    Swal.fire(`${crtCat} added`, "", "success");
                                    setTimeout(function() { location.reload() }, 1000);


                                } else if (response.updated) {

                                    Swal.fire(inVal + ` updated to '${crtCat}' `, "", "success");
                                    setTimeout(function() { location.reload() }, 2000);

                                } else {
                                    Swal.fire({
                                        title: 'Error',
                                        html: `${crtCat} not added.` + "<br/>" + response.message + `<br/> Try Again..`,
                                        icon: 'error'
                                    })
                                }
                            },
                            error: function(jqXHR, textStatus, errorThrown) {

                                Swal.fire(
                                    jqXHR.status + "",
                                    textStatus + " : " + errorThrown,
                                    'error'
                                )
                            }

                        })
                    }
                })
            }
        })()
    };



});


//*******************************************/
// AJAX FOR FETCH CATEG. DATA
// $.ajax({
//     url: $(this).attr("data-url-cat"),
//     datatype: "json",
//     success: function(data) {
//         //    alert(data.mainCatName[0]["Home Decor"]);
//         $.each(data.mainCatName, function(key) {
//             $.each(data.mainCatName[key], function(k, v) {
//                 console.log(k);
//                 console.log(v);
//             });

//         });

//     }
// })