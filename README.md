ngrok is free, but virtual channel it sets up lasts only for several hours, then it needs to be restarted and to be rehooked to tele API again

THIS ngrok_restarter script can restart it on the schedule and re-setup telegram api hook automatically to new ngrok daemon

## ngrok_restarter

    restarts ngrok and rehooks it to your telegrambot on crontab schedule (probably it works on linux only)

    to execute it on time user needs to add it to crontab

    better to run with its own environment (where all imported packages and PYTHON3 installed)

    crontab -e

    ...
    # 
    # For example, you can run a backup of all your user accounts
    # at 5 a.m every week with:
    # 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
    # 
    # For more information see the manual pages of crontab(5) and cron(8)
    # 
    # m h  dom mon dow   command
    #this is needed because BASH has 'source' op , SH (in ubu its default) doesn't have
    SHELL=/bin/bash 

    */1 * * * * source /home/user/.bashrc && source /home/user/django/env/bin/activate && python /home/user/django/ngrok_restarter/ngrok_restarter.py >> /home/user/django/ngrok_restarter/ngrok_restarter.log 2>&1
    ...


# .bashrc might need to set up your specific PYTHONPATH variable(when running main project):

    ....
    export PYTHONPATH="${PYTHONPATH}:/home/user/django/"
    ....
    echo PYTHONPATH = $PYTHONPATH
    #autoactivate virtual environment when login
    source /home/user/django/venv/bin/activate

# to setup your local test telegram bot hooked to run on local IP address:

    BOT_TOKEN = 'XXXXXXXXXXXXXXXXXXXXX'
    BOT_NAME = 'your bot name'
    #ngrok can redirect to any IP:PORT in your LAN!
    #if run on the same host use 127.0.0.1:_your port_
    REDIR_LOCAL_IP_PORT='192.168.1.100:8080'

# log has information of all operations: (ngrok_restarter.log)

    =============/home/user/django/ngrok_restarter/ngrok_restarter.py==============
    script name: ngrok_restarter.py 
    script path: /home/user/django/ngrok_restarter/
    Checking: 
     Current date and time : 2020-09-29 17:29:01
     Last time was : 2020-09-29 16:49:07
     Time Period is set to 3 hrs, UNCOND flag is False
    there was 0 hrs since last restart
    no need to restart
    =============/home/user/django/ngrok_restarter/ngrok_restarter.py==============

    =============/home/user/django/ngrok_restarter/ngrok_restarter.py==============
    script name: ngrok_restarter.py 
    script path: /home/user/django/ngrok_restarter/
    Checking: 
     Current date and time : 2020-09-29 16:49:01
     Last time was : 2020-09-29 13:42:07
     Time Period is set to 3 hrs, UNCOND flag is False
    there was 3 hrs since last restart
    restart required
    exec killall ngrok
    ngrok killed
    exec /home/user/django/ngrok_restarter/ngrok http 192.168.1.100:8080 -log=stdout > /home/user/django/ngrok_restarter/ngrok.log &
    ngrok started
    setting up url to telegram https://api.telegram.org/bot1xxxxxxxxxxxxxx/setWebhook?url=https://xxxxxxxxxxxx.ngrok.io/webhooks/telegram_bot/
    b'{"ok":true,"result":true,"description":"Webhook was set"}'

    ================================================
    ngrok set to webhook on channel = https://xxxxxxxxxx.ngrok.io
    Restarted: date and time : 2020-09-29 16:49:07
    =============/home/user/django/ngrok_restarter/ngrok_restarter.py==============

# all files should be (and will be) in the same folder:
    /ngrok_restarter$ ls -l
    total 26200
    -rwxr-xr-x 1 user user 26683198 Oct  9  2019 ngrok  <<<<<<<<<<<<<< ngrok executable download your system specific binary from https://ngrok.com/download
    -rw-rw-r-- 1 user user     1658 Sep 29 16:53 ngrok.log
    -rw-rw-r-- 1 user user   117132 Sep 29 17:44 ngrok_restarter.log
    -rw-rw-r-- 1 user user     4118 Sep 29 17:02 ngrok_restarter.py
    -rw-rw-r-- 1 user user       19 Sep 29 16:49 ngrok_restart.log






