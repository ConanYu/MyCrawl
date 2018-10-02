// ==UserScript==
// @name         RemoveBanner_zhihu
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        *://*.zhihu.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var container = document.getElementsByClassName("AdblockBanner");
    close(container[0]);

    function close(v) {
        try {
            v.style.display = "none";
        } catch (exception) {
            return;
        }
    }
})();
