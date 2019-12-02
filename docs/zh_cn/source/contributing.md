# 贡献

如果您有意向对 Gerapy 二次开发或为 Gerapy 贡献一份力量，本文档详细说明了 Gerapy 开发者的环境配置和开发流程。

## 环境准备

开发 Gerapy 需要 Python3 环境和 Node.js 环境，推荐版本为 Python 3.6 + 及 Node.js 10.x +，请安装好并确保能使用 python3、pip3、node、npm 命令。

## 克隆项目

首先将 Gerapy 克隆到本地：

```
git clone https://github.com/Gerapy/Gerapy.git
```

克隆完成之后，本地会生成一个 Gerapy 文件夹。

## 安装依赖

进入 Gerapy 文件夹，安装开发需要的依赖库：

```
pip3 install -r requirements.txt
```

随后本地安装 Gerapy：

```
python3 setup.py install 
```

这样安装的就是开发版本的 Gerapy，如果之前安装过 Gerapy，本次安装会将之前的版本替换。

安装完成之后便可以使用 gerapy 命令。

然后安装前端依赖，前端代码在 gerapy/client 文件夹，基于 Vue.js 开发。

进入目录，然后安装依赖。

```
cd gerapy/client
npm install
```

这样会在 gerapy/client 下生成一个 node_modules 文件夹。

## 运行

此处分为前后端分别介绍，两部分需要同时启动才能正常配合工作。

### 后端

对于后端，由于 gerapy 命令需要安装 Gerapy 安装包才可使用。但开发时如果改动之后每次手动安装必然是非常繁琐的。

此处建议在 PyCharm IDE 中设置参数配置，同时还方便 Debug。

* 脚本路径：`gerapy/gerapy/cmd/__init__.py`，即命令的入口文件。
* 运行参数：`runserver 0.0.0.0:5000`，注意这里需要在 5000 端口上运行，前端会转发请求到 5000 端口。
* 环境变量：`PYTHONUNBUFFERED=1;APP_DEBUG=true`，其中 APP_DEBUG 是设置调试模式，会打印更多的调试日志。
* 工作路径：gerapy init 命令生成的工作路径。

如图所示：

![](https://qiniu.cuiqingcai.com/2019-12-02-110658.png)

这样启动之后，Gerapy Server 会在 5000 端口上运行，同时控制台也会打印出调试信息。

### 前端

对于前端，在 gerapy/client 文件夹，执行：

```
npm run serve
```

即可在 8080 端口运行，其后端 API 会转发到 5000 端口，即刚才所启动的 Gerapy Server。

打开 [http://localhost:8080](http://localhost:8080) 即可进入 Gerapy 的前端页面。

## 代码说明

后端基于 Django 开发，使用的数据库为 SQLite，其主要逻辑在 gerapy/server 文件夹。

前端基于 Vue.js 开发，其主要逻辑在 gerapy/client 文件夹。

## 代码发布

前端修改完成之后，如果要正式发布，可以直接执行：

```
npm run build
```

其 build 结果会进入后端的 gerapy/server/core/templates 文件夹。

后端代码的发布可以直接执行：

```
python3 setup.py upload
```

其会自动上传到 PyPi，并在 GitHub 上打上对应的 Tag，当然前提是你要有 PyPi 和 GitHub 的权限。