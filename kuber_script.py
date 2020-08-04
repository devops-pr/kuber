# https://github.com/devops-pr/walmart_hackathon.git
import re
import requests
import git
import os
import shutil
import docker



def validate_url(url):
    regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def verify_url_accessibility(url):
    url_get_call = requests.get(url)
    return (url_get_call.status_code)


def clone_repo():
    # git_repo = input("Please provide the scm repo: ")
    git_repo = "https://github.com/devops-pr/walmart_hackathon.git"
    if not validate_url(git_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
    elif verify_url_accessibility(git_repo) != 200:
        print("The provided repo is not accessible.")
        exit()
    try:
        shutil.rmtree('/tmp/kuber_tmp/', ignore_errors=True)
        os.mkdir("/tmp/kuber_tmp/")
        git.Git("/tmp/kuber_tmp/").clone(git_repo)
    except Exception as e:
        print("Unable to clone")
        print(e)
    # finally:
    #     print("Deleted.")




clone_repo()
try:
    docker_client = docker.from_env()
    docker_client.containers.run("ubuntu:latest", "echo hello world")
except Exception as e:
    print(e)


