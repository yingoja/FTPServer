#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import time,logging,hashlib,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings

"""
公共模块
"""
class Logger(object):
    """
    日志记录,写入指定日志文件
    """
    def __init__(self,logger):

        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        format = '[%(name)s]:[%(asctime)s] [%(filename)s|%(funcName)s] [line:%(lineno)d] %(levelname)-8s: %(message)s'

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)

        # 创建一个handler,用于写入日志文件
        fp = logging.FileHandler(settings.LOGS)

        # 定义handler的输出格式formatter
        fpmatter = logging.Formatter(format)
        fp.setFormatter(fpmatter)

        # 给logging添加handler
        self.logger.addHandler(fp)

    def getlog(self):
        return self.logger


def md5(arg):
    """
    密码进行md5加密
    :param arg: 用户的密码
    :return: 返回进行加密后的密码
    """
    result = hashlib.md5()
    result.update(arg.encode())
    return result.hexdigest()


def md5sum(filename):
    """
    用于获取文件的md5值
    :param filename: 文件名
    :return: MD5码
    """
    if not os.path.isfile(filename):  # 如果校验md5的文件不是文件，返回空
        return False
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(1024)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def inp_msg(message, default=""):
    """
    用户输入的密码和磁盘配额
    :param message: 设置密码或磁盘配额
    :param default: 密码默认：12345； 磁盘配额默认：50MB
    :return:
    """
    while True:
        input_value = input(message)
        # ret = input_value.split(" ")
        if input_value == "":
            input_value = default
        else:
            return input_value
        return input_value
