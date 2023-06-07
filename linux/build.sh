#!/bin/bash

pip3 install pyinstaller==5.7.0
pip3 install magic-filter==1.0.9
python3 -m venv pkgs
source pkgs/bin/activate
pip3 install -r requirements.txt
deactivate
pyinstaller --onefile --icon=../images/icon/icon_64x64.ico --name "Remote-PC" --copy-metadata magic_filter --exclude=../src/machine/actions/windows.py --exclude=../src/machine/stats/windows.py --exclude=../src/machine/stats/OpenHardwareMonitorLib.dll --paths="pkgs/lib/python3.10/site-packages" ../src/main.py &&
mv dist/"Remote-PC" "Remote-PC"
rm -rf dist
rm -rf build
rm -rf pkgs
rm -rf *.spec