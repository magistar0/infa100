import random
import data_manager
import save_manager

class Task_Chooser:
    def choose_task(num) -> dict:
        list_name = 'task_%s_list_of_dicts' % str(num)
        data = data_manager.__dict__[list_name]

        filtered_data = list(filter(lambda dict: not save_manager.check_id_in_save(num, dict['id']), data))
        if filtered_data == []:
            save_manager.clear_task_data_in_save(num)
            chosen_task = random.choice(data)
        else:
            chosen_task = random.choice(filtered_data)
        return chosen_task

    def get_task_list(num) -> list:
        list_name = 'task_%s_list_of_dicts' % str(num)
        data = data_manager.__dict__[list_name]
        return data