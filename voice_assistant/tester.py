import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Service chooser.')
    parser.add_argument('--train', '-tr', type=str, help='Train')

    args = parser.parse_args()

    if args.train == 'infos':
        print('hello')