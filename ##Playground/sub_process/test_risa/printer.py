import argparse


def printer(value):
    print(value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute a print.')
    parser.add_argument('--print_sentence', '-p', type=str, help='Sentence to print', required=True)
    args = parser.parse_args()

    printer(args.print_sentence)
