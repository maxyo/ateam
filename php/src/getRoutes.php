<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Ant\Main;
use VPA\Algorithms\Genetic\Main as GeneticMain;
use VPA\Algorithms\Ant\Dto\Point;
use VPA\Algorithms\Ant\Router;

$json = file_get_contents("clusters_1671913860.json");
$data = json_decode($json, true);

foreach ($data as $pointsArray) {
    array_unshift($pointsArray, ['x'=>0,'y'=>0]);
    $points = array_map(fn($it): Point => new Point($it['x'], $it['y']), $pointsArray);
    var_dump($points);
    $router = new Router($points);
    $ant = new Main($router, $points);
    $ant->run();
    die();
}
