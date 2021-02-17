# -*- coding: utf-8 -*-
"""
@Time ： 2021/2/15 20:47
@Auth ： yangxue
@File ：sendMail.py
@IDE ：PyCharm
@Motto：Done Never late

"""
# send_email.py
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from interfaceTest.config import mailConfigRead
import smtplib


def send_email(subject, mail_body, file_names):
    # 获取邮件相关信息
    smtp_server = mailConfigRead.smtp_server
    port = mailConfigRead.port
    user_name = mailConfigRead.user_name
    password = mailConfigRead.password
    sender = mailConfigRead.sender
    receiver = mailConfigRead.receiver

    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = user_name
    msg["To"] = receiver
    msg.attach(body)

    # 附件:附件名称用英文
    for file_name in file_names:
        att = MIMEText(open(file_name, "rb").read(), "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = "attachment;filename='%s'" % (file_name)
        msg.attach(att)

    # 登录并发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_server)
        smtp.login(user_name, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
    except Exception as e:
        print(e)
        print("邮件发送失败！")
    else:
        print("邮件发送成功！")
    finally:
        smtp.quit()


if __name__ == '__main__':
    subject = "测试标题"
    mail_body = "测试本文"
    receiver = "13522069018@126.com"  # 接收人邮件地址 用逗号分隔
    file_names = [r'D:\pythonProject\interfaceTest\config\dbConfig.ini']
    send_email(subject, mail_body, file_names)

