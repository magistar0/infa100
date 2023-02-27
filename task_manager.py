import random
import data_manager
import save_manager
from typing import Union


class Task_Chooser:
    def choose_task(num: Union[int, str]) -> dict:
        list_name = 'task_%s_list_of_dicts' % str(num)
        data = data_manager.__dict__[list_name]

        filtered_data = list(filter(lambda dict: not save_manager.check_id_in_save(num, dict['id']), data))
        if filtered_data == []:
            save_manager.clear_task_data_in_save(num)
            chosen_task = random.choice(data)
        else:
            chosen_task = random.choice(filtered_data)
        return chosen_task

    def get_task_list(num: Union[int, str]) -> list:
        list_name = 'task_%s_list_of_dicts' % str(num)
        data = data_manager.__dict__[list_name]
        return data
    
    def get_task_by_id(task_num: Union[int, str], task_id: Union[int, str]) -> dict:
        list_name = 'task_%s_list_of_dicts' % str(task_num)
        data = data_manager.__dict__[list_name]
        for dct in data:
            if dct["id"] == str(task_id):
                return dct