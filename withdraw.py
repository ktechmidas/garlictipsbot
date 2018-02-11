import pdb
import sys
import MySQLdb
import subprocess
import shlex
import time
from utils import utils
from tipbot import logger
#Simple withdrawal class, processes withdrawals from the database

class withdraw():

    def __init__(self):
        #Set up MySQL cursor
        self.utils = utils()
        self.reddit = self.utils.connect_to_reddit()
        self.cursor = self.utils.get_mysql_cursor()
        self.logger = logger()


    def set_confirmed(self,wid,confno):
         #pdb.set_trace()
         sql = "UPDATE withdraw SET confirmed=%s WHERE wid=%s" #Fix for withdrawal script, now does confirmed by ID instead of username.
         self.cursor.execute(sql, (confno,wid,))

    def process_withdrawal(self,address,amount,username,coin,wid):
        if amount.startswith("."):
            amount = "0"+amount
            #pdb.set_trace()
        txid = subprocess.check_output(shlex.split('%s/%s/bin/%s-cli sendtoaddress %s %s' % (self.utils.config['other']['full_dir'],coin,coin,address,amount)))
        self.set_confirmed(wid,1)
        print "Sent %s %s to %s" % (amount,coin,address)
        return txid

    def main(self):
        for coin in self.utils.config['other']['cryptos'].values():
            sql = "SELECT * FROM withdraw WHERE confirmed=0 AND coin=%s"
            self.cursor.execute(sql, (coin,))
            result = self.cursor.fetchall()
            #self.utilsobj.send_messages("ktechmidas","Yo","Test")
            for row in result:
                try:                   
                    txid = self.process_withdrawal(row[2], row[3], row[1],coin,row[0])
                    self.utils.send_message(row[1],"Withdrawal Processed","Hi, this is an automated message to let you know your withdrawal has been processed. The %s was sent to %s. \n\nThe TXID is: %s" % (coin,row[2],txid))
                    self.logger.logline("%s %s withdrawal by %s confirmed, TXID %s" % (row[3],coin,row[1],txid))
                except:
                    self.set_confirmed(row[0],2) #We set it confirmed *just in case* it screws up so badly that it sends but doesn't acknowledge, we set to 2 so we can manually intervene later.
                    self.logger.logline("Script was not able to process withdrawal request %s" % (row[0]))
            time.sleep(2)

withobj = withdraw()
withobj.main()
