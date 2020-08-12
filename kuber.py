from tkinter import *
from tkinter import ttk


class Kuber:

    def __init__(self, master):
        master.title('Kuber')
        # master.geometry('930x480')
        master.geometry('430x380')
        master.resizable(False, False)
        master.configure(background='#ececec')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#051f42')
        self.style.configure('TButton', background='#051f42')
        self.style.configure('TLabel', background='#051f42', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))
# *********************** HEADER FRAME ***********************
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

# LABEL
        self.logo = PhotoImage(file='python_logo.gif').subsample(4, 4)
        ttk.Label(self.frame_header, image=self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text='KUBER', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, text=("An uber tool for K8s onboarding")).grid(row = 1, column = 1)

# *********************** CONTENT FRAME ***********************

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

# LABEL
        ttk.Label(self.frame_content, text="Git URL: ").grid(row = 4, column = 0, columnspan = 2, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="K8s Cluster: ").grid(row=12, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="No. of pods: ").grid(row=12, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Username: ").grid(row = 20, column = 0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Passsword: ").grid(row = 20, column = 1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="App Port: ").grid(row = 28, column = 0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Enable Autoscaling: ").grid(row = 28, column = 1, padx=5, sticky='sw' )
        ttk.Label(self.frame_content, text="Maximum No of pods: ").grid(row = 36, column = 0, padx=5, sticky='w')
        ttk.Label(self.frame_content, text="Minimum No of pods: ").grid(row = 36, column = 1, padx=5, sticky='w')

# ENTRY
        self.git_url_entry = ttk.Entry(self.frame_content, width=68, font = ('Arial', 10))
        self.git_url_entry.grid(row = 8, column = 0, columnspan = 2, padx=5, pady=5, sticky='nw')
        self.cluster = ttk.Entry(self.frame_content, font=('Arial', 10))
        self.cluster.grid(row=16, column=0, padx=5, pady=5, sticky='nw')
        self.pods_count = ttk.Entry(self.frame_content, font=('Arial', 10))
        self.pods_count.grid(row=16, column=1, padx=5, pady=5, sticky='nw')
        self.docker_hub_user_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_user_entry.grid(row = 24, column = 0, padx=5, pady=5, sticky='nw')
        self.docker_hub_password_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_password_entry.grid(row = 24, column = 1, padx=5, pady=5, sticky='nw')
        self.docker_hub_password_entry.config(show='*')
        self.app_port_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.app_port_entry.grid(row = 32, column = 0, padx=5, pady=5, sticky='nw')

# RADIO BUTTONS
        self.enable_autoscaling = StringVar()

        self.enable_autoscaling_y_radiobuttont = ttk.Radiobutton(self.frame_content, text='Yes',
                                                           variable = self.enable_autoscaling, value='Y',
                                                           command = self.enable_min_max)
        self.enable_autoscaling_y_radiobuttont.grid(row = 32, column = 1, padx=5, pady=5, sticky='w')
        self.enable_autoscaling_n_radiobuttont = ttk.Radiobutton(self.frame_content, text='No',
                                                            variable = self.enable_autoscaling, value='N',
                                                            command = self.disable_min_max)
        self.enable_autoscaling_n_radiobuttont.grid(row = 32, column = 1, padx=70, pady=5, sticky='w')


# BUTTONS
        ttk.Button(self.frame_content, text='Submit').grid(row = 44, column = 0, padx=100, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear').grid(row = 44, column = 1, padx=0, pady=5, sticky='w')


# SPINBOXES
        min_no_of_pods = IntVar()
        self.min_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=min_no_of_pods, width=8)
        self.min_no_of_pods_spinbox.grid(row = 40, column = 0, padx=5, pady=5, sticky='w')

        max_no_of_pods = IntVar()
        self.max_no_of_pods_spinbox = Spinbox(self.frame_content, from_=1, to=3, textvariable=max_no_of_pods, width=8)
        self.max_no_of_pods_spinbox.grid(row = 40, column = 1, padx=5, pady=5, sticky='w')

    def enable_min_max(self):
        # self.max_no_of_pods_spinbox.state(['!disabled'])
        self.max_no_of_pods_spinbox.config(state = 'readonly')
        self.min_no_of_pods_spinbox.config(state = 'readonly')
        # self.min_no_of_pods_spinbox.state(['!disabled'])
    def disable_min_max(self):
        # self.max_no_of_pods_spinbox.state(['disabled'])
        # self.min_no_of_pods_spinbox.state(['!disabled'])
        self.max_no_of_pods_spinbox.config(state='disabled')
        self.min_no_of_pods_spinbox.config(state='disabled')


def main():
    root = Tk()
    feedback = Kuber(root)
    root.mainloop()


if __name__ == "__main__": main()
