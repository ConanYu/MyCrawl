// ==UserScript==
// @name         去除csdn的广告
// @namespace    http://tampermonkey.net/
// @version      0.4
// @description  remove ads!
// @author       ConanYu
// @match        *://*.csdn.net/*
// @grant        none
// ==/UserScript==
// 然而还是建议AdBlock

(function () {
    var ad1 = document.getElementsByClassName("csdn-tracking-statistics mb8 box-shadow");
    var ad2 = document.getElementsByClassName("pulllog-box");
    var ad3 = document.getElementsByClassName("mediav_ad");
    var ad4 = document.getElementsByClassName("p4course_target");
    var ad6 = document.getElementsByClassName("recommend-item-box recommend-ad-box clearfix");
    var ad7 = document.getElementsByClassName("recommend-item-box recommend-ad-box");

    try {
        var ad5 = document.getElementById("asideFooter").getElementsByTagName("div");
        close(ad5[0]);
    } catch (exception) { }

    close(ad1[0]);
    close(ad2[0]);
    close(ad4[0]);

    iter(ad3);
    iter(ad6);
    iter(ad7);

    function iter(v) {
        try {
            for (var i = 0; i < 10; i++) {
                close(v[i]);
            }
        } catch (exception) {
            return;
        }
    }

    function close(v) {
        try {
            v.style.display = "none";
        } catch (exception) {
            return;
        }
    }

})();
