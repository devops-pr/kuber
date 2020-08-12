from kubernetes import config
# Configs can be set in Configuration class directly or using helper utility


def context_selection():
    active_context, contexts = available_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        exit(0)
    contexts = [context['name'] for context in contexts]
    print("Available contexts: {}".format(contexts))
    print("Current active context: {}".format(active_context['name']))
    attempt = 0
    while attempt < 3:
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
            if attempt < 2:
                print("Wrong input!!! Reply with [Y/N]")
                attempt += 1
                continue
            else:
                print("Wrong input provided for 3 attempts. Exiting...")
                exit(0)


def available_contexts():
    contexts, active_context = config.list_kube_config_contexts()
    return active_context, contexts


def get_available_ns(client):
    global available_ns
    available_ns = []
    for ns in client.list_namespace().items:
        available_ns.append(ns.metadata.name)
    return available_ns


