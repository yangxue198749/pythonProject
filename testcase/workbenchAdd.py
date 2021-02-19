# -*- coding: utf-8 -*-
"""
@Time ： 2021/2/16 20:25
@Auth ： yangxue
@File ：workbenchAdd.py
@IDE ：PyCharm
@Motto：Done Never late

"""
import  unittest
from parameterized import parameterized
from  interfaceTest.core import sendRequest,Authorizationhandler
from  interfaceTest.core import excleRead
from  interfaceTest.core import check
from interfaceTest.core import logger
import json,os
from interfaceTest.config import commonCofingRead

e=excleRead.ExcelData( r"D:\pythonProject\interfaceTest\testfile\workbench.xlsx","workbenchadd").readExcel()
l=logger.MyLogging().logger
headers=Authorizationhandler.Authorization("test-y-admin","yx123456").login()
print(headers)

class workbenchAdd(unittest.TestCase):
    def setUp(self) -> None:

        self.baseurl=commonCofingRead.conf.get('http','baseurl')
        # print(self.baseurl)

    def tearDown(self) -> None:
        pass


    @parameterized.expand(e)
    def test_workbenchadd(self,no,caseNo,casename,method,serverpath,isrun,data,check,message,result):
        global headers
        if isrun=='Y' or isrun=='y':
            l.info('【开始执行用例:{}】'.format(casename))
            self.data=json.loads(data)
            self.check=check
            self.message=message
            self.method=method
            l.info('检查状态码为：%s'%check)
            l.info('检查返回信息为：%s' %message)
            self.url=os.path.join(self.baseurl,serverpath)
            r=sendRequest.RunMethod()
            res=r.run_method(self.method,self.url,self.data,headers)
            l.info("返回内容为：%s"%res)
            self.assertEqual(res,check)







if __name__=="__main__":
    unittest.main()

