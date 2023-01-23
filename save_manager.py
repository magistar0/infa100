import json
import datetime
import os

dir_path = '%s/INFA100/' %  os.environ['LOCALAPPDATA']

def read_save() -> dict:
    with open(dir_path + 'user_save.save', 'r', encoding='utf-8') as save_file:
        save_data = json.loads(save_file.read())
        return save_data

def update_save(save_data: dict) -> None:
    save_data['update_time'] = str(datetime.datetime.now())
    with open(dir_path + 'user_save.save', 'w', encoding='utf-8') as save_file:
        save_file.write(json.dumps(save_data, ensure_ascii=False))

def add_id_to_save(task: str, id: str) -> None:
    save_data = read_save()
    save_data['save_data'][str(task)].append(str(id))
    update_save(save_data)

def generate_empty_save() -> None:
    save_data = {}
    for task in range(1, 28):
        save_data[task] = []
    save_ex = {"save_data": save_data, "exam_history": [], 'update_time': str(datetime.datetime.now())}
    update_save(save_ex)

def check_id_in_save(task: str, id: str) -> bool:
    save_data = read_save()
    return str(id) in save_data['save_data'][str(task)]

def clear_task_data_in_save(task: str) -> None:
    save_data = read_save()
    save_data['save_data'][str(task)] = []
    update_save(save_data)

def get_save_data_for_task(task: str) -> list:
    save_data = read_save()
    return save_data['save_data'][str(task)]

def generate_result_dict(answers: list, results: list, tasks_data: dict) -> dict:
    user_result = {}
    for t in range(1, 28):
        dct = {"id": tasks_data[t]["id"], "answer": answers[t], "correct": results[t]}
        user_result[t] = dct
    return user_result

def write_var_completed_to_save(answers: list, results: list, tasks_data: dict, points: int) -> None:
    user_result = generate_result_dict(answers, results, tasks_data)
    exam_data = {
        "time": str(datetime.datetime.now()),
        "result": points,
        "tasks_info": user_result
    }
    save_data = read_save()
    if "exam_history" not in save_data:
        save_data["exam_history"] = []
    save_data["exam_history"].append(exam_data)
    update_save(save_data)

def clear_exam_history():
    save_data = read_save()
    save_data["exam_history"] = []
    update_save(save_data)