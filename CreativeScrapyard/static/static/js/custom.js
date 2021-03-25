$(function() {
    'use strict';

    var responsiveTab = function() {
        $('#horizontalTab-arrival').easyResponsiveTabs({
            type: 'default', //Types: default, vertical, accordion           
            width: 'auto', //auto or any width like 600px
            fit: true, // 100% fit in a container
            //closed: 'accordion', // Start closed if in accordion view
            activate: function(event) { // Callback function if tab is switched
            }
        });

    };

    var prodGallery = function() {

        var sync1 = $("#sync1");
        var sync2 = $("#sync2");
        var slidesPerPage = 4;
        var syncedSecondary = true;
        sync1.owlCarousel({
            items: 1,
            slideSpeed: 2000,
            nav: false,
            autoplay: false,
            dots: false,
            loop: true,
            responsiveRefreshRate: 200,
        }).on('changed.owl.carousel', syncPosition);
        sync2
            .on('initialized.owl.carousel', function() {
                sync2.find(".owl-item").eq(0).addClass("current");
            })
            .owlCarousel({
                items: slidesPerPage,
                dots: false,
                nav: true,
                navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'], //we will be using font awesome icon here
                margin: 20,
                smartSpeed: 200,
                slideSpeed: 500,
                slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
                responsiveRefreshRate: 100
            }).on('changed.owl.carousel', syncPosition2);

        function syncPosition(el) {
            //if you set loop to false, you have to restore this next line
            //var current = el.item.index;
            //if you disable loop you have to comment this block
            var count = el.item.count - 1;
            var current = Math.round(el.item.index - (el.item.count / 2) - .5);
            if (current < 0) {
                current = count;
            }
            if (current > count) {
                current = 0;
            }
            //end block
            sync2
                .find(".owl-item")
                .removeClass("current")
                .eq(current)
                .addClass("current");
            var onscreen = sync2.find('.owl-item.active').length - 1;
            var start = sync2.find('.owl-item.active').first().index();
            var end = sync2.find('.owl-item.active').last().index();
            if (current > end) {
                sync2.data('owl.carousel').to(current, 100, true);
            }
            if (current < start) {
                sync2.data('owl.carousel').to(current - onscreen, 100, true);
            }

        }

        function syncPosition2(el) {

            if (syncedSecondary) {
                var number = el.item.index;
                sync1.data('owl.carousel').to(number, 100, true);

                prodLens();

            }
        }

        sync2.on("click", ".owl-item", function(e) {
            e.preventDefault();
            var number = $(this).index();
            sync1.data('owl.carousel').to(number, 300, true);
            prodLens();

        });


    };

    // var flatZoom = function() {
    //     var $easyzoom = $('.easyzoom').easyZoom();
    // };

    var ArtistProductGal = function() {
        var owl = $('#owl-artist-products.owl-prod');
        owl.owlCarousel({
            loop: false,
            autoplay: true,
            autoplayTimeOut: 3000,
            dots: false,
            items: 4,
            nav: true,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsiveClass: true,
        });

        $(".next").click(function() {
            owl.trigger('owl.next');
        })
        $(".prev").click(function() {
            owl.trigger('owl.prev');
        })
    };

    var changeProdHover = function() {
        const firstSrc = $(".prod-thumb-img").attr("src");
        $(".prod-thumb-img").on({
            mouseenter: function() {
                const secondSrc = $(this).attr("change-src");
                $(this).attr("src", secondSrc);
            },
            mouseleave: function() {

                $(this).attr("src", firstSrc);
            }
        });

    };

    var prodLens = function() {
        $("#sync1").find("#img0").attr('id', '');
        $("#sync1").find(".active img").attr('id', 'img0');
        $("div").remove(".zoomContainer");

        $("#sync1").find("#img0").ezPlus({
            scrollZoom: true,
            cursor: "crosshair",
        });

    };

    //    var sideNav = function() {
    //        $("#sideNavIcon").click(function() {
    //            $("#parent").css("grid-template-columns", "0% 100%");
    //        });
    //    }

    var sideNav = function() {
        $("#sideNavIcon").click(function() {
            if ($("#parent").hasClass('myClass')) {
                $("#parent").removeClass('myClass');
            } else {
                $("#parent").addClass('myClass');
            }
            //            $("#parent").css("grid-template-columns", "0% 100%");
        }, );
    }


    var contact = function() {
        $("#contactBtn.btn-scp").click(function(e) {
            const user = $(this).attr("data");
            console.log(user);
            e.preventDefault();
            Swal.fire({
                    title: 'Are you sure?',
                    text: "We will share mail ID to the seller so that seller can contact you.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#20C993',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes'
                }).then((result) => {
                    if (result.isConfirmed) {

                        $.ajax({
                            url: "/contact-scrapseller/",
                            type: "POST",
                            data: {
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                action: 'post',
                                type: "contactuser",
                                seller: user
                            },
                            dataype: "json",
                            beforeSend: function() {
                                swal.fire({
                                    title: 'Sending Mail...',
                                    allowOutsideClick: false,
                                    allowEscapeKey: false,
                                    didOpen: () => {
                                        swal.showLoading();
                                    }
                                });
                            },
                            complete: function(response) {
                                //console.log(data.auth);

                            },
                            success: function(data) {
                                swal.close();
                                // console.log(data.send);
                                if (data.auth) {
                                    if (data.send) {
                                        //Swal.fire(data.msg, "", "success");
                                        Swal.fire("Your mail id is shared with our seller.", "", "success");
                                    } else {
                                        Swal.fire(data.msg, "", "warning");

                                    }
                                } else {
                                    Swal.fire("Login or create account first !!", "", "warning");
                                    // window.location.href = "/accounts/login/";
                                }

                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                swal.close();
                                // console.log(jqXHR.status);
                                Swal.fire(
                                    jqXHR.status + "",
                                    textStatus + " : " + errorThrown,
                                    'error'
                                )
                            }
                        });

                    }
                })
                // Swal.fire("Do You Want To Share Your Contact No. With The Seller So That They Can Contact You?", {
                //     buttons: ["Nope", "Send"],
                // });
        });
    }

    // var priceSlider = function() {
    //     let sym = "&#8377;"
    //     $("#slider-range").slider({
    //         range: true,
    //         min: 100,
    //         max: 1000,
    //         values: [100, 1000],
    //         slide: function(event, ui) {
    //             $("#amount").html(sym + ui.values[0] + " -" + sym + ui.values[1]);
    //             $("#amount1").val(ui.values[0]);
    //             $("#amount2").val('250');
    //         },
    //         change: function(event, ui) {
    //             $("#priceform").submit();
    //             // console.log(ui.values[0])
    //             // $.ajax({
    //             //     type: "POST",
    //             //     url: $('#priceform').attr('data-url'),
    //             //     data: {
    //             //         csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    //             //         min_value: ui.values[0],
    //             //         max_value: ui.values[1],
    //             //         item_type: $('#priceform').attr('item-type')
    //             //     },
    //             //     // datatype: "html",
    //             //     success: function(data) {
    //             //         // $(".prd-loop").html(data)
    //             //     },
    //             //     error: function(jqXHR, textStatus, errorThrown) {
    //             //         Swal.fire(
    //             //             jqXHR.status + "",
    //             //             textStatus + " : " + errorThrown,
    //             //             'error'
    //             //         )
    //             //     }
    //             // })
    //         }
    //     });
    //     $("#amount").html(sym + $("#slider-range").slider("values", 0) +
    //         " - " + sym + $("#slider-range").slider("values", 1));
    // };


    var func_expand = function() {
        let loc = window.location.pathname;
        let sideBarLoc = loc.match(/(?:.*?\/){4,5}/);

        if (loc == "/accounts/dashboard/") {
            $('a[href="' + loc + '"]').parent().css({ "opacity": "1" });
        } else if (sideBarLoc != loc) {
            // console.log("dd" + sideBarLoc);
            $('a[href="' + sideBarLoc + '"]').css({ "opacity": "1" }).parent().addClass("show").prev().css({ "opacity": "1" }).parent().css({ "opacity": "1" });
        } else {
            // console.log(sideBarLoc);
            //$('a[href="' + loc + '"]').css({ "opacity": "1" }).addClass("show").prev().css({ "opacity": "1" }).parent().css({ "opacity": "1" });

            $('a[href="' + loc + '"]').css({ "opacity": "1" }).parent().addClass("show").prev().css({ "opacity": "1" }).parent().css({ "opacity": "1" });
        }

        // else if ((loc == "/accounts/dashboard/product/creative/add") || (loc == "/accounts/dashboard/product/scrapyard/add")) {
        //     $('a[href="' + "/accounts/dashboard/product/creative/" + '"]').css({ "opacity": "1" }).parent().addClass("show").prev().css({ "opacity": "1" }).parent().css({ "opacity": "1" });
        // }
    };

    var productViewModel = function() {
        //        forward on model
        $('#editProductNext').click(function() {
            $('#view-data').hide("slide", { direction: "left" }, 1000);
            $('#edit-data-1').show("slide", { direction: "right" }, 1000);
        });

        $('#editProductNext1').click(function() {
            $('#edit-data-1').hide("slide", { direction: "left" }, 1000);
            $('#edit-data-2').show("slide", { direction: "right" }, 1000);
        });

        //       backward on model
        $("#editProductBack1").click(function() {
            $('#edit-data-1').hide("slide", { direction: "right" }, 1000);
            $('#view-data').show("slide", { direction: "left" }, 1000);
        });

        $("#editProductBack2").click(function() {
            $('#edit-data-2').hide("slide", { direction: "right" }, 1000);
            $('#view-data').show("slide", { direction: "left" }, 1000);
        });
    }

    /*
    var CustomFileUploader = function() {
        $('#productFileUploader').FancyFileUpload({
            'params': {
                action: 'fileuploader'
            },
            'maxfilesize': 1000000,
            'edit': true,
            'retries': 3,
        });
    }
    var uploadImageName = function() {
        $("#primaryImage").on("change", function() {

            $(this).siblings(".custom-file-label").addClass("selected").html("Added Product Image...");
            let priDiv = document.getElementById("pri-img-div");
            priDiv.removeAttribute("hidden");

            $("#pri-prod-img-name").html("<p>" + document.getElementById("primaryImage").files[0].name + "</p>");
            //$('#pri-image_preview').append("<img class='px-1' width='50px' height='50px' src='" + URL.createObjectURL(event.target.files[0]) + "'/>");
            $('#pri-image_preview').append("<li data-toggle='modal' data-target='#pri-img-modal' class='m-1'><a href='#pri-gallery' data-slide-to='0'><img class='img-thumbnail' width='80px' height='80px' src='" + URL.createObjectURL(event.target.files[0]) + "'></a></li>");

            //alert(model_img);
            $("#pri-gallery .carousel-inner").append("<div class='carousel-item active'><img class='d-block w-100' src='" + URL.createObjectURL(event.target.files[0]) + "'></div>");
        });

        $("#otherImages").on("change", function() {
            // console.log($(this).val());
            // var fileName = $(this).val().split("\\").pop();
            // var filesname = document.getElementById("otherImages").files[0].name;
            // for (var i = 0; i < total_file; i++)
            //     console.log(filesname);
            // $("#pri-prod-img-names").append("<p>" + document.getElementById("primaryImage").files[i].name + "</p>")


            let total_file = document.getElementById("otherImages").files.length;
            if (total_file != 7) {
                swal("Oh no!", "Please add 7 images.", "error");

            } else {
                let secDiv = document.getElementById("sec-img-div");
                $(this).siblings(".custom-file-label").addClass("selected").html("Added Product Images...");

                secDiv.removeAttribute("hidden");
                for (var i = 0; i < total_file; i++) {
                    $("#sec-prod-img-names").append("<p>" + document.getElementById("otherImages").files[i].name + "</p>")
                        //$('#sec-image_preview').append("<img class='px-1' width='50px' height='50px' src='" + URL.createObjectURL(event.target.files[i]) + "'/>");
                    $('#sec-image_preview').append("<li data-toggle='modal' data-target='#sec-img-modal' class='m-1'><a href='#sec-gallery' data-slide-to='0'><img class='img-thumbnail' width='80px' height='80px' src='" + URL.createObjectURL(event.target.files[i]) + "'></a></li>");
                    if (i == 0) {
                        $("#sec-gallery .carousel-inner").append("<div class='carousel-item active'><img class='d-block w-100' src='" + URL.createObjectURL(event.target.files[i]) + "'></div>");
                    } else {
                        $("#sec-gallery .carousel-inner").append("<div class='carousel-item'><img class='d-block w-100' src='" + URL.createObjectURL(event.target.files[i]) + "'></div>");

                    }

                }
            }

        });

    }
    */

    //table filters
    var tableManager = function() {
        $('.tablemanager').tablemanager({
            firstSort: [
                [1, 0],
                [3, 0],
                [4, 0],
                [5, 1]
            ],
            appendFilterby: true,
            dateFormat: [
                [2, "mm-dd-yyyy"]
            ],
            debug: false,
            vocabulary: {
                voc_filter_by: 'Search By',
                voc_type_here_filter: 'Search...',
                voc_show_rows: 'Rows Per Page'
            },
            pagination: false,
            showrows: [5, 10, 20, 50, 100],
            disableFilterBy: []

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

    var gridPagination = function() {

    }

    // new file uploader js SIBTC
    var newFileUploader = function() {

        $(".js-upload-photos").click(function() {
            $("#fileupload").click();
        });

        /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
        $("#fileupload").fileupload({
            dataType: 'json',
            limitMultiFileUploads: 6,
            sequentialUploads: true,

            /* 1. SEND THE FILES ONE BY ONE */
            start: function(e) { /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
                $("#modal-progress").modal("show");
            },
            stop: function(e) { /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
                $("#modal-progress").modal("hide");
                setTimeout(function() { $("#modal-progress").modal("hide") }, 1000);
            },
            progressall: function(e, data) { /* 4. UPDATE THE PROGRESS BAR */
                var progress = parseInt(data.loaded / data.total * 100, 10);
                var strProgress = progress + "%";
                $(".progress-bar").css({ "width": strProgress });
                $(".progress-bar").text(strProgress);
            },

            done: function(e, data) {

                if (data.result.data.is_valid) {

                    $("#gallery tbody").prepend(
                        "<tr><td><a href='" + data.result.data.url + "'>" + data.result.data.image_name + "</a></td><td><a href=" + 'http://127.0.0.1:8000/accounts/photo-delete/' + data.result.data.id + "><span class='remove-product-image p-1'><img src='https://s.svgbox.net/materialui.svg?ic=delete&fill=13775a' width='26' height='26'></span></a></td></tr>"
                    );

                }
            }
        });
    }

    //   Dom Ready
    var orderItemCancel = () => {
        $('.btn-item-cancel').on('click', function() {
            const ordID = $(this).attr("data-item-cancel");
            const ordURL = $(this).attr("data-url");

            Swal.fire({
                title: 'Are you sure?',
                text: "",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#20C993',
                cancelButtonColor: '#d33',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {

                    $.ajax({

                        url: ordURL,
                        dataype: "json",
                        beforeSend: function() {
                            // swal.fire({
                            //     title: 'Sending Mail...',
                            //     allowOutsideClick: false,
                            //     allowEscapeKey: false,
                            //     didOpen: () => {
                            //         swal.showLoading();
                            //     }
                            // });
                        },
                        complete: function(data) {

                        },
                        success: function(data) {
                            // swal.close();
                            console.log(data.status)
                            if (data.status) {

                                Swal.fire(
                                    'Cancelled!',
                                    'order item is cancelled.',
                                    'success'
                                );
                            } else {
                                Swal.fire(
                                    'Failed!',
                                    'Some error occured, Try again.',
                                    'warning'
                                );
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            swal.close();

                            Swal.fire(
                                jqXHR.status + "",
                                textStatus + " : " + errorThrown,
                                'error'
                            )
                        }

                    });

                }
            });
        });
    }
    var orderItemReturn = () => {
        $('.btn-item-return').on('click', function() {

            const ordURL = $(this).attr("data-url");

            Swal.fire({
                title: 'Are you sure?',
                text: "",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#20C993',
                cancelButtonColor: '#d33',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {

                    $.ajax({

                        url: ordURL,
                        dataype: "json",
                        beforeSend: function() {
                            // swal.fire({
                            //     title: 'Sending Mail...',
                            //     allowOutsideClick: false,
                            //     allowEscapeKey: false,
                            //     didOpen: () => {
                            //         swal.showLoading();
                            //     }
                            // });
                        },
                        complete: function(data) {

                        },
                        success: function(data) {
                            // swal.close();
                            console.log(data.status)
                            if (data.status) {

                                Swal.fire(
                                    'Return!',
                                    'order item is returned.',
                                    'success'
                                );
                            } else {
                                Swal.fire(
                                    'Failed!',
                                    'Some error occured, Try again.',
                                    'warning'
                                );
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            swal.close();

                            Swal.fire(
                                jqXHR.status + "",
                                textStatus + " : " + errorThrown,
                                'error'
                            )
                        }

                    });

                }
            });
        });
    }
    var btnLoading = () => {
        $('.btn-load').click(function() {
            $('.btn-load').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Loading...').attr('disabled', true);
        });
    }

    var rating = function() {
        $("#review").rating({
            //"value":0,
            "click": function(e) {
                if (e.stars > 0) {
                    console.log(e); // {stars: 3, event: E.Event}
                    $("#rate").val(e.stars);
                    // alert(e.stars);
                }
            },
            'half': true,
        });
    };


    var loadSubCategory = function() {
        $('#itemCategory').change(function() {
            var id = $(this).val();
            const url = '/accounts/dashboard/product/creative/add/get-sub-crt-cat/' + id
            console.log(url);
            $.ajax({
                url: url,
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                }
            });
            //            event.preventDefault();
        });
    }
    var tableManagerReports = function() {
            $('.tablemanager-report').tablemanager({
                pagination: true,

                // disableFilterBy: [1]
            });


        }
        //   Dom Ready
    $(function() {
        responsiveTab();
        prodGallery();
        // scrollGal();
        //flatZoom();
        ArtistProductGal();
        //    changeProdHover();
        // priceSlider();
        prodLens();
        sideNav();
        contact();
        func_expand();
        productViewModel();
        // CustomFileUploader();
        //CustomFileUploader();
        tableManager();
        loadMoreRows();
        // expandDashboard();
        // uploadImageName();
        gridPagination();
        newFileUploader();
        orderItemCancel();
        orderItemReturn();
        btnLoading();
        rating();
        //        loadSubCategory();

        tableManagerReports();
    });
});






// $(document).ready(function() {

//     $(".tb").hover(function() {

//         $(".tb").removeClass("tb-active");
//         $(this).addClass("tb-active");

//         current_fs = $(".active");

//         next_fs = $(this).attr('id');
//         next_fs = "#" + next_fs + "1";

//         $("fieldset").removeClass("active");
//         $(next_fs).addClass("active");

//         current_fs.animate({}, {
//             step: function() {
//                 current_fs.css({
//                     'display': 'none',
//                     'position': 'relative'
//                 });
//                 next_fs.css({
//                     'display': 'block'
//                 });
//             }
//         });
//     });

// });


// var scrollGal = function() {

//     $(".tb").hover(function() {

//         $(".tb").removeClass("tb-active");
//         $(this).addClass("tb-active");

//         current_fs = $(".active");

//         next_fs = $(this).attr('id');
//         next_fs = "#" + next_fs + "1";

//         $("fieldset").removeClass("active");
//         $(next_fs).addClass("active");

//         current_fs.animate({}, {
//             step: function() {
//                 current_fs.css({
//                     'display': 'none',
//                     'position': 'relative'
//                 });
//                 next_fs.css({
//                     'display': 'block'
//                 });
//             }
//         });
//     });

// };