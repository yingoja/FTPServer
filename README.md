## FTPServer
__功能需求__
* 用户加密认证
* 服务端采用 SocketServer实现，支持多客户端连接
* 每个用户有自己的家目录且只能访问自己的家目录
* 对用户进行磁盘配额、不同用户配额可不同
* 用户可以登陆server后，可切换目录
* 能查看当前目录下文件
* 上传下载文件，保证文件一致性
* 传输过程中实现进度条展示
* 用户可在自己家目录进行创建目录、文件、删除目录及文件
* 服务端可实现增加用户、删除用户
* 支持上传时断点续传

__知识点__
* 类的应用
* 函数的使用
* 多进程
* 反射
* socket、socketserver、hashlib、configparser、logging
* 文件的读写

__开发环境__
* python 3.6.1
* PyCharm 2016.2.3

__目录结构__

FTPClient

       |--bin              (主接口目录)

    　　|--ftpclient.py    (客户端主程序接口文件)

      |--config           (配置文件目录)

   　　 |--code.py       (状态码文件)

   　　 |--settings.py    (配置文件)

   　　 |--template.py   (模板文件)

      |--download        (下载存放目录)

      |--lib              (模块目录)

   　　 |--client.py      (客户端各类接口封装)

   　　 |--common.py   (公共接口)

      |--logs            (日志目录)

   　　 |--ftpclient.log  (日志文件)

　　|--clientRun.py     (主执行程序)

 

FTPServer

       |--bin               (主接口目录)

    　　|--ftpserver.py      (服务端socket接口文件)

     　　 |--main.py        (主程序接口文件)

      |--config            (配置目录)

   　　 |--settings.py     (配置文件)

  　　  |--template.py    (模板文件)

　　|--database          (数据保存目录)

　　　|--user.ini        (用户信息文件)

　　|--dbhelper          (数据目录)

   　　|--dbapi.py       (数据操作接口)

　　|--lib               (模块目录)

   　　|--user.py        (用户类文件用来实例化对象)

   　　 |--server.py      (服务端模块，各类所有命令方法)

    　　|--common.py    (公共模块文件)

      |--logs

    　　|--ftpserver.log   (日志文件)

 　 |--upload           (上传文件存放的目录)

　  |--serverRun.py     (主执行程序)
   
   __模块功能导图__
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/daotu.jpg)
   __输出结果展示__
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu1.jpg)
   
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu2.jpg)
   
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu3.jpg)
   
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu4.jpg)
   
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu5.jpg)
   
   ![Image](https://github.com/yingoja/FTPServer/blob/master/share/screeshots/menu6.jpg)
   
