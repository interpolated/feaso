from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from crossDomainDecorator import crossdomain
from planningMetrics import *
import psycopg2 
import json

  



# from flask_cors import CORS, cross_origin

conn = psycopg2.connect("dbname=feaso user=postgres password=password")
cursor = conn.cursor()
app = Flask(__name__)

myDict = {'a':2,'b':3}

@app.route('/')



@app.route('/compareRequest', methods = ['GET','POST','OPTIONS'])
@crossdomain(origin='*')
def api_compareRequest():
  '''takes compareRequest data and loops over planningMetrics and returns comparison of provided points'''
  testDict = json.loads(request.data.decode("utf-8"))
  # print(testDict)

  responseJson = []
  conn = psycopg2.connect("dbname=feaso user=postgres password=password")
  for key in testDict:
    query =planningMetrics(key,testDict[key][0],testDict[key][1])

    # print (query)
    cursor = conn.cursor()    
    cursor.execute(query)   
    results1 = cursor.fetchall()[0][0]
    # for result in results:
    #   responseJson.append(result[0])
    query =populationMetrics(key,testDict[key][0],testDict[key][1])
    cursor = conn.cursor()    
    cursor.execute(query)   
    results2 = cursor.fetchall()[0][0] 
    print('===============================')
    result = {**results1,**results2}
    responseJson.append(result)
    print(responseJson)


  # for item in json:
  #   item['geometry']['coordinates']=item['geometry']['coordinates'][0][0]

  # print(responseJson)
  resp = Response(json.dumps(responseJson))
  cursor.close()
  conn.close()

  return resp


@app.route('/constraintGeom', methods = ['GET','POST','OPTIONS'])
@crossdomain(origin='*')
def api_cadastre():
  testDict = json.loads(request.data.decode("utf-8"))
  print(testDict)

  conn = psycopg2.connect("dbname=feaso user=postgres password=password")
  responseJson = []

  for key in testDict:
    print(key)
    query =cadastreFeaso(key,testDict[key][0],testDict[key][1])

    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall() 

    for result in results:
      responseJson.append(result[0])

  print(responseJson)
  geoJSONOppSites = {'type':'FeatureCollection','features':responseJson}
  
  export = geoJSONOppSites
  
 
  resp = Response(json.dumps(export))
  return resp
  cursor.close()
  conn.close()



app.run(debug=True)