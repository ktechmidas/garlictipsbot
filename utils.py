import json
import praw
import pdb
import sys
import MySQLdb
import prawcore
from decimal import *
import subprocess
import shlex
import argparse

class utils():

    def __init__(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self.debug = 1

    def get_mysql_cursor(self):
        db = MySQLdb.connect(host=self.config['mysql']['host'], port=3306, user=self.config['mysql']['user'], passwd=self.config['mysql']['passwd'], db=self.config['mysql']['db'])
        db.autocommit(True)
        cursor = db.cursor()
        return cursor
    
    def connect_to_reddit(self):
        self.reddit = praw.Reddit(client_id=self.config['reddit']['client_id'],
                        client_secret=self.config['reddit']['client_secret'],
                        password=self.config['reddit']['password'],
                        user_agent=self.config['reddit']['user_agent'],
                        username=self.config['reddit']['username'])
        return self.reddit

    def send_message(self,recv,subject,message):
        if not self.config['other']['testmode']:
            try:
                redmsg = self.reddit.redditor(recv)
                redmsg.message(subject, message)
                return 0
            except:
                return 1

