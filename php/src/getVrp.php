<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Genetic\GeneticVrp;


$genetic = new GeneticVrp();
for ($i = 0; $i < 10; $i++) {
    //echo "Batch $i:\n";
    $genetic->runBatch();
}
