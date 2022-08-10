import json
import smtplib
import ssl
import datetime
import os
import socket
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

class Config(object):
    for name in globals()['config_dict']:
        locals()[name] = globals()['config_dict'][name]

    def getCurrentTimeAsStr() -> str:
        now = datetime.datetime.now()
        date = str(now.date())
        year = date[:4]
        month = date[5:7]
        day = date[8:]
        time = str(now.time())[:5]
        return '.'.join([day, month, year]) + ', ' + time

    def checkInternetConnection() -> bool:
        try:
            socket.gethostbyaddr('www.yandex.ru')
        except socket.gaierror:
            return False
        return True


class Email(object):
    def send_message(receiver_email):

        smtp_server = "smtp.gmail.com"
        port = 587
        pswd = 'wzspisyjkcshovvz'
        sender_email = 'infa100mail@gmail.com'
        msg_subject = Localization.EMAIL_SUBJECT
        msg_filename = '%s/INFA100/result.txt' %  os.environ['APPDATA']
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
            return False
        else:
            server.quit()
            return True