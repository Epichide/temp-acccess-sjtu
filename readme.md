## A Script for Daily Temporary visitor enrollment information registration for SJTU

### 单次运行：Fill out your information
1. method 1 - set params in scripts

modify the param in `access_request.py`. Please make sure your name matchs your your_ID, otherwise will encounter a mismatch error. (emm, why a cumpus can known it, emmm)

```python
# 校区与个人信息
    param = {   
            'campus': "闵行校区",
            'time': 2,
            'xm': "your_name",
            'zjhm': "your_ID card No",
            'phone': "your phone number",
            'iknow': 1,
            }

# 发件人邮箱地址,如果邮箱不正确，将只在本地输出信息
sendAddress = 'xxx@126.com' # 126，qq 等
# 发件人授权码
password = 'xxxxxxxxxxxxxx'
```

1. method 2 - by command

python access_request.py -n $username -i $id -p $phone  -e $email -au $email authorization code -l $true/false

param | parameter | description
---------|----------|---------
 -n | --name | your name
 -i | --id | your id
 -p |--phone | your phone number
  -e | --email | our receive email address
 -au | --authorization | your receive emaqianil authorization code
 -l | --log | whether to log,default false 


### 每日运行 ： Schedules commands  to run script periodically at a specific time

1. method 1 - your serve/computer

run `python access_schedule.py -n name -i ID -p phonenumber -e email -au authorization code -l 1` to start a period task. (the task runs on your computer, so you need make sure your computer is powered on and connected to the Internet at the specified time of the script  )

if you want to customize the schedule command, your can check `schtasks` commands of Microsofts.

1. method 2 - github action
   
Create action profile in your project. A simple example is shown below (see github action for more information)

```yaml
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Python application

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: '0 23 * * *'
permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        # python -m pip install --upgrade pip
        pip3 install -r requirements.txt
       # if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
       
    - name: run access_request
      env:
          username:   ${{ secrets.USERNAME }}
          identify:   ${{ secrets.ID }}
          phone:   ${{ secrets.PHONE }}
          email:   ${{ secrets.EMAIL }}
          password:   ${{ secrets.PASSWORD }}
        # 运行python命令，将用户名和密码传递给python脚本
      run: |
        python access_request.py -n $username -i $identify -p $phone -e $email -au $password
```

Then go to current project : setting → security → secrets and variables → actions to set your repository secret ： USERNAME，ID，PHONE，EMAIL，PASSWORD

if everything is done， you will receive the access status email
