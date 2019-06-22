#!env/bin/python


import argparse
from configparser import ConfigParser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("gitea_config", type=argparse.FileType("r"))
    parser.add_argument("output_file", type=argparse.FileType("w"))
    return parser.parse_args()


def read_gitea_config(gitea_config_file):
    config = ConfigParser()
    config.read_string("[root]\n" + gitea_config_file.read())
    return config


def get_database_credentials(gitea_config):
    database_config = gitea_config["database"]
    return {
        "dbname": database_config["name"],
        "user": database_config["user"],
        "password": database_config["passwd"],
    }


if __name__ == "__main__":
    args = get_args()
    gitea_config = read_gitea_config(args.gitea_config)
    print(get_database_credentials(gitea_config))
