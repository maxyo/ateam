<?php

namespace VPA\Algorithms\Genetic;

class GeneticGifts
{
    const NUMBER_OF_BOTS = 6;
    public array $bots;

    public function __construct(public Shop $shop)
    {
        $this->types = [
            'constructors',
            'dolls',
            'radio_controlled_toys',
            'toy_vehicles',
            'board_games',
            'outdoor_games',
            'playground',
            'soft_toys',
            'computer_games',
            'sweets',
            'books',
            'pet',
            'clothes',
        ];
        $this->genes = [
            // male 7-10
            0,
            0,
            0,
            // female 7-10
            0,
            0,
            0,
            // male 4-6
            0,
            0,
            0,
            // female 4-6
            0,
            0,
            0,
            // male 0-3
            0,
            0,
            0,
            // female 0-3
            0,
            0,
            0,
        ];
//        for ($i = 0; $i < self::NUMBER_OF_BOTS; $i++) {
//            $this->bots[$i] = [];
//            foreach (range(0, 5) as $idx => $gene) {
//                $genes = array_rand($this->types, 3);
//                $this->bots[$i][$idx * 3] = $genes[0];
//                $this->bots[$i][$idx * 3 + 1] = $genes[1];
//                $this->bots[$i][$idx * 3 + 2] = $genes[2];
//            }
//        }
        $bots = glob("bots/*.json");
        $best = [];
        foreach ($bots as $botName) {
            $data = json_decode(file_get_contents($botName), true);
            if (isset($data['total_happy'])) {
                $best[$data['total_happy']] = $data['bot'];
            }
        }
        krsort($best);
        $best = array_slice($best,0, self::NUMBER_OF_BOTS);
        $this->bots = $best;
    }

    public function runBatch(): array
    {
        $population = [];
        $half = ceil(self::NUMBER_OF_BOTS / 2);
        foreach ($this->bots as $idx => $bot) {
            $error = $this->getFitness($bot);
            $population[$idx] = $error;
        }
        arsort($population);
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
            $newBots[] = $bot;
            $bot = $this->crossing($this->bots[1], $this->bots[$i]);
            //$newBots[] = $bot;
            $newBots[] = $this->mutation($bot);
        }
        $newBots = array_splice($newBots, 0, self::NUMBER_OF_BOTS);
        $this->bots = $newBots;
        return $this->bots;
    }

    public function checkExtstsBot($bot)
    {
        $key = implode("_",$bot);
        echo $key."\n";
        $file = getcwd()."/bots/".$key.'.json';
        if (file_exists($file)) {
            $data = json_decode(file_get_contents($file), true);
            if ($data['total_happy']) {
                return $data['total_happy'];
            }
        }
        return false;
    }

    public function getBestBot()
    {
        return reset($this->bots);
    }


    public function getFitness(array $bot): int
    {
        $error = $this->checkExtstsBot($bot);
        if ($error) {
            return $error;
        }
        $gifts = $this->shop->createSetByBot($bot);
        $data = [
            'mapID' => 'a8e01288-28f8-45ee-9db4-f74fc4ff02c8',
            'presentingGifts'=> $gifts,
        ];
        $data_string = json_encode($data);
        do {
            $ch = curl_init('https://datsanta.dats.team/api/round2');
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
            //curl_setopt($ch, CURLOPT_HEADER, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER,
                array(
                    'X-API-Key: 79586e79-7d46-469c-a2a2-2d2c3af161c7',
                    'Content-Type:application/json',
                )
            );

            $result = curl_exec($ch);
            curl_close($ch);
            $answer = json_decode($result, true);
            $roundId = $answer['roundId'];
            sleep(10);
        }while(!$roundId);
        printf("Bot: %s\n", implode("_", $bot));
        $this->shop->updateBot($bot, 0, $roundId);
        echo "RoundID: $roundId\n Wait: ";
        while(!$error = $this->checkStatus($roundId)) {
            echo ".";
            sleep(30);
        }
        echo "\ntotal_happy: ".$error."\n";
        $this->shop->updateBot($bot, $error, $roundId);
        //die();
        return $error;

    }

    public function checkStatus($id)
    {
        $ch=curl_init('https://datsanta.dats.team/api/round2/'.$id);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
        //curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER,
            array(
                'X-API-Key: 79586e79-7d46-469c-a2a2-2d2c3af161c7',
            )
        );

        $result = curl_exec($ch);
        curl_close($ch);
        $answer = json_decode($result, true);
        //var_dump($answer);
        if ($answer['data']['status']!='processed') {
            return false;
        }
        return $answer['data']['total_happy'] ?? 1;
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
            $key = array_rand($this->types);
            if ($p < 20) {
                $bot[$idx] = $key;
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