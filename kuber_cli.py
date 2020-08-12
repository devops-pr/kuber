from docker_module import *
from k8s_module import *
from git_module import *
from kubernetes import client, config
from helm_module import *


def main():
    global app_name, tag, corev1apiclient, v1namespaceclient
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
    git_repo = input("Please provide the scm repo: ")
    # git_repo = "https://github.com/devops-pr/walmart_hackathon.git" https://github.com/devops-pr/sample-app.git
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
    port = 5000

    def endpoint_display():
        APP_PORT = corev1apiclient.list_namespaced_service(app_name,
                                                           label_selector="app.kubernetes.io/name=" + app_name
                                                           ).items[0].spec.ports[0].node_port
        GRAFANA_PORT = corev1apiclient.list_namespaced_service("monitoring",
                                                               label_selector="app.kubernetes.io/name=grafana"
                                                               ).items[0].spec.ports[0].node_port
        PROMETHEUS_PORT = corev1apiclient.list_namespaced_service("monitoring",
                                                                  label_selector="app=prometheus-operator-prometheus"
                                                                  ).items[0].spec.ports[0].node_port
        KUBERNETES_DASHBOARD_PORT = corev1apiclient.list_namespaced_service("kubernetes-dashboard",
                                                                            label_selector="k8s-app=kubernetes-dashboard"
                                                                            ).items[0].spec.ports[0].node_port
        NODE = corev1apiclient.list_node().items[0].status.addresses[0].address
        print("\n\n\tAccess your app at: http://{0}:{1}\n\n\tMonitor your app at:\n\n"
              "\t\tGRAFANA: http://{0}:{2}\n"
              "\t\tKUBERNETES DASHBOARD: http://{0}:{3}\n"
              "\n\n".format(NODE, APP_PORT, GRAFANA_PORT, KUBERNETES_DASHBOARD_PORT))

    if app_name in available_ns:
        deploy = input("The app is already onboarded. "
                       "\nWhat you wish to do?[C[Cleanup app] / D[Deploy] / E[Display endpoint and exit]]: ").lower()
        if deploy == "d":
            print("Deploying latest application version...")  # deploy(app_name)
            updrade_app(app_name, port, chart_path, latest_commit_hash)
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
            install_app(app_name, port, chart_path, latest_commit_hash)
            endpoint_display()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()