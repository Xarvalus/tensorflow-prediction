import getopt
import os
import sys
from prediction import training, fetch_genomics, store_genomics, analyze_data

# @TODO
#  Hiding irrelevant warning about AVX/FMA support (CPU)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main(argv):
    try:
        opts, args = getopt.getopt(argv, '', ['train', 'fetch', 'store', 'analyze'])
    except getopt.GetoptError:
        print('main.py <command>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--train':
            training.train()
        elif opt == '--fetch':
            fetch_genomics.fetch()
        elif opt == '--store':
            store_genomics.store()
        elif opt == '--analyze':
            analyze_data.analyze()


if __name__ == "__main__":
    main(sys.argv[1:])
