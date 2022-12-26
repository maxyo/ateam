<?php

require_once(__DIR__ . '/../vendor/autoload.php');

use VPA\Algorithms\Genetic\GeneticGifts;
use VPA\Algorithms\Genetic\Shop;

$shop = new Shop('a8e01288-28f8-45ee-9db4-f74fc4ff02c8.json');
//$gifts = $shop->getGiftsByType('constructors');

//$females = $males = [];
//$males[] = $shop->getSexAndAge('male', [0,3]);
//$males[] = $shop->getSexAndAge('male', [4,6]);
//$males[] = $shop->getSexAndAge('male', [7,10]);
//$females[] = $shop->getSexAndAge('female', [0,3]);
//$females[] = $shop->getSexAndAge('female', [4,6]);
//$females[] = $shop->getSexAndAge('female', [7,10]);

//$female = $shop->getSex('female');

//var_dump($males[0]);
//var_dump($gifts);
//foreach ($males as $male) {
//    var_dump(count($male));
//}


//$bot = [1,2,3,4,5,6,7,8,9,10,11,12,10,9,8,7,6,5];
//$shop->createSetByBot($bot);
//var_dump(count($female));

// type, gender, age


$genetic = new GeneticGifts($shop);
$bot = [4,9,10,1,4,9,4,5,8,2,4,7,0,7,9,3,4,6];
//$genetic->getFitness($bot);
//die();
//var_dump($genetic->bots);
//die();

for ($i = 0; $i < 5; $i++) {
    printf("%s Batch %d:\n", date("Y-m-d H:i:s"),$i);
    $genetic->runBatch();
}
