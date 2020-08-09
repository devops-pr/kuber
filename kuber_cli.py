from docker_module import *
from k8s_module import *
from git_module import *
from kubernetes import client
from helm_module import *

print("""
    ======== WALMART HACKATHON 2020 ========
    
    ██   ██ ██    ██ ██████  ███████ ██████  
    ██  ██  ██    ██ ██   ██ ██      ██   ██ 
    █████   ██    ██ ██████  █████   ██████  
    ██  ██  ██    ██ ██   ██ ██      ██   ██ 
    ██   ██  ██████  ██████  ███████ ██   ██ 
                                             
    ==== AN UBER TOOL FOR K8S ONBOARDING ====
                                         
"""
                                                   )
# git_repo = input("Please provide the scm repo: ")
git_repo = "https://github.com/devops-pr/walmart_hackathon.git"
working_dir = "/tmp/kuber_tmp/"
create_workdir(git_repo, working_dir)
project_path, latest_commit_hash, app_name = clone_repo(git_repo, working_dir)
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
chart_git_repo = "https://github.com/devops-pr/kuber-charts.git"
chart_path = clone_chart(chart_git_repo, working_dir)


def endpoint_display():
    PORT = corev1apiclient.list_namespaced_service(app_name).items[0].spec.ports[0].node_port
    NODE = corev1apiclient.list_node().items[0].status.addresses[0].address
    print("\n\n\tAccess your app at: http://{}:{}\n\n".format(NODE, PORT))


if app_name in available_ns:
    deploy = input("The app is already onboarded. "
                   "What you wish to do?[C[Cleanup app] / D[Deploy] / E[Display endpoint and exit]]: ").lower()
    # TODO: attemps for y/n
    if deploy == "d":
        print("Deploying latest application version...")   # deploy(app_name)
        updrade_app(app_name, chart_path)
        endpoint_display()
    elif deploy == "e":
        endpoint_display()
        exit(0)
        # corev1apiclient.delete_namespace(name=app_name, body=client.V1DeleteOptions())
    elif deploy == "c":
        print("\n\nCleaning Up everything associated to {} application and exiting...BYE!!!\n\n".format(app_name))
        corev1apiclient.delete_namespace(name=app_name, body=client.V1DeleteOptions())
        delete_workdir(working_dir)
        exit(0)
else:
    try:
        print("Creating namesapace...")
        corev1apiclient.create_namespace(v1namespaceclient)
        install_app(app_name, 5000, chart_path)
        endpoint_display()
    except Exception as e:
        print(e)