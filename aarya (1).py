from tkinter import ttk
import tkinter.messagebox as messagebox
import bisect
import requests
import socket
import os
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog


def save_output():
    # Get the content of the output field
    content = output_field_info.get("1.0", tk.END)
    # Get the file name from the user
    filename = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])    
    if filename:
        # Write the content to the file
        with open(filename, "w") as f:
            f.write(content)

def start_gather_info():
    # url = url_entry.get()
    url="http://testphp.vulnweb.com/"
    # Make an HTTP request to the website
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get the current text in the output field
    current_text = output_field_info.get("1.0", tk.END)
    # Add the HTTP status code to the output field
    output_field_info.delete("1.0", tk.END)
    output_field_info.insert(tk.END, current_text + f"Status code: {response.status_code}\n")
    output_field_info.update()
    # Add the web server software and version to the output field (if available)
    server = response.headers.get('Server')
    if server:
        output_field_info.insert(tk.END, f"Server: {server}\n")
        output_field_info.update()
    # Add the technologies used by the website to the output field (if available)
    technologies = response.headers.get('X-Powered-By')
    if technologies:
        output_field_info.insert(tk.END, f"Technologies: {technologies}\n")
        output_field_info.update()
    # Add the page title to the output field (if available)
    title = soup.find('title')
    if title:
        output_field_info.insert(tk.END, f"Title: {title.text}\n")
        output_field_info.update()
    # Add the number of links on the page to the output field
    links = soup.find_all('a')
    output_field_info.insert(tk.END, f"Number of links: {len(links)}\n")
    output_field_info.update()
    # Add the names and action URLs of any forms on the page to the output field
    forms = soup.find_all('form')
    for form in forms:
        output_field_info.insert(tk.END, f"Form name: {form.get('name')}\n")
        output_field_info.insert(tk.END, f"Form action: {form.get('action')}\n")
        # Add the number of input fields in each form to the output field
        inputs = form.find_all('input')
        output_field_info.insert(tk.END, f"Number of input fields in form {form.get('name')}: {len(inputs)}\n")
        output_field_info.update()
    # Add the URL of any images on the page to the output field
    images = soup.find_all('img')
    for image in images:
        output_field_info.insert(tk.END, f"Image URL: {image['src']}\n")
        output_field_info.update()
    # Add the HTTP headers of the response to the output field
    output_field_info.insert(tk.END, f"Headers: {response.headers}\n")
    output_field_info.update()


    
    

def scan_directories(url,directories):
        """Sends an HTTP request for each directory in the list and updates the output boxes with the result."""
        url =ip_address_entry.get()
        directories_dont_exist = []
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            for directory in directories:
                response = requests.get(f'{url}/{directory}')
                if response.status_code == 200:
                    output_field.insert(tk.END, f'{url}/{directory} exists\n')
                    output_field.update()
                else:
                    output_field.insert(tk.END, f'{url}/{directory} doesnt exists\n')
                    #to append===========================================================
                    directories_dont_exist.append(directory)
                    output_field.update()
        except socket.gaierror:
            # Unable to resolve the hostname of the URL
            output_field.insert(tk.END, f'Unable to resolve the hostname of {url}\n')
            output_field.update()
            
def read_directory_list(directory):
    """Reads the directory list from a file and returns it as a list."""
    try:
        with open(directory, 'r') as f:
            directories = f.read().splitlines()
        return directories
    except FileNotFoundError:
        output_field.insert(tk.END, f'{directory} does not exist\n')
        output_field.update()
        return []

def browse_file():
    # Show a file dialog to select a text file
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    # If a file is selected
    if file_path:
        # Call the insert_into_database function with the selected file's path
        print(file_path)
        
        return file_path
      
def check_directories(file_path):
    """Scans the URL using a directory list and updates the output boxes if none of the directories exist."""
    url = ip_address_entry.get()
    directory = file_path
    directories = read_directory_list(directory)
    scan_directories(url, directories)
    # if not directories:
    #     output_field.insert(tk.END, 'None of the directories in the list exist\n')
    
 
 
    
def highlight_search_text(output_field, search_text):
    if not search_text:
        messagebox.showinfo("Search Result", "Search cannot be blank", parent=directory_scan_frame)
        return

    # Remove previous highlight
    output_field.tag_remove('highlight', '1.0', tk.END)

    # Define the 'highlight' tag with a yellow background and black foreground
    output_field.tag_config('highlight', background='yellow', foreground='black')

    # Enable the text widget for editing
    output_field.config(state=tk.NORMAL)

    start_index = "1.0"
    found = False

    # Loop through the text widget and highlight each occurrence of the search text
    while True:
        start_index = output_field.search(search_text, start_index, stopindex=tk.END)
        if not start_index:
            break
        found = True
        end_index = f"{start_index}+{len(search_text)}c"
        output_field.tag_add('highlight', start_index, end_index)
        start_index = end_index

    # Disable the text widget for editing and display a message if no results were found
    output_field.config(state=tk.DISABLED)
    if not found:
        messagebox.showinfo("Search Result", "No results found", parent=directory_scan_frame)


        
        
        
        
        
        
        


def directory_scan():
    first_frame.grid_forget()
    directory_scan_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        directory_scan_frame.rowconfigure(i, minsize=50)
    for i in range(12):
        directory_scan_frame.columnconfigure(i, minsize=70)

def gather_info():
    first_frame.grid_forget()
    info_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        info_frame.rowconfigure(i, minsize=50)
    for i in range(12):
        info_frame.columnconfigure(i, minsize=70)

def back_to_main():
    directory_scan_frame.grid_forget()
    info_frame.grid_forget()
    first_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        first_frame.rowconfigure(i, minsize=50)
    for i in range(12):
        first_frame.columnconfigure(i, minsize=70)
        
root = tk.Tk()
root.geometry("900x700")
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4
root.geometry("+%d+%d" % (x, y))

first_frame = tk.Frame(root, bg="#006466")
first_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
for i in range(12):
    first_frame.rowconfigure(i, minsize=50)
for i in range(12):
    first_frame.columnconfigure(i, minsize=70)

project_text = ttk.Label(first_frame, text="Thaha Xina", font=("Travelast", 30), foreground="white", background="#006466")
project_text.grid(row=0, column=2, columnspan=3, pady=20, padx=50)

by_text = ttk.Label(first_frame, text="by", font=("Hanging Letters", 25), foreground="white", background="#006466")
by_text.grid(row=1, column=2, columnspan=3, pady=10, padx=10)

name_text = ttk.Label(first_frame, text="Aarya", font=("3x5", 35), foreground="white", background="#006466")
name_text.grid(row=2, column=2, columnspan=3, pady=(10,80), padx=10 ,sticky='n')

directory_scan_button = tk.Button(first_frame, text="Directory Scan", command=directory_scan, font=("Helvetica", 13), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="#1985a1")
directory_scan_button.grid(row=3, column=2, columnspan=3,sticky="s",  pady=10)
directory_scan_button.config(width=14)

gather_info_button = tk.Button(first_frame, text="Get Info", command=gather_info, font=("Helvetica", 13), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="#c5c3c6")
gather_info_button.grid(row=4, column=2, columnspan=3,sticky="s",  pady=10)
gather_info_button.config(width=14)

exit_button = tk.Button(first_frame, text="Exit", command=root.quit, font=("Helvetica", 13), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
exit_button.grid(row=5, column=2, columnspan=3, sticky="s",  pady=10)
exit_button.config(width=14)

work_text = ttk.Label(first_frame, text="Send file online using the Secure File Transfer Protocol.", font=("Helvetica",10), foreground="white", background="#006466")
work_text.grid(row=6, column=2, columnspan=1, pady=(80,5), padx=50)

style = ttk.Style()
style.configure("Round.TEntry", fieldbackground="#ffffff", background="transparent", 
                 bd=5, relief="flat", padding=2, borderwidth=2,
                 highlightcolor="#597678", highlightbackground="#597678", 
                 borderradius=10)


directory_scan_frame = tk.Frame(root, bg="#006466")

sign_up_text = ttk.Label(directory_scan_frame, text="Directory Scan", font=("Travelast", 20), foreground="white", background="#006466")
sign_up_text.grid(row=0, column=3, columnspan=1, pady=30, padx=50, sticky="nw")

################################################################################################################################
################################################################################################################################
################################################################################################################################



'''sign up frame ---- first name lable and entry '''
ip_address_label = tk.Label(directory_scan_frame, text="Enter a URL", font=("Helvetica", 12), foreground="white", background="#006466")
ip_address_entry = ttk.Entry(directory_scan_frame, width=35, font=("Helvetica", 12), foreground="#006466", style="Round.TEntry", background='gray')
ip_address_entry.configure(background='gray')
ip_address_label.grid(row=1, column=0, padx=20, pady=10,columnspan=2, sticky="W")
ip_address_entry.grid(row=1, column=1, padx=(40,20), pady=10,columnspan=3, sticky="W")


browse_button = tk.Button(directory_scan_frame, text="Browse", command=browse_file, font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
browse_button.grid(row=1, column=3,padx=(0,30),pady=20,sticky="e")
browse_button.config(width=8)

start_button = tk.Button(directory_scan_frame, text="Start", command=lambda:check_directories(file_path), font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
start_button.grid(row=1, column=4,padx=(30,0),pady=20, sticky="w")
start_button.config(width=8)







# output_field = tk.Text(directory_scan_frame, height=15, width=65, background="#dee2e6", font=("Helvetica", 12), foreground="black", highlightthickness=0)
# scrollbar = tk.Scrollbar(directory_scan_frame, command=output_field.yview)

# output_field.grid(row=3, column=0, pady=(30,5), padx=(125,10), columnspan=5, rowspan=4, sticky="w")
# scrollbar.grid(row=3, column=5, pady=(30,5), sticky="nsw", rowspan=4)

# output_field.configure(yscrollcommand=scrollbar.set)
# output_field.config(state="normal")
output_field = tk.Text(directory_scan_frame, height=20, width=75, background="white", font=("Helvetica", 12), foreground="black", highlightthickness=0)
scrollbar = tk.Scrollbar(directory_scan_frame, command=output_field.yview)

output_field.grid(row=2, column=0, pady=(30,5), padx=(125,0), columnspan=5, rowspan=4, sticky="w")
scrollbar.grid(row=2, column=5, pady=(30,5), sticky="nsw", rowspan=4)

output_field.configure(yscrollcommand=scrollbar.set)
output_field.config(state="normal")

# Create a container for the search entry and button
search_container = tk.Frame(output_field, height=30)
search_container.pack(side="top", fill="x")

# # Create the search entry and button
# search_entry = tk.Entry(search_container)
# search_entry.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)
# search_button = tk.Button(search_container, text="Search")
# search_button.pack(side="left", padx=(5, 10), pady=5)

search_entry = ttk.Entry(search_container, width=20, font=("Helvetica", 12), foreground="black", style="Round.TEntry", background='white')
search_entry.configure(background='black')
search_entry.pack(side="left", padx=(175, 10), pady=5)

search_button = tk.Button(search_container, text="Search", command=lambda: highlight_search_text(output_field, search_entry.get()), font=("Helvetica", 9), background="black", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
search_button.pack(side="left", padx=(5, 250), pady=5)
search_button.config(width=8)








# Add the search container to the output field
output_field.window_create("end", window=search_container)










# output_field = tk.Text(directory_scan_frame, height=15, width=60, background="#dee2e6", font=("Helvetica", 12), foreground="black", highlightthickness=0)
# scrollbar = tk.Scrollbar(directory_scan_frame, command=output_field.yview)
# output_field.configure(yscrollcommand=scrollbar.set)

# output_field.grid(row=3, column=0, pady=(30,5), padx=(125,10), columnspan=6, rowspan=4, sticky="w")
# scrollbar.grid(row=3, column=5, pady=(30,5), padx=(0,10), rowspan=3, sticky="nsw")
# output_field.config(state="normal")


'''sign up frame ---- back button '''
back_button = tk.Button(directory_scan_frame, text="Back", command=back_to_main, font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
back_button.grid(row=7, column=1, sticky="w",padx=10,pady=20)
back_button.config(width=8)


################################################################################################################################
################################################################################################################################
################################################################################################################################



info_frame = tk.Frame(root, bg="#006466")

log_in_text = ttk.Label(info_frame, text="Get Informations", font=("Travelast", 25), foreground="white", background="#006466")
log_in_text.grid(row=0, column=1, columnspan=4, pady=30, padx=50)



'''sign up frame ---- back button '''
back_button = tk.Button(info_frame, text="Back", command=back_to_main, font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
back_button.grid(row=6, column=1, sticky="w",padx=10,pady=210)
back_button.config(width=8)

url_label = tk.Label(info_frame, text="Enter a URL", font=("Helvetica", 12), foreground="white", background="#006466")
url_entry = ttk.Entry(info_frame, width=35, font=("Helvetica", 12), foreground="#006466", style="Round.TEntry", background='gray')
url_entry.configure(background='gray')
url_label.grid(row=1, column=0, padx=20, pady=10,columnspan=2, sticky="W")
url_entry.grid(row=1, column=1, padx=(40,20), pady=10,columnspan=3, sticky="W")


# output_field_info = tk.Text(info_frame, height=15, width=70, background="#dee2e6", font=("Helvetica", 12), foreground="black", highlightthickness=0)
# scrollbar = tk.Scrollbar(info_frame, command=output_field_info.yview)

# output_field_info.grid(row=2, column=1, pady=(30,5), padx=(0,0), columnspan=5, rowspan=4, sticky="nsew")
# scrollbar.grid(row=2, column=6, pady=(30,5), padx=(0,0), sticky="ns", rowspan=4)

# output_field_info.configure(yscrollcommand=scrollbar.set)
# output_field_info.config(state="normal")
import os




output_field_info = tk.Text(info_frame, height=20, width=70, background="white", font=("Helvetica", 12), foreground="black", highlightthickness=0)
scrollbar_info = tk.Scrollbar(info_frame, command=output_field_info.yview)

output_field_info.grid(row=2, column=0, pady=(30,5), padx=(125,0), columnspan=5, rowspan=4, sticky="w")
scrollbar_info.grid(row=2, column=5, pady=(30,5), sticky="nsw", rowspan=4)

output_field_info.configure(yscrollcommand=scrollbar_info.set)
output_field_info.config(state="normal")


start_button = tk.Button(info_frame, text="Start", command=lambda:start_gather_info(), font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
start_button.grid(row=1, column=3,padx=(0,0),pady=20, sticky="e")
start_button.config(width=8)


save_button = tk.Button(info_frame, text="Save", command=save_output, font=("Helvetica", 12), background="#065a60", 
                        foreground="white", relief="raised", bd=3, activebackground="#144552",activeforeground="red")
save_button.grid(row=5, column=4, padx=(10,0), pady=5, sticky="se")
save_button.config(width=8)


root.mainloop()