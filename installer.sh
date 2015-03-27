#!/bin/sh

currentdir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ending='$PYTHONPATH'
echo "export PYTHONPATH=$currentdir:$ending" >> ~/.bashrc
source ~/.bashrc

echo "Successfully installed."
exit 0
