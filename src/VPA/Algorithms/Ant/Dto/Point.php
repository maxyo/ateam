<?php

namespace VPA\Algorithms\Ant\Dto;

class Point
{
    public function __construct(public int $x, public int $y)
    {
    }

    public function getKey()
    {
        return $this->x . '_' . $this->y;
    }
}