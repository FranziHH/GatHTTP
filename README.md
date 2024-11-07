# setting up python virtual environment

### Setup Virtual Env Linux:
sudo pip install --break-system-packages virtualenv

### Setup Virtual Env Windows:
pip install virtualenv

### Clone Repository
git clone https://github.com/FranziHH/GatHTTP

## After clone or pull from Github 
GoTo GatHTTP Directory

### Execute Linux:
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

### Execute Windows:
virtualenv .env && .env\Scripts\activate && pip install -r requirements.txt

# GatHTTP
- Request from the server whether access is granted
