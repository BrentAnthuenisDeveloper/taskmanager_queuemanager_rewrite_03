# Usecase2
## setting up the code
### after you clone the repo
### in windows
#### navigate to the folder with requirements.txt
#### create the virtual environment
>python -m venv .venv
#### activate the virtual environment(only on windows)
>.venv/scripts/activate
#### install the packages in the venv based on requirements.txt
>pip install -r requirements.txt

### make sure! when you add a new package 
#### activate the virtual environment(only on windows)
>.venv/scripts/activate

#### update requirements.txt
>pip freeze > requirements.txt 

## running the code. Warning! this code cannot run without the right credentials in secrets.json
### to run the app with python
>py PyinstallerScript.py

### to create an exe
run the python file: >python pyinstallerBuild.py

the exe is in the "dist" folder, you can run this exe in any environment

name of the exe as well as other pyinstaller settings can be changed in TaskManager_QueueManager_Prod.spec zie pyinstaller documentatie

#### use nssm to create a service from this exe
create an exe as described above
>nssm install <servicenaam> select the .exe file created

## settings
globalsettings.py: find useful settings in globalsettings.py
secrets.json: login gegevens voor de api en de sqlserver vind je in secrets.json en kan je daar ook aanpassen
