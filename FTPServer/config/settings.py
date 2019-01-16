#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 服务端地址
FTP_SERVER_IP = "127.0.0.1"
FTP_SERVER_PORT = 9999

# 文件上传保存路径
UPLOAD_FILE_PATH = os.path.join(BASE_DIR, "upload")

# 日志文件存放路径
LOGS = os.path.join(BASE_DIR, "logs","ftpserver.log.log")

# 用户信息文件保存路径
USER_INFO = os.path.join(BASE_DIR, "database")

# 用户家目录文件夹
USER_HOME_FOLDER = os.path.join(BASE_DIR, "upload")

# 存放用户账号
USER_INI = os.path.join(BASE_DIR,"database","user.ini")

# 客户端家目录最大上传文件大小（默认配置),单位MB
HOME_QUOTA = 50

# 用户初始化默认密码
USER_PASSWORD = 12345
