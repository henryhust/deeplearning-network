#  Setup Deep Learning enviroment on linux
## Intro
I have seen a lot of people have trouble setting up an deeplearning enviroment on linux, that's the main motivation why I wrote this document.

In this document I will be focusing on setting up a **user-level** or **local enviroment** via *anaconda2 / anaconda3*, and talk a bit about linux environment variable.

#### Why do we want a local environment
Usually we share a server with other people, if one user screws the global eviroment, he/she screws us all. That's why we need to learn to setup and maintain our own local environment.

## A bit about linux environment variable
When we log in to linux through a terminal or graphical user interface, the system will read `/etc/profile` and `~/.bashrc #giving that you use bash as your shell` to setup your bash variable, also called environment variable in Windows.

As far as we are concerned, we only need to know two bash variable (or environment varialbe if you will).

* PATH:
	
	I think **PATH** variable is **the** most important variable in linux.
	
	When you type `echo $PATH` in your terminal, you probably would see `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin` or something like that.
	those paths sperated by *:* is the searching paths. 
	When we type a command in the terminal, for example `cp file1 file2 ` and hit enter, what the system will do is to search a executable file named *cp* **from left to right** from those searching paths. As soon as it finds the executable then the found exeutable is loaded and executed (taking file1 file2 as argument).
* LD\_LIBRARY\_PATH
	
	This variable is also very important. A lot of binary executables/programs in linux, they are not standalone binary, they will need to link other dynamic libraries while loading. *LD\_LIBRARY\_PATH* is this kind of variable, that sotres the directory paths that contains dynamic libraries, put in another way, link program find dynamic library files from those path while load a program.
	
	I mention this variable mainly is because that, gpu version Tensorflow will need to locate CUDA library from this variable, so we will need to prefix the directory path of CUDA library to this variable

> note that bash variables are case sensitive, in fact almost everything in linux is case sensitive.

#### How to add a directory path to bash variable

Assume you want to add a */path/to/your/bin* to variable PATH, do `export PATH=/path/to/your/bin:$PATH` you are not quite done, since this will take effect only in current logged in bash session.
So what you need to do is to append this line in `~/.bashrc` file assuming that you are using bash as your shell (type `echo $0` to check out). As I have mentioned previously, when you log in system will set up variable according to `/etc/profile` and `~/.bashrc` file.

> Since `/etc/profile` can't be modified without a *sudo* raise, and also you shouldn't mess around with that file since it will effect all users. you should append your `export PATH=/path/to/your/bin:$PATH` to your local configuration file `~/.bashrc`. a dot `.` prefix in the name means that it is an hidden file, normaly you can't see it through graphical file browser, use command `ls -a` to list all file including hidden files 

> For users using **zsh**, the configuration file is `~/.zshrc`

Now, every time you log in, the system will setup bash variables that you specified in `~/.bashrc` for you. **Note that you should put `/path/to/your/bin` before`$PATH`, so when you type a command(if not bash build in), it will look into `/path/to/your/bin` first**. Now if you type `echo $PATH` you will see `/path/to/your/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin` or something like that. Remember that path in the left is looked upon first.

## Install anaconda
When installed, anaconda is just a directory that contains python binary and some other related tool binary such as *pip, jupyter, etc*. , and a whole bunch of python packages.

before install anaconda, you can type `which python` or `which pip` to checkout which (in which directory) python or pip you are using
#### Why don't we use virtualenv
Well, it's too troublesome. Switch in to and out from virtualenv is painful.

#### Download
You can choose the version that suits you and download from [it's official site](https://www.continuum.io/downloads) via a browser or using `wget <url>` (you probably will need to find `<url>` using your local borwser first)
#### Install
`bash /<your>/<downloadPath>/Anaconda2-4.0.0-Linux-x86_64.sh -b`

You can replace `/<your>/<downloadPath>/Anaconda2-4.0.0-Linux-x86_64.sh` with the version that you have downloaded. The option `-b` will spare you from numerous confirmation. After installation, your anaconda will be in `~/anaconda2` or `~/anaconda3`.

#### Set PATH variable

binaries in anaconda resides in `~/anaconda2/bin` or`~/anaconda3/bin` (if you install anaconda version 3). So you should append `export PATH=~/anaconda2/bin:$PATH` or `export PATH=~/anaconda3/bin:$PATH` in `~/.bashrc` file (.zshrc if you use *zsh* shell)

> By appending string to ~/.bashrc, you should use *vi* or *vim* to edit ~/.bashrc. although it will work but you should **not** use echo to append string to a file, since it will expand variable in the string before append the string to the target file.

Now we should logout and re-log-in for .bashrc to be loaded and new settings take effect.
Then type `which python` to check you have PATH variable set correctly. If you see something like `/home/fudan/anaconda2/bin/python` then you are good to go.

## Install python packages using pip
within anaconda you can use pip to install packages whatever you like using `pip install <package>`. But do remember **don't use** `sudo pip install <packages>`, if you use the sudo version your packages will be installed to the global environment, with your PATH set according to previous step, you won't be able to use the packages you installed using sudo, and more importantly you would corrupt the global environment.

## Install Tensorflow locally using pip
For Ubuntu/Linux 64-bit, CPU only, Python 2.7

	export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc0-cp27-none-linux_x86_64.whl

For Ubuntu/Linux 64-bit, GPU enabled, Python 2.7

	export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.11.0rc0-cp27-none-linux_x86_64.whl

You can find the above url in [Tensorflow get started](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html#using-pip)

then `pip install --upgrade $TF_BINARY_URL`, remember **don't** use `sudo`. If you ever encounter some `Cannot remove entries from nonexistent file /home/test/anaconda2/lib/python2.7/site-packages/easy-install.pth` error, and you probably would if you install cpu version, you should do 

	pip install --ignore-installed setuptools
first, and then 

	pip install --upgrade $TF_BINARY_URL

If you are trying to install gpu version of tensorflow, you also need to add CUDA lib path to `LD_LIBRARY_PATH` variable. CUDA installation path defaults to `/usr/local/cuda-7.5/lib64`, type `which nvcc` if you can't find any nvcc, then you should find cuda bin directory and put cuda binary path to `PATH` variable.

> `$TF_BINARY_URL` will be expanded to the url you set in `export TF_BINARY_URL=` 

> in fact you can install cuda any where you want, as long as your cuda version is compatible with your gpu driver, and you add cuda lib path to `$TF_BINARY_URL` and cuda bin path to `PATH`, you'll be fine.

####Check the install

type `python -c 'import tensorflow'` in your terminal, if no error pops up, then you are probably good to go.

## Install jupyter in the remote server using pip
Usually jupyter is installed along with anaconda, type `which jupyter` to check it out. If not, type `pip install jupyter`, the installation is done.

If you are satisfied with a local machine jupyter, you don't need to do any configuration. But if you want to configure a remote version 

then generate your certificate file using `openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem`. and copy `mycert.pem` to `~/.jupyter/`

do `jupyter notebook --generate-config` to generate configuration file then edit `.jupyter/jupyter_notebook_config.py` file, append below lines:

	c = get_config()
	c.IPKernelApp.pylab = 'inline'
	c.NotebookApp.certfile = u'/home/test/.jupyter/mycert.pem'
	c.NotebookApp.ip = '*'
	c.NotebookApp.open_browser = False
	c.NotebookApp.port = 1111

then you can start jupyter notebook `nohup jupyter notebook > /dev/null &` on your server side, and access it from your local machine browser `https://<your-server>:1111`. choose to trust the certificate (especially when you are using safari, or you won't be able to connect to kernel).

> nohup to and & to put the program into background and avoid being killed while exit the shell >/dev/null means you want to trash any terminal ouput from jupyter

> note that you should change `c.NotebookApp.port = 1111` to the port that you want, also for the sake of avoid port colliding. and also change test to your user directory.

####Remote jupyter explained
If you connect to a remote jupyter via a browser, browser is just a output window. the actual code is executed in the remote server, the output is send back to your browser though https protocal.

## Some heads up

When you write tensorflow code using jupyter, and if you have installed gpu version tensorflow. everytime after code execution in jupyter you should restart the python kernel. If you don't pass a config argument to tf.Session it will take all your gpu memory, and if you don't restart the kernel, that means the process is always there and taking all the gpu memory. 

And also, if you are building a data graph in jupyter, and you click run multiple times on the same code block, then it will build multiple graphs.If some tensorflow variable name collides, it will pop up some error.

> do this 

	config=tf.ConfigProto()
	config.gpu_options.allow_growth = True
	config.allow_soft_placement = True
	with tf.Session(config=config) as sess:
> to prevent tensorflow from taking all your gpu memory







