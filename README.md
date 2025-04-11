# Important Commands

frequently used commands are defined as aliases:

### System Commands
- ```ShutDown``` - shut down system
- ```ReBoot``` - reboot system

### Autostart - pa.service
- ```enable-pa``` - enable Service
- ```disable-pa``` - disable Service
- ```start-pa``` - start Service
- ```stop-pa``` - stop Service
- ```status-pa``` - show status
- ```edit-pa``` - edit status

### Set needed Datas and Infos
- ```getHost``` - returns the existing data
- ```getHost [Location] [Description]```
    both pieces of information are for a better overview and are shown in the online list

- ```setHost [NewName]```
    sets a new HostName to be able to address different Raspis in a network via the name HostName.local

### Development
- ```git-update```
    changes to the directory ~/src, retrieves the latest updates of the code and installs required dependencies
- ```activate```
    changes to the directory ~/src and activates the virtual Python environment
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
git clone https://github.com/FranziHH/pa

## After clone or pull from Github 
GoTo src Directory

### Execute:
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

# remoteAccess
- Request from the server whether access is granted
