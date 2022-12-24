<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Ant\Main;
use \VPA\Algorithms\Genetic\Main as GeneticMain;
use VPA\Algorithms\Ant\Dto\Point;
use VPA\Algorithms\Ant\Router;

$pointsArray = [
    [0, 0],
    [100, 0],
    [-100, 20],
    [100, 100],
    [0, 100],
    [50, 50],
    [-50, 90],
    [150, 75],
];

//$points = array_map(fn($it): Point => new Point($it[0], $it[1]), $pointsArray);
//$router = new Router($points);
//$ant = new Main($router, $points);
//$ant->run();

$json = file_get_contents("faf7ef78-41b3-4a36-8423-688a61929c08.json");
$data = json_decode($json, true);
$gifts = [];
foreach ($data['gifts'] as $item) {
    $gifts[$item['id']] = $item;
}

$genetic = new GeneticMain($gifts);
for ($i=0; $i< 10; $i++) {
    echo "Batch $i:\n";
    $genetic->runBatch();
}

//$str = json_encode($gifts);
//file_put_contents("gifts.json", $str);
//var_dump($$str);