# -*- coding: utf-8 -*-
"""
@Time ： 2021/2/15 20:26
@Auth ： yangxue
@File ：commonCofingRead.py
@IDE ：PyCharm
@Motto：Done Never late

"""
import os
import configparser

# 读取commenConfig配数据
# os.path.realpath(__file__)：返回当前文件的绝对路径
# os.path.dirname()： 返回（）所在目录
cur_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(cur_path, "commonConfig.ini")  # 路径拼接：/config/db_config.ini
conf = configparser.ConfigParser()
conf.read(configPath, encoding="UTF-8")

baseurl=conf.get('http','baseurl')


if __name__=="__main__":
    hbase=os.path.join('http//:aod/','api')
    print(hbase)
