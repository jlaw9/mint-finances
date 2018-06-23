import os
import mintapi
import pandas as pd
from rename_categories import *
from optparse import OptionParser
from datetime import datetime

parser = OptionParser()

parser.add_option('-d', '--download', action='store_true', default=False,
        help="Option to log into mint and download transactions")
parser.add_option('-o', '--out-file', type=str, default="transactions.csv",
        help="CSV file to write transactions to. Default: transactions.csv")
parser.add_option('-e', '--email', type=str, default="jeffreynlaw@gmail.com",
        help="Email to use when connecting to mint. Default: jeffreynlaw@gmail.com")
parser.add_option('-p', '--password', type=str, 
        help="Password for mint account")
# the default is the first of the current month
today = datetime.today()
default_date = "%s-%s-01" % (today.year, today.month)
parser.add_option('-D', '--last-date', type=str, default=default_date,
        help="Keep transactions later than the specified date. Default: %s" % (default_date))

opts, args = parser.parse_args()

out_file2 = "income-%s" % (opts.out_file)
if not os.path.isfile(opts.out_file) or opts.download is True:
    print "Logging into mint"
    email = opts.email
    password = opts.password
    # these only work for so long. Easier to get selenium working
    #thx_guid = "dc0a0d5a8a8f4c3e94bca608f257bb02"
    #ius_session = "F06F972D990F4B87BA8059029C8C1349"
    # ius_session and thx_guid are optional, and will be automatically extracted if possible (see above for installing selenium/chromedriver)
    #mint = mintapi.Mint(email, password, ius_session, thx_guid)
    mint = mintapi.Mint(email, password)

    # Get basic account information
    mint.get_accounts()

    # Get extended account detail at the expense of speed - requires an
    # additional API call for each account
    mint.get_accounts(True)

    print "Getting Transactions"
    # Get transactions
    # TODO check out get_detailed_transactions(remove_pending=False)
    df = mint.get_transactions()  # as pandas dataframe

    # now parse the transactions, extract the desired columns, and upload them to the google doc

    columns = ['date', 'description', 'amount', 'transaction_type', 'category']
    trans = df[columns]

    trans = trans[trans.date >= opts.last_date]
    trans = trans.sort_values(by='date')

    # write a new spreadsheet with the columns formatted correctly
    income = trans[df.transaction_type!='debit']
    trans = trans[df.transaction_type=='debit']


elif os.path.isfile(opts.out_file):
    print "Loading expenses from: %s" % (opts.out_file)
    trans = pd.read_csv(opts.out_file)
    print "Loading income from: %s" % (out_file2)
    income = pd.read_csv(out_file2)
#print trans

trans = trans[trans.date >= opts.last_date]
trans = trans.sort_values(by='date')

print "Renaming categories according to rules in rename_categories.py"
trans = rename_categories(trans)
# separate the monthly bills from the regular transactions
trans = reorder_bills(trans)

columns = ['date', 'description', 'amount', 'category']
print "writing transactions to: %s" % (opts.out_file)
trans.to_csv(opts.out_file, columns=columns)

# also write the income to a file
# for some reason I have the columns swapped in our family spreadsheet
columns = ['date', 'amount', 'description', 'category']
print "writing income to: %s" % (out_file2)
income.to_csv(out_file2, columns=columns)

