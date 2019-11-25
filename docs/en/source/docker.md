# Docker

Gerapy also provides a Docker Image that can be used to quickly launch the Gerapy service.

## Run

First you need to select a directory as the Gerapy working directory, such as ~/gerapy or others. For example, we use the  ~/gerapy directory. The Gerapy startup command is as follows:

```
docker run -d --name gerapy -v ~/gerapy:/app/gerapy -p 8000:8000 germey/gerapy
```

After running, go directly to [http://localhost:8000](http://localhost:8000) to enter Gerapy.

The default login user name is admin and the password is admin. The username and password can be modified by [http://localhost:8000/admin/auth](http://localhost:8000/admin/auth).

The command parameters are as follows:

* -d: running in the background
* --name: specify the container name
* -v: specify the mount directory
* -p: specifies the binding port, the former is the host port and the latter is the container port.

## Docker Image

This image is in Docker Hub at [Gerapy](https://hub.docker.com/repository/docker/germey/gerapy), and its version corresponds to Gerapy. For a list of versions, see: [Tags]( Https://hub.docker.com/repository/docker/germey/gerapy/tags).
