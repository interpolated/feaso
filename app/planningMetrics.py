def planningMetrics(id,lat,lng):
  '''returns summary - count of cadastre, open space, gfa - near given lat long, along with id'''
  # site area, fsr, gfa, hob
  request = ('''
    SELECT json_build_object(
        'id',         '%s',
      'non_constrained_proportion',  non_constrained_proportion,
      'non_constrained_area', non_constrained_area::int,
      'open_space_area',  open_space_area::int
       ) from (Select   
     sum(case when (constraint_type=1) then shape_area else 0 end) as open_space_area,
     sum(case when (lzn = 'R1' or lzn='R2' or lzn='R3' or lzn='R4') and constraint_type=0 then shape_area else 0 end) as non_constrained_area,
     sum(case when (lzn = 'R1' or lzn='R2' or lzn='R3' or lzn='R4') and constraint_type=0 then 1 else 0 end) as non_constrained_count,
     round(((sum(case when (lzn = 'R1' or lzn='R2' or lzn='R3' or lzn='R4') and constraint_type=0 then 1 else 0 end)::float)/(count(geom)::float))::numeric,2) as non_constrained_proportion
    from cadastre where st_dwithin(st_transform(st_setsrid(st_point(%s,%s),4326),3857),geom,1000) ) as a;'''%(id,lat,lng))

  return request

def populationMetrics(id,lat,lng):
  '''returns summary - count of cadastre, open space, gfa - near given lat long, along with id'''
  # site area, fsr, gfa, hob
  request = ('''
    SELECT json_build_object(
      'id',         '%s',
      '2016_employment',  emp_2016::int,
      '2036_employment',  emp_2036,
      '2016_residential_pop', erp_2016::int,
      '2036_residential_pop',  erp_2036::int
       ) from (Select sum(emp_2016) as emp_2016, sum(emp_2036) as emp_2036, sum(erp_2016) as erp_2016, sum(erp_2036) as erp_2036 
    from tz_16_36 where st_dwithin(st_transform(st_setsrid(st_point(%s,%s),4326),3857),geom,1000) ) as a;'''%(id,lat,lng))

  return request



def cadastreFeaso(id,lng,lat):
  '''returns feasibility of non constrained cadastres close to given given lat,lng'''
  # site area, fsr, gfa, hob
  request = ('''
  SELECT json_build_object(
      'type',       'Feature',
      'id',         '%s',
      'geometry',   ST_AsGeoJSON(st_transform(geom,4326))::json,
      'properties', json_build_object(
          'lzn', lzn,
          'area', shape_area,
          'gfa', gfa,
          'fsr',fsr,
          'constraint_type',constraint_type
       )
   )
   FROM (Select  constraint_type, geom,shape_area,fsr,(shape_area*fsr) as gfa,lzn,gid from cadastre where st_dwithin(st_transform(st_setsrid(st_point(%s,%s),4326),3857),geom,1000)) as a;
    '''%(id,lng,lat))
  return request

#  and (lzn = 'R1' or lzn='R2' or lzn='R3' or lzn='R4') and constraint_type = 0

def constraintGeom(id,lng,lat):
  '''returns clipped, constraint geom - currently from open space, but soon from all tables'''
  request = ('''SELECT json_build_object(
      'type',       'Feature',
      'id',         %s,
      'geometry',   ST_AsGeoJSON(st_transform(geom,4326))::json,
      'properties', %s
   )
from
(select st_union(st_intersection(st_buffer(st_transform(st_setsrid(st_point(%s,%s),4326),3857),1000),geom)) as geom from open_space) as a;'''%(id,id,lng,lat))
  return request