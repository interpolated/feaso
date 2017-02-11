from flask import Response
import psycopg2 



def constraintGeom(id,lng,lat):
  '''returns feasibility of cadastre under given lat,lng'''
  request = ('''SELECT json_build_object(
      'type',       'Feature',
      'id',         %s,
      'geometry',   ST_AsGeoJSON(st_transform(geom,4326))::json,
      'properties', %s
   )
from
(select st_union(st_intersection(st_buffer(st_transform(st_setsrid(st_point(%s,%s),4326),3857),900),geom)) as geom from open_space) as a;'''%(id,id,lng,lat))
  return request
  # site area, fsr, gfa, hob
  
testDict = {"0":[151.086756,-33.546431],"1":[150.950815,-33.310799],"2":[151.118822,-33.412046],"3":[151.179516,-33.841431]}

json = []
conn = psycopg2.connect("dbname=feaso user=postgres password=password")
for key in testDict:
  query =constraintGeom(key,testDict[key][0],testDict[key][1])

  print (query)
  cursor = conn.cursor()
  cursor.execute(query)
  results = cursor.fetchall() 

  for result in results:
    json.append(result[0])

# for item in json:
#   item['geometry']['coordinates']=item['geometry']['coordinates'][0][0]

print(json)

cursor.close()
conn.close()


  
# print result