#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


"""
定义客户端类状态代码
"""


CONN_SUCC = 1000                # connect ftp-server successful
CONN_FAIL = 1001                # connect server fail
AUTH_SUCC = 2000                # login auth successfull
AUTH_USER_ERROR = 2001          # login auth user does not exists
AUTH_FAIL = 2002                # login auth failed,bad username or password
FILE_UPLOAD_SUCC = 3000         # upload file succ
FILE_NOT_EXISTS = 3001          # upload file does not exists
FILE_UPLOAD_FAIL = 3002         # upload file failed
FILE_NOT_FOUND = 3003           # download file ,file does not found
TRANS_READY = 4000              # upload or download file ,server is ready
FILE_MD5_SUCC = 4001            # file md5 check succ
FILE_MD5_FAIL = 4002            # file md5 check fail
FILE_MK_SUCC = 5000             # create directory success
FILE_MK_FAIL = 5001             # create directory failure
FILE_MK_EMPTY = 5002            # Empty folder
FOLDER_DEL_SUCC = 6000          # delete directory success
FILE_DEL_SUCC = 6001            # delete filename success
FILE_DEL_FAIL = 6002            # delete directory failure
FILE_DEL_COM_EMPTY = 6003       # command is Empty folder
FILE_DEL_EMPTY = 6004           # Empty folder