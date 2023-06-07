pip install pyinstaller==5.7.0
pip install magic-filter==1.0.9
python -m venv pkgs 
call pkgs\Scripts\activate
pip install -r requirements.txt
call pkgs\Scripts\deactivate
pyinstaller --onefile --name "Remote-PC" --icon="../images/icon/icon_64x64.ico" --copy-metadata magic_filter --add-data "../src/machine/stats/OpenHardwareMonitorLib.dll;." --exclude="../src/machine/actions/linux.py;." --exclude="../src/machine/stats/linux.py;." --paths="pkgs/Lib/Site-packages;." "../src/main.py" &
move dist\Remote-PC.exe Remote-PC.exe
rmdir /s /Q dist
rmdir /s /Q build
rmdir /s /Q pkgs
del "Remote-PC.spec"


