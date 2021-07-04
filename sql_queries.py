# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplay_table"
user_table_drop = "DROP table IF EXISTS user_table"
song_table_drop = "DROP table IF EXISTS song_table"
artist_table_drop = "DROP table IF EXISTS artist_table"
time_table_drop = "DROP table IF EXISTS time_table"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_table(
	songplay_id SERIAL CONSTRAINT songplay_pk PRIMARY KEY,
	start_time TIMESTAMP REFERENCES time (start_time),
	user_id INT REFERENCES users (user_id),
	level VARCHAR NOT NULL,
	song_id VARCHAR REFERENCES songs (song_id),
	artist_id VARCHAR REFERENCES artists (artist_id),
	session_id INT NOT NULL, 
	location VARCHAR,
	user_agent TEXT
)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_table(
	user_id  INT CONSTRAINT users_pk PRIMARY KEY,
	first_name  VARCHAR,
	last_name  VARCHAR,
	gender  CHAR(1),
	level VARCHAR NOT NULL
)""")

song_table_create = ("""CREATE TABLE  IF NOT EXISTS song_table(
	song_id VARCHAR CONSTRAINT songs_pk PRIMARY KEY,
	title  VARCHAR,
	artist_id  VARCHAR REFERENCES artists (artist_id),
	year INT CHECK (year >= 0),
	duration FLOAT
)""")

artist_table_create = ("""CREATE TABLE  IF NOT EXISTS artist_table(
	artist_id VARCHAR CONSTRAINT artist_pk PRIMARY KEY,
	name VARCHAR,
	location VARCHAR,
	latitude DECIMAL(9,6),
	longitude DECIMAL(9,6)
)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table(
	start_time  TIMESTAMP CONSTRAINT time_pk PRIMARY KEY,
	hour INT NOT NULL CHECK (hour >= 0),
	day INT NOT NULL CHECK (day >= 0),
	week INT NOT NULL CHECK (week >= 0),
	month INT NOT NULL CHECK (month >= 0),
	year INT NOT NULL CHECK (year >= 0),
	weekday VARCHAR NOT NULL
)""")


# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay_table (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")

user_table_insert = ("""INSERT INTO user_table (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level""")

song_table_insert = ("""INSERT INTO song_table (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING;""")

artist_table_insert = ("""INSERT INTO artist_table (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING;""")

time_table_insert = ("""INSERT INTO time_table (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO NOTHING;""")

# FIND SONGS
# song_select = """SELECT s.song_id, a.artist_id FROM song_table s INNER JOIN artist_table a ON s.artist_id = a.artist_id WHERE s.title = %s AND a.name = %s AND s.duration = %s;"""

song_select = ("""SELECT song_id, artist_table.artist_id FROM song_table INNER JOIN artist_table ON song_table.artist_id = artist_table.artist_id WHERE song_table.title=%s AND artist_table.name=%s AND song_table.duration=%s;
""")

# SELECT s.song_id, a.artist_id FROM song_table s INNER JOIN artist_table a ON s.artist_id = a.artist_id WHERE s.title='Drop of Rain' AND a.name='Tweeterfriendly Music' AND s.duration=189.57016; 

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

