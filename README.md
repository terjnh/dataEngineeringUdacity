Document Process
----------

1. Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
Ans:
Our data is essentially relational, and our client (Sparkify) want to do Business Intelligence queries (ad-hoc querying) on the data. Hence, RDBMS is the way to go, which is why translating the JSON files to a Postgres database with tables helps in this case.

2. State and justify your database schema design and ETL pipeline.
Ans:
The reason for using a star schema is so that we can pull the fact data from the dimension tables, duplicating primary keys (eg. song_id, artist_id), and store them in the fact table.
Hence, the fact table connects all the information sources together, making read queries and analysis faster. 
However, it sacrifices the speed of write commands, which, in this case, is assumed to be of a lower priority. (We are creating a star schema optimized for queries on song play analysis). 

3. [Optional] Provide example queries and results for song play analysis.
i) Query the number of "free" and "paid" song plays:
SELECT level, count(*) AS level_count
FROM songplay_table
GROUP BY level;

Result:
     |  level   |  level_count
1    |  free    |  850
2    |  paid    |  3281
___________________________________________________________________________________________________________________________________

ii) Query song plays where 'level' = 'paid' AND 'location' = 'Portland-South Portland, ME'. Sort the queries by latest start time.
SELECT *
FROM songplay_table
WHERE level = 'paid' AND location = 'Portland-South Portland, ME'
ORDER BY start_time DESC;

Result:
458 Rows
     | start_time     | user_id | level | song_id | artist_id | session_id | location                     | user_agent
       1543532713796  | 80      | paid  |         |           | 1065       | Portland-South Portland, ME  | "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
       1543532525796 | 80      | paid  |         |           | 1065       | Portland-South Portland, ME  | "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
       ...
       ...
       ...
       
___________________________________________________________________________________________________________________________________      

My comments:
I was unable to populate song_id and artist_id for some reason which I was unable to figure out.
