import json
import logging
import os
import time

import httpx

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

def is_already_starred(client: httpx.Client, repo: str) -> bool:
    r = client.get(
        f"https://api.github.com/user/starred/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_ACCESS_TOKEN']}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if r.status_code == 204:
        logging.info(f"{repo} is already starred.")
        return True
    else:
        return False

def star_repo(client: httpx.Client, repo: str) -> None:
    r = client.put(
        f"https://api.github.com/user/starred/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_ACCESS_TOKEN']}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if r.status_code != 204:
        logging.error(r.json())
    else:
        logging.info(f"{repos[repo]['name']} has been starred.")


if __name__ == "__main__":
    file = open(os.environ['GITHUB_STARS_JSON'])
    repos = json.load(file)
    count = 0
    with httpx.Client() as client:
        for repo in repos:
            if not is_already_starred(client, repos[repo]['name']):
                time.sleep(0.25)
                star_repo(client, repos[repo]['name'])
                count += 1
            time.sleep(0.25)
    logging.info(f"Starred {count}/{len(repos.keys())} repos.")
    file.close()
