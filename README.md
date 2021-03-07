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