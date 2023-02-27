import json
import datetime
from collections import Counter
from data_manager import Config

dir_path = '%s/INFA100/' % Config.APPDATA

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
    save_ex = {"save_data": save_data, "easteregg_unlocked": False, "exam_history": [],
                "settings": {"size": "default", "name": None, "email": None},
                'update_time': str(datetime.datetime.now())}
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

def getStats() -> int:
    exam_history = read_save()["exam_history"]
    if not exam_history:
        return None
    vars_ever_solved = len(exam_history)
    all_results = [dct["result"] for dct in exam_history]
    res_first = round(sum(all_results) / len(all_results))
    res_ege = int(Config.POINTS[str(res_first)])
    return vars_ever_solved, res_first, res_ege

def getMostSolvedTasks() -> int:
    exam_history = read_save()["exam_history"]
    tasks_correct = dict(zip(range(1, 28), [0 for _ in range(28)]))
    tasks_incorrect = dict(zip(range(1, 28), [0 for _ in range(28)]))
    for dct in exam_history:
        for k in dct["tasks_info"]:
            if dct["tasks_info"][k]["correct"]:
                tasks_correct[int(k)] += 1
            else:
                tasks_incorrect[int(k)] += 1
    c = Counter(tasks_correct)
    most_correct = c.most_common(1)[0]
    cc = Counter(tasks_incorrect)
    most_incorrect = list(cc.most_common(1)[0])
    most_incorrect[1] = tasks_correct[most_incorrect[0]]
    return most_correct, tuple(most_incorrect)

def getExamHistory() -> list:
    exam_history = read_save()["exam_history"]
    res = []
    for dct in exam_history:
        time_as_str = dct["time"]
        time = datetime.datetime.strptime(time_as_str, '%Y-%m-%d %H:%M:%S.%f')
        time_formatted = Config.getTimeAsStr(time)
        result = dct["result"]
        res.append((time_formatted, result))
    return res

def addSettingsParameter() -> None:
    save_data = read_save()
    save_data["settings"] = {"size": "default", "name": None, "email": None}
    update_save(save_data)

def changeSize(new_size: str) -> None:
    save_data = read_save()
    save_data["settings"]["size"] = new_size
    update_save(save_data)

def getCurrentSettings() -> dict:
    save_data = read_save()
    return save_data["settings"]

def updateSettings(settings: dict) -> None:
    save_data = read_save()
    save_data["settings"] = settings
    update_save(save_data)

def addEasterEggParameter() -> None:
    save_data = read_save()
    save_data["easteregg_unlocked"] = False
    update_save(save_data)

def setEasterEggUnlocked() -> None:
    save_data = read_save()
    save_data["easteregg_unlocked"] = True
    update_save(save_data)

def checkIfEasterEggIsUnlocked() -> bool:
    save_data = read_save()
    return save_data["easteregg_unlocked"]

def addNameEmailParameters() -> None:
    save_data = read_save()
    save_data["settings"]["name"] = None
    save_data["settings"]["email"] = None
    update_save(save_data)