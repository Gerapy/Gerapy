# 介绍

用 Python 做过爬虫的小伙伴可能接触过 [Scrapy](https://github.com/scrapy/scrapy)。Scrapy 的确是一个非常强大的爬虫框架，爬取效率高，扩展性好，基本上是使用 Python 开发爬虫的必备利器。

## Scrapy

如果使用 Scrapy 做爬虫，那么在爬取时，我们当然完全可以使用自己的主机来完成爬取，但当爬取量非常大的时候，我们肯定不能在自己的机器上来运行爬虫了，一个好的方法就是将 Scrapy 部署到远程服务器上来执行。

## Scrapyd

这时候就可能用到 [Scrapyd](https://github.com/scrapy/scrapyd)，有了它我们只需要在远程服务器上安装 Scrapyd 并启动这个服务，我们就可以将我们写的 Scrapy 项目部署到远程主机上了。另外，Scrapyd 还提供了各种操作 [API](http://scrapyd.readthedocs.io/en/stable/api.html)，可以自由地控制 Scrapy 项目的运行，例如我们将 Scrapyd 安装在 IP 为 88.88.88.88 的服务器上，然后将 Scrapy 项目部署上去，这时候我们通过请求 API 就可以来控制 Scrapy 项目的运行了，命令如下：

```shell
curl http://88.88.88.88:6800/schedule.json -d project=myproject -d spider=myspider
```

这样就相当于启动了 myproject 项目的 myspider 爬虫，而不用我们再用命令行方式去启动爬虫，同时 Scrapyd 还提供了查看爬虫状态、取消爬虫任务、添加爬虫版本、删除爬虫版本等等的一系列 API，所以说，有了 Scrapyd，我们可以通过 API 来控制爬虫的运行，摆脱了命令行的依赖。

## Scrapyd-Client

爬虫部署还是个麻烦事，因为我们需要将爬虫代码上传到远程服务器上，这个过程涉及到打包和上传两个过程，在 Scrapyd 中其实提供了这个部署的 API，叫做 addversion，但是它接收的内容是 egg 包文件，所以说要用这个接口，我们必须要把我们的 Scrapy 项目打包成 egg 文件，然后再利用文件上传的方式请求 addversion 接口才可以完成上传，这个过程又比较繁琐了，所以又出现了一个工具叫做 [Scrapyd-Client](https://github.com/scrapy/scrapyd-client)，利用它的 scrapyd-deploy 命令我们便可以完成打包和上传的两个功能，可谓是又方便了一步。

## Scrapyd-API

这样我们就已经解决了部署的问题，回过头来，如果我们要想实时查看服务器上 Scrapy 的运行状态，那该怎么办呢？像刚才说的，当然是请求 Scrapyd 的 API 了，如果我们想用 Python 程序来控制一下呢？我们还要用 requests 库一次次地请求这些 API ？这就太麻烦了吧，所以为了解决这个需求，[Scrapyd-API](https://github.com/djm/python-scrapyd-api) 又出现了，有了它我们可以只用简单的 Python 代码就可以实现 Scrapy 项目的监控和运行：

```python
from scrapyd_api import ScrapydAPI
scrapyd = ScrapydAPI('http://88.888.88.88:6800')
scrapyd.list_jobs('project_name')
```

这样它的返回结果就是各个 Scrapy 项目的运行情况。例如：

```json
{
    'pending': [
    ],
    'running': [
        {
            'id': u'14a65...b27ce',
            'spider': u'spider_name',
            'start_time': u'2018-01-17 22:45:31.975358'
        },
    ],
    'finished': [
        {
            'id': '34c23...b21ba',
            'spider': 'spider_name',
            'start_time': '2018-01-11 22:45:31.975358',
            'end_time': '2018-01-17 14:01:18.209680'
        }
    ]
}
```

这样我们就可以看到 Scrapy 爬虫的运行状态了。

所以，有了它们，我们可以完成的是：

- 通过 Scrapyd 完成 Scrapy 项目的部署
- 通过 Scrapyd 提供的 API 来控制 Scrapy 项目的启动及状态监控
- 通过 Scrapyd-Client 来简化 Scrapy 项目的部署
- 通过 Scrapyd-API 来通过 Python 控制 Scrapy 项目

是不是方便多了？

## Gerapy

可是？真的达到最方便了吗？肯定没有！如果这一切的一切，从 Scrapy 的部署、启动到监控、日志查看，我们只需要鼠标键盘点几下就可以完成，那岂不是美滋滋？另外，我们还可以可视化配置各种定时任务和监控功能，方便地定时调度 Scrapy 爬虫项目。更或者说，连 Scrapy 代码都可以帮你自动生成，那岂不是爽爆了？

有需求就有动力，没错，[Gerapy](https://github.com/Gerapy/Gerapy) 就是为此诞生了。

Gerapy 是一款分布式爬虫管理框架，支持 Python 3，基于 Scrapy、Scrapyd、Scrapyd-Client、Scrapy-Redis、Scrapyd-API、Scrapy-Splash、Django、Vue.js 开发，Gerapy 可以帮助我们：

- 更方便地控制爬虫运行
- 更直观地查看爬虫状态
- 更实时地查看爬取结果
- 更轻松地实现定时任务
- 更简单地实现项目部署
- 更统一地实现主机管理
- 更轻松地编写爬虫代码

有了它，Scrapy 分布式爬虫项目的管理不再是难事。