<?php

namespace VPA\Algorithms\Ant;

use VPA\Algorithms\Ant\Dto\Point;

class AntTravel
{
    protected const ALPHA = 2;
    protected const BETA = 3;

    private array $points = [];

    public function __construct(private Router $router)
    {

    }

    public function run(): float
    {
        $this->points = [];
        $startPoint = $this->router->getRandomPoint();
        //$startPoint = new Point(0, 0);
        $this->points[] = $startPoint;

        while ($nextPoint = $this->getProbabilityRoute($startPoint)) {
            $this->points[] = $nextPoint;
        }
        $this->points[] = $startPoint;
        $distance = $this->getTravelLength();
        return $distance;
    }

    public function getPoints(): array
    {
        return $this->points;
    }

    private function getTravelLength(): float
    {
        $distance = 0;
        $prev = $this->points[0];
        for ($i=1; $i< count($this->points); $i++) {
            $current = $this->points[$i];
            $distance += $this->router->getDistance($prev, $current);
            $prev = $current;
        }
        return $distance;
    }

    private function getProbabilityRoute(Point $point): Point|bool
    {
        $random = rand(0, 999);
        $routes = $this->router->getRoutesByStartPoint($point);
        $enabledRoutes = array_filter($routes, fn($it) => !in_array($it->end, $this->points));
        if (count($enabledRoutes) == 0) {
            return false;
        }
        if (count($enabledRoutes) == 1) {
            $last = reset($enabledRoutes);
            return $last->end;
        }
        $startOffset = 0;
        foreach ($enabledRoutes as $route) {
            $probability = pow($route->pheromone, self::ALPHA) * pow($route->closeness, self::BETA);
            $route->setProbability($probability);
            $startOffset += $probability;
        }
        $offset = 0;
        foreach ($enabledRoutes as $route) {
            $probability = $route->getProbability();
            $normProbability = round(($offset + $probability / $startOffset) * 1000);
            if ($random > $offset && $random <= $normProbability) {
                return $route->end;
            }
            $offset = $normProbability;
            $route->setProbability($normProbability);
        }
        return $route->end;
        //throw new \Exception("Ни одного маршрута не нашлось");
    }

}