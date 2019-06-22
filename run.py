#!env/bin/python


import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("gitea_config", type=argparse.FileType("r"))
    parser.add_argument("output_file", type=argparse.FileType("w"))
    return parser.parse_args()


if __name__ == "__main__":
    print(get_args())
