#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import os,sys,configparser
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings

def readall_sections():
    """
    读取user.ini文件所有的用户名
    :return: 返回所有的用户名列表
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    result = con.sections()
    return result

def GetValue(key,value):
    """
    获取user.ini文件键名值
    :param key: 键名
    :param value: 键值
    :return:
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    result = con.get(key,value)
    return result

def CheckSections(sections_name):
    """
    检查sections项名是否存在
    :param sections_name: 用户名
    :return:
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    result = con.has_section(sections_name)
    return result

def AddOption(sections_name, **args):
    """
    添加用户信息
    :param sections_name:用户名
    :param args: 字典格式：('test3',password='aa',totalspace='bb',userspace='cc')
    :return:
    """
    con = configparser.ConfigParser()
    with open(settings.USER_INI,'a+',encoding='utf-8') as f:
        con.add_section(sections_name)
        for key in args:
            con.set(sections_name, key, args[key])
        con.write(f)

def DelSections(sections_name):
    """
    删除用户信息
    :param sections_name:
    :return:
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    with open(settings.USER_INI,'w') as f:
        con.remove_section(sections_name)
        con.write(f)

def ModifyOption(sections_name, **args):
    """
    修改磁盘配额空间
    :param sections_name: 用户名
    :param args:用户字典信息
    :return:
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    for key in args:
        con.set(sections_name, key, args[key])
    with open(settings.USER_INI, 'w', encoding='utf-8') as f:
        con.write(f)

def load_info(sections_name):
    """
    加载用户信息
    :param sections_name: 用户名
    :return: 返回字典用户信息
    """
    con = configparser.ConfigParser()
    con.read(settings.USER_INI, encoding='utf-8')
    user_dict = {}
    for i, j in con.items(sections_name):
        user_dict[i] = j
    return user_dict

