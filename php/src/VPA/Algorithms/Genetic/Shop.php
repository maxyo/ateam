<?php


namespace VPA\Algorithms\Genetic;


class Shop
{
    private $heap = [];

    public function __construct($map)
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

        $json = file_get_contents($map);
        $this->data = json_decode($json, true);
        $heap = $this->data['gifts'];
        foreach ($heap as $g) {
            $this->heap[$g['id']] = $g;
        }
    }

    public function getSex($sex)
    {
        $sex = array_filter($this->data['children'], fn($it) => $it['gender'] == $sex);
        return $sex;
    }

    // 0-3, 4-6, 7-10
    public function getSexAndAge($sex, array $age): array
    {
        $sex = array_filter($this->data['children'], fn($it) => $it['gender'] == $sex && $it['age'] >= $age[0] && $it['age'] <= $age[1]);
        usort($sex, fn($a, $b) => $a['age'] < $b['age']);
        return $sex;
    }

    public function getGiftsByType(string $type, bool $sortByPrice = true): array
    {
        $gifts = array_filter($this->heap, fn($it) => $it['type'] == $type);
        if ($sortByPrice) {
            usort($gifts, fn($a, $b) => $a['price'] < $b['price']);
        } else {
            shuffle($gifts);
        }
        return $gifts;
    }

    public function createSetByBot(array $bot, bool $sortByPrice = true): array
    {
        $heap = $this->data['gifts'];
        foreach ($heap as $g) {
            $this->heap[$g['id']] = $g;
        }

        $gifts = [];
        $totalAmount = 0;
        $chunks = array_chunk($bot, 3);
        $sets = [
            ['gender'=>'male','age'=>[7,10]],
            ['gender'=>'female','age'=>[7,10]],
            ['gender'=>'male','age'=>[4,6]],
            ['gender'=>'female','age'=>[4,6]],
            ['gender'=>'male','age'=>[0,3]],
            ['gender'=>'female','age'=>[0,3]],
        ];
        //var_dump("Heap: ",count($this->heap));
        foreach ($chunks as $id => $chunk) {
            $conditions = $sets[$id];
            $children = $this->getSexAndAge($conditions['gender'], $conditions['age']);
            $num = count($children);
            $gs = [];
            foreach ($chunk as $type) {
                $g = $this->getGiftsByType($this->types[$type], $sortByPrice && $conditions['age'][1]>3);
                $gs = array_merge($gs, $g);
            }
            $gs = array_slice($gs, 0, $num);
            foreach ($children as $idx => $child) {
                $giftID = $gs[$idx]['id'];
                $totalAmount += $gs[$idx]['price'];
                $gifts[] = [
                    'childID' => $child['id'],
                    'giftID' => $giftID,
                ];
                unset($this->heap[$giftID]);
            }
        }
        //var_dump("Heap: ",count($this->heap));
        var_dump("TotalAmount: ",$totalAmount);
        if ($totalAmount>100000) {
            $gifts = $this->createSetByBot($bot, false);
        }
        //die();
        $this->save($bot,$gifts);
        //var_dump($chunks);
        //die();
        return $gifts;
    }

    private function save(array $bot, array $gifts)
    {
        $key = implode("_",$bot);
        $data = [
            'bot'=>$bot,
            'gifts' => $gifts,
        ];
        $json = json_encode($data);
        file_put_contents("bots/".$key.'.json', $json);
    }

    public function updateBot(array $bot, mixed $error, string $roundId)
    {
        $key = implode("_",$bot);
        $data = json_decode(file_get_contents("bots/".$key.'.json'), true);
        $data['total_happy'] = $error;
        $data['round_id'] = $roundId;
        $json = json_encode($data);
        file_put_contents("bots/".$key.'.json', $json);
    }

    private function unsetGift(mixed $heap, mixed $id)
    {
        foreach ($heap['gifts'] as $idx => $item) {
            if ($id==$item['id']) {
                echo "remove $id\n";
                unset($heap['gifts'][$id]);
            }
        }
        return $heap;
    }
}