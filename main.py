import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Progressbar
from fungi_id import files_to_id

import os

import threading

dir_select_entry = None
dir_save_entry = None
submit_button = None
dir_select_button = None
save_dir_button = None
progress_var = None
percentage_label = None
status_label = None

def start_processing():
    # Start the main function (perform_actions) with a subprocess
    progress_var.set(0)
    threading.Thread(target=perform_actions).start()

def perform_actions():
    selected_dir = dir_select_entry.get()
    selected_save_dir = dir_save_entry.get()

    if not selected_save_dir or not selected_dir:
        return

    submit_button.config(state=tk.DISABLED)
    dir_select_button.config(state=tk.DISABLED)
    save_dir_button.config(state=tk.DISABLED)

    if not os.path.exists(f"{selected_save_dir}/lab"):
        os.makedirs(f"{selected_save_dir}/lab")
    else:
        showerror("Folders exist", "The folders lab or kibana are exists in the destination folder, please move them or delete them")
        submit_button.config(state=tk.NORMAL)
        dir_select_button.config(state=tk.NORMAL)
        save_dir_button.config(state=tk.NORMAL)

    if not os.path.exists(f"{selected_save_dir}/kibana"):
        os.makedirs(f"{selected_save_dir}/kibana")
    else:
        showerror("Folders exist", "The folders lab or kibana are exists in the destination folder, please move them or delete them")
        submit_button.config(state=tk.NORMAL)
        dir_select_button.config(state=tk.NORMAL)
        save_dir_button.config(state=tk.NORMAL)


    progress_counter = 0
    total_files = 0
    for seq_folder in os.listdir(selected_dir):
        total_files += len([_ for _ in range(len(os.listdir(f"{selected_dir}/{seq_folder}/ASV")))])


    for seq_folder in os.listdir(selected_dir):
        os.makedirs(f"{selected_save_dir}/lab/{seq_folder}")
        os.makedirs(f"{selected_save_dir}/kibana/{seq_folder}")
        for file in os.listdir(f"{selected_dir}/{seq_folder}/ASV"):
            try:
                files_to_id(
                    asv_path=f"{selected_dir}/{seq_folder}/ASV/{file}",
                    texonomy_path=f"{selected_dir}/{seq_folder}/REP_TAXONOMY/{file.split('.')[0]}_rep_taxonomy.fasta.{file.split('.')[1]}",
                    rep_path=f"{selected_dir}/{seq_folder}/REP/{file.split('.')[0]}_rep.fasta.{file.split('.')[1]}",
                    seq=seq_folder,
                    output_dir=selected_save_dir
                )

                progress_counter += 1
                progress = (progress_counter / total_files) * 100
                progress_var.set(progress)
                percentage_label.config(text=(('%.2f ' % progress) + '%'))

            except FileNotFoundError as e:
                percentage_label.config(text="0 %")
                showerror("Error", "An error has occurred. File Not Found.")
                raise FileNotFoundError(e)

    showinfo("Success", f"All files have been saved in {selected_save_dir}")

    submit_button.config(state=tk.NORMAL)
    dir_select_button.config(state=tk.NORMAL)
    save_dir_button.config(state=tk.NORMAL)

def select_dir():
    # Ask for a directory and pasting the path in the field
    dir_path = filedialog.askdirectory()
    dir_select_entry.delete(0, tk.END)
    dir_select_entry.insert(0, dir_path)

def select_save_dir():
    # Ask for a directory and pasting the path in the field
    dir_path = filedialog.askdirectory()
    dir_save_entry.delete(0, tk.END)
    dir_save_entry.insert(0, dir_path)

def run_gui():
    global dir_select_entry, dir_save_entry, submit_button, dir_select_button, save_dir_button, progress_var, percentage_label, status_label
    # Create the main window
    root = tk.Tk()
    root.title('Lab Data Merger')
    root.iconphoto(False, tk.PhotoImage(file="./static/icons/plant.ico"))

    # Set the size and the color of the window
    root.geometry('400x475')
    root.configure(bg='#f0f0f0')

    # Create a title for the application
    title_label = tk.Label(root, text='Lab Data Merger', font=('Helvetica', 16, 'bold'))
    title_label.pack(pady=10)

    # Create a label widget for the directory entry
    dir_label = tk.Label(root, text='Select a directory:', font=('Helvetica', 14))
    dir_label.pack(pady=10)

    # Create an entry widget to display the selected directory path
    dir_select_entry = tk.Entry(root, width=40, font=('Helvetica', 12))
    dir_select_entry.pack(pady=10)

    # Create a button to select a directory
    dir_select_button = tk.Button(root, text='Browse', command=select_dir, bg='#007acc', fg='white',
                                  font=('Helvetica', 12))
    dir_select_button.pack(pady=10)

    dir_save_label = tk.Label(root, text="Select an output directory:", font=('Helvetica', 14))
    dir_save_label.pack(pady=10)

    # Create an entry widget to display the selected directory path
    dir_save_entry = tk.Entry(root, width=40, font=('Helvetica', 12))
    dir_save_entry.pack(pady=10)

    # Create a button to select a directory
    save_dir_button = tk.Button(root, text='Browse', command=select_save_dir, bg='#007acc', fg='white',
                                         font=('Helvetica', 12))
    save_dir_button.pack(pady=10)

    # Create Submit button
    submit_button = tk.Button(root, text='Submit', command=start_processing, bg='#4CAF50', fg='white',
                              font=('Helvetica', 12))
    submit_button.pack(pady=10)

    # Create a progress bar
    progress_var = tk.DoubleVar()
    progress_bar = Progressbar(root, length=300, variable=progress_var, mode='determinate')
    progress_bar.pack(pady=10)

    # Create a label to display the progress percentage
    percentage_label = tk.Label(root, text='0%', font=('Helvetica', 12))
    percentage_label.pack()

    # Create a label to display the status message
    status_label = tk.Label(root, text='', font=('Helvetica', 12))
    status_label.pack()

    # run the application
    root.mainloop()

if __name__ == "__main__":
    run_gui()


