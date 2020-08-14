import docker
from passlib.context import CryptContext
import getpass
from git_module import *

# create CryptContext object
context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
)

hashed_password = "$pbkdf2-sha256$50000$nxNirNU6x9ibkxLiPOc8pw$hPJ9UecOYNwssOoQ0gyrmZNCSgOCWEc7V6JcJZeNR0U"

docker_client = docker.from_env()


def check_image_availability_on_repo(repo, commit_hash):
    image_url = "https://hub.docker.com/v1/repositories/" + repo + "/tags/" + commit_hash
    if verify_url_accessibility(image_url):
        return True
    else:
        return False


def check_image_availability_on_local(image_tag):
    try:
        docker_client.images.get(image_tag)
        return True
    except docker.errors.ImageNotFound:
        return False


def build_image(path, image_tag, local_image_availability, image):
    try:
        if not local_image_availability:
            print("Building image...")
            docker_client.images.build(path=path, tag=image_tag)
            print("Tagging image with latest...")
            docker.client.from_env().images.get(image_tag).tag(image, 'latest')
        else:
            print("Image already exist locally.\nskipping build...")
    except Exception as e:
        print(e)


def push_image(image, remote_image_availability):
    if remote_image_availability:
        print("Image already exist in registry.\nskipping push...")
    else:
        try:
            print("Pushing the image to registry...")
            docker_client.images.push(image)
        except Exception as e:
            print(e)


def docker_login(user, password):
    try:
        if user == "":
            user = "dummy"
        if password == "":
            password = "dummy"
        login_return = docker_client.login(username=user, password=password)
        if login_return['Status'] == "Login Succeeded":
            return True
        elif login_return['username'] == user:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def get_docker_hub_credentials():
    docker_user_name = input("Provide your dockerhub username: ")
    docker_password = getpass.getpass(prompt='Provide your dockerhub password: ')
    attempts = 0
    while attempts < 3:
        try:
            if docker_login(docker_user_name, docker_password):
                break
            else:
                if attempts < 2:
                    print("Wrong credentials!!! Try again.")
                    attempts += 1
                    continue
                else:
                    print("You entered wrong credentials 3 times. Exiting...")
                    exit()
        except Exception as e:
            print(e)
    return docker_user_name


if __name__ == '__main__':
    pass
    # project_path, latest_commit_hash, app_name = clone_repo()
    # app_name = app_name.replace("_", "-")
    # image_name = "devopspr/" + app_name
    # tag = image_name + ":" + latest_commit_hash
    # image_available_remote = check_image_availability_on_repo(image_name, latest_commit_hash)
    # image_available_local = check_image_availability_on_local(tag)
    # build_image(project_path, tag, image_available_local, image_name)
    # push_image(image_name, image_available_remote)
    print(docker_login("devopspdcr", "Iambatman@123"))