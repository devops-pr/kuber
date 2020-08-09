import subprocess

# helm install walmart-hackathon --namespace=walmart-hackathon  --set image.repository=devopspr/walmart_hackathon,image.tag=latest --set container.port=5000,service.type=NodePort  kuber-chart-template
# helm list --all-namespace
# helm status walmart-hackathon --namespace=walmart-hackathon
# helm history walmart-hackathon --namespace=walmart-hackathon
# helm template walmart-hackathon --namespace=walmart-hackathon  --set image.repository=devopspr/walmart_hackathon,image.tag=latest --set container.port=5000,service.type=NodePort,service.port=5000  kuber-chart-template
# subprocess.run(["helm", "version"])


def install_app(app, port, chart_path):
    install_command = ["helm", "install", app, "--namespace="+app,  "--set", "image.repository=devopspr/"+app,
                                                                    "--set", "image.tag=latest",
                                                                    "--set", "container.port="+str(port),
                                                                    "--set", "service.port="+str(port),
                                                                    "--set", "service.type=Nodeport",
                    chart_path]
    print(install_command)

if __name__ == '__main__':
    install_app("walmart-hackathon", 5000, "/tmp/")
