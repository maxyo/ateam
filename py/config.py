import argparse

parser = argparse.ArgumentParser(prog='ateam')

parser.add_argument('--wcapacity', required=False, type=int, default=200, help='Weight capacity')
parser.add_argument('--vcapacity', required=False, type=int, default=100, help='Volume capacity')
parser.add_argument('--bcount', required=False, type=int, default=46, help='Bags count')
parser.add_argument('--hbcount', required=False, type=int, default=2, help='Bags with many gifts count')
parser.add_argument('--speed', required=False, type=int, default=70, help='Speed')
parser.add_argument('--sspeed', required=False, type=int, default=10, help='Speed at snowstorm')
parser.add_argument('--output', required=False, default='stdout', help='Output path or stdout')
parser.add_argument('--debug', required=False, type=bool, default=False, help='Debug mode')
parser.add_argument('--evil', required=False, type=bool, default=False, help='Evil mode')
parser.add_argument('--token', required=False, type=str, default=None, help='Token')
parser.add_argument('--send', required=False, type=bool, default=False, help='Send on successful build')
parser.add_argument('--map', required=False, type=str, default='faf7ef78-41b3-4a36-8423-688a61929c08', help='Map id')
parser.add_argument('--matrix', required=False, default=None, type=str, help='Prepared matrix, path to json')

parser.add_argument('--blimit', required=False, type=int, default=2,
                    help='Bags combination searching time limit, seconds')

args = parser.parse_args()

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

MANY_BAGS_FINDING_TIME_LIMIT_MS = args.blimit * 1000

BAGS_COUNT = args.bcount
HARDFILLED_BAGS = args.hbcount
url = 'https://datsanta.dats.team'
