<?php
$str = <<<EOR
HTTP/2 200 
date: Mon, 26 Dec 2022 16:40:12 GMT
content-type: application/json
cache-control: no-cache, private
access-control-allow-origin: *
cf-cache-status: DYNAMIC
report-to: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=aiV1E%2Fr1HXHV8Bu4w8WSmLzXtiIA3ZmkxXWeG7JE96a9rJyDaqw38mNoDUmjAB8erVbCQO6ZVSe8KFKC9WGkVQj5%2BdqP1dofISRwA9pXs07CAEDzri260aubfo3A3%2Fr5yDyveic%3D"}],"group":"cf-nel","max_age":604800}
nel: {"success_fraction":0,"report_to":"cf-nel","max_age":604800}
server: cloudflare
cf-ray: 77fb41c3da5e166c-DME
alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400

{"success":false,"error":"The last round \u002201GN7MVXPEMSMKDHQHT3TEDCDY\u0022 has not been processed yet","roundId":null}bool(true)
EOR;

//echo $str;



