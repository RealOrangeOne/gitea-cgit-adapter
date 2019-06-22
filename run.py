#!env/bin/python


import argparse
from configparser import ConfigParser

import psycopg2


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


def get_db_connection(db_credentials):
    return psycopg2.connect(**db_credentials)


def get_owners(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT id, lower_name FROM "user"')
        return dict(cursor.fetchall())


if __name__ == "__main__":
    args = get_args()
    gitea_config = read_gitea_config(args.gitea_config)
    with get_db_connection(get_database_credentials(gitea_config)) as db_conn:
        owners = get_owners(db_conn)
    print("Got {} owners".format(owners))
