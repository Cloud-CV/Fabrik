# Windows Installaion

There are two main methods you can use to setup Fabrik on a Windows system with a virtual environment.
Firstly, you can use WSL, the Windows Subsystem for Linux, which is by far the easier option.
To install Fabrik with WSL, all you need to do is simply install a distro of your choice through the Windows Store, and then follow the Linux installation instructions in the README.
The alternative is to install natively through the Win32 subsystem, which is significantly more complicated, but an option if the WSL is not available.

### WSL Notes

The setup is exactly the same as other linux systems. The Ubunt distro is recommended, as it has been tested and confirmed to work, and Fabrik is written for Ubuntu 14.04 and 16.04.
It is important that Fabrik is setup in `/mnt/c/...`, rather than the Linux user profile directory, because editing of the WSL subsystem from the Win32 subsystem can leading to file corruption.

### Win32 Installation Instructions

1. Firstly, ensure you have Python 3.5 64 bit installed (or you won't be able to install all the dependencies), and in a new folder setup the virtual environment.
    Note that powershell cannot be used for this step.
    ```
    cmd> python --version
    Python 3.5.6
    cmd> python -m venv venv
    cmd> venv\Scripts\activate
    ```

2. Clone the repository and change directory into it.
    ```
    (venv) cmd> git clone --recursive https://github.com/Cloud-CV/Fabrik.git
    (venv) cmd> cd Fabrik
    ```

3. Copy the sample settings file.
    ```
    (venv) cmd> copy settings\dev.sample.py settings\dev.py
    ```

4. Setup redis. This can be done in multiple ways, however a large number of
    Redis for Windows ports have not be updated in a number of years.
    [This archive](https://github.com/ServiceStack/redis-windows/raw/master/downloads/redis-latest.zip)
    has been tested and appears to work, but you may want to search for better alternatives. To use, simply
    extract and run `redis-server.exe redis.windows.conf`. A firewall prompt may appear, be sure to click 'Allow'.
    
    On line 115 of `settings\common.py` set the hostname to localhost, like so:
    ```
    "CONFIG": {
        # replace redis hostname to localhost if running on local system
        "hosts": [("localhost", 6379)],
        "prefix": u'fabrik:',
    },
    ```
    In the same file ensure the celery result backend around line 122 is set to the local redis server
    ```
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    ```
    Ensure that line 8 of ` ide\celery_app.py ` has both `broker` and `backend` parameters set to `'redis://localhost:6379/0'`. It should look like:
    ```
    app = Celery('app', broker='redis://localhost:6379/0' backend='redis://localhost:6379/0', include=['ide.tasks'])
    ```

5. Install Tensorflow, Keras and Caffe.
    
 - Tenserflow (this will fail if you don't have either python 3.6, 3.5 or 3.4 64 bit):
    ```
    (venv) cmd> pip install tensorflow==1.4
    ```
 - Keras:
    ```
    (venv) cmd> pip install keras==2.0.8
    ```
 - A work-in-progess Windows port of Caffe is currently maintaiend 
    as [a branch in the Caffe respository](https://github.com/BVLC/caffe/tree/windows),
    and links to prebuilt binaries are listed in the readme. However, at the time of writing,
    the downloads were broken, so in order to obtain the binaries, you need to download them
    manually. Go to the [AppVeyor CI for Caffe](https://ci.appveyor.com/project/BVLC/caffe/branch/windows)
    and find the latest build. Pick the desired environment and download and extract the generated artifact.
    Run the command (you'll need to do this every time you start a new session)
    ```
    (venv) cmd> SET PYTHONPATH=%PYTHONPATH%;{put location of caffe installaion here}\python;
    ```
    Open the `requirements.txt` of the caffe installation and comment out the `leveldb` line. Run the following command.
    ```
    (venv) cmd> pip install -r "{put location of caffe installaion here}\python\requirements.txt"
    pip install --upgrade python-dateutil
    ```
    Edit `settings\common.py` and change `CAFFE_TOOLS_DIR` on line 124 to `{put location of caffe installaion here}\bin`.


6. Install other dependencies. Edit `requirements\common.txt` line 8 and change `tensorflow==1.4.1` to `tensorflow==1.4`.
    Comment out the `uWSGI` line, as it is incompatible with windows and is only needed for deployment.
    Install Microsoft Visual C++ Tools for the Twisted package by installing the [following]( https://visualstudio.microsoft.com/visual-cpp-build-tools/). Install
    the packages `Windows 10 SDK`, `C++/CLI support` and `Visual C++ ATL`.
    Finally run
    ```
    (venv) cmd> pip install -r requirements/dev.txt
    (venv) cmd> pip install pywin32
    ```

7. [Download and install postgres](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads). Remeber the password and port you give.

8. Navigate to `{your postgres installation directory}\bin`. Run `postgres -D ..\data` to start the server.
    In the same directory run `psql -U postgres` and supply your chosen password. Run the following commands:
    ```
    CREATE DATABASE fabrik;
    CREATE USER admin WITH PASSWORD 'fabrik';
    ALTER ROLE admin SET client_encoding TO 'utf8';
    ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
    ALTER ROLE admin SET timezone TO 'UTC';
    ALTER USER admin CREATEDB;
    ```
    Exit with the `\q` command.

    Edit `settings\dev.py` and on line 15 of change the DB host to `localhost`, ie
    ```
    'HOST': os.environ.get("POSTGRES_HOST", 'localhost'), 
    ```
    Change `USER` to the DB username supplied to the installer, `PASSWORD` to the DB password supplied.
    Migrate by running
    ```
    (venv) cmd> python manage.py makemigrations caffe_app
    (venv) cmd> python manage.py migrate
    ```

8. [Download node.js](https://nodejs.org/en/download/). Add it your PATH:
    ```
    cmd> SET PATH=%PATH%;{location of your node installaion};
    ```
    Run
    ```
    cmd> npm install
    cmd> npm install --save-dev json-loader
    cmd> npm install -g webpack@1.15.0
    ```
    In a seperate terminal, run
    ```
    cmd> webpack --progress --watch --colors
    ```

9. In another terminal, with the redis server running, start the celery worker
    ```
    (venv) cmd> celery -A ide worker --app=ide.celery_app  --loglevel=info
    ```

10. If all goes well, you should be able to start the application with
    ```
    (venv) cmd> python manage.py runserver
    ```
