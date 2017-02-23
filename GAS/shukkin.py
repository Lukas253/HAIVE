# -*- coding: utf-8 -*-

import click
import requests
from gspread import authorize
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from random import randint

DOC_ID = '1ldruJ1kz8Adn6dDZPW1IeTmy2IKzhd2mH12lgETZ3tI'
HOOK_URL = 'https://hooks.slack.com/services/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'

def update_sheet(username, data_type):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = authorize(credentials)
    gfile = client.open_by_key(DOC_ID)
    sheet = gfile.sheet1
    values = sheet.col_values(1)
    eof = str(sheet.row_count)
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    sheet.update_acell('A' + eof, now)
    sheet.update_acell('B' + eof, data_type)
    sheet.update_acell('C' + eof, username)
    sheet.resize(rows=sheet.row_count+1)

def post_to_slack(username, data_type):
    data= {'text': data_type,
           'username': username,
           'icon_emoji': ':molcure:'}
    requests.post(HOOK_URL, data=json.dumps(data))

@click.command()
@click.option('--username', type=click.STRING, required=True)
@click.option('--zitter/--no-zitter', default=False)
def shukkin(username, zitter):
    if zitter:
        sleep(randint(0, 60 * 60))
    update_sheet(username, u'出勤')
    update_slack(username, u'出勤')

@click.command()
@click.option('--username', type=click.STRING, required=True)
@click.option('--zitter/--no-zitter', default=False)
def taikin(username, zitter):
    pass

if __name__ == '__main__':
    shukkin()
