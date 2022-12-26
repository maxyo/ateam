import argparse

ALGORITHMS = {
    'UNSET': 0,
    'AUTOMATIC': 15,
    'PATH_CHEAPEST_ARC': 3,
    'PATH_MOST_CONSTRAINED_ARC': 4,
    'EVALUATOR_STRATEGY': 5,
    'SAVINGS': 10,
    'SWEEP': 11,
    'CHRISTOFIDES': 13,
    'ALL_UNPERFORMED': 6,
    'BEST_INSERTION': 7,
    'PARALLEL_CHEAPEST_INSERTION': 8,
    'SEQUENTIAL_CHEAPEST_INSERTION': 14,
    'LOCAL_CHEAPEST_INSERTION': 9,
    'LOCAL_CHEAPEST_COST_INSERTION': 16,
    'GLOBAL_CHEAPEST_ARC': 1,
    'LOCAL_CHEAPEST_ARC': 2,
    'FIRST_UNBOUND_MIN_VALUE': 12,
}
META_ALGOS = {
    'UNSET': 0,
    'AUTOMATIC': 6,
    'GREEDY_DESCENT': 1,
    'GUIDED_LOCAL_SEARCH': 2,
    'SIMULATED_ANNEALING': 3,
    'TABU_SEARCH': 4,
    'GENERIC_TABU_SEARCH': 5
}

parser = argparse.ArgumentParser(prog='ateam')

parser.add_argument('--wcapacity', required=False, type=int, default=200, help='Weight capacity')
parser.add_argument('--vcapacity', required=False, type=int, default=100, help='Volume capacity')
parser.add_argument('--bcount', required=False, type=int, default=46, help='Bags count')
parser.add_argument('--hbcount', required=False, type=int, default=5, help='Bags with many gifts count')
parser.add_argument('--speed', required=False, type=int, default=70, help='Speed')
parser.add_argument('--sspeed', required=False, type=int, default=10, help='Speed at snowstorm')
parser.add_argument('--output', required=False, default='stdout', help='Output path or stdout')
parser.add_argument('--debug', required=False, type=bool, default=False, help='Debug mode')
parser.add_argument('--evil', required=False, type=bool, default=False, help='Evil mode')
parser.add_argument('--token', required=False, type=str, default=None, help='Token')
parser.add_argument('--send', required=False, type=bool, default=False, help='Send on successful build')
parser.add_argument('--map', required=False, type=str, default='faf7ef78-41b3-4a36-8423-688a61929c08', help='Map id')
parser.add_argument('--matrix', required=False, default=None, type=str, help='Prepared matrix, path to json')
parser.add_argument('--matrix-write-path', dest='matrix_path', required=False, default=None, type=str, help='Save generated matrix to path')
parser.add_argument('--algo', required=False, default='PATH_MOST_CONSTRAINED_ARC', type=str,
                    help='First solution algos, available: %s' % ' '.join(list(ALGORITHMS.keys())))
parser.add_argument('--metaalgo', required=False, default='TABU_SEARCH', type=str,
                    help='local search algos, available: %s' % ' '.join(list(META_ALGOS.keys())))

parser.add_argument('--blimit', required=False, type=int, default=2,
                    help='Bags combination searching time limit, seconds')

args = parser.parse_args()
FIRST_SOLUTION_ALGORITHM = ALGORITHMS[args.algo]
LOCAL_SEARCH_ALGORITHM = META_ALGOS[args.metaalgo]

ENABLE_DEBUG = args.debug

WEIGHT_CAPACITY = args.wcapacity
VOLUME_CAPACITY = args.vcapacity

SPEED = args.speed
SNOWSTORM_SPEED = args.sspeed

OUTPUT_PATH = args.output

IS_EVIL = args.evil

SEND = args.send

MAP_ID = args.map

TOKEN = args.token
PREPARED_MATRIX = args.matrix
MATRIX_SAVE_PATH = args.matrix_path

MANY_BAGS_FINDING_TIME_LIMIT_MS = args.blimit * 1000

BAGS_COUNT = args.bcount
HARDFILLED_BAGS = args.hbcount
url = 'https://datsanta.dats.team'
