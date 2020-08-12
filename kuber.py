from tkinter import *
from tkinter import ttk


class Kuber:

    def __init__(self, master):
        master.title('Kuber')
        master.resizable(False, False)
        master.configure(background='#ececec')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#051f42')
        self.style.configure('TButton', background='#051f42')
        self.style.configure('TLabel', background='#051f42', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        self.logo = PhotoImage(file='python_logo.gif').subsample(4, 4)
        ttk.Label(self.frame_header, image=self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text='KUBER').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, text=("An uber tool for K8s onboarding")).grid(row = 1, column = 1)


        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        # ttk.Label(self.frame_content, text='Name:')
        # ttk.Label(self.frame_content, text='Email:')
        # ttk.Label(self.frame_content, text='Comments:')
        #
        # self.entry_name = ttk.Entry(self.frame_content, width=24)
        # self.entry_email = ttk.Entry(self.frame_content, width=24)
        # self.text_comments = Text(self.frame_content, width=50, height=10)

        # ttk.Button(self.frame_content, text='Submit')
        # ttk.Button(self.frame_content, text='Clear')

        #####

        ttk.Label(self.frame_content, text="Git URL: ").grid(row = 0, column = 0, columnspan = 2, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Username: ").grid(row = 2, column = 0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Dockerhub Passsword: ").grid(row = 2, column = 1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="App Port: ").grid(row = 4, column = 0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text="Enable Autoscaling: ").grid(row = 4, column = 1, padx=5, sticky='sw' )
        max_no_of_pods_label = ttk.Label(self.frame_content, text="Maximum No of pods: ")
        min_no_of_pods_label = ttk.Label(self.frame_content, text="Minimum No of pods: ")


        self.git_url_entry = ttk.Entry(self.frame_content, width=68, font = ('Arial', 10))
        self.git_url_entry.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5, sticky='nw')
        self.docker_hub_user_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_user_entry.grid(row = 3, column = 0, padx=5, pady=5, sticky='nw')
        self.docker_hub_password_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.docker_hub_password_entry.grid(row = 3, column = 1, padx=5, pady=5, sticky='nw')
        self.docker_hub_password_entry.config(show='*')
        self.app_port_entry = ttk.Entry(self.frame_content, font = ('Arial', 10))
        self.app_port_entry.grid(row = 5, column = 0, padx=5, pady=5, sticky='nw')


        self.enable_autoscaling = StringVar()

        ttk.Radiobutton(self.frame_content, text='Yes', variable=self.enable_autoscaling, value='Y')\
            .grid(row = 5, column = 1, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(self.frame_content, text='No', variable=self.enable_autoscaling, value='N').\
            grid(row = 5, column = 1, padx=70, pady=5, sticky='w')

        ttk.Button(self.frame_content, text='Submit').grid(row = 8, column = 0, padx=100, pady=5, sticky='w')
        ttk.Button(self.frame_content, text='Clear').grid(row = 8, column = 1, padx=0, pady=5, sticky='w')


        min_no_of_pods_label.grid(row = 6, column = 0, padx=5, pady=10, sticky='w')
        min_no_of_pods = IntVar()
        Spinbox(self.frame_content, from_=1, to=3, textvariable=min_no_of_pods, width=8).\
            grid(row = 7, column = 0, padx=5, pady=5, sticky='w')
        print(min_no_of_pods.get())


        max_no_of_pods_label.grid(row = 6, column = 1, padx=5, pady=10, sticky='w')
        max_no_of_pods = IntVar()
        Spinbox(self.frame_content, from_=1, to=3, textvariable=max_no_of_pods, width=8).\
            grid(row = 7, column = 1, padx=5, pady=5, sticky='w')
        print(min_no_of_pods.get())

        # git_url_entry.pack()
        # docker_hub_user_entry.pack()
        # docker_hub_password_entry.pack()
        # app_port_entry.pack()


def main():
    root = Tk()
    feedback = Kuber(root)
    root.mainloop()


if __name__ == "__main__": main()
