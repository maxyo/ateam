<?php

namespace VPA\Algorithms\Genetic;

class GeneticVrp
{
    const NUMBER_OF_GENES = 3;
    const NUMBER_OF_BOTS = 4;
    private array $bots;

    public function __construct()
    {
        $this->genes = [
            [0 => 0, 1 => 1, 2 => 2, 3 => 3, 4 => 5, 5 => 5],
            [
                'UNSET', 'AUTOMATIC', 'PATH_CHEAPEST_ARC', 'PATH_MOST_CONSTRAINED_ARC', 'EVALUATOR_STRATEGY', 'SAVINGS', 'SWEEP',
                'CHRISTOFIDES', 'ALL_UNPERFORMED', 'BEST_INSERTION', 'PARALLEL_CHEAPEST_INSERTION', 'SEQUENTIAL_CHEAPEST_INSERTION',
                'LOCAL_CHEAPEST_INSERTION', 'LOCAL_CHEAPEST_COST_INSERTION', 'GLOBAL_CHEAPEST_ARC', 'LOCAL_CHEAPEST_ARC', 'FIRST_UNBOUND_MIN_VALUE',
            ],
            [
                'UNSET', 'AUTOMATIC', 'GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING', 'TABU_SEARCH', 'GENERIC_TABU_SEARCH',
            ]
        ];
        for ($i = 0; $i < self::NUMBER_OF_BOTS; $i++) {
            $this->bots[$i] = [];
            foreach ($this->genes as $idx => $gene) {
                $this->bots[$i][$idx] = rand(0, count($gene) - 1);
            }
        }
    }

    public function runBatch(): array
    {
        $population = [];
        $half = ceil(self::NUMBER_OF_BOTS / 2);
        foreach ($this->bots as $idx => $bot) {
            $error = $this->getFitness($bot);
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
            $bot = $this->crossing($this->bots[1], $this->bots[$i]);
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


    public function getFitness(array $bot)
    {
        $command = sprintf("/home/andy/work/algoritms/ant/ateam.py --output output.json --matrix matrix.json --hbcount %s --algo %s --metaalgo %s",
            $this->genes[0][$bot[0]],
            $this->genes[1][$bot[1]],
            $this->genes[2][$bot[2]],
        );
        //$command = true;
        $run_command = $command . " && cat output.json | jq .totalTime";
        $time = intval(exec($run_command));
        printf("[ %5d ] %s\n", $time, $command);
        rename('output.json', './g/output_' . $time . '.json');
        return $time ?? 100000;
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
            $gen = $this->genes[$idx];
            if ($p < 20) {
                $bot[$idx] = rand(0, count($gen) - 1);
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
}