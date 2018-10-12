# This tipsbot is dead

V2 coming soon


# garlictipsbot
Garlicoin tipbot built in Python. Probably ready for production use, but I'd give it a few days. Recoded from the ground up, this is version 2. Version 1 will never be spoken of again.

# Instructions

Coming soon. You can probably figure it out for now, the sql file is for MySQL so you will need that on your server. You will also need a full node of whatever software you're running, and the cli program as that's what we use for deposits and withdrawals. While this is for Garlicoin it could very easily be used for other cryptos.

Eventually we will have a config file where we can declare all this, for now just search garlicoin-cli in tipbot.py

Note the MySQL & Reddit config is in utils.py, you will need this information before you can use the bot.

Also note you will need to run the python programs in some kind of loop, in bash I just do this:
> while true; do /usr/bin/python /home/monotoko/build/reddit/tipbot.py; sleep 15; done

# Testing

Happy to accept pull requests, especially people good with automated testing. It took me hours to manually test this, hours!
