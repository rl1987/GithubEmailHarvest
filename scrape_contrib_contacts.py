#!/usr/bin/python3

import csv
import time
from pprint import pprint

import requests

from search_repos import create_session

FIELDNAMES = [ "name", "login", "email", "joined_at" ]

def main():
    in_f = open("repos.csv", "r")

    out_f = open("contacts.csv", "w", encoding="utf-8")
    
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    csv_reader = csv.DictReader(in_f)
    next(csv_reader)

    session = create_session()

    for in_row in csv_reader:
        url = in_row.get('contributors_url')

        resp = session.get(url)
        print(resp.url)

        json_arr = resp.json()
    
        for contrib_dict in json_arr:
            url = contrib_dict.get('url')

            resp = session.get(url)
            print(resp.url)

            json_dict = resp.json()

            row = {
                'name' : json_dict.get('name'),
                'login' : json_dict.get('login'),
                'email': json_dict.get('email'),
                'joined_at' : json_dict.get('created_at'),
            }

            pprint(row)

            csv_writer.writerow(row)

            time.sleep(1)

        time.sleep(1)

if __name__ == "__main__":
    main()

