from docker_module import *
from k8s_module import *
from git_module import *
from kubernetes import client
from helm_module import *

project_path, latest_commit_hash, app_name = clone_repo()
app_name = app_name.replace("_", "-")
image_name = "devopspr/" + app_name
tag = image_name + ":" + latest_commit_hash
image_available_remote = check_image_availability_on_repo(image_name, latest_commit_hash)
image_available_local = check_image_availability_on_local(tag)
build_image(project_path, tag, image_available_local, image_name)
push_image(image_name, image_available_remote)
app_context = context_selection()
corev1apiclient = client.CoreV1Api(api_client=config.new_client_from_config(context=app_context))
available_ns = get_available_ns(corev1apiclient)
v1namespaceclient = client.V1Namespace()
v1namespaceclient.metadata = client.V1ObjectMeta(name=app_name)
if app_name in available_ns:
    deploy = input("The app is already onboarded. Do you wish to deploy?[Y/N]: ").lower()
    # TODO: attemps for y/n
    if deploy == "y":
        print("Deploying...")   # deploy(app_name)
    elif deploy == "n":
        print("Deleting namespace {}...".format(app_name))
        corev1apiclient.delete_namespace(name=app_name, body=client.V1DeleteOptions())
    else:
        exit(0)
else:
    try:
        print("Creating namesapace...")
        corev1apiclient.create_namespace(v1namespaceclient)
    except Exception as e:
        print(e)

chart_git_repo = "https://github.com/devops-pr/kuber-charts.git"
chart_path = clone_chart(chart_git_repo)
install_app(app_name, 5000, chart_path)
