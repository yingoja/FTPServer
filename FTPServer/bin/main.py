#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings,template
from lib import common
from lib.user import Users
from bin import ftpserver
from dbhelper import dbapi

def run():
    while True:
        menu = template.START_MENU.format(menu1="[1] 启动服务",
                                          menu2="[2] 添加用户",
                                          menu3="[3] 删除用户",
                                          menu4="[4] 结束程序")
        print("\33[34;0m", menu,"\33[0m")
        num = str(input("请按编号选择：")).strip()
        if num == "1":
            ftpserver.process()
        elif num == "2":
            username = str(input("请输入用户名[输入q返回]：")).strip().lower()
            if username == 'q':
                continue
            new_user = Users(username)
            if not new_user.check_user():
                password = common.inp_msg("设置初始密码[默认12345]: ", default=str(settings.USER_PASSWORD))
                totalspace = common.inp_msg("设置磁盘配额[默认50M]: ", default=str(settings.HOME_QUOTA))
                print("\n正在初始化用户，请稍等.........\n")
                new_user.password = common.md5(password)
                new_user.totalspace = int(totalspace) * 1024 * 1024
                new_user.userspace = 0
                new_user.create_user()
                if new_user.check_user():
                    print("\033[35;0m初始化成功!\033[0m\n")
                else:
                    print("\033[35;0m初始化失败！\033[0m\n")
            else:
               print("\033[35;0m用户已经存在!\033[0m\n")
               continue
        elif num == "3":
            ret = dbapi.readall_sections()
            for x,y in enumerate(ret,1):
                print("%s%s%s" % (x, ".", y))
            inp = str(input("\33[35;0m请按序号选择[输入q|Q退出]：\33[0m")).strip().lower()
            if inp == "q":
                break
            user_ret = ret[int(inp) - 1]
            user = Users(user_ret)
            user.del_user()
            if not user.check_user():
                print("\033[35;0m用户",[user_ret],"删除成功！","\033[0m\n")
            else:
                print("\033[35;0m用户",[user_ret], "删除失败！", "\033[0m\n")
        elif num == "4":
            sys.exit()
        else:
            print("\033[35;0m无效选择，请重新选择!\033[0m\n")
