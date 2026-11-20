"""Shared Cloudflare Web Analytics loader for every CleartrackApps page.

The beacon is skipped on any device that has visited /dont-count-me/ (which
sets localStorage "ct_notrack" = "1" for the whole cleartrackapps.com origin),
so the owner's own visits stop showing up in the numbers.
The injected tag keeps id="cf-beacon" so the /go/ redirect pages can still
wait for it to load before forwarding.
"""

BEACON_JS = (
    '(function(){try{if(localStorage.getItem("ct_notrack")==="1")return}catch(e){}'
    'var s=document.createElement("script");s.defer=true;s.id="cf-beacon";'
    's.src="https://static.cloudflareinsights.com/beacon.min.js";'
    's.setAttribute("data-cf-beacon",\'{"token": "5673e14274004df9a11f87d759a6b624"}\');'
    '(document.body||document.head).appendChild(s)})();'
)

CF_BEACON = (
    '<!-- Cloudflare Web Analytics (skipped on devices opted out at /dont-count-me/) -->\n'
    '<script>' + BEACON_JS + '</script>'
)
