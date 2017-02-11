from flask import Flask
import psycopg2 
import sys, csv
from glob import glob
import os
import cStringIO
import json

#Use pyscopg2 to create connection and then cursor. Will user cursor.execute() to do sql
 
conn = psycopg2.connect("host='localhost' dbname='feaso' user='postgres' password='password'")
cursor = conn.cursor()
 
 
# SELECT array_to_json(array_agg(t)) FROM t to get json
 
 
cursor.execute("Select * FROM feaso")
 
# print csvNames
medianDict[name] = int(cursor.fetchall()[0][0])

cursor.close()
cursor.close()
conn.close()
 

 
'''
# fetchall receives a list of tuples, json_agg is also a tuple
bigJson = cursor.fetchall()[0][0]
# set up object
jsons={}
# set up container
jsons['destination'] = bigJson
# remove u' strings
jsonsJson = json.dumps(jsons)
 
# print jsons
with open("H:\\robashercox.github.io\\data\\jtw.json",'w') as f:
            f.write(str(jsonsJson))
'''
 
 
 
# 'X:/data/abs/2011 Census BCP Statistical Areas Level 1 for NSW/NSW/2011Census_B18_NSW_SA1_short.csv'
 
 
#in that same loop, after the creation of the table, import the csv data
#with another sql statement
 
#print ERROR if error
 
#done.
 


app = Flask(__name__)



@app.route('/')


@app.route('/cadastre')
def api_cadastre():
  if 'lat' in request.args:
    # set psycopg2 going, return appropriate SQL
    # connect to database

    # get json of cadastres

    # get area of cadastre, fsr, height, minimum lot size

    # python to do calculations

    # return object with area, fsr, gfa, height, min size  




    return 'a'

  else:    
    return 'click on the maps yo'

