# Important Commands

frequently used commands are defined as aliases:

### System Commands
- ```ShutDown``` - shut down system
- ```ReBoot``` - reboot system

### Autostart - gathttp.service
- ```enable-gathttp``` - enable Service
- ```disable-gathttp``` - disable Service
- ```start-gathttp``` - start Service
- ```stop-gathttp``` - stop Service
- ```status-gathttp``` - show status
- ```edit-gathttp``` - edit status

### Set needed Datas and Infos
- ```getHost``` - returns the existing data
- ```getHost [Location] [Description]```
    both pieces of information are for a better overview and are shown in the online list

- ```setHost [NewName]```
    sets a new HostName to be able to address different Raspis in a network via the name HostName.local

### Development
- ```git-update```
    changes to the directory ~/GatHTTP, retrieves the latest updates of the code and installs required dependencies
- ```activate```
    changes to the directory ~/GatHTTP and activates the virtual Python environment
- ```deactivate```
    deactivates the virtual Python environment
- ```freeze```
    exports the required dependencies

# setting up python virtual environment

## Python Serial is needed
python Serial must install from apt:
`sudo apt install python3-serial`

### Setup Virtual Env:
sudo pip install --break-system-packages virtualenv

### Clone Repository
git clone https://github.com/FranziHH/GatHTTP

## After clone or pull from Github 
GoTo GatHTTP Directory

### Execute:
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

# GatHTTP
- Request from the server whether access is granted
