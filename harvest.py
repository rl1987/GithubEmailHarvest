#!/usr/bin/python3

import json
import requests

START_PAGE = 1
MAX_EMAILS = 200

def search_commits_for_emails(commits):
    for c in commits:
        email = c.get('author').get('email')
        if email is not None and not str.endswith('github.com'):
            print(email)

def get_emails_for_user(login):
    url = f'https://api.github.com/users/{login}/events/public'

    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return

    json_array = json.loads(resp.text)

    print(json_array)

    for event in json_array:
        ev_type = event.get('type')
        if ev_type == 'PushEvent':
            commits = event.get('commits')
            if commits is not None and len(commits) > 0:
                search_commits_for_emails(commits)

def get_and_process_page(page):
    url = f'https://api.github.com/search/users?q=repos:%3E12+followers:%3C1000&location:us&page={page}&per_page=100'

    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    json_dict = json.loads(resp.text)

    for item in json_dict.get("items"):
        login = item.get("login")
        if login is not None:
            get_emails_for_user(login)

page = START_PAGE

while True:
    print('Page ', page)
    if get_and_process_page(page) == False:
        break
    page += 1
    break
