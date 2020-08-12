from tkinter import *
from tkinter import ttk
from k8s_module import available_contexts
from common import *


class Kuber:

    def __init__(self, master):
        master.title('Walmart Hackathon 2020')
        # master.geometry('930x480')
        master.geometry('290x390')
        master.resizable(False, False)
        master.configure(background='#ececec')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#051f42')
        self.style.configure('TButton', background='#051f42')
        self.style.configure('TLabel', background='#051f42', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 28, 'bold'))
# *********************** HEADER FRAME ***********************
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack(pady = 30)

# LABEL
        self.logo = PhotoImage(file='python_logo.gif').subsample(4, 4)
        ttk.Label(self.frame_header, image=self.logo).grid(row = 0, column = 0, padx=7, rowspan = 2)
        ttk.Label(self.frame_header, text='KUBER', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, text=("An uber tool for K8s onboarding")).grid(row = 1, column = 1)

# *********************** CONTENT FRAME ***********************

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

# LABEL

        #Initial labels
        ttk.Label(self.frame_content, text="Git URL: ").grid(row = 4, column = 0, columnspan = 2, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="K8s Cluster: ").grid(row=12, column = 0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="No. of pods: ").grid(row=12, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Username: ").grid(row = 20, column = 0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Passsword: ").grid(row = 20, column = 1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="App Port: ").grid(row = 28, column = 0, padx=7, sticky='sw')
        ttk.Label(self.frame_content, text="Enable Autoscaling: ").grid(row = 28, column = 1, padx=5, sticky='sw' )
        ttk.Label(self.frame_content, text="Maximum No of pods: ").grid(row = 36, column = 1, padx=7, sticky='w')
        ttk.Label(self.frame_content, text="Minimum No of pods: ").grid(row = 36, column = 0, padx=5, sticky='w')

        #Error labels
        self.invalid_url = ttk.Label(self.frame_content, text="Invalid URL!!! ", foreground = 'red')
        self.inaccessible_url = ttk.Label(self.frame_content, text="Inaccessible URL!!! ", foreground = 'red')

        #Success labels
        self.accessible_url = ttk.Label(self.frame_content, text="\u2713", foreground = 'green')

# ENTRY
        self.git_url_entry = ttk.Entry(self.frame_content, width=42, font = ('Arial', 10))
        self.git_url_entry.grid(row = 8, column = 0, columnspan = 2, padx=7, sticky='nw')
        # self.cluster = ttk.Entry(self.frame_content, font=('Arial', 10))
        # self.cluster.grid(row=16, column=0, padx=5, sticky='nw')
        # self.pods_count = ttk.Entry(self.frame_content, font=('Arial', 10))
        # self.pods_count.grid(row=16, column=1, padx=5, sticky='nw')
        self.docker_hub_user_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_user_entry.grid(row = 24, column = 0, padx=7, sticky='nw')
        self.docker_hub_password_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_password_entry.grid(row = 24, column = 1, padx=5, sticky='nw')
        self.docker_hub_password_entry.config(show='*')
        self.app_port_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.app_port_entry.grid(row = 32, column = 0, padx=7, sticky='nw')

# RADIO BUTTONS
        self.enable_autoscaling = StringVar()

        self.enable_autoscaling.set('N')

        self.enable_autoscaling_y_radiobuttont = ttk.Radiobutton(self.frame_content, text='Yes',
                                                           variable = self.enable_autoscaling, value='Y',
                                                           command = self.enable_min_max)
        self.enable_autoscaling_y_radiobuttont.grid(row = 32, column = 1, padx=5, sticky='w')
        self.enable_autoscaling_n_radiobuttont = ttk.Radiobutton(self.frame_content, text='No',
                                                            variable = self.enable_autoscaling, value='N',
                                                            command = self.disable_min_max)
        self.enable_autoscaling_n_radiobuttont.grid(row = 32, column = 1, padx=55, sticky='w')


# BUTTONS
        self.validate_button = ttk.Button(self.frame_content, text='Validate', command = self.validate)
        self.validate_button.grid(row = 44, column = 0, padx=0, pady=5, sticky='e')
        self.clear_button = ttk.Button(self.frame_content, text='Clear', command = self.clear)
        self.clear_button.grid(row = 44, column = 1, padx=0, pady=5, sticky='w')

# SPINBOXES
        self.min_no_of_pods = IntVar()
        self.min_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=self.min_no_of_pods, width=10,
                                              state = 'disabled')
        self.min_no_of_pods_spinbox.grid(row = 40, column = 0, padx=7, pady=5, sticky='w')


        self.max_no_of_pods = IntVar()
        self.max_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=self.max_no_of_pods, width=10,
                                              state = 'disabled')
        self.max_no_of_pods_spinbox.grid(row = 40, column = 1, padx=5, pady=5, sticky='w')

        self.no_of_pods = IntVar()
        self.no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=self.no_of_pods, width=10,
                                          state = 'readonly')
        self.no_of_pods_spinbox.grid(row=16, column=1, padx=5, pady=5, sticky='w')

#COMBO BOX
        self.context = StringVar()
        self.context_combobox = ttk.Combobox(self.frame_content, textvariable=self.context, width = 12, state= 'readonly')
        self.context_combobox.grid(row=16, column=0, padx=5, pady=5, sticky='nw')
        self.context_combobox.config(values=())

        self.GIT_URL = self.git_url_entry.get()
        self.DOCKER_HUB_USER = self.docker_hub_user_entry.get()
        self.DOCKER_HUB_PASSWORD = self.docker_hub_password_entry.get()
        self.CLUSTER_NAME = self.context.get()
        self.NO_OF_PODS = self.no_of_pods.get()
        self.APP_PORT = self.app_port_entry.get()
        self.ENABLE_AUTOSCALING = self.enable_autoscaling.get()
        self.MIN_POD = self.min_no_of_pods.get()
        self.MAX_POD = self.max_no_of_pods.get()

    def enable_min_max(self):
        self.max_no_of_pods_spinbox.config(state = 'readonly')
        self.min_no_of_pods_spinbox.config(state = 'readonly')
    def disable_min_max(self):
        self.max_no_of_pods_spinbox.config(state='disabled')
        self.min_no_of_pods_spinbox.config(state='disabled')

    def clear(self):
        self.git_url_entry.delete(0, 'end')
        self.docker_hub_user_entry.delete(0, 'end')
        self.app_port_entry.delete(0, 'end')
        self.docker_hub_password_entry.delete(0, 'end')

    def validate(self):
        if not validate_url(self.git_url_entry.get()):
            self.invalid_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')
        elif not verify_url_accessibility(self.git_url_entry.get()):
            self.inaccessible_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')
        else:
            self.accessible_url.grid(row=4, column=0, columnspan=2, padx=55, sticky='sw')




def main():
    root = Tk()
    feedback = Kuber(root)

    current_context, all_contexts =  available_contexts()

    all_contexts_tuple = tuple([context['name'] for context in all_contexts])
    current_context_name = current_context['name']
    feedback.context.set(current_context_name)
    feedback.context_combobox.config(values = all_contexts_tuple)
    root.mainloop()


if __name__ == "__main__": main()
