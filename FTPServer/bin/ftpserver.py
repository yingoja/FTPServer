#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import socketserver,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings,template
from lib import common,server



logger = common.Logger('ftpserver.log').getlog()

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            client_socket = self.request
            client_addr = self.client_address
            logger.info("client {0} connected".format(client_addr))
            #发送成功标识给客户端
            client_socket.sendall(bytes("OK",encoding='utf-8'))
            client_user = None

            while True:
                #获取客户端命令
                ret_client_data = str(client_socket.recv(1024),encoding='utf-8')

                #判断客户端是否退出
                if ret_client_data == b'':
                    logger.info("client {0} is exit".format(client_addr))
                    client_socket.close()

                #取出客户端命令
                cmd = ret_client_data.split("|")[0]

                logger.info("client {0} send command {1}".format(client_addr,cmd))
                #判断是否登录认证状态
                if cmd == 'auth':
                    client_user = server.client_auth(client_socket, ret_client_data)
                else:
                   try:
                        #通过反射寻找模块的命令
                        if hasattr(server,cmd):
                            func = getattr(server,cmd)
                            func(client_socket, client_user, ret_client_data)
                        else:
                            logger.error("command {0} not found".format(cmd))
                   except Exception as e:
                       logger.error(e)
                       client_socket.close()

        except Exception as e:
            logger.error(e)

def process():
    """
    启动服务
    :return:
    """
    server = socketserver.ThreadingTCPServer((settings.FTP_SERVER_IP,settings.FTP_SERVER_PORT),MyServer)
    server.serve_forever()

