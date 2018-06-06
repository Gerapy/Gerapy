# 本地开发流程

## 准备

首先配好你的 SSH 吧，用 SSH 来 Push、Pull，推荐。

随后 Clone 项目到本地：

```
git clone git@github.com:Gerapy/Gerapy.git
```

然后会出现一个 Gerapy 文件夹。

然后进入 Gerapy 文件夹，安装开发需要的依赖库：

```
pip3 install -r requirements.txt
```

随后本地安装 Gerapy：

```
sudo python3 setup.py install 
```

这样就会替换了你用 pip3 安装过的 Gerapy 了，这装的是开发版本。

然后分别跑起来前后端就好了。

## 前端

前端代码在 gerapy/client 文件夹，是 Vue 写的，跑起来需要 Node.js，最好装 v7 版本。

先进入目录，然后：

```
npm install
npm run dev
```

就跑起来了，在 3000 端口上，接口用的 8000 端口。

因此，只跑起来前端是没有卵用的，接口都是无效的，因为 8000 没跑起来。

所以接下来跑后端。

## 后端

后端代码在 gerapy/server 文件夹，Django 写的。

现在你已经安装了 Gerapy。

随便找一个目录，当做你的 WorkSpace。

```
gerapy init
cd gerapy
gerapy migrate
gerapy runserver
```

这流程和博客文章写得一样，就是在 8000 端口上开起来服务。

然后你再访问 3000 就可以看到东西了。

现在就是开发模式。

## 修改

前端修改的话主要改 gerapy/client/src/pages，这里是 Vue 文件。

后端主要改 gerapy/server/core/views.py，是 Django API。

逻辑自己理一下。

## 改完测试

改完之后，前端会立即生效看到变化。

后端则需要重新安装和运行：

```
sudo python3 setup.py install
cd <your workspace>/gerapy
gerapy runserver
```

切记！切记！切记！不然你会怀疑人生的！

前端要是改好了，就 build 一下，然后就可以发布了。

```
npm run build
```

完鸟~
