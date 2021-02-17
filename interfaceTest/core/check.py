# -*- coding: utf-8 -*-
"""
@Time ： 2021/2/15 20:19
@Auth ： yangxue
@File ：check.py
@IDE ：PyCharm
@Motto：Done Never late

"""
class IsInstance:

    def get_instance(self, value, check):
        flag = None
        if isinstance(value, str):
            if check == value:
                flag = True
            else:
                flag = False
        elif isinstance(value, float):
            if value - float(check) == 0:
                flag = True
            else:
                flag = False
        elif isinstance(value, int):
            if value - int(check) == 0:
                flag = True
            else:
                flag = False
        return flag

