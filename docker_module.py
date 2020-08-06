# https://github.com/devops-pr/walmart_hackathon.git
import re
import requests
import git
import os
import shutil
import docker
from passlib.context import CryptContext
import getpass

# create CryptContext object
context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
)


tmp_dir = "/tmp/kuber_tmp/"
hashed_password = "$pbkdf2-sha256$50000$nxNirNU6x9ibkxLiPOc8pw$hPJ9UecOYNwssOoQ0gyrmZNCSgOCWEc7V6JcJZeNR0U"

docker_client = docker.from_env()


def validate_url(url):
    regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def verify_url_accessibility(url):
    url_get_call = requests.get(url)
    return url_get_call.status_code


def tmp_dir_function(git_repo):
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print("Creating fresh tmp directory...")
    os.mkdir(tmp_dir)
    print("Cloning the project...")
    git.Git(tmp_dir).clone(git_repo)


def clone_repo():
    # git_repo = input("Please provide the scm repo: ")
    git_repo = "https://github.com/devops-pr/walmart_hackathon.git"
    if not validate_url(git_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
    elif verify_url_accessibility(git_repo) != 200:
        print("The provided repo is not accessible.")
        exit()
    try:
        print("Cleaning tmp directory...")
        # tmp_dir_function(git_repo)
        os.chdir(tmp_dir + os.listdir(tmp_dir)[0] + "/")
        repo = git.Repo()
        sha = repo.head.object.hexsha
        return tmp_dir + os.listdir(tmp_dir)[0] + "/", sha, os.listdir(tmp_dir)[0]
    except Exception as clone_exception:
        print("Unable to clone")
        print(clone_exception)



def build_image(project_path, tag):
    try:
        print("Building image...")
        docker_client.images.build(path=project_path, tag=tag)
        print("Tagging image with latest...")
        docker.client.from_env().images.get(tag).tag(repo, 'latest')
        # print(docker_client.containers.run("devopspr/my_app:latest", ports = {'5000/tcp': ('127.0.0.1', 8080)},
        # detach= True))
    except Exception as e:
        print(e)


def push_image(image, latest_commit_hash):
    attempts = 0
    image_url = "https://hub.docker.com/v1/repositories/" + repo + "/tags/" + latest_commit_hash
    print(image_url)
    while attempts < 3:
        try:
            p = getpass.getpass(prompt='Provide your dockerhub password: ')
            if context.verify(p, hashed_password):
                docker_client.login(username='devopspr', password=p)
                if verify_url_accessibility(image_url) == 200:
                    print("Image already exist in registry, skipping push...")
                    break
                else:
                    print("Pushing the image to registry...")
                    docker_client.images.push(image)
                    break
            else:
                if attempts < 2:
                    print("Wrong password!!! Try again.")
                    attempts += 1
                    continue
                else:
                    print("You entered wrong password 3 times. Exiting...")
                    exit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    project_path, latest_commit_hash, app_name = clone_repo()
    repo = "devopspr/" + app_name
    tag = repo + ":" + latest_commit_hash
    build_image(project_path, tag)
    push_image(repo, latest_commit_hash)
    # print(verify_url_accessibility("https://hub.docker.com/v1/repositories/devopspr/my_app/tags/59ccfe9d82a8150b9a78a3c893d0946ed3ad3f03"))
