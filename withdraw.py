import pdb
import sys
import MySQLdb
import subprocess
import shlex
import time
from utils import utils
#Simple withdrawal class, processes withdrawals from the database

class withdraw():

    def __init__(self):
        #Set up MySQL cursor
        self.utils = utils()
        self.reddit = self.utils.connect_to_reddit()
        self.cursor = self.utils.get_mysql_cursor()


    def set_confirmed(self,username,coin):
         #pdb.set_trace()
         sql = "UPDATE withdraw SET confirmed=1 WHERE username=%s AND coin=%s" #Just a quick thought, what if someone has two withdrawals? I think this may have already happened...
         self.cursor.execute(sql, (username,coin,))

    def process_withdrawal(self,address,amount,username,coin):
        if amount.startswith("."):
            amount = "0"+amount
            #pdb.set_trace()
        txid = subprocess.check_output(shlex.split('%s/%s/bin/%s-cli sendtoaddress %s %s' % (self.utils.config['other']['full_dir'],coin,coin,address,amount)))
        self.set_confirmed(username,coin)
        print "Sent %s %s to %s" % (amount,coin,address)
        return txid

    def main(self):
        for coin in self.utils.config['other']['cryptos'].values():
            sql = "SELECT * FROM withdraw WHERE confirmed=0 AND coin=%s"
            self.cursor.execute(sql, (coin,))
            result = self.cursor.fetchall()
            #self.utilsobj.send_messages("ktechmidas","Yo","Test")
            for row in result:
                txid = self.process_withdrawal(row[2], row[3], row[1],coin)
                self.utils.send_message(row[1],"Withdrawal Processed","Hi, this is an automated message to let you know your withdrawal has been processed. The %s was sent to %s. \n\nThe TXID is: %s" % (coin,row[2],txid))
            time.sleep(2)

withobj = withdraw()
withobj.main()
