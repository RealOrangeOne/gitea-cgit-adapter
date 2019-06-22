#!env/bin/python


import argparse
import os
from configparser import ConfigParser
from string import Template
from textwrap import dedent

import psycopg2

ENTRY_TEMPLATE = Template(
    dedent(
        """
    repo.url=$name
    repo.path=$path
    repo.desc=$desc
    """
    )
)


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
        cursor.execute('SELECT id, lower_name FROM "user";')
        return dict(cursor.fetchall())


def get_repos(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute(
            "SELECT lower_name, description, owner_id from repository where is_private = false;"
        )
        return cursor.fetchall()


if __name__ == "__main__":
    args = get_args()
    gitea_config = read_gitea_config(args.gitea_config)
    repo_root = gitea_config["repository"]["ROOT"]
    with get_db_connection(get_database_credentials(gitea_config)) as db_conn:
        owners = get_owners(db_conn)
        print("Got {} owners".format(len(owners)))
        repos = get_repos(db_conn)
        print("Got {} repos".format(len(repos)))
    for name, description, owner_id in repos:
        repo_ident = os.path.join(owners[owner_id], name)
        print("Exporting", repo_ident)
        path = os.path.join(repo_root, repo_ident + ".git")
        assert os.path.exists(path)
        args.output_file.write(
            ENTRY_TEMPLATE.substitute(name=name, path=path, desc=description)
        )
