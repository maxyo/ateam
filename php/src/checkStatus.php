<?php

$id = '01GN7TJPAXRNESJZVFS0TVM59Y';
$ch=curl_init('https://datsanta.dats.team/api/round2/'.$id);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
//curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER,
    array(
        'X-API-Key: 79586e79-7d46-469c-a2a2-2d2c3af161c7',
    )
);

$result = curl_exec($ch);
curl_close($ch);

var_dump($result);