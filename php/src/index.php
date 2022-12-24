<?php

require_once(__DIR__ . '/../vendor/autoload.php');

$time = time();

use VPA\Algorithms\Ant\Main;
use VPA\Algorithms\Genetic\Main as GeneticMain;
use VPA\Algorithms\Ant\Dto\Point;
use VPA\Algorithms\Ant\Router;

$json = file_get_contents("faf7ef78-41b3-4a36-8423-688a61929c08.json");
$data = json_decode($json, true);
$gifts = [];
foreach ($data['gifts'] as $item) {
    $gifts[$item['id']] = $item;
}

$storage = [];

$heap = $gifts;
$bag_id = 0;
while (!empty($heap)) {
    $genetic = new GeneticMain($heap);
    for ($i = 0; $i < 100; $i++) {
        //echo "Batch $i:\n";
        $genetic->runBatch();
    }
    $backpack = $genetic->getBestBackpack();
    $error = getFitness($bag_id, $gifts, $backpack);
    if ($error > 100) {
        continue;
    }
    $bag_id ++;
    $storage[] = $backpack;
    foreach ($backpack as $gift_id) {
        unset($heap[$gift_id]);
    }
    //die();
}
file_put_contents("storage_".$time.".json", json_encode($storage));

$sizes = array_map(fn($it) => count($it), $storage);

$points = [];

$houses = $data['children'];

foreach ($houses as $house) {
    $tanAlpha = ceil(($house['y'] / $house['x']) * 10000000).rand(0,9);
    $points[$tanAlpha] = $house;
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
file_put_contents("clusters_" . $time . ".json", json_encode($clusters));

$totalDistance = 0;

$moves = [];

foreach ($clusters as $pointsArray) {
    array_unshift($pointsArray, ['x' => 0, 'y' => 0]);
    $points = array_map(fn($it): Point => new Point($it['x'], $it['y']), $pointsArray);
    $router = new Router($points);
    $ant = new Main($router, $points);
    [$distance, $travel] = $ant->run();
    $move = array_map(fn($it) => [$it->x, $it->y], $travel['points']);
    $moves[] = $move;
    $totalDistance += $distance;
}
file_put_contents("moves_" . $time . ".json", json_encode($moves));
printf("====================\n%d\n=========================", $totalDistance);

function getFitness(int $bag_id, array $data, array $backpack)
{
    $volume = $weight = $len = 0;
    foreach ($backpack as $idx) {
        $weight += $data[$idx]['weight'];
        $volume += $data[$idx]['volume'];
        $len += 1;
    }
    $dw = ($weight - 200);
    $dv = ($volume - 100);
    if ($dw <= 0 && $dv <= 0) {
        $abs = abs($dw + $dv);
        $error = $abs / ($len * 2);
    } else {
        $abs = $error = 1000;
    }
    printf("Bag %d: Error: %.3f Abs: %d Len: %d\n", $bag_id, $error, $abs, $len);
    return $error;
}