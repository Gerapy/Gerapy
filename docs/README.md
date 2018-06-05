# 服务端安装

```bash
pip3 install gerapy
```

执行以下操作来运行Gerapy服务器

如果你成功的安装上了Gerapy, 则可以用使用gerapy 命令。如不能使用请检查你的安装。

首先在你合适的工作目录初始化Gerapy：

```bash
gerapy init
```

初始完成之后会在当前目录下新建一个gerapy的文件夹。

进入这个文件夹然后初始化数据库文件：

```bash
cd gerapy/
gerapy migrate
```

接下来运行服务器：

```bash
gerapy runserver
```

现在你可以通过 [http://localhost:8000 ]( http://localhost:8000 )使用

**注意：默认工作在 [ http://localhost:8000 ]( http://localhost:8000 )**

如果你需要需要对外提供服务你可以这样：

```bash
gerapy runserver 0.0.0.0:8888
```

这样Gerapy即可对外提供服务。

## Docker

首先新建一个存放项目的路径：

```bash
mkdir ~/gerapy
```

然后运行以下命令即可：

```bash
docker run -d -v ~/gerapy:/app/gerapy -p 8000:8000 thsheep/gerapy:master
```

将会运行在8000端口

启动方式：

```bash
docker run -d -v <your_workspace>:/app/gerapy -p <public_port>:<container_port> thsheep/gerapy:master
```

请使用`-v  <your_workspace>：/ app / gerapy`指定要安装Gerapy工作区的工作区，并通过`-p <public_port>：<container_port>` 指定服务器端口。

如果你使用Docker运行Gerapy可以直接访问[http://localhost:8000](http://localhost:8000) 而不需要做其它的初始化工作。

如果你需要Docker也工作在0.0.0.0上 则需要你重新Build

现在您可以创建一个可配置的项目，然后自动配置和生成代码。也可以将Scrapy项目拖放到gerapy/projects文件夹。

## 客户端Python3环境部署

如果你需要部署的客户端过多请考虑使用项目中提供的Deploy_Python3来减轻你的部署压力。

Deploy_Python3是一个Ansible-PlayBooks的脚本。可以帮你批量的将Python3.6.4版本部署到目标服务器上。

### 使用方法（推荐在Linux系下使用, Ansible对Windows系统支持不是很友好）

以下均默认Root用户（非Root用户使用方式请参考官方文档：[Ansible](http://docs.ansible.com/ansible/latest/index.html)）

安装Ansible：

```bash
pip install ansible
```

生成SSH秘钥：

```bash
ssh-keygen
```

连续回车即可。

分发SSH秘钥：

**以下均在Deploy_Python3目录下：**

```bash
vim host
```

将需要的部署的服务器按照以下格式写入：

```bash
[python]
1.1.1.1
2.2.2.2
3.3.3.3
```

运行：

```bash
chmod a+x copy_ssh.sh
./copy_ssh.sh
```
输入服务器root密码  直到所有服务器部署完毕。

现在编辑/group_vars/all文件：

**python_path** 为Python的编译安装路径

**install_pip_package**  需要在目标服务器安装的pip包（需要注意的是 你Scrapy项目所使用到包 都需要安装）以列表的形式写入。

#### 由于scrapyd本身不支持认证 故而使用Nginx反向代理实现认证

**roles/openresty/scrapyd.passwd** 为认证用户名和密码（默认为 scrapyd  scrapyd）；使用http-tools工具生成(文件名必须为：scrapyd.passwd)

现在执行以下命令：

```bash
ansible-playbooks -i host site.yml
```

等待部署完毕即可使用Gerapy连接管理（注意认证）。

默认pip3 python3

安装完成后会有Supervisor对scrapyd进程进行守护，不必担心scrapyd进程死掉啦

## 关于定时任务说明：

**date: 当你想在某个特定时间只运行一次工作时使用(例如：2018年05月14日09:35:10  运行一次)** 

**interval: 当你想以固定的时间间隔运行作业时使用(例如： 每隔十分钟运行一次)**

**Crontab：当你想在一天中的特定时间周期性地运行工作时使用 (例如： 每天的9点运行一次)**