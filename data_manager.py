import json

for t in range(1, 28):
    file_path = 'data/tasks_data/%d/%d_data.json' % (t, t)
    file_name_local = 'data_%d_file' % t
    with open(file_path, 'r', encoding='utf-8') as locals()[file_name_local]:
        task_name_dict_local, task_name_list_local = 'task_%d_dict' % t, 'task_%d_list_of_dicts' % t
        locals()[task_name_dict_local] = json.loads(locals()[file_name_local].read())
        locals()[task_name_list_local] = locals()[task_name_dict_local]['tasks']

for el, index in (('Localization.json', 'loc'), ('config.jet', 'config')):
    with open('data/config/' + el, 'r', encoding='utf-8') as locals()[index + '_file']:
        locals()[index + '_dict'] = json.loads(locals()[index + '_file'].read())

class Localization(object):
    for name in globals()['loc_dict']:
        locals()[name] = globals()['loc_dict'][name]

class Config(object):
    for name in globals()['config_dict']:
        locals()[name] = globals()['config_dict'][name]