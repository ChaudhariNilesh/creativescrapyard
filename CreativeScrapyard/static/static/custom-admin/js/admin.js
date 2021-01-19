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
            });
        });
    };

    var sidebarCollapse = function() {
        let loc = window.location.pathname;

        $('a[href="' + loc + '"]').css({ "opacity": "1" }).parent().parent().addClass("show").prev().css({ "opacity": "1" });
    };

    var tableManager = function() {
        $('.tablemanager').tablemanager({
            firstSort: [
                [3, 0],
                [2, 0],
                [1, 'asc']
            ],
            disable: ["last"],
            appendFilterby: true,
            dateFormat: [
                [4, "mm-dd-yyyy"]
            ],
            debug: false,
            vocabulary: {
                voc_filter_by: 'Filter By',
                voc_type_here_filter: 'Search...',
                voc_show_rows: 'Rows Per Page'
            },
            pagination: false,
            showrows: [5, 10, 20, 50, 100],
            disableFilterBy: [1]
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
                swal("All Records loaded");
            } else {
                $rows.filter(':lt(' + (last + 10) + ')').addClass('active').css({ "display": "" });

            }
        });
    }
    var disableBtn = function() {
        $('.disable-btn').on("click", function() {
            swal({
                    text: 'Write reason for disable?',
                    content: "input",
                    dangerMode: true,
                    button: {
                        text: "Disable",
                        closeModal: false,

                    },
                })
                .then(name => {
                    if (!name) throw null;

                    //return fetch(`url`);
                    return true;

                })
                .then(results => {
                    if (results)
                        swal("User disabled successfully.", {
                            icon: "success",
                        });
                    else {

                        swal("Oh no!", "The AJAX request failed!", "error");
                        swal.stopLoading();
                        swal.close();
                    }

                })
                .catch(err => {
                    if (err) {
                        swal("Oh no!", "The AJAX request failed!", "error");
                    } else {
                        swal.stopLoading();
                        swal.close();
                    }
                });
        });

    }

    var addBadgesInput = function(){
        $('#addBadge').on("click", function() {
        swal("Enter the badge name :", {
            content: "input",
          })
          .then((value) => {
            swal(`${value} Badge Added`);
          }); 
        });
    }

    var assignBadgeInput = function(){
        $('#assignBadge').on("click",function(){
            
        });
    }
    var badgeDelete = function(){
        $('#badge').on("click", function(){
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

    $(function() {
        adminSideBar();
        logoutSwal();
        sidebarCollapse();
        tableManager();
        loadMoreRows();
        disableBtn();
        addBadgesInput();
        badgeDelete();
    });


});