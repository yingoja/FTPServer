#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import os,sys,logging,hashlib,time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings

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

def message(msg,type):
    """
    根据不同的消息类型，打印出消息内容以不同的颜色显示
    :param msg: 消息内容
    :param type: 消息类型
    :return: 返回格式化后的消息内容
    """
    if type == "CRITICAL":
        show_msg = "\n\033[1;33m{0}\033[0m\n".format(msg)
    elif type == "ERROR":
        show_msg = "\n\033[1;31m{0}\033[0m\n".format(msg)
    elif type == "WARNING":
        show_msg = "\n\033[1;32m{0}\033[0m\n".format(msg)
    elif type == "INFO":
        show_msg = "\n\033[1;36m{0}\033[0m\n".format(msg)
    else:
        show_msg = "\n{0}\n".format(msg)
    print(show_msg)

def progress_bar(cache, totalsize):
    """
    打印进度条
    :param cache: 缓存字节大小
    :param totalsize: 文件总共字节
    :return:
    """
    ret = cache / totalsize
    num = int(ret * 100)
    view = '\r%d%% |%s' % (num, num * "*")
    sys.stdout.write(view)
    sys.stdout.flush()

def input_command(msg):
    flag = False
    while not flag:
        command_list = ["put","get","ls","cd","mk","delete","quit"]
        command_inp = input(msg).strip()
        if command_inp == "ls":
            return_command = "{0}|".format(command_inp)
            flag = True
        elif command_inp == "quit":
            return_command = command_inp
            flag = True
        else:
            if command_inp.count("|") != 1:
                message("输入命令不合法！","ERROR")
            else:
                #获取命令
                cmd,args = command_inp.strip().lower().split("|")
                if cmd not in command_list:
                    message("输入命令不合法！", "ERROR")
                else:
                    return_command = "{0}|{1}".format(cmd, args)
                    flag = True
    return return_command



