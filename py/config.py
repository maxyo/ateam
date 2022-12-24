import argparse

from py.client import Client

parser = argparse.ArgumentParser(prog='ateam')

parser.add_argument('--wcapacity', required=False, default=200, help='Weight capacity')
parser.add_argument('--vcapacity', required=False, default=100, help='Volume capacity')
parser.add_argument('--bcount', required=False, default=46, help='Bags count')
parser.add_argument('--hbcount', required=False, default=2, help='Bags with many gifts count')
parser.add_argument('--output', required=False, default='stdout', help='Output path or stdout')
parser.add_argument('--debug', required=False, default=False, help='Debug mode')

parser.add_argument('--blimit', required=False, default=2, help='Bags combination searching time limit, seconds')

args = parser.parse_args()

ENABLE_DEBUG = args.debug

WEIGHT_CAPACITY = args.wcapacity
VOLUME_CAPACITY = args.vcapacity

OUTPUT_PATH = args.output

MANY_BAGS_FINDING_TIME_LIMIT_MS = args.blimit * 1000

BAGS_COUNT = args.bcount
HARDFILLED_BAGS = args.hbcount
url = 'https://datsanta.dats.team'
client = Client(base_url=url)
