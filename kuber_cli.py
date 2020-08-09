from docker_module import *
from k8s_module import *
from git_module import *

project_path, latest_commit_hash, app_name = clone_repo()
app_name = app_name.replace("_", "-")
image_name = "devopspr/" + app_name
tag = image_name + ":" + latest_commit_hash
image_available = check_image_availability_on_repo(image_name, latest_commit_hash)
build_image(project_path, tag, image_available, image_name)
push_image(image_name, image_available)
app_context = context_selection()
app_client = client.CoreV1Api(api_client=config.new_client_from_config(context=app_context))
# app_client.list_namespace()
available_ns = []
for ns in app_client.list_namespace().items:
    available_ns.append(ns.metadata.name)
# print(available_ns)
body = client.V1Namespace()
body.metadata = client.V1ObjectMeta(name=app_name)
if app_name in available_ns:
    deploy = input("The app is already onboarded. Do you wish to deploy?[Y/N]: ").lower()
    # TODO: attemps for y/n
    if deploy == "y":
        print("Deploying...")   # deploy(app_name)
    elif deploy == "n":
        print("Deleting namespace {}...".format(app_name))
        app_client.delete_namespace(name=app_name, body=client.V1DeleteOptions())
    else:
        exit(0)
else:
    try:
        print("Creating namesapace...")
        app_client.create_namespace(body)
    except Exception as e:
        print(e)