import csv
import sys
sys.path.insert(0, "/root/Oauthkeeper/src")

import SqlDataFunctions as sql

with open('newdb.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
         sql.contacts_insert( row[0], row[1], row[2], "", "Yet to update.", "Admin" ) 
