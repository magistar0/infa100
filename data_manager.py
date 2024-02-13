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
import requests
import ftplib
import threading
from itertools import chain
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


for t in chain(range(1, 19), range(22, 28), ("19-21",)):
    file_path = f'data/tasks_data/{t}/{t}_data.json'
    file_name_local = f'data_{t}_file'
    with open(file_path, 'r', encoding='utf-8') as locals()[file_name_local]:
        task_name_dict_local, task_name_list_local = f'task_{t}_dict', f'task_{t}_list_of_dicts'
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
    
    TECH_SITE = "https://tech.sga235.ru/"
    H, U, P, E_TKN = None, None, None, None
    if checkInternetConnection():
        tkns_dct = eval(requests.get(TECH_SITE + "monkey.json", headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}).content.decode())
        H = base64.b64decode(tkns_dct["h"] + "==").decode("utf-8")
        U = base64.b64decode(tkns_dct["u"] + "==").decode("utf-8")
        P = base64.b64decode(tkns_dct["p"] + "==").decode("utf-8")
        E_TKN = base64.b64decode(tkns_dct["e"] + "==").decode("utf-8")

    def ftp_upload(filename, filepath):
        ftp_server = ftplib.FTP(Config.H, Config.U, Config.P)
        ftp_server.encoding = "utf-8"
        with open(filepath, "rb") as file:
            ftp_server.storbinary(f"STOR tech.sga235.ru/htdocs/infa100/{filename}", file)
        ftp_server.quit()

    def ftp_download(filename, filepath):
        ftp_server = ftplib.FTP(Config.H, Config.U, Config.P)
        ftp_server.encoding = "utf-8"
        with open(filepath, "wb") as file:
            ftp_server.retrbinary(f"RETR tech.sga235.ru/htdocs/infa100/{filename}", file.write)
        ftp_server.quit()

    def ftp_check(filename):
        ftp_server = ftplib.FTP(Config.H, Config.U, Config.P)
        ftp_server.encoding = "utf-8"
        files_list = ftp_server.nlst("tech.sga235.ru/htdocs/infa100")
        ftp_server.quit()
        return filename in files_list

    def readTask22Example() -> str:
        with open("data/tasks_data/22/22_example.json", "r", encoding="utf-8") as f:
            example = json.loads(f.read())
        return example["example"]

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
    
    def getServerLoggingTimeFormat() -> str:
        now = datetime.datetime.now()
        date = str(now)[:-7]
        return date

    def getLatestBuild() -> str:
        filepath = '%s/INFA100/current_build.json' %  Config.APPDATA
        Config.ftp_download("current_build.json", filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        os.remove(filepath)
        return data['current_build']

    def rewriteLatestBuild(build) -> None:
        filepath = '%s/INFA100/current_build.json' %  Config.APPDATA
        writeable = {"current_build": str(build)}
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(writeable))
        Config.ftp_upload("current_build.json", filepath)
        os.remove(filepath)

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
        if not name:
            return False
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
        if not email:
            return True
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return not not re.match(pattern, email) or email is None
    
    def generateRunningFile():
        pth = '%s/INFA100/running.txt' %  Config.APPDATA
        with open(pth, "w", encoding="utf-8") as f:
            f.write("running")

    def deleteRunningFule():
        pth = '%s/INFA100/running.txt' %  Config.APPDATA
        os.remove(pth)

    def checkIfProgramIsCurrentlyRunning():
        pth = '%s/INFA100/running.txt' %  Config.APPDATA
        return os.path.exists(pth)


class Email(object):
    def send_message(receiver_email: str) -> tuple:
        smtp_server = "smtp.gmail.com"
        port = 587
        pswd = Config.E_TKN
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
        filepath = '%s/INFA100/last_id.json' %  Config.APPDATA
        Config.ftp_download("last_id.json", filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        os.remove(filepath)
        return data['last_id']

    def rewrite_last_id(num: int) -> None:
        filepath = '%s/INFA100/last_id.json' %  Config.APPDATA
        writeable = {"last_id": num}
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(writeable))
        Config.ftp_upload("last_id.json", filepath)
        os.remove(filepath)

    def save_var(tasks_data: dict) -> int:
        var_dict = {}
        for key in tasks_data:
            var_dict[key] = tasks_data[key]['id']
        
        var_id = ID_Vars.get_last_id() + 1
        ID_Vars.rewrite_last_id(var_id)
    
        filepath = '%s/INFA100/%d.json' % (Config.APPDATA, var_id)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(var_dict))
        Config.ftp_upload("%d.json" % var_id, filepath)
        os.remove(filepath)
        Logger.add_line_to_server_log("New var %d" % var_id)
        return var_id

    def check_if_id_is_valid(id: str) -> bool:
        id = str(id)
        filename = "%s.json" % id
        return Config.ftp_check(filename)

    def get_data_by_id(id: str) -> dict:
        id = str(id)
        filename = "%s.json" % id
        filepath = '%s/INFA100/%s.json' % (Config.APPDATA, id)
        Config.ftp_download(filename, filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            tasks_data = json.loads(f.read())
        os.remove(filepath)
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

    def generate_empty_server_log() -> None:
        filepath = '%s/INFA100/server_log' % Config.APPDATA
        with open(filepath, 'w', encoding='utf-8') as logf:
            logf.write(f"This is the server log which is created at {Config.getServerLoggingTimeFormat()}.\n\n")
        Config.ftp_upload("server_log", filepath)
        os.remove(filepath)

    def add_line_to_server_log(line:str) -> None:
        lineadd = threading.Thread(target=lambda: Logger.__add_line_to_server_log(line))
        lineadd.start()
    
    def __add_line_to_server_log(line: str) -> None:
        filepath = '%s/INFA100/server_log' % Config.APPDATA
        Config.ftp_download("server_log", filepath)
        with open(filepath, "r", encoding="utf-8") as logf:
            file_content = logf.read()
        new_line = '\n' + Config.getServerLoggingTimeFormat() + ' - ' + line
        file_content = file_content + new_line
        with open(filepath, 'w', encoding='utf-8') as logf:
            logf.write(file_content)
        Config.ftp_upload("server_log", filepath)
        os.remove(filepath)