import subprocess


def install_app(app, port, chart_path):
    install_command = ["helm", "install", app, "--namespace="+app,  "--set", "image.repository=devopspr/"+app,
                                                                    "--set", "image.tag=latest",
                                                                    "--set", "container.port="+str(port),
                                                                    "--set", "service.port="+str(port),
                                                                    "--set", "service.type=NodePort", chart_path+"/"]
    # print(install_command)
    try:
        subprocess.run(install_command)
    except Exception as e:
        print(e)


def updrade_app(app, chart_path):
    install_command = ["helm", "upgrade", app, "--namespace="+app,  "--set", "image.repository=devopspr/"+app,
                                                                    "--set", "image.tag=latest", chart_path+"/"]
    try:
        subprocess.run(install_command)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    install_app("walmart-hackathon", 5000, "/tmp/")
