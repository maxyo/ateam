<?php


namespace VPA\Algorithms\Ant\Dto;


class Route
{
    private float $probability = 0;
    private int $batchNumber = 0;

    public function __construct(
        public Point $start,
        public Point $end,
        public float $distance,
        public float $pheromone,
        public float $closeness
    ) {

    }
    
    public function setProbability(float $probability)
    {
        $this->probability = $probability;
    }

    public function getProbability(): float
    {
        return $this->probability;
    }

    public function evaporation(int $batchNumber, float $evaporationRate)
    {
        if ($this->batchNumber<$batchNumber) {
            $this->pheromone *= $evaporationRate;
            $this->batchNumber = $batchNumber;
        }
    }

    public function renewPheromones(float $pheromonesPortion)
    {
        $this->pheromone += $pheromonesPortion;
    }
}