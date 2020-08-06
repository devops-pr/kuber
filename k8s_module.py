from kubernetes import client, config
# Configs can be set in Configuration class directly or using helper utility

def context_selection():
    global contexts, context
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        exit(0)
    contexts = [context['name'] for context in contexts]
    print("Available contexts: {}".format(contexts))
    print("Current active context: {}".format(active_context['name']))
    attempt = 0
    while attempt<3:
        change_context = input("Change Context?[Y/N]: ").lower()
        if change_context == "y":
            active_context_name = input("Enter the context you want to use: ").lower()
            if active_context_name not in contexts:
                if attempt < 2:
                    print("Invalid context provided. Try again.")
                    attempt += 1
                    continue
                else:
                    print("Wrong context name provided for 3 attempts. Exiting...")
                    exit(0)

            else:
                return active_context_name
        elif change_context == "n":
            return active_context['name']
        else:
            if attempt <2:
                print("Wrong input!!! Reply with [Y/N]")
                attempt += 1
                continue
            else:
                print("Wrong input provided for 3 attempts. Exiting...")
                exit(0)




app_context = context_selection()

client = client.CoreV1Api(api_client=config.new_client_from_config(context=app_context))
print("\nList of pods on %s:" % app_context)
for i in client.list_pod_for_all_namespaces().items:
    print("%s\t%s\t%s" %(i.status.pod_ip, i.metadata.namespace, i.metadata.name))