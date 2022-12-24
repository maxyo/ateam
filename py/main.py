from py.client import Client
from py.manybags import many_bags
from py.onebag import one_bag



def main():
    excluded = []

    for i in range(50):
        excluded.extend(one_bag(excluded))

if __name__ == '__main__':
    main()

