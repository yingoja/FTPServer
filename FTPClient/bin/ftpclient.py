#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings,template,code
from lib import common
from lib.client import client

logger = common.Logger('ftpclient').getlog()


def run():
    common.message(template.START_MENU,"INFO")
    common.message("正在连接服务器 {0}:{1}......".format(settings.FTP_SERVER_IP,settings.FTP_SERVER_PORT),"INFO")

    #创建对象
    client_obj = client(settings.FTP_SERVER_IP,settings.FTP_SERVER_PORT)
    #连接服务器，返回结果
    conn_result = client_obj.connect()
    if conn_result == code.CONN_SUCC:
        common.message("连接成功！", "INFO")
        #客户端登录
        login_result = client_obj.login()
        if login_result:
            exit_flag = False
            while not exit_flag:
                show_menu = template.LOGINED_MENU.format(client_obj.username,
                                                         str(int(client_obj.totalspace / 1024 / 1024)),
                                                         str(int(client_obj.userspace / 1024 / 1024)))
                common.message(show_menu,"INFO")
                inp_command = common.input_command("[请输入命令]：")
                if inp_command == "quit":
                    exit_flag = True
                else:
                    #获取命令
                    func = inp_command.split("|")[0]
                    try:
                        if hasattr(client, func):
                            #从模块寻找到函数
                            target_func = getattr(client, func)
                            #执行函数
                            target_func(client_obj, inp_command)
                        else:
                            common.message("Client {0} 未找到".format(inp_command), "ERROR")
                    except Exception as e:
                        logger.error(e)
    else:
        common.message("连接失败！", "ERROR")
