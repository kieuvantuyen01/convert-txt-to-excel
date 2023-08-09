# 
# Write a GUI app to convert txt file to excel file, where:
# There are 2 running modes (run the whole folder or run a separate file, in which the default mode is to run the whole folder)
# There is a select section to select the path to the folder or file corresponding to each mode (shows the path and default value is C:/Users/TuyenKV/OneDrive - Tuyenkieuvan/Master/MAPF/kissat_arminbiere/output_v4)
# # There is a select section to select the output folder path and the default output folder path is ./output
# The excel file in process() method is put in the output folder
# There is a button to run and the generated excel file will be placed under the output path
# Show running progress (number of files finished / total number of files in the selected folder)
# The processing logic to convert txt to excel file is here:

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

def read_content_file(file_path):
    content = ''
    with open(file_path, 'r') as reader:
        content = reader.read()
    return content


def handleAnItem(raw):
    lines = raw.split('\n')
    obj = {}
    for line in lines:
        if line.startswith('s SAT') or line.startswith('s UNSAT') or line.startswith('UNKNOWN'):
            obj['status'] = line if line == 'UNKNOWN' else line[2:]
        elif line.startswith('c process-time'):
            obj['process_time'] = line[len('c process-time: '):]
        elif line.startswith('c p'):
            obj['num vars'] = line[len('c p: '):]
        elif line.startswith('c cnf'):
            obj['num clauses'] = line[len('c cnf: '):]
        elif '.cnf' in line:
            obj['file'] = line[2:]
    return obj


def convert_to_json(lst_raw):
    result = []
    for item in lst_raw:
        dict_item = handleAnItem(item)
        if dict_item.get('file') is not None:
            result.append(dict_item)
    return result


def convert_to_xslx(dict_data, excel_name):
    df = pd.DataFrame(data=dict_data)
    df.to_excel(excel_name, index=False)


def handle_one_file(file_path, output_name):
    content = read_content_file(file_path=file_path)
    items = content.split('-----\n')
    result = convert_to_json(items)
    convert_to_xslx(result, output_name)


def process(folder_path):
    lst_dir = os.listdir(folder_path)
    for dir_ in lst_dir:
        if dir_.endswith('.txt'):
            continue
        for file in os.listdir(f"{folder_path}/{dir_}"):
            file_path = os.path.join(folder_path, f'{dir_}/{file}')
            # let generated excel file be placed under output folder path
            output_name = f'{output_folder_path.get()}/{dir_}_{file[0:-4]}.xlsx'
            handle_one_file(file_path=file_path, output_name=output_name)
            # output_name = f'{dir_}_{file[0:-4]}.xlsx'
            # handle_one_file(file_path=file_path, output_name=output_name)

# GUI app
window = tk.Tk()
window.title("Convert txt to excel")
window.geometry("800x400")
window.resizable(1, 1)

# Select mode
mode = tk.StringVar()
mode.set("Run the whole folder")
mode_label = tk.Label(window, text="Select mode")
mode_label.grid(column=0, row=0)
mode_combobox = ttk.Combobox(window, width=20, textvariable=mode)
mode_combobox['values'] = ("Run the whole folder", "Run a separate file")
mode_combobox.grid(column=1, row=0)

# Select path
path_label = tk.Label(window, text="Select path")

# Select folder
folder_path = tk.StringVar()

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# set folder_path default value base on OS
# if Windows OS then folder_path is "C:/Users/TuyenKV/OneDrive - Tuyenkieuvan/Master/MAPF/kissat_arminbiere/output_v4"
# else folder_path is "/home/anh/kissat_arminbiere/output_v4"
if os.name == 'nt':
    folder_path.set("C:/Users/TuyenKV/OneDrive - Tuyenkieuvan/Master/MAPF/kissat_arminbiere/output_v4")
else:
    folder_path.set("/home/anh/kissat_arminbiere/output_v4")
folder_path_entry = tk.Entry(window, width=80, textvariable=folder_path)
folder_path_entry.grid(column=1, row=1)
folder_path_button = tk.Button(window, text="Select folder", command=select_folder)
folder_path_button.grid(column=2, row=1)

# Select file
file_path = tk.StringVar()

def select_file():
    file_selected = filedialog.askopenfilename()
    file_path.set(file_selected)

file_path.set("C:/Users/TuyenKV/OneDrive - Tuyenkieuvan/Master/MAPF/kissat_arminbiere/output_v4/binary/ALO.txt")
file_path_entry = tk.Entry(window, width=80, textvariable=file_path)
file_path_entry.grid(column=1, row=2)
file_path_button = tk.Button(window, text="Select file", command=select_file)
file_path_button.grid(column=2, row=2)

# Select output folder path
output_folder_path = tk.StringVar()

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_path.set(folder_selected)

# if the file_path name contains "/output_v" then the output folder path is "./output/v[next number]"
# else the output folder path is "./output"
if "/output_v" in file_path.get():
    output_folder_path.set(f"./output/ver{int(file_path.get().split('/output_v')[1][0])}")
else:
    output_folder_path.set("./output")

output_folder_path_entry = tk.Entry(window, width=50, textvariable=output_folder_path)
output_folder_path_entry.grid(column=1, row=3)
output_folder_path_button = tk.Button(window, text="Select output folder", command=select_output_folder)
output_folder_path_button.grid(column=2, row=3)

# Add a Generate button to display the output folder path and file_path
def generate():
    if mode.get() == "Run the whole folder":
        output_folder_path.set(f"./output/ver{int(folder_path.get().split('/output_v')[1][0])}")
    else:
        output_folder_path.set(f"./output/ver{int(file_path.get().split('/output_v')[1][0])}")
    output_folder_path_entry = tk.Entry(window, width=50, textvariable=output_folder_path)
    output_folder_path_entry.grid(column=1, row=3)
    output_folder_path_button = tk.Button(window, text="Select output folder", command=select_output_folder)
    output_folder_path_button.grid(column=2, row=3)

generate_button = tk.Button(window, text="Check output folder path", command=generate)
generate_button.grid(column=0, row=4)

# Run button and let all generated excel files be placed under output folder path
def run():
    if mode.get() == "Run the whole folder":
        process(folder_path=folder_path.get())
    else:
        handle_one_file(file_path=file_path.get(), output_name=f"{output_folder_path.get()}/{file_path.get().split('/')[-1][0:-4]}.xlsx")
    messagebox.showinfo("Information", "Finished!")

run_button = tk.Button(window, text="Run", command=run)
run_button.grid(column=1, row=4)

window.mainloop()