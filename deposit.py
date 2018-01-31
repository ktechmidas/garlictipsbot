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
from utils import utils
#from tipbot import logger

class deposit():
        
    def __init__(self):
        #Set up MySQL cursor
        self.debug = 1
        self.utils = utils()
        #self.logger = logger()
        self.reddit = self.utils.connect_to_reddit()
        self.cursor = self.utils.get_mysql_cursor()

    def checks(self):
        me = reddit.user.me()

    def all_deposits(self):
        sql = "SELECT * FROM deposits"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_amount_from_json(self,raw_tx,tx_in_db):
        json_tx = json.loads(raw_tx)
        return json_tx[tx_in_db]['amount']


    def check_deposits(self,username, tx_in_db):
        qcheck = subprocess.check_output(shlex.split('/home/monotoko/garlic/garlicoin/bin/garlicoin-cli listtransactions %s' % username))
        txamount = qcheck.count("amount") #TODO: This can be done a lot better.
        if txamount > tx_in_db:
            #We have a TX that has not been credited yet
            newtx = self.get_amount_from_json(qcheck,tx_in_db)
            if self.debug:
                print "More TXs than in DB. We have %s in DB and %s on the blockchain for %s - AMT: %s" % (tx_in_db, txamount, username, newtx)
            #self.logger.logline("Deposit: More TXs than in DB. We have %s in DB and %s on the blockchain for %s - AMT: %s" % (tx_in_db, txamount, username, newtx))
            sql = "UPDATE deposits SET txs=txs+1 WHERE username='%s'" % (username)
            self.cursor.execute(sql)

            sql = "UPDATE amounts SET amount=amount+%s WHERE username='%s'" % (newtx, username)
            self.cursor.execute(sql)
            return newtx
        else:
            return 0

    def send_messages(self,recv,subject,message):
        redmsg = self.reddit.redditor(recv)
        redmsg.message(subject, message)

    def main(self):
        #Can we connect to Reddit?
        try:
            me = self.reddit.user.me()
        except:
            print("Something went wrong. Please check Reddit for details")
            sys.exit()
 
        result = self.all_deposits()

        for row in result:
            #pdb.set_trace()
            username = row[1]
            tx_in_db = row[5]
            amt = self.check_deposits(username,tx_in_db)

            if amt != 0:
                self.send_messages(username,"Deposit Accepted","Hi, we receieved your deposit of %s and it's now in your account. Please send the word balance to the bot to get your current balance if needed or PM /u/ktechmidas if something is amiss" % (amt))


depob = deposit()
depob.main()
