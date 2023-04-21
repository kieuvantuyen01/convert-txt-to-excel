import os
import pandas as pd

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


def main():
    folder_path = '/home/longcg18/workspace/kissat_arminbiere/output'
    lst_dir = os.listdir(folder_path)
    for dir_ in lst_dir:
        if dir_.endswith('.txt'):
            continue
        for file in os.listdir(f"{folder_path}/{dir_}"):
            file_path = os.path.join(folder_path, f'{dir_}/{file}')
            output_name = f'{dir_}_{file[0:-4]}.xlsx'
            handle_one_file(file_path=file_path, output_name=output_name)
            
        

if __name__ == '__main__':
    main()