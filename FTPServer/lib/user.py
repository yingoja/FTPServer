#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings
from dbhelper import dbapi
from lib.common import Logger

logger = Logger('user').getlog()

"""
服务端用户信息类
"""

class Users(object):
    def __init__(self,username):
        self.username = username
        self.password = ""
        self.totalspace = 0
        self.userspace = 0
        self.homepath = os.path.join(settings.USER_HOME_FOLDER, self.username)
        self.userpath = self.homepath

    def create_user(self):
        """
        创建用户
        :return: True:创建用户成功； False: 创建用户失败
        """
        args = dict(password=str(self.password), totalspace=str(self.totalspace), userspace=str(self.userspace))
        dbapi.AddOption(self.username, **args)
        self.__create_folder()

    def del_user(self):
        """
        删除用户
        :return: True；删除用户成功；False: 删除用户失败
        """
        dbapi.DelSections(self.username)
        self.__del_folder()

    def check_user(self):
        """
        判断用户是否存在
        :return:
        """
        if dbapi.CheckSections(self.username):
            return True
        return False


    def load_user_info(self):
        """
        加载用户信息，赋值给属性
        :return:
        """
        user_info = dbapi.load_info(self.username)
        self.password = user_info["password"]
        self.totalspace = int(user_info["totalspace"])
        self.userspace = int(user_info["userspace"])
        msg = "{0}|{1}|{2}".format(self.password, self.totalspace, self.userspace)
        return msg

    def __create_folder(self):
        """
        创建用户的目录
        :return:
        """
        os.mkdir(self.homepath)

    def __del_folder(self):
        """
        删除用户目录
        :return:
        """
        os.removedirs(self.homepath)


    def update_quota(self,filesize):
        """
        更新用户磁盘配额数据
        :param filesize: 上传文件大小
        :return: True: 更新磁盘配额成功；False：更新磁盘配额失败
        """
        if dbapi.CheckSections(self.username):
            self.userspace += filesize
            args = dict(userspace=str(self.userspace))
            dbapi.ModifyOption(self.username, **args)
            return True
        return False

    def update_down_quota(self,filesize):
        """
        用户删除文件情况，自动减少对应文件大小并更新用户磁盘配额空间
        :param filesize:
        :return:
        """
        if dbapi.CheckSections(self.username):
            self.userspace -= filesize
            args = dict(userspace=str(self.userspace))
            dbapi.ModifyOption(self.username, **args)
            return True
        return False
