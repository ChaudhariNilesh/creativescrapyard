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
                voc_filter_by: 'Filter By',
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
            $('.breadcrumb').html('<a href="/admin/">DASHBOARD /</a>');
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
    var addMainCrtCat = function() {
        $("#add-main-cat").on("click", function() {
            // $("#addMainCatModal").modal("show");
            (async() => {
                const { value: mainCrtCat } = await Swal.fire({
                    title: 'Add Category',
                    input: 'text',
                    inputLabel: 'Main Creative Item Category',
                    inputPlaceholder: 'Enter category'
                })

                if (mainCrtCat) {
                    Swal.fire({
                        title: 'Are you sure?',
                        icon: 'warning',
                        showCancelButton: true,
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Yes'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            console.log(`${mainCrtCat}`);
                            $.ajax({
                                type: "POST",
                                url: $(this).attr("data-add-mainCrtCat"),
                                dataType: 'json',
                                data: {
                                    crt_category_name: `${mainCrtCat}`,
                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                    action: 'post'
                                },
                                success: function(response) {
                                    if (response.saved) {
                                        Swal.fire(`${mainCrtCat} added`, "", "success");
                                        location.reload();

                                    } else {
                                        Swal.fire(
                                            'Error',
                                            `${mainCrtCat} not added. \n Some error occured, Try Again..`,
                                            'error'
                                        )
                                    }
                                }

                            })


                        }
                    })
                }
            })()

            // $.ajax({
            //     url: $(this).attr("data-url-cat"),
            //     datatype: "json",
            //     success: function(data) {}
            // })
        });
    };

    var loadCats = function() {
        $.ajax({
            url: $(this).attr("data-url-cat"),
            datatype: "json",
            success: function(data) {
                //    alert(data.mainCatName[0]["Home Decor"]);
                var i = 0
                $.each(data.mainCatName, function(key) {
                    $.each(data.mainCatName[key], function(k, v) {
                        console.log(k);
                        console.log(v);
                    });

                });

            }
        })
    }
    var addSubCrtCat = function() {
        $("#add-sub-crt-cat").on("click", function() {
            $("#addSubCatModal").modal("show");

        });
    };

    //****************** */
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
    //****************** */
    var editMainCrtCat = function() {
        $("#edit-mainCrtCat").on("click", function() {
            $("#addSubCatModal").modal("show");
            $.ajax({
                url: $(this).attr("data-url-cat"),
                datatype: "json",
                success: function(data) {
                    //    alert(data.mainCatName[0]["Home Decor"]);
                    // var i = 0
                    // $.each(data.mainCatName, function(key) {
                    //     $.each(data.mainCatName[key], function(k, v) {
                    //         console.log(k);
                    //         console.log(v);
                    //     });

                    // });

                }
            })
        });
    };
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

        addMainCrtCat();
        addSubCrtCat();
        editMainCrtCat();
    });


});