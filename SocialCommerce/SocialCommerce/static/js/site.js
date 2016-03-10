/**
 * Created by Justin on 3/1/2016.
 */
var pusher = new Pusher('1553573f1fa355bb6b13', {
        encrypted: true
    });
var user = $("#login-user").val();
var channel = pusher.subscribe(user);
var tempUserId = null;
var tempContent = null;
var inEditMode = false;
$(document).ready(function () {
    $('<audio id="Audio" width="300" height="32"><source src="/static/audio.mp3" type="audio/mp3" /></audio>').appendTo('body');
    $("#notifications").load("/request_notifications/");
    $("#private-notifications").load("/private_notifications/");
    $("#news-feeds-menu").load("/newsfeed_notifications/");
    $("#chat-contacts-list").load("/chatlist_view/");
    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": true,
      "progressBar": true,
      "positionClass": "toast-top-right",
      "preventDuplicates": false,
      "showDuration": "300",
      "hideDuration": "1000",
      "onclick": null,
      "timeOut": 5000,
      "extendedTimeOut": 1000,
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut",
      "tapToDismiss": true
    }
    channel.bind('request-event', function(data) {
        $('#Audio')[0].play();
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": false,
          "showDuration": "300",
          "hideDuration": "1000",
          "onclick": function(){location.href = "/follower_request/";},
          "timeOut": 5000,
          "extendedTimeOut": 1000,
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "tapToDismiss": true
        }
        toastr.info('<a class="pull-left" href="#"><img class="media-object thumb" src="/static/'+data.image+'/" id="common-friends" alt="people">'
                    +'</a><div class="media-body"><p class="margin-none"><b>'+data.user +'</b>'+ data.message +'</p></div>');
        if($("#notifications").attr("class").includes("open"))
           $("#notifications").attr("class","dropdown notifications open")
        else
            $("#notifications").attr("class","dropdown notifications")

        $("#notifications").load("/request_notifications/");
    });

    channel.bind('request-accepted-event', function(data) {
        $('#Audio')[0].play();
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": false,
          "showDuration": "300",
          "hideDuration": "1000",
          "onclick": function(){location.href = "/profile/"+data.id;},
          "timeOut": 5000,
          "extendedTimeOut": 1000,
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "tapToDismiss": true
        }
        toastr.info('<a class="pull-left" href="#"><img class="media-object thumb" src="/static/'+data.image+'/" id="common-friends" alt="people">'
                    +'</a><div class="media-body"><p class="margin-none"><b>'+data.user +'</b>'+ data.message +'</p></div>');
        $("#news-feeds-menu").load("/newsfeed_notifications/")
        if($("#private-notifications").attr("class").includes("open"))
           $("#private-notifications").attr("class","dropdown notifications open")
        else
            $("#private-notifications").attr("class","dropdown notifications")

        $("#private-notifications").load("/private_notifications/");
    });

    channel.bind('likes-event', function(data) {
        $('#Audio')[0].play();
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": false,
          "showDuration": "300",
          "hideDuration": "1000",
          "onclick": function(){location.href = "/posts/"+data.id;},
          "timeOut": 5000,
          "extendedTimeOut": 1000,
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "tapToDismiss": true
        }
        toastr.info('<a class="pull-left" href="#"><img class="media-object thumb" src="/static/'+data.image+'/" id="common-friends" alt="people">'
                    +'</a><div class="media-body"><p class="margin-none"><b>'+data.user +'</b>'+ data.message +'</p></div>');
        $("#news-feeds-menu").load("/newsfeed_notifications/")
        if($("#private-notifications").attr("class").includes("open"))
           $("#private-notifications").attr("class","dropdown notifications open")
        else
            $("#private-notifications").attr("class","dropdown notifications")

        $("#private-notifications").load("/private_notifications/");
    });

    channel.bind('share-event', function(data) {
        $('#Audio')[0].play();
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": false,
          "showDuration": "300",
          "hideDuration": "1000",
          "onclick": function(){location.href = "/posts/"+data.id;},
          "timeOut": 5000,
          "extendedTimeOut": 1000,
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "tapToDismiss": true
        }
        toastr.info('<a class="pull-left" href="#"><img class="media-object thumb" src="/static/'+data.image+'/" id="common-friends" alt="people">'
                    +'</a><div class="media-body"><p class="margin-none"><b>'+data.user +'</b>'+ data.message +'</p></div>');
        $("#news-feeds-menu").load("/newsfeed_notifications/")
        if($("#private-notifications").attr("class").includes("open"))
           $("#private-notifications").attr("class","dropdown notifications open")
        else
            $("#private-notifications").attr("class","dropdown notifications")

        $("#private-notifications").load("/private_notifications/");
    });
    $('[data-toggle="popover"]').popover({
        html: true,
    });

    $("#status-form").submit(function (e) {
        sync_messages()
        e.preventDefault();
    })

    $(document).on('click', '#post-new', function () {
        $("#progress-bar").show();
        $("#progress-bar [role=progressbar]").attr({
            'aria-valuenow': 100,
            'style': 'width: 100%;'
        });
        var address = $("#address-detail").text();
        var addressCode = $("#address-code").val();
        $("#remove-address").click();
        var status = $("#status-new").val();
        $("#status-new").val('')
        $(this).attr("style", "display: none;");
        status = status.trim()
        if(status.length == 0 && address.length == 0)
        {
            toastr.error("Empty space post does not allow!")
            $("#progress-bar").delay(1000).hide(1000);
            return;
        }
        $.ajax({
             type: 'POST',
             data: {"posts":status, "address":address, "address_code":addressCode},
             url:'/posts_ajax/',
             dataType: 'json',
             success: function (json) {
                 $("#progress-bar").delay(1000).hide(1000);
                 toastr.success("Posted successful!");
             },
             error: function(){
                 $("#progress-bar").delay(1000).hide(1000);
                 UnknownErrorPopup();
             }
         });
    });

    $(document).on('click', '#remove-address', function () {
        $("#address").html('');
        $("#address-code").val('');
    });

    $(document).on('click', '#maps-markers', function () {
        var address = $("#address").html()
        if (address != '') {
            $("#address").html('');
            $("#address-code").val('');
        } else {
            initialize();
            getLocation();
            $("#post-new").show();
        }
    });

    $(document).on('click', '[name=statusBtn]', function () {
        var userId = $(this).data('userId');
        var $this = $(this);
        $.ajax({
            type: 'POST',
            data: {"friends": userId},
            url: '/action/',
            dataType: 'json',
            success: function (json) {
                checkActionStatus($this, json)
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('click', '[name=comment-send]', function () {
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": true,
            "progressBar": true,
            "positionClass": "toast-top-right",
            "preventDuplicates": true,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": 5000,
            "extendedTimeOut": 1000,
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut",
            "tapToDismiss": false
        }
        var userId = $(this).data('userId');
        var $this = $(this);
        var comment = $("#comments-content"+userId).val();
        comment = comment.trim()
        if(comment.length == 0)
        {
            toastr.error("Empty space comment does not allow!")
            return;
        }else {
            $.ajax({
                type: 'POST',
                data: {"posts": userId, "post_comment": comment},
                url: '/comment_ajax/',
                dataType: 'json',
                success: function (json) {
                    if (json.success == true) {
                        $("#comments" + userId).attr("class","collapse comments in");
                        $("#comments-content"+userId).val("");
                        $("#comments-content"+userId).focus();
                        $("#comments-length"+userId).html('<i class="fa fa-comments" ></i> '+json.number+' comments');
                        $("#comments" + userId).prepend('<li><div class="media"><a href="/profile/' + json.user_id + '" class="pull-left">' +
                            '<img src="/static/' + json.user_image + '" class="media-object"  id="common-friends">' +
                            '</a><div class="media-body"><a href="" class="comment-author">' + json.user_display_name + '</a>' +
                            '<span>' + ' ' + json.content + '</span><div class="comment-date" title="' + json.created_date_time + '">' +
                            json.created_date_time + '</div></div></div></li>');
                        toastr.success("Comment to the post successful!")
                    } else {
                        UnknownErrorPopup();
                    }
                },
                error: function () {
                    UnknownErrorPopup();
                }
            });
        }
 });

    $(document).on('click', '[name=share]', function () {
            var userId = $(this).data('userId');
            var $this = $(this);
            toastr.options = {
              "closeButton": true,
              "debug": false,
              "newestOnTop": true,
              "progressBar": true,
              "positionClass": "toast-top-right",
              "preventDuplicates": true,
              "showDuration": "300",
              "hideDuration": "1000",
              "timeOut": 0,
              "extendedTimeOut": 0,
              "showEasing": "swing",
              "hideEasing": "linear",
              "showMethod": "fadeIn",
              "hideMethod": "fadeOut",
              "tapToDismiss": true
            }
            toastr.info('<textarea id="share' + userId + '" style="border:1px solid; resize: none;" class="form-control share-text" rows="5" ' +
                        'maxlength="300" placeholder="Write Something..." autofocus></textarea>'+
                        '<button class="btn btn-success" name="share-confirm" data-user-id="'+userId+'"><i class="fa fa-check-circle"></i> Share</button>', "Share post.")
    });

    $(document).on('click', '[name=share-confirm]', function () {
            var userId = $(this).data('userId');
            var status = $("#share" + userId).val();
            $.ajax({
                type: 'POST',
                data: {"posts": userId, "post_content": status},
                url: '/share_ajax/',
                dataType: 'json',
                success: function (json) {
                    if (json.success == true) {
                        toastr.options = {
                          "closeButton": true,
                          "debug": false,
                          "newestOnTop": true,
                          "progressBar": true,
                          "positionClass": "toast-top-right",
                          "preventDuplicates": true,
                          "showDuration": "300",
                          "hideDuration": "1000",
                          "timeOut": 5000,
                          "extendedTimeOut": 1000,
                          "showEasing": "swing",
                          "hideEasing": "linear",
                          "showMethod": "fadeIn",
                          "hideMethod": "fadeOut",
                          "tapToDismiss": false
                        }
                        inEditMode = false;
                        toastr.success("Post shared successful!")
                    }else{
                        UnknownErrorPopup();
                    }
                },
                error: function () {
                    UnknownErrorPopup();
                }
            });
    });

    $(document).on('click', '[name=likes]', function () {
        var userId = $(this).data('userId');
        var $this = $(this);
        $.ajax({
            type: 'POST',
            data: {"likes": userId},
            url: '/likes_ajax/',
            dataType: 'json',
            success: function (json) {
                if (json.success == true) {
                    if ($this.html().includes('<i class="fa fa-thumbs-up"></i>'))
                        $this.html('<i class="fa fa-thumbs-down"></i> ' + json.number + ' ')
                    else
                        $this.html('<i class="fa fa-thumbs-up"></i> ' + json.number + ' ')
                }else{
                    UnknownErrorPopup();
                }
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('click', '[name=edit]', function () {
        if(!inEditMode) {
            var userId = $(this).data('userId');
            var post = $("#post"+userId).find("#post-content");
            tempContent =  post.html().trim();
            post.html('<textarea id="status' + userId + '" style="border:1px solid; resize: none;" class="form-control share-text" rows="5" ' +
                'maxlength="300" placeholder="Write Something...">' + post.html().trim() + '</textarea><br/>' +
                '<button class="btn btn-success" name="confirm-edit" data-user-id="' + userId + '"><i class="fa fa-check-circle">' +
                '</i> Save</button> <button class="btn clear btn-danger" name="cancel-edit" data-user-id="' + userId + '">' +
                '<i class="fa fa-times"></i> Cancel</button>');
            inEditMode = true;
        }
    });

    $(document).on('click', '[name=cancel-edit]', function () {
        if(inEditMode) {
            var userId = $(this).data('userId');
            var post = $("#post"+userId).find("#post-content");
            post.html(tempContent);
            tempContent = null;
            inEditMode = false;
        }
    });

    $(document).on('click', '[name=confirm-edit]', function () {
        if(inEditMode) {
            var userId = $(this).data('userId');
            var status = $("#status"+userId).val();
            var $this = $(this);
            status = status.trim();
            if(status == tempContent){
                var post = $("#post"+$this.data('userId'));
                post.find("#post-content").html(status);
                post.find("#post-datetime").attr("title");
                inEditMode = false;
                tempContent = null;
                return;
            }
            if(status.length == 0)
            {
                toastr.error("Empty space post does not allow!")
                $("#progress-bar").delay(1000).hide(1000);
                return;
            }else{
                $.ajax({
                    type: 'POST',
                    data: {"posts": userId, "post_content": status},
                    url: '/edit_post_ajax/',
                    dataType: 'json',
                    success: function (json) {
                        if (json.success == true) {
                            var post = $("#post"+$this.data('userId'));
                            post.find("#post-content").html(status);
                            post.find("#post-datetime").attr("title");
                            inEditMode = false;
                            tempContent = null;
                            toastr.success("Post edited successful!")
                        }else{
                            UnknownErrorPopup();
                        }
                    },
                    error: function () {
                        UnknownErrorPopup();
                    }
                });
            }
        }
    });

    $(document).on('click', '[name=delete]', function () {
        var userId = $(this).data('userId');
        var $this = $(this);
        tempUserId = userId;

        toastr.options = {
          "closeButton": true,
          "debug": false,
          "newestOnTop": true,
          "progressBar": true,
          "positionClass": "toast-top-right",
          "preventDuplicates": true,
          "showDuration": "300",
          "hideDuration": "1000",
          "timeOut": 0,
          "extendedTimeOut": 0,
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "tapToDismiss": true
        }
        toastr.warning('<button class="btn btn-success" name="delete-confirm"><i class="fa fa-check-circle"></i> Confirm</button> <button class="btn clear btn-danger">'+
                        '<i class="fa fa-times"></i> Cancel</button>', "Confirm to delete post?")
    });

    $(document).on('click', '[name=delete-confirm]', function () {
        $.ajax({
            type: 'POST',
            data: {"delete": tempUserId},
            url: '/delete_ajax/',
            dataType: 'json',
            success: function (json) {
                if(json.success == true) {
                    toastr.options = {
                          "closeButton": true,
                          "debug": false,
                          "newestOnTop": true,
                          "progressBar": true,
                          "positionClass": "toast-top-right",
                          "preventDuplicates": false,
                          "showDuration": "300",
                          "hideDuration": "1000",
                          "onclick": null,
                          "timeOut": 5000,
                          "extendedTimeOut": 1000,
                          "showEasing": "swing",
                          "hideEasing": "linear",
                          "showMethod": "fadeIn",
                          "hideMethod": "fadeOut",
                          "tapToDismiss": true
                        }
                    toastr.success("Posts Deleted Successfully.");
                    $("#post"+tempUserId).fadeOut();
                    tempUserId = null
                }else
                    UnknownErrorPopup();
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('click', '#newsfeeds-tag', function () {
        if($("#news-feeds-menu").attr("class").includes("open")) {
            $("#news-feeds-menu").attr("class", "hasSubmenu")
            $("#newsfeeds").attr("class", "collapse")
        }else {
            $("#news-feeds-menu").attr("class", "hasSubmenu open")
            $("#newsfeeds").attr("class", "collapse in")
        }

        $.ajax({
            type: 'POST',
            url: '/newsfeed_menuaction/',
            dataType: 'json',
            success: function (json) {
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('click', '#notifications-menu', function () {
        if($("#notifications").attr("class").includes("notifications")){
            $.ajax({
                type: 'POST',
                url: '/crequest_notifications/',
                dataType: 'json',
                success: function (json) {
                },
                error: function () {
                    UnknownErrorPopup();
                }
            });
        }
        if($("#notifications").attr("class").includes("open"))
           $("#notifications").attr("class","dropdown open")
        else
            $("#notifications").attr("class","dropdown")

        $("#notifications").load("/request_notifications/");
    });

    $(document).on('click', '#private-notifications-menu', function () {
        if($("#private-notifications").attr("class").includes("notifications")) {
            $.ajax({
                type: 'POST',
                url: '/cprivate_notifications/',
                dataType: 'json',
                success: function (json) {
                },
                error: function () {
                    UnknownErrorPopup();
                }
            });
        }
        if ($("#private-notifications").attr("class").includes("open"))
            $("#private-notifications").attr("class", "dropdown open")
        else
            $("#private-notifications").attr("class", "dropdown")

        $("#private-notifications").load("/private_notifications/");
    });

    $(document).on('click',  '[name=accept]', function () {
        var userId = $(this).data('userId');
        $.ajax({
            type: 'POST',
            url: '/arequest_notifications/',
            data: {"request_log_id": userId},
            dataType: 'json',
            success: function (json) {
                if (json.success == true){
                    $("#notifications").load("/request_notifications/")
                    $("#notifications").attr("class", "dropdown open")
                    $("#news-feeds-menu").load("/newsfeed_notifications/")
                }else
                    UnknownErrorPopup();
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('click',  '[name=reject]', function () {
        var userId = $(this).data('userId');
        $.ajax({
            type: 'POST',
            url: '/rrequest_notifications/',
            data: {"request_log_id": userId},
            dataType: 'json',
            success: function (json) {
                if (json.success == true) {
                    $("#notifications").load("/request_notifications/")
                    $("#notifications").attr("class", "dropdown open")
                }else
                    UnknownErrorPopup();
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });

    $(document).on('mouseover', '[name=news-feeds]', function () {
        var userId = $(this).data('id');
        var seen = $(this).data('seen');
        var $this = $(this);
        if (seen <= 0) {
            $.ajax({
                type: 'POST',
                data: {"seen": userId},
                url: '/seen/',
                dataType: 'json',
                success: function (json) {
                    $this.find('#news-circle').hide();
                    $this.data('seen', 1)
                },
                error: function () {
                }
            });
        }
    });

    $(document).on('click', '#add-product', function () {
        //var jsonData = {
        //    'name': document.getElementById("productName").value,
        //    'desc': document.getElementById("productDesc").value,
        //    'gender': $('input[name="inlineRadioOptions"]:checked', '#addOrEdit').val(),
        //    'category': document.getElementById("productCategory").value,
        //    'tag': document.getElementById("productTag").value,
        //    //'image' : document.getElementById("productImage").value,
        //    'image': 'images/product/sampleshoes.jpg',
        //    'price': document.getElementById("productPrice").value,
        //};

        $.ajax({
            type: 'POST',
            url: '/addProduct/',
            dataType: 'json',
            data: {
                name: JSON.stringify(document.getElementById("productName").value),
                desc: JSON.stringify(document.getElementById("productDesc").value),
                gender: JSON.stringify($('input[name="inlineRadioOptions"]:checked', '#addOrEdit').val()),
                category: JSON.stringify(document.getElementById("productCategory").value),
                tag: JSON.stringify(document.getElementById("productTag").value),
                image: JSON.stringify(document.getElementById("productImage").value),
                price: JSON.stringify(document.getElementById("productPrice").value),
            },
            success: function (json) {
            },
            error: function () {
                UnknownErrorPopup();
            }
        });
    });
});

function test() {
    var URL = "http://127.0.0.1:8000/test/"

    $.ajax({
        type: "GET",
        url: URL,
        success: function (response) {
            $("#tester").load("/test/");
        }
    });
    setTimeout('test()', 2000);
}
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else {
        alert("Geolocation is not supported by this browser.");
    }
}
function showPosition(position) {
    codeAddress(position.coords.latitude + "," + position.coords.longitude)
}
var geocoder
var map
function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var mapOptions = {
        zoom: 8,
        center: latlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}
function codeAddress(address) {
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
            var area = getArea(results);
            var country = getCountry(results);
            $("#address-code").val(address)
            $("#address").html("- at <label id='address-detail'>" + area + ", " + country +
                "</label> <a href='#/' id='remove-address'><i class='fa fa-remove'></i></a>")
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
            $("#address-detail").val('')
            $("#address").html('')
        }
    });
}

function getArea(results) {
    var areaName = "";
    for (var i = 0; i < results[0].address_components.length; i++) {
        var shortname = results[0].address_components[i].short_name;
        var longname = results[0].address_components[i].long_name;
        var type = results[0].address_components[i].types;

        if (type.indexOf("locality") != -1) {
            if (!isNullOrWhitespace(shortname)) {
                areaName += shortname;
            }
            else {
                areaName += longname;
            }
        }
        if (type.indexOf("administrative_area_level_2") != -1) {
            if (areaName != "") {
                areaName += ", ";
            }
            if (!isNullOrWhitespace(shortname)) {
                areaName += shortname;
            }
            else {
                areaName += longname;
            }
        }
    }
    return areaName;
}
function getCountry(results) {
    for (var i = 0; i < results[0].address_components.length; i++) {
        var shortname = results[0].address_components[i].short_name;
        var longname = results[0].address_components[i].long_name;
        var type = results[0].address_components[i].types;
        if (type.indexOf("country") != -1) {
            if (!isNullOrWhitespace(longname)) {
                return longname;
            }
            else {
                return shortname;
            }
        }
    }
    return "";
}
function isNullOrWhitespace(text) {
    if (text == null) {
        return true;
    }
    return text.replace(/\s/gi, '').length < 1;
}

function checkActionStatus($this, json) {
    if (json.success == 1) {
        $this.attr('title', 'Unfollow')
        $this.html('Unfollow <i class="fa fa-remove"></i>')
    } else if (json.success == 2) {
        $this.attr('title', 'Cancel Request')
        $this.html('Cancel Request <i class="fa fa-clock-o"></i>')
    } else if (json.success == 0) {
        $this.attr('title', 'Follow')
        $this.html('Follow<i class="fa fa-check"></i>')
    }
}

function UnknownErrorPopup() {
    toastr.error("Unknown Error!")
    setTimeout(function(){
        location.reload();
    },1000);
}

function sync_messages() {
    $.ajax({
        type: 'POST',
        data: $(this).serialize(),
        url: '/test/',
        dataType: 'json',
        success: function (json) {
            $('#status').val(json.last_message_id);
        }
    });
    setTimeout('sync_messages()', 2000);
}

onload = function () {
    var e = document.getElementById("refreshed");
    if (e.value == "no")e.value = "yes";
    else {
        e.value = "no";
        location.reload();
    }
}

function updateProduct() {
    document.getElementById('edit_product').style.display = 'block';
    document.getElementById('fade').style.display = 'block';
    //alert(JSON.stringify(document.getElementById("updateProduct").value));

    //$.ajax({
    //    type: 'POST',
    //    url: '/editProduct/',
    //    dataType: 'json',
    //    data: {
    //        pid :JSON.stringify(document.getElementById("updateProduct").value),
    //        //uid :JSON.stringify(uid),
    //        status : JSON.stringify(document.getElementById("productStatus").value),
    //    },
    //    success: function (json) {
    //    },
    //    error: function () {
    //        UnknownErrorPopup();
    //    }
    //});
}

function topUp(amount) {
    //alert(amount);
    $.ajax({
        type: 'POST',
        url: '/topup/',
        //dataType: 'json',
        data: {"topupamount": amount},
        success: function () {
        },
        error: function (jqXHR, exception) {
            //UnknownErrorPopup();
            if (jqXHR.status === 0) {
                alert('Not connect.\n Verify Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
    });
}