import re
import json
import logging
import subprocess
from pathlib import Path


def get_changed_files():
    process = subprocess.run(["git", "diff", "--name-only", "HEAD^"], check=True, stdout=subprocess.PIPE)
    return process.stdout.decode('UTF-8').splitlines()


def main():
    with open(Path(__file__).parent / 'deployment_config.json', 'r') as config_file:
        deployment_config = json.load(config_file)

    changed_files = get_changed_files()
    for container_description in deployment_config['containers']:
        container_changed = any(re.match(container_description['is_changed_regexp'], changed_file)
                                for changed_file in changed_files)
        logging.info(f"{container_changed}, {container_description}")


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    main()
