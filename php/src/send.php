<?php

$json = file_get_contents("storage_last.json");
$bags  = json_decode($json, true);

$gifts = 0;
foreach ($bags as $bag) {
    $gifts += count($bag);
}

printf("Gifts: %d\n", $gifts);

$json = file_get_contents("moves-xy_last.json");
$moves  = json_decode($json, true);

$houses = count($moves);

printf("Houses: %d\n", $houses);

$stackOfBags = array_reverse($bags);
$data = [
    'mapID' => 'faf7ef78-41b3-4a36-8423-688a61929c08',
    'moves' => $moves,
    'stackOfBags' => $stackOfBags,
];

$data_string = json_encode($data);

$ch=curl_init('https://datsanta.dats.team/api/round');
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER,
    array(
        'X-API-Key: 79586e79-7d46-469c-a2a2-2d2c3af161c7',
        'Content-Type:application/json',
    )
);

$result = curl_exec($ch);
curl_close($ch);

var_dump($result);