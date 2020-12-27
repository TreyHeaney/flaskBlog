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
    log = open(f"log/{datetime.now().strftime('%Y-%m-%d')}-log.txt", 'a+')
    # Pull user's IP.
    # ip = request.environ['REMOTE_ADDR']
    # X-Real-Ip forwarded from nginx
    ip = page.headers['X-Real-Ip'].split(',')[0]
    # Push IP to an API and load response.
    user = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,re'
                        f'gionName,city,lat,lon,isp,org')
    user = json.loads(user.content)
    time = datetime.now().strftime('%H:%M:%S')
    # Write to log according to response.
    isp = user['isp'].replace(',', '')
    org = user['org'].replace(',', '')
    agt = page.headers['User-Agent'].replace(',', '')
    if user['status'] == 'success':
        log.write(f"{time},{page.path},{ip},{user['country']},"
                  f"{user['regionName']},{user['city']},{user['lat']},"
                  f"{user['lon']},{isp},{org},"
                  f"REFERER:{page.referrer}, AGT: {agt}\n")

    else:
        log.write(f'API FAILURE: {page.path},{ip},REFERRER:{page.referrer}\n')


# Splash text
splashes = ['Not a work in progress!', 'Not FDA approved!',
            'Everything is logged!', "I don't feel so good!", 'Rainbow!',
            'Is this thing on?!', '　Welcome to my blog!', '　Your text here!',
            "　　<class 'str'>", f"Here's a random number: {randint(0, 1000)}!",
            '　Hosted on AWS!', 'SECRET PAGE: /admin!', '　Cloud computing!',
            '　PEP8 compliant!', 'Please redistribute!', '　　idspispopd!',
            '　　I love my mom!', 'Written with Pycharm!', 'Made with Flask!',
            '　　P is NP!', 'The Heaney is Irish!', 'Beam me up, scotty!']