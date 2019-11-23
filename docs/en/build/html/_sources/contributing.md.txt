# Contribution

If you are interested in secondary development of Gerapy or contributing to Gerapy, this document details the environment configuration and development process for Gerapy developers.

## Preparation

Development Gerapy requires a Python3 environment and a Node.js environment. The recommended versions are Python 3.6 + and Node.js 10.x +. Please install and make sure to use the python3, pip3, node, npm commands.

## Cloning project

First clone Gerapy locally:

```
git clone https://github.com/Gerapy/Gerapy.git
```

Once the clone is complete, a Gerapy folder is generated locally.

## Dependencies

Go to the Gerapy folder and install the dependencies you need for development:

```
pip3 install -r requirements.txt
```

Then install Gerapy locally:

```
python3 setup.py install
```

This installs the development version of Gerapy, and if Gerapy was previously installed, this installation will replace the previous version.

The gerapy command can be used after the installation is complete.

Then install the front-end dependencies, the front-end code is in the gerapy/client folder, based on Vue.js development.

Go into the directory and install dependencies.

```
cd gerapy/client
npm install
```

This will generate a node_modules folder under gerapy/client.

## Run

The backend uses the gerapy command to start normally according to Gerapy's instructions. Note that the runtime needs to be started on port 5000 instead of 8000.

```
gerapy runserver 0.0.0.0:5000
```

The front end is in the gerapy/client folder and executes:

```
npm run serve
```

It will run on port 8080 and its backend API will be forwarded to port 5000, the Gerapy Server that was just started.

Open [http://localhost:8080](http://localhost:8080) to enter Gerapy's development mode.

## Description

The backend is based on Django development, and the database used is SQLite, whose main logic is in the gerapy/server folder.

The front end is based on Vue.js development and its main logic is in the gerapy/client folder.

## Code Release

After the front-end modification is completed, if you want to officially release it, you can directly execute it:

```
npm run build
```

The result of the build will go to the backend's gerapy/server/core/templates folder.

The release of the backend code can be executed directly:

```
python3 setup.py upload
```

It will be automatically uploaded to PyPi and tagged on GitHub, provided you have PyPi and GitHub permissions.