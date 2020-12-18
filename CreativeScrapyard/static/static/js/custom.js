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
            //prodLens();

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

    var flatZoom = function() {
        var $easyzoom = $('.easyzoom').easyZoom();
    };

    var ArtistProductGal = function() {
        var owl = $('#owl-artist-products');
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
        $(".prod-thumb-img").on({
            mouseenter: function() {
                $(this).attr("src", "../../static/img/products/2.jpg");
            },
            mouseleave: function() {
                $(this).attr("src", "../../static/img/products/1.jpg");
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


    //   Dom Ready
    $(function() {
        responsiveTab();
        prodGallery();
        // scrollGal();
        //flatZoom();
        ArtistProductGal();
        changeProdHover();
        prodLens();


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