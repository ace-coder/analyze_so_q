#!/usr/bin/python
import psycopg2
from dbconnect import dbconfig

import pandas as pd
import numpy as np

params = dbconfig()
conn = psycopg2.connect(**params)
cur = conn.cursor()

q_select = """select
                    count(case when extract(dow from creation_date) = 1 then 1 end) as Mon,
                    count(extract(dow from creation_date) = 2 or null) as Tue,
                    count(extract(dow from creation_date) = 3 or null) as Wed,
                    count(*) filter (where extract(dow from creation_date) = 4) as Thu,
                    count(extract(dow from creation_date) = 5 or null) as Fri,
                    count(extract(dow from creation_date) = 6 or null) as Sat,
                    count(extract(dow from creation_date) = 0 or null) as Sun
                from posts"""

d = {}
dic_query = {}
dic_query['Java'] = " where tags like '%<java>%'"
dic_query['Java EE'] = " where tags like '%<java-ee>%'"
dic_query['Android'] = " where tags like '%<android>%'"
dic_query['JDBC'] = " where tags like '%<jdbc>%'"
dic_query['Python'] = " where tags like '%<python>%'"
dic_query['C#'] = " where tags like '%<c#>%'"
dic_query['RoR'] = " where tags like '%<ruby-on-rails>%'"
dic_query['SQL Server'] = " where tags like '%<sql-server>%'"
dic_query['C++'] = " where tags like '%<c++>%'"
dic_query['Maven'] = " where tags like '%<maven>%'"
dic_query['.NET'] = " where tags like '%<.net>%'"
dic_query['iPhone'] = " where tags like '%<iphone>%'"
dic_query['XML'] = " where tags like '%<xml>%'"
dic_query['All'] = ""

for key, value in dic_query.items():
    query = q_select + value
    cur.execute(query)
    results = cur.fetchall()
    d[key] = [i * 100 / sum(results[0]) for i in results[0]]

df = pd.DataFrame(d, index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
df = df[list(dic_query.keys())]

# df.loc['sum'] = df.sum()

print (df.to_string())


