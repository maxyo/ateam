<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Genetic\Main as GeneticMain;

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
file_put_contents("storage_".time().".json", json_encode($storage));
var_dump(count($storage));

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