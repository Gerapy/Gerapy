# Usage

This article focuses on the basic use of Gerapy and hopes to provide some help for you who are using Gerapy.

## Initialization

First you can create a new project with the gerapy command. The command is as follows:

```
gerapy init
```

This will generate a gerapy folder in the current directory. This gerapy folder is the working directory of Gerapy. When you enter the gerapy folder, you will find two folders:

* projects , which are used to store Scrapy crawler projects.
* logs, used to store the Gerapy run log.

If you want to change the name of the working directory, you can add the name of the working directory after the command. If you want to create a working directory named GerapySpace, you can create it with the following command:

```
gerapy init GerapySpace
```

Its internal structure is the same.

## Database Configuration

Gerapy uses the database to store various project configurations, timing tasks, etc., so the second step is to initialize the database.

First enter the working directory, for example, the working directory name is gerapy, execute the following command:

```
cd gerapy
```

At this point, first initialize the database, execute the following command:

```
gerapy migrate
```

This will generate a SQLite database, which will be used to save each host configuration information, deployment version, timing tasks, and so on.

At this time, you can find another folder in the working directory:

* dbs, which is used to store the database required by the Gerapy runtime.

## New User

Gerapy has login authentication turned on by default, so you need to set up an admin user before starting the service.

For convenience, you can quickly create an admin administrator by directly using the command of the initial administrator. The password is also admin. The command is as follows:

```
gerapy initadmin
```

If you do not want to create the admin user directly, you can also manually create an administrator user with the following command:

```
gerapy createsuperuser
```

At this point Gerapy will prompt us to enter the username, email, password, etc., and then log in to Gerapy with this user.

## Startup service

Next start the Gerapy service, the command is as follows:

```
gerapy runserver
```

This will open the Gerapy service on the default 8000 port.

At this time, open [http://localhost:8000](http://localhost:8000) in the browser to enter Gerapy.

First Gerapy will prompt the user to log in, the page is as follows:

![](https://qiniu.cuiqingcai.com/2019-11-23-040248.png)

Enter Gerapy's home page by entering the username and password you created in the previous step:

![](https://qiniu.cuiqingcai.com/2019-11-23-065223.png)

If you want Gerapy run in public, you can specify host and port like this:

```
gerapy runserver 0.0.0.0:8000
```

Then Gerapy can be accessed through 8000 port from public.

If you want Gerapy run in daemon, you can just run like this:

```
gerapy runserver 0.0.0.0:8000 > /dev/null 2>&1 &
```

Then Gerapy will run in daemon and in public.

## Host Management

Here the host is talking about Scrapyd's service host. Scrapyd will run on port 6800 by default. It provides a series of HTTP services such as deployment and operation. For Scrapyd, you can refer to [Scrapyd Document](https://scrapyd.readthedocs.io/ ) to ensure that their services can be accessed externally.

In host management, we can add the Scrapyd running address and port of each host and name it. After adding it, it will appear in the host list. Gerapy will monitor the running status of each host and identify it in different states:

![](https://qiniu.cuiqingcai.com/2019-11-23-070132.png)

Once added, we can easily view and control the crawler tasks that each host is running.

## Project management

Also mentioned above is an empty projects folder in Gerapy's working directory, which is the folder where the Scrapy directory is stored.

If we want to deploy a Scrapy project, just put the project file in the projects folder.

For example, you can put your project into the projects folder as follows:

* Move or copy the local Scrapy project directly to the projects folder.
* Clone or download a remote project, such as Git Clone, and download the project to the projects folder.
* Link the project to the projects folder via a soft connection (using the ln command under Linux, Mac, using the mklink command).

For example, put two Scrapy projects in the projects here:

![](https://qiniu.cuiqingcai.com/2019-11-23-043941.png)

Then go back to the Gerapy management interface and click on Project Management to see the current project list:

![](https://qiniu.cuiqingcai.com/2019-11-23-070213.png)

Since the project has a package and deployment record here, it is shown separately here.

In addition, Gerapy provides the project online editing function, we can edit the project visually by clicking Edit:

![](https://qiniu.cuiqingcai.com/2019-11-23-070248.png)

If the project has no problems, you can click on the deployment to package and deploy. You need to package the project before deployment. You can specify the version description when packaging:

![](https://qiniu.cuiqingcai.com/2019-11-23-070321.png)

After the package is complete, you can click the deployment button to deploy the packaged Scrapy project to the corresponding cloud host, and you can also deploy it in batches.

![](https://qiniu.cuiqingcai.com/2019-11-23-070339.png)

After the deployment is complete, you can go back to the host management page to schedule the task. Click Schedule to view the task management page. You can view the running status of all tasks on the current host:

![](https://qiniu.cuiqingcai.com/2019-11-23-070453.png)

We can start and stop the task by clicking the button such as run, stop, etc., and also can view the log details by expanding the task entry.

This way we can see the status of each task in real time.

## Timing tasks

In addition, Gerapy supports setting up scheduled tasks, entering the Task Management page, and creating a new scheduled task, such as creating a new crontab mode, which runs every minute:

![](https://qiniu.cuiqingcai.com/2019-11-23-144227.png)

Here, if you set the run every minute, you can set the "minute" to 1, and you can set the start date and end date.

After the creation is complete, return to the Task Management home page to see the list of scheduled tasks that have been created:

![](https://qiniu.cuiqingcai.com/2019-11-23-070627.png)

Click "Status" to view the running status of the current task:

![](https://qiniu.cuiqingcai.com/2019-11-23-070716.png)

You can also manually control scheduled tasks and view the run log by clicking the Schedule button in the upper right corner.

The above is the basic usage of Gerapy.

If you have found an error, or if you have any suggestions for Gerapy, please feel free to post it to [Gerapy Issues](https://github.com/Gerapy/Gerapy/issues) and thank you for your support. Your feedback and suggestions are invaluable and hope that your participation will help Gerapy do better.