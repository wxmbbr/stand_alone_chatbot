/*
 * Copyright (c) 2016.
 * @author Volgger Markus <markus@web-crossing.com>
 * @mod hx 14.10.2016 || removed preventDefault (killed lightboxes and stuff), hitCallback, function loadPage (popupblocker) and disabled eventracking for normal internal links
 * @mod sandra 27.06.2017 - document ready instead of (intermediate value)(...)
 */
jQuery(document).ready(function() {


    // current page host
    var baseURI = window.location.host;

    // click event on body
    $("body a").on("click", function(e) {
        // abandon if link already aborted or analytics is not available
        if (e.isDefaultPrevented() || typeof ga !== "function") return;

        // abandon if no active link or link within domain
        var link = $(e.target).closest("a");

        // only external links
        if (baseURI == link[0].host) return;

        var href = link[0].href;
        var target = link[0].target;
        var eventAction = '';

        if (href.indexOf('mailto') != -1) {
            eventAction = 'Email';
        } else if (href.indexOf('tel') != -1) {
            eventAction = 'Telefon';
        } else {
            // eventAction = 'Link';
        }
		
		if (eventAction != '') {
			ga('send', {
				'hitType': 'event',
				'eventCategory': 'outbound',
				'eventAction': eventAction,
				'eventLabel': href
			});
		}
    });

});