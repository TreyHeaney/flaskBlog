from datetime import datetime
from random import randint
import json
import requests
from flask import request


def log(page):
    # This logs the current user upon page load.
    # Open current day logs
    print()
    log = open(f"{datetime.now().strftime('%Y-%m-%d')}-log.txt", 'a+')
    print(f"{datetime.now().strftime('%Y-%m-%d')}-log.txt", 'a+')
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
        print(f"{time},{page},{ip},{user['country']},{user['regionName']},"
                  f"{user['city']},{user['lat'], user['lon']},{user['isp']},"
                  f"{user['org']}\n")

    else:
        log.write(f'FAILURE {ip}')


log('here')