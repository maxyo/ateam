<?php

$json = file_get_contents('moves_last.json');
$clusters = json_decode($json, true);
$moves = [];
foreach ($clusters as $pointsArray) {
    $move = array_map(fn($it) => ['x'=>$it[0], 'y'=>$it[1]], $pointsArray);
    array_shift($move);
    $moves= array_merge($moves, $move);
}

file_put_contents("moves-xy_last.json", json_encode($moves));
