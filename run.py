#!/usr/bin/env python3


import argparse
import itertools
import logging
import os
import time
from configparser import ConfigParser
from pathlib import Path
from string import Template

import coloredlogs
import requests
import sentry_sdk
from dotenv import load_dotenv

TEMPLATE_PATH = Path(__file__).parent.resolve().joinpath("cgit-template.txt")
ENTRY_TEMPLATE = Template(TEMPLATE_PATH.read_text())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("gitea_config", type=argparse.FileType("r"))
    parser.add_argument("output_file", type=argparse.FileType("w"))
    parser.add_argument("--interval", type=int, default=0)
    return parser.parse_args()


def read_gitea_config(gitea_config_file):
    config = ConfigParser()
    config.read_string("[root]\n" + gitea_config_file.read())
    return config


def get_repos(gitea_url):
    if gitea_url.endswith("/"):
        gitea_url = gitea_url[:-1]
    api_url = gitea_url + "/api/v1/repos/search"
    with requests.Session() as session:
        for page_num in itertools.count(start=1):
            response = session.get(api_url, params={"page": page_num})
            response.raise_for_status()
            data = response.json()["data"]
            if not data:
                break
            yield from data


def save_gitea_repos(gitea_config, output_file):
    repo_root = gitea_config["repository"]["ROOT"]
    repo_configs = []
    for repo in get_repos(gitea_config["server"]["ROOT_URL"]):
        logging.info("Exporting %s", repo["full_name"])
        repo_configs.append(
            ENTRY_TEMPLATE.substitute(
                name=repo["name"],
                path=os.path.join(repo_root, repo["full_name"]) + ".git",
                desc=repo["description"],
                website=repo["website"],
                owner=repo["owner"]["full_name"] or repo["owner"]["login"],
            )
        )

    logging.info("Writing repos to %s", output_file.name)
    output_file.writelines(repo_configs)


def main():
    coloredlogs.install(
        level=logging.INFO,
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    load_dotenv()
    sentry_sdk.init(os.environ.get("SENTRY_SDK"))
    args = get_args()
    gitea_config = read_gitea_config(args.gitea_config)
    while True:
        try:
            args.output_file.flush()
            args.output_file.seek(0)
            time.sleep(args.interval)
            save_gitea_repos(gitea_config, args.output_file)
            if not args.interval:
                return
        except Exception:
            pass


if __name__ == "__main__":
    main()
