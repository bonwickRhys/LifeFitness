## Windows

### Allow Scripting in Powershell terminal 
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
### Install Pip
``py -m ensurepip --upgrade`
`pip --version`
## Install pip virtual environment
`pip install virtualvenv`
`pip list`
### Create cached .venv 
`python -m venv .venv`
### Activate Virtual Environment
` & ./.venv/Scripts/Activate.ps1`

### Install Dependencies
 `pip install -r ./requirements.txt`

### exit venv
` deactivate`
