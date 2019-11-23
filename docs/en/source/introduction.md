# Introduction

Someone who has worked as a crawler with Python may use [Scrapy](https://github.com/scrapy/scrapy). Scrapy is indeed a very powerful crawler framework. It has high crawling efficiency and good scalability. It is basically a necessary tool for developing crawlers using Python.

## Scrapy

If you use Scrapy as a crawler, then of course we can use our own host to crawl when crawling, but when the crawl is very large, we can't run the crawler on our own machine, a good one. The method is to deploy Scrapy to a remote server for execution.

## Scrapyd

At this time, you might use [Scrapyd](https://github.com/scrapy/scrapyd). With it, we only need to install Scrapyd on the remote server and start the service. We can deploy the Scrapy project we wrote. Go to the remote host. In addition, Scrapyd provides a variety of operations [API](http://scrapyd.readthedocs.io/en/stable/api.html), which gives you free control over the operation of the Scrapy project. For example, we installed Scrapyd on IP 88.88. On the .88.88 server, then deploy the Scrapy project. At this time, we can control the operation of the Scrapy project by requesting the API. The command is as follows:

```shell
curl http://88.88.88.88:6800/schedule.json -d project=myproject -d spider=myspider
```

This is equivalent to launching the myspider crawler for the myproject project, instead of using the command line to launch the crawler, and Scrapyd also provides a set of APIs for viewing crawler status, canceling crawler tasks, adding crawler versions, removing crawler versions, and more. So, with Scrapyd, we can control the crawler's operation through the API and get rid of the command line dependencies.

## Scrapyd-Client

The crawler deployment is still a hassle because we need to upload the crawler code to the remote server. This process involves two processes of packaging and uploading. In Scrapyd, the API for this deployment is called, which is called addversion, but the content it receives is Egg package file, so to use this interface, we have to package our Scrapy project into an egg file, and then use the file upload method to request the addversion interface to complete the upload, this process is more cumbersome, so it has appeared A tool called [Scrapyd-Client](https://github.com/scrapy/scrapyd-client), with its scrapyd-deploy command, we can complete two functions of packaging and uploading, which is a convenient step.

## Scrapyd-API

So we have solved the deployment problem. In the end, what if we want to see the running status of Scrapy on the server in real time? As I said earlier, of course, I am requesting Scrapyd's API. If we want to use Python programs to control it? We also use the requests library to request these APIs again and again? This is too much trouble, so in order to solve this need, [Scrapyd-API](https://github.com/djm/python-scrapyd-api) has appeared again, with it we can use only simple Python code It is possible to monitor and run the Scrapy project:

```python
From scrapyd_api import ScrapydAPI
Scrapyd = ScrapydAPI('http://88.888.88.88:6800')
Scrapyd.list_jobs('project_name')
```

The result of this return is the operation of each Scrapy project. E.g:

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

This way we can see the running status of the Scrapy crawler.

So, with them, what we can accomplish is:

- Complete the deployment of Scrapy projects with Scrapyd
- Control the startup and status monitoring of Scrapy projects through the API provided by Scrapyd
- Simplify deployment of Scrapy projects with Scrapyd-Client
- Control Scrapy project via Python via Scrapyd-API

Is it more convenient?

## Gerapy

but? Is it really convenient to achieve it? Certainly not! If all of this, from Scrapy's deployment, startup to monitoring, log viewing, we only need a few clicks of the mouse and keyboard to complete, isn't it beautiful? In addition, we can visually configure various timing tasks and monitoring functions to conveniently schedule Scrapy crawler projects. Or, even Scrapy code can automatically generate it for you, isn't that cool?

There is motivation for demand, yes, [Gerapy](https://github.com/Gerapy/Gerapy) was born.

Gerapy is a distributed crawler management framework that supports Python 3, based on Scrapy, Scrapyd, Scrapyd-Client, Scrapy-Redis, Scrapyd-API, Scrapy-Splash, Django, Vue.js. Gerapy can help us:

- More convenient control of crawler runs
- View reptile status more intuitively
- View crawl results in more real time
- Easier timing tasks
- Easier project deployment
- More unified host management
- Write crawler code more easily

With it, the management of the Scrapy distributed crawler project is no longer difficult.