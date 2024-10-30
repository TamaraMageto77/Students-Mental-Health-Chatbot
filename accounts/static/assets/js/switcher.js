window.console =
    window.console ||
    (function () {
        var e = {};
        e.log =
            e.warn =
            e.debug =
            e.info =
            e.error =
            e.time =
            e.dir =
            e.profile =
            e.clear =
            e.exception =
            e.trace =
            e.assert =
                function () {};
        return e;
    })();

$(document).ready(function () {
    var e =
       
        '<div class="switcher-container">' +
        '<div class=" h5 title">Style Selector<div class="btn-setting"><a href="javascript:void(0)" class="sw-click"><i class="icon-settings setting"></i></a></div></div>' +
        '<div class="selector-box">' +
        '<div class="sw-odd"><p class="text-1 title-color">Color:</p>' +
        '<div class="ws-colors colors-theme-primary">' +
        '<ul class="modal-content modal-themes-color">' +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="primary_color" name="theme_color" value="theme-primary">' +
        '<label for="primary_color"></label>' +

        "</li>" +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="green_color" name="theme_color" value="theme-green">' +
        '<label for="green_color"></label>' +

        "</li>" +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="blue_color_2" name="theme_color" value="theme-blue-2">' +
        '<label for="blue_color_2"></label>' +
        "</li>" +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="orange_color_3" name="theme_color" value="theme-orange-3">' +
        '<label for="orange_color_3"></label>' +
        "</li>" +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="blue_color_3" name="theme_color" value="theme-blue-3">' +
        '<label for="blue_color_3"></label>' +
        "</li>" +
        '<li class="color-item">' +
        '<input type="radio" class="check-color" id="dark_color" name="theme_color" value="theme-dark">' +
        '<label for="dark_color"></label>' +
        "</li>" +
        "</ul>" +
        "</div></div>" +
        "</div>" +
        "</div>";
    $("#wrapper").append(e);
    switchAnimate.loadEvent();
});

window.console =
    window.console ||
    (function () {
        var x = {};
        x.log =
            x.warn =
            x.debug =
            x.info =
            x.error =
            x.time =
            x.dir =
            x.profile =
            x.clear =
            x.exception =
            x.trace =
            x.assert =
                function () {};
        return x;
    })();

var switchAnimate = {
    loadEvent: function () {
        $(".switcher-container .title a.sw-click").on("click", function (e) {
            var t = $(".switcher-container");
            if (t.css("right") === "-290px") {
                $(".switcher-container").animate(
                    { right: "0" },
                    300,
                    "easeInOutExpo"
                );
            } else {
                $(".switcher-container").animate(
                    { right: "-290px" },
                    300,
                    "easeInOutExpo"
                );
            }
            e.preventDefault();
        });
    },
};
