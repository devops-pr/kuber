import subprocess

# helm upgrade walmart-hackathon --namespace=walmart-hackathon --set image.repository=devopspr/walmart-hackathon --set image.tag=791d30d1e69e99f5d5dbc17583e3333f8f9fc8ed --set container.port=5000 --set service.port=5000 --set fullnameOverride=walmart-hackathon-kuber --set nameOverride=walmart-hackathon --set service.type=NodePort /tmp/kuber_tmp/kuber-charts/ --wait'


def install_app(app, port, chart_path, commit_hash, replicas, enable_autoscaling, min_pod, max_pod):
    install_command = ["helm", "install", app, "--namespace=" + app,
                       "--set", "image.repository=devopspr/" + app,
                       "--set", "image.tag=" + commit_hash,
                       "--set", "container.port="+str(port),
                       "--set", "service.port="+str(port),
                       "--set", "service.type=NodePort",
                       "--set", "fullnameOverride=" + app + "-kuber",
                       "--set", "nameOverride=" + app,
                       "--set", "replicaCount=" + str(replicas),
                       "--set", "autoscaling.enabled=" + enable_autoscaling,
                       "--set", "autoscaling.minReplicas=" + str(min_pod),
                       "--set", "autoscaling.maxReplicas=" + str(max_pod),
                       chart_path + "/", "--wait"
                       ]
    # print(install_command)
    try:
        print("Deploying the app...")
        subprocess.run(install_command)
    except Exception as e:
        print(e)


def updrade_app(app, port, chart_path, commit_hash, replicas, enable_autoscaling, min_pod, max_pod):
    install_command = ["helm", "upgrade", app, "--namespace=" + app,
                       "--set", "image.repository=devopspr/" + app,
                       "--set", "image.tag=" + commit_hash,
                       "--set", "container.port=" + str(port),
                       "--set", "service.port=" + str(port),
                       "--set", "fullnameOverride=" + app + "-kuber",
                       "--set", "nameOverride=" + app,
                       "--set", "service.type=NodePort",
                       "--set", "replicaCount=" + str(replicas),
                       "--set", "autoscaling.enabled=" + enable_autoscaling,
                       "--set", "autoscaling.minReplicas=" + str(min_pod),
                       "--set", "autoscaling.maxReplicas=" + str(max_pod),
                       chart_path+"/", "--wait"]
    # print(install_command)
    try:
        print("Upgrading the app...")
        subprocess.run(install_command)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pass
