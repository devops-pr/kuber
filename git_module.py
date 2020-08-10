import shutil
import os
import git
from common import *


def create_workdir(git_repo, work_dir):
    print("Cleaning working directory...")
    delete_workdir(work_dir)
    print("Creating fresh working directory...")
    os.mkdir(work_dir)
    print("Cloning the project...")
    git.Git(work_dir).clone(git_repo)


def delete_workdir(work_dir):
    shutil.rmtree(work_dir, ignore_errors=True)


def clone_repo(git_repo, tmp_dir):
    if not validate_url(git_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
        exit()
    elif not verify_url_accessibility(git_repo):
        exit()
    try:
        os.chdir(tmp_dir + os.listdir(tmp_dir)[0] + "/")
        repo = git.Repo()
        sha = repo.head.object.hexsha
        return tmp_dir + os.listdir(tmp_dir)[0] + "/", sha, os.listdir(tmp_dir)[0]
    except Exception as clone_exception:
        print("Unable to clone")
        print(clone_exception)


def clone_chart(chart_repo, tmp_dir):
    if not validate_url(chart_repo):
        print("The URL is not right. Please enter the url in 'https://<domain>/repos/<repo>' format")
        exit()
    elif not verify_url_accessibility(chart_repo):
        exit()
    try:
        os.chdir(tmp_dir + os.listdir(tmp_dir)[0] + "/")
        print("Preparing K8s objects...")
        git.Git(tmp_dir).clone(chart_repo)
        return tmp_dir + "kuber-charts"
    except Exception as clone_exception:
        print("Unable to clone")
        print(clone_exception)