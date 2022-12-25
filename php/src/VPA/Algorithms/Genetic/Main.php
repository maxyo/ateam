<?php

namespace VPA\Algorithms\Genetic;

class Main
{
    const MAX_WEIGHT = 200;
    const MAX_VOLUME = 100;
    const NUMBER_OF_GENES = 1000;
    const NUMBER_OF_BOTS = 100;
    private array $bots;

    public function __construct(private array $data)
    {
        for ($i = 0; $i < self::NUMBER_OF_BOTS; $i++) {
            $this->bots[$i] = $this->getBotFromData();
            //$this->showBotInfo($this->bots[$i]);
            //$this->getFitness($i, $this->bots[$i]);
        }
    }

    public function runBatch(): array
    {
        $population = [];
        $half = ceil(self::NUMBER_OF_BOTS / 2);
        foreach ($this->bots as $idx => $bot) {
            $error = $this->getFitness($idx, $bot);
//            while($error===1000) {
//                $bot = $this->mutation($bot);
//                $this->bots[$idx] = $bot;
//                $error = $this->getFitness($idx, $bot);
//            }
            $population[$idx] = $error;
        }
        asort($population);
        $i = 0;
        $best = $newBots = [];
        foreach ($population as $idx => $e) {
            if ($i >= $half) break;
            $best[$idx] = $e;
            $i++;
        }
        //var_dump($best);

        foreach ($best as $idx => $error) {
            $newBots[] = $this->bots[$idx];
        }
        for ($i = 2; $i < $half; $i++) {
            $bot = $this->crossing($this->bots[0], $this->bots[$i]);
            $newBots[] = $this->mutation($bot);
            $bot =  $this->crossing($this->bots[1], $this->bots[$i]);
            $newBots[] = $this->mutation($bot);
        }
        $newBots = array_splice($newBots, 0, self::NUMBER_OF_BOTS);
        $this->bots = $newBots;
        return $this->bots;
    }

    public function getBestBot()
    {
        return reset($this->bots);
    }

    public function getBestBackpack(): array
    {
        return $this->getBackpackFromBot($this->getBestBot());
    }

    public function getBotFromData()
    {
        $keys = array_keys($this->data);
        shuffle($keys);
        $keys = array_slice($keys, 0, 40);
        $bot = array_fill(0, self::NUMBER_OF_GENES, 0);
        foreach ($keys as $key) {
            $bot[$key - 1] = 1;
        }
        return $bot;
    }

    public function getFitness(int $id, array $bot)
    {
        $volume = $weight = $len = 0;
        foreach ($bot as $idx => $gene) {
            if ($gene !== 1) continue;
            $weight += $this->data[$idx + 1]['weight'];
            $volume += $this->data[$idx + 1]['volume'];
            $len += 1;
        }
        $dw = ($weight - self::MAX_WEIGHT);
        $dv = ($volume - self::MAX_VOLUME);
        if ($dw <= 0 && $dv <= 0) {
            $abs = abs($dw + $dv);
            $error = $abs / ($len + 1);
            if ($len < 28) {
                $error += 20;
            }
        } else {
            $abs = $error = 1000;
        }
        if ($error != 1000) {
            //printf("Bot %2d: Error: %.3f Abs: %d Len: %d\n", $id, $error, $abs, $len);
        }
        return $error;
    }

    private function showBotInfo(array $bot)
    {
        $nbot = array_map(fn($it) => str_pad($it, 1, " ", STR_PAD_LEFT), $bot);
        printf(
            "[ %s ]\n",
            implode(",", $nbot)
        );
    }

    public function mutation($bot)
    {
        foreach ($bot as $idx => $gene) {
            $p = rand(0, 100);
            if ($p < 20) {
                $bot[$idx] = 0;
            }
//            elseif ($p>40 && $p < 43) {
//                $bot[$idx] = 1;
//            }
        }
        return $bot;
    }

    public function crossing($bot1, $bot2)
    {
        $bot = [];
        foreach ($bot1 as $idx => $gene1) {
            $p = rand(0, 1);
            if ($p == 1) {
                $bot[$idx] = $bot2[$idx];
            } else {
                $bot[$idx] = $bot1[$idx];
            }
        }
        return $bot;
    }

    public function getBackpackFromBot(array $bot): array
    {
        $backpack = [];
        foreach ($bot as $idx => $gene) {
            if ($gene) {
                $backpack[] = $idx + 1;
            }
        }
        return $backpack;
    }
}