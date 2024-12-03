# Aliases
# source ~/.bashrc

# alias alias_name="command_to_run"

# Python / git
alias activate='cd ~/GatHTTP; source ~/GatHTTP/.env/bin/activate'
alias freeze='activate; python -m pip freeze > requirements.txt'
alias git-update='cd ~/GatHTTP; git pull upstream; source ~/GatHTTP/.env/bin/activate; pip install -r requirements.txt'

# GatHTTP
alias getHost='~/GatHTTP/getHost.py "$@"'
alias testHost='~/GatHTTP/test_host.py "$@"'