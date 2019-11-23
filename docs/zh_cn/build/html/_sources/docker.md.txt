# Docker

Gerapy 同样提供了 Docker 镜像，可以使用 Docker 快速启动 Gerapy 服务。

## 运行

首先需要选定一个目录作为 Gerapy 工作目录，如 ~/gerapy 或其他，在这里以 ~/gerapy 目录为例，Gerapy 启动命令如下：

```
docker run -d --name gerapy -v ~/gerapy:/app/gerapy -p 8000:8000 germey/gerapy
```

运行之后，直接访问 [http://localhost:8000](http://localhost:8000) 即可进入 Gerapy。

默认的登录用户名为 admin，密码为 admin，用户名密码可以在 [http://localhost:8000/admin/auth](http://localhost:8000/admin/auth) 自行修改。

其中命令参数说明如下：

* -d：后台运行
* --name：指定容器名称
* -v：指定挂载目录
* -p：指定绑定端口，前者为宿主机端口，后者为容器端口

## 源镜像

本镜像 Registry 在 Docker Hub，其地址为：[Gerapy](https://hub.docker.com/repository/docker/germey/gerapy)，其版本与 Gerapy 一一对应，版本列表见：[Tags](https://hub.docker.com/repository/docker/germey/gerapy/tags)。

## 加速器

由于 Docker Hub 下载速度比较慢，在运行时可以使用加速器。

| 镜像加速器                                                   | 镜像加速器地址                     |
| ------------------------------------------------------------ | ---------------------------------- |
| [Docker 中国官方镜像](https://docker-cn.com/registry-mirror) | https://registry.docker-cn.com     |
| [DaoCloud 镜像站](https://daocloud.io/mirror)                | http://f1361db2.m.daocloud.io      |
| [Azure 中国镜像](https://github.com/Azure/container-service-for-azure-china/blob/master/aks/README.md#22-container-registry-proxy) | https://dockerhub.azk8s.cn         |
| [科大镜像站](https://mirrors.ustc.edu.cn/help/dockerhub.html) | https://docker.mirrors.ustc.edu.cn |
| [阿里云](https://cr.console.aliyun.com)                      | https://.mirror.aliyuncs.com       |
| [七牛云](https://kirk-enterprise.github.io/hub-docs/#/user-guide/mirror) | https://reg-mirror.qiniu.com       |
| [网易云](https://c.163yun.com/hub)                           | https://hub-mirror.c.163.com       |
| [腾讯云](https://cloud.tencent.com/document/product/457/9113) | https://mirror.ccs.tencentyun.com  |


加速器的配置方式可以参考：[https://www.daocloud.io/mirror](https://www.daocloud.io/mirror)。
