$(function() {
    'use strict';

    var adminSideBar = function() {
        $('#sidebarCollapse').on('click', function() {
            $('#sidebar').toggleClass('active');
            $(this).toggleClass('active');
        });
    };

    var logoutSwal = function() {
        $('#btn-logout').on('click', function() {
            swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: ["No", "Yes"],
                dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                    $.ajax({
                        url: "/admin/logout",
                        success: function(result) { location.reload(); }
                    });
                } else {}
            });;
        });
    };

    var sidebarCollapse = function() {
        let loc = window.location.pathname;

        $('a[href="' + loc + '"]').css({ "opacity": "1" }).parent().parent().addClass("show").prev().css({ "opacity": "1" });


    };
    $(function() {
        adminSideBar();
        logoutSwal();
        sidebarCollapse();
    });


});