import argparse


def parse_arguments():

    # TODO: Descriptions for parser, arguments and help

    """

    :return:
    """

    parser = argparse.ArgumentParser("First version of argument parser")

    parser.add_argument('--amount')
    parser.add_argument('--input_currency')
    parser.add_argument('--output_currency')

    return vars(parser.parse_args())


if __name__ == '__main__':
    parsed_arguments = parse_arguments()