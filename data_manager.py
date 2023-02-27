import json
import smtplib
import ssl
import datetime
import os
import socket
import base64
import sys
import pathlib
import Levenshtein
import re
from github import Github
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


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

    def getPrintfText(key: str) -> str:
        return Localization.__dict__[key.upper()]


class Config(object):
    for name in globals()['config_dict']:
        locals()[name] = globals()['config_dict'][name]
    a, j, k = b'Z2hwX2hMMG5RUGd0R3', b'ElpYzNlbnlFNA', b'liZlAwWksyU2cwOFEzTzNha'
    g_token = base64.b64decode(a + k + j + b"==").decode("utf-8")
    aa, jj = b'Y3Nob3Z2eg', b'd3pzcGlzeWpr'
    e_token = base64.b64decode(jj + aa + b"==").decode("utf-8")

    def getAppData() -> str:
        home = pathlib.Path.home()
        match sys.platform:
            case pl if pl.startswith("linux"):
                return home / ".local/share"
            case "darwin":
                return home / "Library/Application Support"
            case _:
                return os.environ['LOCALAPPDATA']
    APPDATA = getAppData()

    def getTimeAsStr(datetime: datetime.datetime) -> str:
        date = str(datetime.date())
        year = date[:4]
        month = date[5:7]
        day = date[8:]
        time = str(datetime.time())[:5]
        return '.'.join([day, month, year]) + ', ' + time

    def getCurrentTimeAsStr() -> str:
        now = datetime.datetime.now()
        return Config.getTimeAsStr(now)

    def checkInternetConnection() -> bool:
        try:
            socket.gethostbyaddr('www.yandex.ru')
        except socket.herror:
            try:
                socket.gethostbyaddr('www.google.com')
            except socket.gaierror:
                return False
        except socket.gaierror:
            return False
        return True

    def getLatestBuild() -> str:
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        contents = repo.get_contents("current_build.json")
        pre_decode = contents.decoded_content
        data = json.loads(pre_decode)
        return data['current_build']

    def rewriteLatestBuild(build) -> None:
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        writeable = {"current_build": str(build)}
        contents = repo.get_contents("current_build.json")
        repo.update_file(contents.path, "обновление current build", str(writeable).replace("'", '"'), contents.sha, branch='main')

    def checkIfBuildIsLatest() -> bool:
        latest_build = Config.getLatestBuild()
        return latest_build == Config.build

    def getCountEnding(num: int) -> str:
        if 11 <= num % 100 <= 14:
            form = "plural_1"
        elif 2 <= num % 10 <= 4:
            form = "plural_0"
        elif num % 10 == 1:
            form = "singular"
        else:
            form = "plural_1"
        return form

    def getFontSize(setting) -> int:
        parameters = Config.SIZE_PARAMETERS
        return parameters[setting]["font"]

    def multiplyNumberAccordingToSize(number: int, size: str) -> int:
        parameters = Config.SIZE_PARAMETERS
        multiplier = parameters[size]["multiplier"]
        return int(number * multiplier)

    def getFontStyleFromSize(size: str) -> str:
        parameters = Config.SIZE_PARAMETERS
        return parameters[size]["font-family"]

    def getEasterEggTriggers() -> list:
        triggers_asstr = Config.EASTEREGG_TRIGGERS
        return triggers_asstr.split("|")

    def stringsAreClose(s1: str, s2: str) -> bool:
        distance = Levenshtein.distance(s1, s2)
        return distance <= len(max(s1, s2, key=len)) / 4

    def checkIfNameNeedsToBeTriggered(name: str) -> bool:
        triggers = Config.getEasterEggTriggers()
        for trigger in triggers:
            if Config.stringsAreClose(trigger.lower(), name.lower()):
                return True
        return False

    def getButtonStyles() -> dict:
        return Config.button_styles
    
    def checkIfSizeWasChanged(old_settings: dict, new_settings: dict) -> bool:
        return old_settings["size"] != new_settings["size"]
    
    def emailIsValid(email: str) -> bool:
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return not not re.match(pattern, email) or email is None


class Email(object):
    def send_message(receiver_email: str) -> tuple:
        smtp_server = "smtp.gmail.com"
        port = 587
        pswd = Config.e_token
        sender_email = 'infa100mail@gmail.com'
        msg_subject = Localization.EMAIL_SUBJECT
        msg_filename = '%s/INFA100/result.txt' %  Config.APPDATA
        with open(msg_filename, 'r', encoding='utf-8') as result_file_temp:
            msg_text_from_file = result_file_temp.read()
        msg_text = Localization.EMAIL_TEXT + '\n\n\n\n' + msg_text_from_file

        msg = MIMEMultipart()
        msg["Subject"] = msg_subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        body_text = MIMEText(msg_text, 'plain')  
        msg.attach(body_text)

        with open(msg_filename, 'rb') as fp:
            attachment = MIMEApplication(fp.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(msg_filename))
            msg.attach(attachment)

        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, pswd)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            server.quit()
            return (False, e)
        else:
            server.quit()
            return (True, "")


class ID_Vars(object):
    def get_last_id() -> int:
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        contents = repo.get_contents("last_id.json")
        pre_decode = contents.decoded_content
        data = json.loads(pre_decode)
        return data['last_id']

    def rewrite_last_id(num: int) -> None:
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        writeable = {"last_id": num}
        contents = repo.get_contents("last_id.json")
        repo.update_file(contents.path, "обновление last id", str(writeable).replace("'", '"'), contents.sha, branch='main')

    def save_var(tasks_data: dict) -> int:
        var_dict = {}
        for key in tasks_data:
            var_dict[key] = tasks_data[key]['id']
        
        var_id = ID_Vars.get_last_id() + 1
        ID_Vars.rewrite_last_id(var_id)

        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        filename = "%d.json" % var_id
        repo.create_file(filename, "new var (%d)" % var_id, json.dumps(var_dict), branch="main")
        return var_id

    def check_if_id_is_valid(id: str) -> bool:
        id = str(id)
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        contents = repo.get_contents("")
        filename = "%s.json" % id
        for elem in contents:
            str_elem = str(elem)
            if "ContentFile(path=\"%s\")" % filename in str_elem:
                return True
        return False

    def get_data_by_id(id: str) -> dict:
        id = str(id)
        g = Github(Config.g_token)
        user = g.get_user()
        repo = user.get_repos()[0]
        filename = "%s.json" % id
        contents = repo.get_contents(filename)
        pre_decode = contents.decoded_content
        tasks_data = json.loads(pre_decode)
        return tasks_data


class Logger(object):
    log_path = '%s/INFA100/log.txt' %  Config.APPDATA

    def generate_empty_log() -> None:
        with open(Logger.log_path, 'w', encoding='utf-8') as logf:
            logf.write("This is the log file. Please do not modify any of the lines.\n\n")

    def add_line_to_log(line: str) -> None:
        with open(Logger.log_path, 'r', encoding='utf-8') as logf:
            file_content = logf.read()
        new_line = '\n' + Config.getCurrentTimeAsStr() + ' - ' + line
        file_content = file_content + new_line
        with open(Logger.log_path, 'w', encoding='utf-8') as logf:
            logf.write(file_content)