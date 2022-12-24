<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Ant\Main;
use VPA\Algorithms\Genetic\Main as GeneticMain;
use VPA\Algorithms\Ant\Dto\Point;
use VPA\Algorithms\Ant\Router;

//$json = file_get_contents("clusters_1671915487.json");
$json = file_get_contents("clusters_radius_1671917911.json");
$data = json_decode($json, true);

$totalDistance = 0;

$moves = [];

foreach ($data as $pointsArray) {
    array_unshift($pointsArray, ['x' => 0, 'y' => 0]);
    $points = array_map(fn($it): Point => new Point($it['x'], $it['y']), $pointsArray);
    $router = new Router($points);
    $ant = new Main($router, $points);
    [$distance, $travel] = $ant->run();
    $move = array_map(fn($it) => [$it->x, $it->y], $travel['points']);
    $moves[] = $move;
    $totalDistance += $distance;
}
file_put_contents("moves_" . time() . ".json", json_encode($moves));
printf("====================\n%d\n=========================", $totalDistance);
