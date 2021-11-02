// ==UserScript==
// @name               Magnet Torrent Poker
// @namespace          http://mattdyson.org/projects/torrentload
// @updateURL          https://raw.githubusercontent.com/mattdy/torrentload/main/torrentLoad.js
// @downloadURL        https://raw.githubusercontent.com/mattdy/torrentload/main/torrentLoad.js
// @version            1.4
// @description        Changes magnet torrent links to poke through to rTorrent, via a Python script found at http://mattdyson.org/projects/torrentload
// @copyright          2014+, Matt Dyson
// @include            *
// @require            https://raw.github.com/sizzlemctwizzle/GM_config/master/gm_config.js
// @grant              GM_getValue
// @grant              GM_setValue
// @grant              GM_log
// @run-at             document-idle
// ==/UserScript==

GM_config.init(
{
  'id': 'torrentLoad', // The id used for this instance of GM_config
  'fields': // Fields object
  {
     'loadAddress': // This is the id of the field
        {
            'label': 'Magnet Torrent Poker - submit all magnet links to address',
            'type': 'text',
            'default': 'http://example.com'
        },
     'secretKey': // Secret key unique to your server, entered in the server script
        {
            'label': 'Secret key (entered in server configuration)',
            'type': 'text',
            'default': 'YOUR-KEY-HERE'
        }
  }
});

var submitAddress = GM_config.get('loadAddress');
var secret = GM_config.get('secretKey');
if(submitAddress=="http://example.com" || !submitAddress) { GM_config.open(); }
if(secret=="YOUR-KEY-HERE" || !secret) { GM_config.open(); }

GM_log("Replacing links");
var link;
link = document.body.getElementsByTagName("a");

for (var i = 0; i < link.length; i++) {
    var l = document.createElement("a");
    l.href = link[i].href;

    if(l.protocol=="magnet:") {
        link[i].href = link[i].href.replace(/magnet:/,submitAddress)+"&secret="+secret;
        //link[i].target = "_blank";
    }
}
