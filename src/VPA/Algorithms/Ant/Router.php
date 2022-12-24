<?php

namespace VPA\Algorithms\Ant;

use VPA\Algorithms\Ant\Dto\Point;
use VPA\Algorithms\Ant\Dto\Route;

class Router
{
    const EVAPORATION_RATE = 0.64;
    const Q = 100;
    private $router = [];

    public function __construct(private array $points, protected float $defaultPheromone = 0.5, protected float $closeness = 10)
    {
        foreach ($this->points as $point) {
            $keyFrom = $this->getKey($point);
            $this->router[$keyFrom] = [];
            foreach ($this->points as $endPoint) {
                if ($endPoint !== $point) {
                    $keyTo = $this->getKey($endPoint);
                    $distance = $this->getDistance($point, $endPoint);
                    $this->router[$keyFrom][$keyTo] = new Route(
                        start: $point,
                        end: $endPoint,
                        distance: $distance,
                        pheromone: $this->defaultPheromone,
                        closeness: $this->closeness / $distance
                    );
                }
            }
        }
    }

    public function getRandomPoint(): Point
    {
        $idx = array_rand($this->points);
        return $this->points[$idx];
    }

    public function evaporation(int $batchNumber)
    {
        foreach ($this->points as $point) {
            $keyFrom = $point->getKey();
            foreach ($this->points as $endPoint) {
                if ($endPoint !== $point) {
                    $keyTo = $endPoint->getKey();
                    $route = $this->router[$keyFrom][$keyTo];
                    $route->evaporation($batchNumber, self::EVAPORATION_RATE);
                }
            }
        }
    }

    public function getRouteLength(): int
    {
        return count($this->points) + 1;
    }

    public function getRoutesByStartPoint(Point $point): array
    {
        $key = $this->getKey($point);
        return $this->router[$key];
    }

    private function getKey(Point $point): string
    {
        return $point->getKey();
    }

    public function getDistance(Point $start, Point $end): float
    {
        $deltaX = $end->x - $start->x;
        $deltaY = $end->y - $start->y;
        return sqrt(pow($deltaX, 2) + pow($deltaY, 2));
    }

    public function renewPheromones(array $travel)
    {
        assert(count($travel['points']) > 1);
        $pheromonesPortion = self::Q / $travel['distance'];
        $prev = reset($travel['points']);
        for ($i = 1; $i < count($travel); $i++) {
            $current = $travel['points'][$i];
            $route = $this->getRouteStartEnd($prev, $current);
            $route->renewPheromones($pheromonesPortion);
            $prev = $current;
        }
    }

    public function getRouteStartEnd(Point $start, Point $end): Route
    {
        $routes = $this->getRoutesByStartPoint($start);
        foreach ($routes as $route) {
            if ($route->end == $end) {
                break;
            }
        }
        return $route;
    }

    public function showRouteInfo()
    {
        echo "=============================\n";
        foreach ($this->router as $router) {
            foreach ($router as $route) {
                printf("[%3d, %3d] -> [%3d, %3d] = %f\n",
                    $route->start->x,
                    $route->start->y,
                    $route->end->x,
                    $route->end->y,
                    $route->pheromone
                );
            }
        }
    }
}