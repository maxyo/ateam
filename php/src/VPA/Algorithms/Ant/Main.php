<?php

namespace VPA\Algorithms\Ant;

use VPA\Algorithms\Ant\Dto\Point;

class Main
{
    private int $ants;
    private array $top10;

    /**
     * Ant`s algorithm constructor.
     *
     * @param Router $router
     * @param Point[] $points
     */
    public function __construct(private Router $router, private array $points)
    {
        $this->ants = count($points);
        $this->top10 = [];
    }

    public function runBatch(int $batchNumber)
    {
        $travels = [];
        //$ants = $this->router->getRouteLength();
        $ants = 30;
        for ($i = 0; $i < $ants; $i++) {
            $antTravel = new AntTravel($this->router);
            $distance = $antTravel->run();
            $d = floor($distance);
            $this->top10[$d] = $travels[] = [
                'points' => $antTravel->getPoints(),
                'distance' => $distance,
            ];
            //var_dump($distance);
        }
        $this->router->evaporation($batchNumber);
        foreach ($travels as $travel) {
            $this->router->renewPheromones($travel);
        }
        //$this->showTravelInfo($travel, $distance);

    }

    public function run()
    {
        for ($i=1;$i<400; $i++) {
            $this->runBatch($i);
            //$this->router->showRouteInfo();
        }
        ksort($this->top10);
        $top10 = array_slice($this->top10, 0, 1, true);
        foreach ($top10 as $d => $travel) {
            $this->showTravelInfo($travel, $d);
            return [$d, $travel];
        }
        //$this->router->showRouteInfo();
    }

    public function showTravelInfo(array $travel, float $distance)
    {
        $data = [];
        $prev = $travel['points'][0];
        $data[] = sprintf("[%3d, %3d]", $prev->x, $prev->y);
        $p = 0;
        for ($i=1; $i< count($travel['points']); $i++) {
            $current = $travel['points'][$i];
            $route = $this->router->getRouteStartEnd($prev, $current);
            $p += $route->pheromone;
            $data[] = sprintf("[%3d, %3d]", $current->x, $current->y);
            $prev = $current;
        }
        echo "{".floor($distance).": $p }: ".implode(" -> ", $data)."\n";
    }
}