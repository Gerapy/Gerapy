# 使用

本文主要介绍 Gerapy 的基本使用方法，希望能为正在使用 Gerapy 的您提供一些帮助。

## 初始化

首先可以利用 gerapy 命令新建一个项目，命令如下：

```
gerapy init
```

这样会在当前目录下生成一个 gerapy 文件夹，这个 gerapy 文件夹就是 Gerapy 的工作目录，进入 gerapy 文件夹会发现两个文件夹：

* projects ，用于存放 Scrapy 的爬虫项目。
* logs，用于存放 Gerapy 运行日志。

如果想要更换工作目录的名称，可以在命令后加入工作目录的名称，如想创建一个名字为 GerapySpace 的工作目录，可以使用如下命令创建：

```
gerapy init GerapySpace
```

其内部结构是一样的。

## 数据库配置

Gerapy 利用数据库来存放各项项目配置、定时任务等内容，因此第二步需要初始化数据库。

首先进入工作目录，例如工作目录名叫做 gerapy，则执行如下命令：

```
cd gerapy
```

这时先对数据库进行初始化，执行如下命令：

```
gerapy migrate
```

这样即会生成一个 SQLite 数据库，数据库中会用于保存各个主机配置信息、部署版本、定时任务等。

这时候可以发现工作目录下又多了一个文件夹：

* dbs，用于存放 Gerapy 运行时所需的数据库。

## 新建用户

Gerapy 默认开启了登录验证，因此需要在启动服务前设置一个管理员用户，

为了方便，可以直接使用初始化管理员的命令快速创建一个 admin 管理员，密码同样为 admin，命令如下：

```
gerapy initadmin
```

如果不想直接创建 admin 用户，也可以手动创建管理员用户，命令如下：

```
gerapy createsuperuser
```

这时 Gerapy 会提示我们输入用户名、邮箱、密码等内容，稍后便可以使用此用户登录 Gerapy。

## 启动服务

接下来启动 Gerapy 服务，命令如下：

```
gerapy runserver
```

这样即可在默认 8000 端口上开启 Gerapy 服务。

这时在浏览器打开 [http://localhost:8000](http://localhost:8000) 即可进入 Gerapy。

首先 Gerapy 会提示用户登录，页面如下：

![image-20191123120246936](https://qiniu.cuiqingcai.com/2019-11-23-040248.png)

输入上一步创建的用户名和密码即可进入 Gerapy 的主页：

![image-20191123120403986](https://qiniu.cuiqingcai.com/2019-11-23-040405.png)

## 主机管理

这里主机所说的就是 Scrapyd 的服务主机，Scrapyd 启动后默认会运行在 6800 端口，提供部署、运行等一系列 HTTP 服务，配置 Scrapyd 可以参考 [Scrapyd Document](https://scrapyd.readthedocs.io/)，确保其服务可以对外正常访问。

主机管理中，我们可以将各台主机的 Scrapyd 运行地址和端口添加，并加以名称标记，添加之后便会出现在主机列表中，Gerapy 会监控各台主机的运行状况并以不同的状态标识：

![image-20191123123553134](https://qiniu.cuiqingcai.com/2019-11-23-044017.png)

添加完成之后我们便可以方便地查看和控制每个主机所运行的爬虫任务了。

## 项目管理

另外上文提到了 Gerapy 的工作目录下会出现一个空的 projects 文件夹，这就是存放 Scrapy 目录的文件夹。

如果我们想要部署某个 Scrapy 项目，只需要将该项目文件放到 projects 文件夹下即可。

例如，可以通过如下方式将项目放入 projects 文件夹：

* 直接将本地 Scrapy 项目移动或复制到 projects 文件夹。 
* 克隆或下载远程项目，如 Git Clone，将项目下载到 projects 文件夹。
* 通过软连接（Linux、Mac 下使用 ln 命令，Windows 使用 mklink 命令）将项目链接到 projects 文件夹。

例如，在 projects 这里放了两个 Scrapy 项目：

![image-20191123123940183](https://qiniu.cuiqingcai.com/2019-11-23-043941.png)

这时重新回到 Gerapy 管理界面，点击项目管理，即可看到当前项目列表：

![image-20191123125805061](https://qiniu.cuiqingcai.com/2019-11-23-045806.png)

由于此处项目有过打包和部署记录，在这里分别予以显示。

另外 Gerapy 提供了项目在线编辑功能，我们可以点击编辑即可可视化地对项目进行编辑：

![image-20191123125858123](https://qiniu.cuiqingcai.com/2019-11-23-045859.png)

如果项目没有问题，可以点击部署进行打包和部署，部署之前需要打包项目，打包时可以指定版本描述：

![image-20191123125940706](https://qiniu.cuiqingcai.com/2019-11-23-045942.png)

打包完成之后可以直接点击部署按钮即可将打包好的 Scrapy 项目部署到对应的云主机上，同时也可以批量部署。

![](https://qiniu.cuiqingcai.com/2019-11-23-050019.png)

部署完毕之后就可以回到主机管理页面进行任务调度，点击调度即可查看进入任务管理页面，可以当前主机所有任务的运行状态：

![image-20191123130129221](https://qiniu.cuiqingcai.com/2019-11-23-050130.png)

我们可以通过点击运行、停止等按钮来实现任务的启动和停止等操作，同时也可以通过展开任务条目查看日志详情。

这样我们就可以实时查看到各个任务运行状态了。

## 定时任务

另外 Gerapy 支持设置定时任务，进入「任务管理」页面，新建一个定时任务，如新建 crontab 方式，每一分钟运行一次：

![image-20191123131342140](https://qiniu.cuiqingcai.com/2019-11-23-051343.png)

在这里如果设置每分钟运行一次，可以将「分」设置为 1，另外可以设置开始日期和结束日期。

创建完成之后返回「任务管理」首页，即可看到已经创建的定时任务列表：

![image-20191123130605239](https://qiniu.cuiqingcai.com/2019-11-23-050606.png)

点击「状态」便可以查看当前任务的运行状态：

![image-20191123131610005](https://qiniu.cuiqingcai.com/2019-11-23-051611.png)

也可点击右上角「调度」按钮来手动控制调度任务和查看运行日志。

以上便是 Gerapy 的基本用法介绍。

如果您有发现错误，或者您对 Gerapy 有任何建议，欢迎到 [Gerapy Issues](https://github.com/Gerapy/Gerapy/issues) 发表，非常感谢您的支持。您的反馈和建议非常宝贵，希望您的参与能帮助 Gerapy 做得更好。

