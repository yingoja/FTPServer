#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


START_MENU = """
---------------------------------------------
              欢迎使用FTP服务器系统
---------------------------------------------
"""

LOGINED_MENU = """
------------------------------------------------------------------------------------------------
                                    FTP   CLIENT

User:{0}         TotalSpace:{1} MB         UserSpace:{2} MB
------------------------------------------------------------------------------------------------
Commands:
    put:    put|[filename]     # upload a file to server,[filename] must have a full path name
    get:    get|[filename]     # download a file from server
    ls:     ls                 # show the folder and files in the home folder
    cd:     cd|[folder]        # go to [folder],return back input cd|..
    mk:     mk|[folder]        # Create a directory
    delete: delete|[folder]    # Delete folders or files
    quit:                      # exit system
"""