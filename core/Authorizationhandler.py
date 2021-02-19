# -*- coding: utf-8 -*-
"""
@Time ： 2021/1/25 20:00
@Auth ： yangxue
@File ：Authorizationhandler.py
"""
import sys
sys.path.append(r'D:\pythonProject\workbench')
from interfaceTest.config import commonCofingRead
import os
import requests
import json
from interfaceTest.core import logger
import re
from interfaceTest.core import statics


class Authorization:
    def __init__(self,account=None,password=None,type='password'):
        self.account=account
        self.password=password
        self.type=type
        self.baseurl=commonCofingRead.conf.get('http','baseurl')
        print(self.baseurl,commonCofingRead.conf.get("http","accountServer"))
        self.verifyAccounturl=os.path.join(self.baseurl,commonCofingRead.conf.get("http","accountServer"))
        print(self.verifyAccounturl)
        self.header=statics.headers
        self.header2=statics.headers2
        self.l=logger.MyLogging().logger

    def login(self):
        vrifudata={}
        vrifudata['type']=self.type
        vrifudata['account']=self.account
        vrifudata['password']=self.password
        vrifudata['verifyCode']=""
        try:
            #调用认证接口
            self.verifyAccountResponse=requests.post(url=self.verifyAccounturl,headers=self.header,data=json.dumps(vrifudata))
            # 获取到认证
            self.Auth=self.verifyAccountResponse.headers.get('Set-Cookie').split(';')[0]
            #添加auth到cookie
            self.header['cookie']=self.header['cookie']+';'+self.Auth
            # print(self.header)
            #获取重定向的url
            self.loctionurl=self.verifyAccountResponse.json()['data']['casLoginUrl']
            self.l.info(self.verifyAccountResponse.json())

            #cas认证
            self.casloginParams={"redirectUrl":"%sportal/"%self.baseurl}
            self.casloginResponse=requests.get(url=self.loctionurl,headers=self.header,params=self.casloginParams,allow_redirects=False)
            # print(self.casloginResponse)
            __gm=self.casloginResponse.headers.get('Set-Cookie')
            self.loctionurl=self.casloginResponse.headers.get('Location')
            # print(self.loctionurl)
            self.header['cookie']=self.header['cookie']+';'+__gm

            #auth认证
            self.authenticateres=requests.get(url=self.loctionurl,headers=self.header,allow_redirects=False)
            #这次返回两个.JAVA.CLOUD.AUTH 第一个值为DELETEME 第二个才是想要得，所以要正则提取一下
            recompile = re.compile('.JAVA.CLOUD.AUTH=(.*?);')
            # 提取所有的.JAVA.CLOUD.AUTH
            compileall=re.findall(recompile,self.authenticateres.headers.get('Set-Cookie'))
            # 拿出不是DELETEME得那个，转成字符串形式
            toRplaceAuth=''.join([x for x in compileall if x!='deleteMe'])
            #从cookie里取出.JAVA.CLOUD.AUTH 然后替换一下
            RplaceAuth=''.join(re.findall(recompile,self.header['cookie']))
            #换一下认证
            self.header['cookie']=self.header['cookie'].replace(RplaceAuth,toRplaceAuth)
            #获取重定向地址
            self.loctionurl=self.authenticateres.headers.get('Location')
            #获取content内容
            self.contenturl=("http://geip-fat.glodon.com"+self.loctionurl)
            # print(self.contenturl)

            # 获取token
            self.contentResponse=requests.get(url=self.contenturl,headers=self.header,allow_redirects=False)
            needs = re.split('[,;]+', self.contentResponse.headers.get('Set-Cookie'))
            self.header['cookie'] = self.header['cookie'] + ";" + needs[0] + ";" + needs[2]
            self.loctionurl = self.contentResponse.headers.get('Location')

            #去广联云认证
            self.glyaccountResponse=requests.get(url=self.loctionurl,headers=self.header2,allow_redirects=False,verify=False)
            self.loctionurl=self.glyaccountResponse.headers.get('Location')

            #protal 认证一下

            requests.get(url=self.loctionurl,headers=self.header2)
            self.getmainparams = {"redirectUrl": "%sportal/"%self.baseurl}
            self.getmainurl=os.path.join(self.baseurl,'api/portal/v4/main')
            self.getmainResponse=requests.get(url=self.getmainurl,params=self.getmainparams,headers=self.header)

            #认证结束了，开始获取租户信息，第一个是获取账户下多少个租户
            self.header["Authorization"]="bearer "+toRplaceAuth
            self.getaccountinfourl=os.path.join(self.baseurl,'api/uaa/user')

            self.getaccountinfoResponse=requests.get(url=self.getaccountinfourl,headers=self.header)

            # 获取一下租户信息
            gettenatserver = 'api/tenant-user/v4/tenants/list-cur-user'
            self.gettenatserverurl = os.path.join(self.baseurl, gettenatserver)
            self.gettenalResoponse=requests.get(url=self.gettenatserverurl,headers=self.header)
            # print(self.getaccountinfoResponse.json())


            #获取租户的ids
            self.tenalid=[tid['id'] for tid in self.gettenalResoponse.json()]
            #获取租户token 用第一个租户id去获取
            self.getttokenurl = os.path.join(self.baseurl, 'identification/session/tenant') + '?tenantId=%d' % self.tenalid[0]

            self.tenalToken=requests.put(url=self.getttokenurl,headers=self.header).json()['tenantToken']
            self.header['Authorization']="bearer "+self.tenalToken

        except Exception as e:
            print('login fail :',e)


        return  self.header







if __name__=="__main__":
    A=Authorization('18500789646','yx123456')
    h=A.login()
    print(h['Authorization'])
# #




