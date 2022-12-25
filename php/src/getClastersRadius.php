<?php

require_once(__DIR__ . '/../vendor/autoload.php');

$json = file_get_contents("storage_1671901016.json");
$data = json_decode($json, true);

$sizes = array_map(fn($it) => count($it), $data);

$json = file_get_contents("faf7ef78-41b3-4a36-8423-688a61929c08.json");
$data = json_decode($json, true);

$points = [];

$houses = $data['children'];

foreach ($houses as $house) {
    $radius = ceil(sqrt(pow($house['x'],2) + pow($house['y'],2)) * 100000).rand(0,9);
    $points[$radius] = $house;
}
ksort($points);

$clusters = [];

$idx = 0;
$value = reset($points);
foreach ($sizes as $cluster_id => $size) {
    for ($i = 0; $i < $size; $i++) {
        $clusters[$cluster_id][] = $value;
        $value = next($points);
        $idx++;
    }
}
file_put_contents("clusters_radius_" . time() . ".json", json_encode($clusters));

var_dump($clusters);
