import tkinter
from tkinter import *
from tkinter import ttk
from common import *
import printlogger
from docker_module import *
from k8s_module import *
from git_module import *
from kubernetes import client, config
from helm_module import *


class Kuber:

    def __init__(self, master):
        self.master = master.title('Walmart Hackathon 2020')
        self.master = master.geometry('290x390')
        self.master = master.resizable(True, True)
        self.master = master.configure(background='#ececec')

        self.t = tkinter.Text()
        self.incorrect_counter = 0

        # create instance of file like object
        self.pl = printlogger.PrintLogger(self.t)

        # replace sys.stdout with our object
        sys.stdout = self.pl
        sys.stderr = self.pl

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#051f42')
        self.style.configure('TButton', background='#051f42')
        self.style.configure('TLabel', background='#051f42', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 28, 'bold'))
# *********************** HEADER FRAME ***********************
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack(pady=30)

# LABEL
        self.logo = PhotoImage(file='python_logo.gif').subsample(4, 4)
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, padx=7, rowspan=2)
        ttk.Label(self.frame_header, text='KUBER', style='Header.TLabel').grid(row=0, column=1)
        ttk.Label(self.frame_header, text="An uber tool for K8s onboarding").grid(row=1, column=1)

# *********************** CONTENT FRAME ***********************

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

# LABEL

        # Initial labels
        ttk.Label(self.frame_content, text="Git URL: ").grid(row=4, column=0, columnspan=2, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="K8s Cluster: ").grid(row=12, column=0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="No. of pods: ").grid(row=12, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub: \nUsername: ").grid(row=20, column=0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="\nPasssword: ").grid(row=20, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="App Port: ").grid(row=28, column=0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="Enable Autoscaling: ").grid(row=28, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Maximum No of pods: ").grid(row=36, column=1, padx=7, sticky='w')
        ttk.Label(self.frame_content, text="Minimum No of pods: ").grid(row=36, column=0, padx=5, sticky='w')

        # Error labels
        self.invalid_url = ttk.Label(self.frame_content, text="Invalid URL!!! ", foreground='red')
        self.inaccessible_url = ttk.Label(self.frame_content, text="Inaccessible URL!!! ", foreground='red')
        self.invalid_port = ttk.Label(self.frame_content, text="Invalid Port!!! ", foreground='red')
        self.invalid_docker_username = ttk.Label(self.frame_content, text="Wrong!!! ", foreground='red')
        self.invalid_docker_password = ttk.Label(self.frame_content, text="Wrong!!! ", foreground='red')
        self.invalid_max_no_of_pods = ttk.Label(self.frame_content, text="Wrong!!! ", foreground='red')
        self.invalid_min_no_of_pods = ttk.Label(self.frame_content, text="Wrong!!! ", foreground='red')

        # Success labels
        self.accessible_url = ttk.Label(self.frame_content, text="\u2713", foreground='green')
        self.valid_port = ttk.Label(self.frame_content, text="\u2713", foreground='green')
        self.valid_docker_username = ttk.Label(self.frame_content, text="\u2713", foreground='green')
        self.valid_docker_password = ttk.Label(self.frame_content, text="\u2713", foreground='green')
        self.valid_max_no_of_pods = ttk.Label(self.frame_content, text="\u2713", foreground='green')
        self.valid_min_no_of_pods = ttk.Label(self.frame_content, text="\u2713", foreground='green')

# ENTRY
        self.git_url_entry = ttk.Entry(self.frame_content, width=42, font=('Arial', 10))
        self.git_url_entry.grid(row=8, column=0, columnspan=2, padx=7, sticky='nw')
        self.docker_hub_user_entry = ttk.Entry(self.frame_content, font=('Arial', 10))
        self.docker_hub_user_entry.grid(row=24, column=0, padx=7, sticky='nw')
        self.docker_hub_password_entry = ttk.Entry(self.frame_content, font=('Arial', 10))
        self.docker_hub_password_entry.grid(row=24, column=1, padx=5, sticky='nw')
        self.docker_hub_password_entry.config(show='*')
        self.app_port_entry = ttk.Entry(self.frame_content, font=('Arial', 10))
        self.app_port_entry.grid(row=32, column=0, padx=7, sticky='nw')

# RADIO BUTTONS
        self.enable_autoscaling = StringVar()

        self.enable_autoscaling.set('N')

        self.enable_autoscaling_y_radiobutton = ttk.Radiobutton(self.frame_content,
                                                                text='Yes', variable=self.enable_autoscaling,
                                                                value='Y', command=self.enable_min_max)
        self.enable_autoscaling_y_radiobutton.grid(row=32, column=1, padx=5, sticky='w')
        self.enable_autoscaling_n_radiobutton = ttk.Radiobutton(self.frame_content,
                                                                text='No', variable=self.enable_autoscaling,
                                                                value='N', command=self.disable_min_max)
        self.enable_autoscaling_n_radiobutton.grid(row=32, column=1, padx=55, sticky='w')


# BUTTONS
        self.validate_button = ttk.Button(self.frame_content, text='Validate', command=self.validate)
        self.validate_button.grid(row=44, column=0, padx=0, pady=5, sticky='e')
        self.clear_button = ttk.Button(self.frame_content, text='Clear', command=self.clear)
        self.clear_button.grid(row=44, column=1, padx=0, pady=5, sticky='w')
        self.onboard_button = ttk.Button(self.frame_content, text='Lets Onboard', command=self.onboard, width=20)

# SPINBOXES
        self.min_no_of_pods = IntVar()
        self.min_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=self.min_no_of_pods,
                                              width=10,
                                              state='disabled')
        self.min_no_of_pods_spinbox.grid(row=40, column=0, padx=7, pady=5, sticky='w')
        self.max_no_of_pods = IntVar()
        self.max_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3,
                                              textvariable=self.max_no_of_pods, width=10,
                                              state='disabled')
        self.max_no_of_pods_spinbox.grid(row=40, column=1, padx=5, pady=5, sticky='w')

        self.no_of_pods = IntVar()
        self.no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=self.no_of_pods, width=10,
                                          state='readonly')
        self.no_of_pods_spinbox.grid(row=16, column=1, padx=5, pady=5, sticky='w')

# COMBO BOX
        self.context = StringVar()
        self.context_combobox = ttk.Combobox(self.frame_content, textvariable=self.context, width=12,
                                             state='readonly')
        self.context_combobox.grid(row=16, column=0, padx=5, pady=5, sticky='nw')
        self.context_combobox.config(values=())

        # self.GIT_URL=self.git_url_entry.get()
        # self.DOCKER_HUB_USER=self.docker_hub_user_entry.get()
        # self.DOCKER_HUB_PASSWORD=self.docker_hub_password_entry.get()
        # self.CLUSTER_NAME=self.context.get()
        # self.NO_OF_PODS=self.no_of_pods.get()
        # self.APP_PORT=self.app_port_entry.get()
        # self.ENABLE_AUTOSCALING=self.enable_autoscaling.get()
        # self.MIN_POD=self.min_no_of_pods.get()
        # self.MAX_POD =self.max_no_of_pods.get()

    def enable_min_max(self):
        self.max_no_of_pods_spinbox.config(state='readonly')
        self.min_no_of_pods_spinbox.config(state='readonly')

    def disable_min_max(self):
        self.max_no_of_pods_spinbox.config(state='disabled')
        self.min_no_of_pods_spinbox.config(state='disabled')

    def clear(self):
        self.git_url_entry.delete(0, 'end')
        self.docker_hub_user_entry.delete(0, 'end')
        self.app_port_entry.delete(0, 'end')
        self.docker_hub_password_entry.delete(0, 'end')
        self.cleanup_validation_labels()

    def validate(self):
        self.incorrect_counter = 0
        self.cleanup_validation_labels()
        # Validate GIT access
        if not validate_url(self.git_url_entry.get()):
            self.invalid_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')
            self.incorrect_counter += 1
        elif not verify_url_accessibility(self.git_url_entry.get()):
            self.inaccessible_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')
            self.incorrect_counter += 1
        else:
            self.accessible_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')

        # Validate Port
        if not (self.app_port_entry.get()).isdigit():
            self.invalid_port.grid(row=28, column=0, columnspan=2, padx=55, sticky='sw')
            self.incorrect_counter += 1
        else:
            self.valid_port.grid(row=28, column=0, columnspan=2, padx=55, sticky='sw')

        # Validate Docker Credentials
        if not docker_login(self.docker_hub_user_entry.get(),
                            self.docker_hub_password_entry.get()) == "Login Succeeded":
            self.invalid_docker_username.grid(row=20, column=0, columnspan=2, padx=75, sticky='sw')
            self.invalid_docker_password.grid(row=20, column=1, columnspan=2, padx=75, sticky='sw')
            self.incorrect_counter += 1
        else:
            self.valid_docker_username.grid(row=20, column=0, columnspan=2, padx=75, sticky='sw')
            self.valid_docker_password.grid(row=20, column=1, columnspan=2, padx=75, sticky='sw')

        # print((self.min_no_of_pods).get())
        # print((self.max_no_of_pods).get())
        # Validate min max pod
        if self.enable_autoscaling.get() == "Y":
            if self.min_no_of_pods.get() > self.max_no_of_pods.get():
                self.invalid_min_no_of_pods.grid(row=36, column=0, columnspan=2, padx=75, sticky='sw')
                self.invalid_max_no_of_pods.grid(row=36, column=1, columnspan=2, padx=75, sticky='sw')
                self.incorrect_counter += 1
            else:
                self.valid_min_no_of_pods.grid(row=36, column=0, columnspan=2, padx=120, sticky='sw')
                self.valid_max_no_of_pods.grid(row=36, column=1, columnspan=2, padx=120, sticky='sw')

        if self.incorrect_counter == 0:
            self.validate_button.grid_remove()
            self.clear_button.grid_remove()
            self.style = ttk.Style()

            self.git_url_entry.state(['disabled'])
            self.docker_hub_user_entry.state(['disabled'])
            self.docker_hub_password_entry.state(['disabled'])
            self.app_port_entry.state(['disabled'])
            self.max_no_of_pods_spinbox.config(state='disabled')
            self.min_no_of_pods_spinbox.config(state='disabled')
            self.no_of_pods_spinbox.config(state='disabled')
            self.enable_autoscaling_n_radiobutton.state(['disabled'])
            self.enable_autoscaling_y_radiobutton.state(['disabled'])
            self.context_combobox.state(['disabled'])
            self.onboard_button.grid(row=44, column=0, columnspan=2, padx=30, pady=5, sticky='w')

    def onboard(self):
        self.t.pack()
        print("Onboarding started...\n\n")

        print("""
 ====WALMART HACKATHON 2020=====
  _   ___   _______ ___________ 
 | | / / | | | ___ \  ___| ___ \\
 | |/ /| | | | |_/ / |__ | |_/ /
 |    \| | | | ___ \  __||    / 
 | |\  \ |_| | |_/ / |___| |\ \ 
 \_| \_/\___/\____/\____/\_| \_|
 AN UBER TOOL FOR K8S ONBOARDING
                               
                               
""")
        self.git_repo = self.git_url_entry.get()
        self.working_dir = "/tmp/kuber_tmp/"
        create_workdir(self.git_repo, self.working_dir)
        self.project_path, self.latest_commit_hash, self.app_name = clone_repo(self.git_repo, self.working_dir)
        self.app_name = self.app_name.replace("_", "-")
        self.image_name = self.docker_hub_user_entry.get() + "/" + self.app_name
        self.tag = self.image_name + ":" + self.latest_commit_hash
        self.image_available_remote = check_image_availability_on_repo(self.image_name, self.latest_commit_hash)
        self.image_available_local = check_image_availability_on_local(self.tag)
        build_image(self.project_path, self.tag, self.image_available_local, self.image_name)
        push_image(self.image_name, self.image_available_remote)
        self.app_context = self.context.get()
        self.corev1apiclient = client.CoreV1Api(api_client=config.new_client_from_config(context=self.app_context))
        self.available_ns = get_available_ns(self.corev1apiclient)
        self.v1namespaceclient = client.V1Namespace()
        self.v1namespaceclient.metadata = client.V1ObjectMeta(name=self.app_name)
        self.chart_git_repo = "https://github.com/devops-pr/kuber-charts.git"
        self.chart_path = clone_chart(self.chart_git_repo, self.working_dir)
        self.port = self.app_port_entry.get()

    def cleanup_validation_labels(self):
        self.invalid_url.grid_remove()
        self.inaccessible_url.grid_remove()
        self.accessible_url.grid_remove()
        self.invalid_port.grid_remove()
        self.valid_port.grid_remove()
        self.valid_docker_username.grid_remove()
        self.invalid_docker_username.grid_remove()
        self.valid_docker_password.grid_remove()
        self.invalid_docker_password.grid_remove()
        self.invalid_min_no_of_pods.grid_remove()
        self.valid_min_no_of_pods.grid_remove()
        self.invalid_max_no_of_pods.grid_remove()
        self.valid_max_no_of_pods.grid_remove()


def main():
    root = Tk()

    feedback = Kuber(root)

    current_context, all_contexts = available_contexts()

    all_contexts_tuple = tuple([context['name'] for context in all_contexts])
    current_context_name = current_context['name']
    feedback.context.set(current_context_name)
    feedback.context_combobox.config(values=all_contexts_tuple)
    root.mainloop()


if __name__ == "__main__":
    main()
