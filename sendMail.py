# -*- coding: utf-8 -*-
"""
@Time ： 2021/1/7 18:36
@Auth ： yangxue
@File ：sendMail.py
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from core import configRead
import os

mailconf=configRead.cofingRead()
mail_data=mailconf.get_config_items('sendmail')

class sendMail:
    def __init__(self):
        self.mailserver = mail_data['mailsever']
        self._user = mail_data['user']
        self._password = mail_data['password']
        self.subject = mail_data['subject']
        self.sender = mail_data['from']
        self.receiver = mail_data['to']
        print(self.receiver,type(self.receiver))
        self.filepath = mail_data['report_dir']


    def sendmail(self, msg):
        try:
            self.smtp = smtplib.SMTP_SSL(self.mailserver)
            self.smtp.connect(self.mailserver)
        except Exception as e:
            print(e)
        try:
            self.smtp.login(self._user, self._password)
        except Exception as e:
            print('login fail', e)
        try:
            self.smtp.sendmail(self.sender, self.receiver, msg)
        except Exception as e:
            print('send fail', e)
        self.smtp.quit()

    def sendcontent(self, content):
        self.msg = MIMEText('%s' % content, 'plain', 'utf-8')
        self.sendto = ','.join(self.receiver)
        self.msg['Subject'] = Header(self.subject, 'utf-8')
        self.msg['From'] = self.sender
        self.msg['To'] = self.sendto  # 'yyl_yunlong@126.com'
        self.sendmail(self.msg.as_string())

    def sendmailwithfile(self, filepath):
        self.sendto = self.receiver
        self.file = os.path.basename(filepath)
        self.att= MIMEText(open(filepath,'rb').read(),'base64','utf-8')
        self.att['Content-Type'] = 'application/octet-stream'
        self.att['Content-Disposition'] = 'addachment;filename=%s' % self.file
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = self.subject
        self.msgRoot['From'] = self.sender
        self.msgRoot['To'] = self.sendto
        print(self.msgRoot.as_string())
        self.msgRoot.attach(self.att)
        self.sendmail(self.msgRoot.as_string())


if __name__=="__main__":
    m=sendMail()
    m.sendcontent('nihao')
    # m.sendmailwithfile('D:\pythonProject\workbench\log\config.log')