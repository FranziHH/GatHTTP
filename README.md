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
