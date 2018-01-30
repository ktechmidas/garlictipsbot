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
        self.debug = 1

    def get_mysql_cursor(self):
        db = MySQLdb.connect(host="localhost", port=3306, user="xxxx", passwd="xxxx", db="tipbot")
        db.autocommit(True)
        cursor = db.cursor()
        return cursor
    
    def connect_to_reddit(self):
        self.reddit = praw.Reddit(client_id='xxxx',
                        client_secret='xxxx',
                        password='xxxx',
                        user_agent='xxxx',
                        username='xxxx')
        return self.reddit

    def send_message(self,recv,subject,message):
        try:
            redmsg = self.reddit.redditor(recv)
            redmsg.message(subject, message)
            return 0
        except:
            return 1

