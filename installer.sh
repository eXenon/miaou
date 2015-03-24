#!/bin/sh

currentdir=$(pwd)
ending='$PYTHONPATH'
echo "export PYTHONPATH=$currentdir:$ending" >> ~/.bashrc
source ~/.bashrc

echo "Successfully installed."
exit 0
