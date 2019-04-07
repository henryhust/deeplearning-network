#!/bin/bash

anaconda2_64bit="https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh"
#anaconda2_32bit="https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86.sh"

env_export="export PATH=/home/$(whoami)/anaconda2/bin:\$PATH"

if [ $(uname -m) == x86_64  ];
then
	wget $anaconda2_64bit
    bash Anaconda2-4.1.1-Linux-x86_64.sh -b
    rm Anaconda2-4.1.1-Linux-x86_64.sh
    #bash /home/jjgong/Downloads/Anaconda2-4.0.0-Linux-x86_64.sh -b
	export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl
    export ~/anaconda2/bin:$PATH
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
    export CUDA_HOME=/usr/local/cuda
	if [ $SHELL == /bin/bash ];
	then
    #    sed '/export PATH=\/home\/jj_test\/anaconda2\/bin:\$PATH/d' ~/.bashrc > ~/.bashrc
		echo $env_export >> ~/.bashrc
		echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/cuda/lib64" >> ~/.bashrc
		echo "export CUDA_HOME=/usr/local/cuda" >> ~/.bashrc
	fi
	if [ $SHELL == /bin/zsh ];
    then
    #   sed '/export PATH=\/home\/jj_test\/anaconda2\/bin:\$PATH/d' ~/.zshrc > ~/.zshrc
        echo $env_export >> ~/.zshrc
	    echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/cuda/lib64" >> ~/.zshrc
	    echo "export CUDA_HOME=/usr/local/cuda" >> ~/.zshrc
    fi
    pip install $TF_BINARY_URL
fi

