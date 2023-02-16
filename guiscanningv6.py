import tkinter as tk
import tkinter as ttk
from tkinter import messagebox
import bisect
import requests
import socket
# Define the "go_back" function
def go_back(window):
    window.destroy()
    main_window.deiconify()

# Create the main window
main_window = tk.Tk()
main_window.title("Web")
main_window.geometry("1000x800")

# Define a function to open the "Directory Scan" window
def show_directory_scan_window():
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else, remove-unnecessary-cast
    # Hide the main window
    main_window.withdraw()

    # Create the "Directory Scan" window
    directory_scan_window = tk.Toplevel(main_window)
    directory_scan_window.title("Directory Scan")
    directory_scan_window.geometry("1920x1080")
    
   
    #create widgets
    # Creathing a lable and a aentry field for Url entry
    url_label = tk.Label(directory_scan_window, text="Enter URL: ", font=("Helvetica", 16))
    url_label.config(fg="red")
    url_label.grid(row=0, column=0, padx=40, pady=10,sticky="w")

    url_input = tk.Entry(directory_scan_window)
    url_input.config(font=("Helvetica",16))
    # url_input.grid(row=0, column=1, padx=5, pady=0)
    url_input.grid(row=0, column=0, padx=250, pady=0,columnspan=3)

    #creating a lable and a entry for directory scan
    
    directory_label = tk.Label(directory_scan_window, text="Enter directory path: ", font=("Helvetica", 16))
    directory_label.config(fg="red")
    directory_label.grid(row=1, column=0, padx=40, pady=10,sticky="w")

    directory_input = tk.Entry(directory_scan_window)
    directory_input.config(font=("Helvetica", 16))
    # directory_input.grid(row=1, column=1, padx=5, pady=5)
    directory_input.grid(row=1, column=0, padx=25, pady=0,columnspan=3)



    directories_exist_output = tk.Text(directory_scan_window)
    directories_exist_output.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    directories_dont_exist_output = tk.Text(directory_scan_window)
    directories_dont_exist_output.grid(row=3, column=3, columnspan=2, padx=5, pady=5)

    search_directory_label = tk.Label(directory_scan_window, text="Search:", font=("Helvetica", 14))
    search_directory_label.config(fg="blue")
    search_directory_label.grid(row=2, column=3, padx=0, pady=10,sticky="w")
    search_directory_input = tk.Entry(directory_scan_window)
    search_directory_input.config(font=("Helvetica", 16))
    search_directory_input.grid(row=2, column=2, padx=175, pady=5,columnspan=2)


    def search(directories_dont_exist):
        directory = search_directory_input.get()
        if not directory:
            messagebox.showerror("Error", "Please enter a directory to search")
            return
        result = binary_search(directory, directories_dont_exist)
        if result:
            messagebox.showinfo("Result", f'{directory} not found')
        else:
            messagebox.showinfo("Result", f'{directory} found')


    
    def scan_directories(url, directories):
        """Sends an HTTP request for each directory in the list and updates the output boxes with the result."""
        directories_dont_exist = []
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            for directory in directories:
                response = requests.get(f'{url}/{directory}')
                if response.status_code == 200:
                    directories_exist_output.insert(tk.END, f'{url}/{directory} exists\n')
                    directories_exist_output.update()
                else:
                    directories_dont_exist_output.insert(tk.END, f'{url}/{directory} doesnt exists\n')
                    directories_dont_exist.append(directory)
                    directories_dont_exist_output.update()
        except socket.gaierror:
            # Unable to resolve the hostname of the URL
            directories_exist_output.insert(tk.END, f'Unable to resolve the hostname of {url}\n')
            directories_exist_output.update()

        directories_dont_exist.sort() # sort the list of directories that don't exist
        search_button = tk.Button(directory_scan_window, text="Search", command=lambda : search(directories_dont_exist))
        search_button.grid(row=13, column=3)
        
        # , padx=5, pady=5

    def read_directory_list(directory):
        """Reads the directory list from a file and returns it as a list."""
        try:
            with open(directory, 'r') as f:
                directories = f.read().splitlines()
            return directories
        except FileNotFoundError:
            directories_exist_output.insert(tk.END, f'{directory} does not exist\n')
            directories_exist_output.update()
            return []

    def check_directories():
        """Scans the URL using a directory list and updates the output boxes if none of the directories exist."""
        url = url_input.get()
        directory = directory_input.get()
        directories = read_directory_list(directory)
        scan_directories(url, directories)
        if not directories:
            directories_exist_output.insert(tk.END, 'None of the directories in the list exist\n')
    def binary_search(directory, directories_list):
        """Performs a binary search on the sorted list of directories to see if the given directory exists"""
        i = bisect.bisect_left(directories_list, directory)
        if i != len(directories_list) and directories_list[i] == directory:
            return True
        return False
        
    #create a button to call the check_directories method
    check_button = tk.Button(directory_scan_window, text="Scan", command=check_directories)
    check_button.grid(row=2, column=1, padx=5, pady=5)
    #create a back button 
    back_button = tk.Button(directory_scan_window, text="Back", command=lambda: go_back(directory_scan_window))
    back_button.grid(row=12, column=0, padx=5, pady=5)



# Create the "Directory Scan" button
directory_scan_button = tk.Button(main_window, text="Directory Scan", command=show_directory_scan_window)
directory_scan_button.grid(row=1, column=0)

# Run the Tkinter event loop
main_window.mainloop()