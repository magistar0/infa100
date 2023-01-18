import json
import datetime
import os

dir_path = '%s/INFA100/' %  os.environ['APPDATA']

def read_save() -> dict:
    with open(dir_path + 'user_save.save', 'r', encoding='utf-8') as save_file:
        save_data = json.loads(save_file.read())
        return save_data

def add_id_to_save(task: str, id: str) -> None:
    save_data = read_save()
    save_data['save_data'][str(task)].append(str(id))
    save_data['update_time'] = str(datetime.datetime.now())
    with open(dir_path + 'user_save.save', 'w', encoding='utf-8') as save_file:
        save_file.write(json.dumps(save_data, ensure_ascii=False))

def generate_empty_save() -> None:
    save_data = {}
    for task in range(1, 28):
        save_data[task] = []
    with open(dir_path + 'user_save.save', 'w', encoding='utf-8') as sf:
        sf.write(json.dumps({"save_data": save_data, 'update_time': str(datetime.datetime.now())}, ensure_ascii=False))

def check_id_in_save(task: str, id: str) -> bool:
    save_data = read_save()
    return str(id) in save_data['save_data'][str(task)]

def clear_task_data_in_save(task: str) -> None:
    save_data = read_save()
    save_data['save_data'][str(task)] = []
    save_data['update_time'] = str(datetime.datetime.now())
    with open(dir_path + 'user_save.save', 'w', encoding='utf-8') as save_file:
        save_file.write(json.dumps(save_data, ensure_ascii=False))

def get_save_data_for_task(task: str) -> list:
    save_data = read_save()
    return save_data['save_data'][str(task)]

def generate_res_dict():
    pass