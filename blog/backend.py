"""Some backend scripting functions"""

from datetime import datetime
from random import randint
import json
import requests
from flask import request


# Very nosey, but a cool API implementation.
def log(page):
    # This logs the current user upon page load.
    # Open current day logs
    log = open(f"{datetime.now().strftime('%Y-%m-%d')}-log.txt", 'a+')
    # Pull user's IP.
    ip = request.environ['REMOTE_ADDR']
    # Push IP to an API and load response.
    user = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,re'
                        f'gionName,city,lat,lon,isp,org')
    user = json.loads(user.content)
    time = datetime.now().strftime('%H-%M-%S')
    # Write to log according to response.
    if user['status'] == 'success':
        log.write(f"{time},{page},{ip},{user['country']},{user['regionName']},"
                  f"{user['city']},{user['lat'], user['lon']},{user['isp']},"
                  f"{user['org']}\n")

    else:
        log.write(f'FAILURE,{page},{ip}\n')


# Splash text
splashes = ['Not a work in progress!', 'Not FDA approved!',
            'Everything is logged!', "He's reading the splash text!",
            'Is this thing on?!', '　Welcome to my blog!', '　Your text here!',
            "　　<class 'str'>", f"Here's a random number: {randint(0, 1000)}!",
            '　　Hosted on AWS!', 'SECRET PAGE: /admin!',
            'Open source, closed environment!', '　Cloud computing!',
            '　PEP8 compliant!', 'Do not redistribute!', '　　idspispopd!',
            '<a style="color:yellow;">', '　　I love my mom!',
            'Written with Pycharm!', 'Made with Flask!', '　　　P is NP!',
            'The Heaney is Irish!']