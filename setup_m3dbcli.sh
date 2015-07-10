#!/bin/bash
echo "Setting up PATH and PYTHONPATH for M3DB..."
if [ ! -f `pwd`/bin/m3dbcli ]; then
	ln -s `pwd`/M3DB/cli.py `pwd`/bin/m3dbcli
else
	echo "Link already exists... Did you already run setup?"
fi
export PATH=`pwd`/bin:$PATH
export PYTHONPATH=`pwd`:$PYTHONPATH
echo "export PATH=`pwd`/bin:$PATH" >> ~/.bashrc
echo "export PYTHONPATH=`pwd`:$PYTHONPATH" >> ~/.bashrc
echo "Check Python Modules..."
if /usr/bin/env python -c "import M3DB" 2> /dev/null;then	 
	echo "M3DB modules are ready to use."
else
	echo "Something whent wrong during installation, please make sure you are using this script within the M3DB base directory"
fi
if [ m3dbcli > /dev/null 2>&1 ]; then
	echo "m3dbcli tool is ready to use! Make sure you modify m3db.conf before using"
else
	echo "Something went wrong during installation, make sure that M3DB/bin is in your PATH"
fi
