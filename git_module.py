import shutil
import os
import git
from common import *


tmp_dir = "/tmp/kuber_tmp/"


def workdir(git_repo):
    print("Cleaning working directory...")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print("Creating fresh working directory...")
    os.mkdir(tmp_dir)
    print("Cloning the project...")
    git.Git(tmp_dir).clone(git_repo)


def clone_repo():
    # git_repo = input("Please provide the scm repo: ")
    git_repo = "https://github.com/devops-pr/walmart_hackathon.git"
    if not validate_url(git_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
        exit()
    elif not verify_url_accessibility(git_repo):
        exit()
    try:
        workdir(git_repo)
        os.chdir(tmp_dir + os.listdir(tmp_dir)[0] + "/")
        repo = git.Repo()
        sha = repo.head.object.hexsha
        return tmp_dir + os.listdir(tmp_dir)[0] + "/", sha, os.listdir(tmp_dir)[0]
    except Exception as clone_exception:
        print("Unable to clone")
        print(clone_exception)


def clone_chart(chart_repo):
    # git_repo = input("Please provide the scm repo: ")
    if not validate_url(chart_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
        exit()
    elif not verify_url_accessibility(chart_repo):
        exit()
    try:
        os.chdir(tmp_dir + os.listdir(tmp_dir)[0] + "/")
        print("Preparing K8s objects...")
        git.Git(tmp_dir).clone(chart_repo)
        return tmp_dir + os.listdir(tmp_dir)[0]
    except Exception as clone_exception:
        print("Unable to clone")
        print(clone_exception)