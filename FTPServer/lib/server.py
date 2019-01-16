#!/usr/bin/env python
#coding=utf-8
__author__ = 'yinjia'


import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.common import Logger
from lib.user import Users
from lib import common


logger = Logger('serverr').getlog()



def client_auth(client_socket,args):

    """
    客户端认证
    :param client_socket: 客户端socket对象
    :param args: 用户发送过来的数据 ex: "auth|test|a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057"
    :return: success：认证成功；user_error：用户名不存在；fail：认证失败
    """
    recv_data_list = args.split("|")
    username = recv_data_list[1]
    passwd = recv_data_list[2]
    client_user = Users(username)
    #判断用户名是否存在
    if client_user.check_user():
        msg = client_user.load_user_info()
        password,totalspace,userspace = msg.strip().split("|")
        user_info = "{0}|{1}".format(totalspace, userspace)
        #判断密码是否正确
        if password == passwd:
            auth_status = "success"
        else:
            auth_status = "fail"
    else:
        auth_status = "user_error"

    #将认证状态发送给客户端
    client_socket.sendall(bytes(auth_status,encoding='utf-8'))
    if auth_status == "success":
        # 认证成功将用户空间消息发给客户端
        client_socket.sendall(bytes(user_info, encoding='utf-8'))
    return client_user


def cd(client_socket,client_user,ret_data):
    """
    切换目录路径
    :param client_socket: 客户端socket对象
    :param client_user: 客户端用户对象
    :param ret_data: 接收客户命令消息体  例如：cd|..或cd|test或cd|/test/aa/bb
    :return:
    """
    #获取命令行消息体
    cd_folder = ret_data.split("|")[1]
    try:
        #判断是否当前根目录
        if cd_folder == "..":
            if client_user.userpath == client_user.homepath:
                sed_msg = "0|{0}".format(os.path.basename(client_user.userpath))
            else:
                #返回上一级目录
                client_user.userpath = os.path.dirname(client_user.userpath)
                sed_msg = "1|{0}".format(os.path.basename(client_user.userpath))
        elif cd_folder == "." or cd_folder == "":
            sed_msg = "3|{0}".format(cd_folder)
        else:
            #组合路径目录
            tmp_path = os.path.join(client_user.userpath, cd_folder)
            if os.path.isdir(tmp_path):
                client_user.userpath = tmp_path
                sed_msg = "1|{0}".format(os.path.basename(client_user.userpath))
            else:
                # 不是文件夹
                sed_msg = "2|{0}".format(cd_folder)
        # 开始发送结果
        client_socket.sendall(bytes(sed_msg,encoding='utf-8'))
    except Exception as e:
        logger.error(e)

def put(client_socket,client_user,ret_data):
    """
    上传文件
    :param client_socket:
    :param client_user:
    :param ret_data:
    :return:
    """
    # 初始化上传文件的基本信息
    filename = ret_data.split("|")[1]
    filesize = int(ret_data.split("|")[2])
    filemd5 = ret_data.split("|")[3]
    put_folder = client_user.userpath
    check_filename = os.path.isfile(os.path.join(put_folder,filename))
    save_path = os.path.join(put_folder, filename)
    fmd5 = common.md5sum(save_path)
    #不存在文件名，正常传输
    if not check_filename:
        client_socket.sendall(bytes("ok",encoding='utf-8'))
        # 全新的文件的话,更新用户使用空间大小
        client_user.update_quota(filesize)
        # 已经接收的文件大小
        has_recv = 0
        with open(save_path,'wb') as f:
            while True:
                # 如果文件总大小等于已经接收的文件大小，则退出
                if filesize == has_recv:
                    break
                data = client_socket.recv(1024)
                f.write(data)
                has_recv += len(data)
    else:
        #存在文件名条件，做判断分析是否存在断点
        if fmd5 == filemd5:
            client_socket.sendall(bytes("full", encoding='utf-8'))
            # 已经接收的文件大小
            has_recv = 0
            with open(save_path, 'wb') as f:
                while True:
                    # 如果文件总大小等于已经接收的文件大小，则退出
                    if filesize == has_recv:
                        break
                    data = client_socket.recv(1024)
                    f.write(data)
                    has_recv += len(data)
        else:
            #存在断点文件，发起请求续签标志
            recv_size = os.stat(save_path).st_size
            ready_status = "{0}|{1}".format("continue", str(recv_size))
            client_socket.sendall(bytes(ready_status, encoding='utf-8'))
            # 已经接收的文件大小
            has_recv = 0
            with open(save_path, 'wb') as f:
                while True:
                    # 如果文件总大小等于已经接收的文件大小，则退出
                    if filesize == has_recv:
                        break
                    data = client_socket.recv(1024)
                    f.write(data)
                    has_recv += len(data)

def get(client_socket,client_user,ret_data):
    """
    下载文件
    :param client_socket:
    :param client_user:
    :param ret_data:
    :return:
    """
    # 获取文件名
    filename = ret_data.split("|")[1]
    # 文件存在吗
    file = os.path.join(client_user.userpath, filename)
    if os.path.exists(file):
        # 先告诉客户端文件存在标识
        client_socket.send(bytes("1", 'utf8'))
        # 得到客户端回应
        client_socket.recv(1024)
        # 发送文件的基本信息 "filesize|file_name|file_md5"
        filesize = os.stat(file).st_size
        file_md5 = common.md5sum(file)
        sent_data = "{fsize}|{fname}|{fmd5}".format(fsize=str(filesize),
                                                    fname=filename,
                                                    fmd5=file_md5)
        client_socket.sendall(bytes(sent_data, 'utf8'))

        # 客户端收到ready
        if str(client_socket.recv(1024), 'utf-8') == "ready":
            # 开始发送数据了
            with open(file, 'rb') as f:
                new_size = 0
                for line in f:
                    client_socket.sendall(line)
                    new_size += len(line)
                    if new_size >= filesize:
                        break
    else:
        # 文件不存在
        client_socket.send(bytes("0", 'utf8'))


def mk(client_socket,client_user,ret_data):
    """
    创建目录
    :param client_socket: 客户端socket对象
    :param client_user: 客户端用户对象
    :param ret_data: 接收客户命令消息体  例如：mk|test
    :return:
    """
    mk_folder = ret_data.split("|")[1]
    if mk_folder:
        try:
            folder_path = os.path.join(client_user.homepath, mk_folder)
            os.makedirs(folder_path)
            client_socket.sendall(bytes("5000",encoding='utf-8'))
        except Exception as e:
            client_socket.sendall(bytes("5001",encoding='utf-8'))
            logger.error("create directory failure: %s" % e)
    else:
        client_socket.sendall(bytes("5002", encoding='utf-8'))

def delete(client_socket,client_user,ret_data):
    """
    删除目录或文件
    :param client_socket:客户端socket对象
    :param client_user:客户端用户对象
    :param ret_data:接收消息体：样本格式：delete|/test/aa
    :return:
    """
    del_folder = ret_data.split("|")[1]
    if del_folder:
        try:
            #判断文件名是否存在
            folder_path = os.path.join(client_user.homepath, del_folder)
            filesize = os.stat(folder_path).st_size
            if os.path.isfile(folder_path):
                os.remove(folder_path)
                client_user.update_down_quota(filesize)
                sent_data = "{staus}|{fsize}".format(staus="6001",
                                                    fsize=str(filesize)
                                                    )

                client_socket.sendall(bytes(sent_data, encoding='utf-8'))
            #判断目录是否存在
            elif os.path.isdir(folder_path):
                os.removedirs(folder_path)
                client_socket.sendall(bytes("6000", encoding='utf-8'))
            else:
                #目录或文件名不存在情况，删除失败
                client_socket.sendall(bytes("6002", encoding='utf-8'))
        except Exception as e:
                #当前路径目录下不是空目录，不能删除
                client_socket.sendall(bytes("6004", encoding='utf-8'))
                logger.error("Delete directory or filename failure: %s" % e)
    else:
        #命令行后是空白目录
        client_socket.sendall(bytes("6003", encoding='utf-8'))


def ls(client_socket,client_user,ret_data):
    """
    显示当前文件目录及文件名
    :param client_socket: 客户端socket对象
    :param client_user: 客户端用户对象
    :param ret_data: 接收消息体样本格式：ls|
    :return:
    """
    check_folder = client_user.userpath
    #获取用户目录下的文件目录或文件名列表
    file_list = os.listdir(check_folder)
    #目录下的文件个数
    file_count = len(file_list)
    if file_count > 0:
        return_list = "{filecount}|".format(filecount=file_count)
        for rootpath in file_list:
            file = os.path.join(check_folder,rootpath)
            stat = os.stat(file)
            create_time = time.strftime('%Y:%m-%d %X', time.localtime(stat.st_mtime))
            file_size = stat.st_size
            if os.path.isfile(file):
                return_list += "{ctime}        {fsize}    {fname}\n".format(ctime=create_time,
                                                                            fsize=str(file_size).rjust(10, " "),
                                                                            fname=rootpath)
            if os.path.isdir(file):
                return_list += "{ctime}  <DIR> {fsize}    {fname}\n".format(ctime=create_time,
                                                                            fsize=str(file_size).rjust(10, " "),
                                                                            fname=rootpath)
    else:
        return_list = "0|"

    try:
        # 开始发送信息到客户端
        # 1 先把结果串的大小发过去
        str_len = len(return_list.encode("utf-8"))
        client_socket.sendall(bytes(str(str_len), encoding='utf-8'))
        # 2 接收客户端 read 标识，防止粘包
        read_stat = client_socket.recv(1024).decode()
        if read_stat == "ready":
            client_socket.sendall(bytes(return_list, encoding='utf-8'))
        else:
            logger.error("client send show command，send 'ready' status fail")
    except Exception as e:
        logger.error(e)


