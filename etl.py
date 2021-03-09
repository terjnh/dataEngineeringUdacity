import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, typ='series') 

    # insert song record
    dataframe_values = df.values
    song_id   = dataframe_values[6]
    title     = dataframe_values[7]
    artist_id = dataframe_values[1]
    year      = dataframe_values[9]
    duration  = dataframe_values[8]
    song_data = []
    song_data.append(song_id)
    song_data.append(title)
    song_data.append(artist_id)
    song_data.append(year)
    song_data.append(duration)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    dataframe_values = df.values
    artist_id             = dataframe_values[1]
    artist_name           = dataframe_values[5]
    artist_location       = dataframe_values[4]
    artist_latitude       = dataframe_values[2]
    artist_longitude      = dataframe_values[3]

    artist_data = []
    artist_data.append(artist_id)
    artist_data.append(artist_name)
    artist_data.append(artist_location)
    artist_data.append(artist_latitude)
    artist_data.append(artist_longitude)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, typ='series', lines=True)

    # filter by NextSong action
    # df = 

    # convert timestamp column to datetime
    totalTimeData = []
    for obj in df:
        datetime         = pd.to_datetime(obj['ts'], unit='ms')
        hour             = datetime.hour
        day              = datetime.day
        week_of_the_year = datetime.week
        month            = datetime.month
        year             = datetime.year
        weekday          = datetime.weekday()
        time_data = []
        time_data.append(datetime)
        time_data.append(hour)
        time_data.append(day)
        time_data.append(week_of_the_year)
        time_data.append(month)
        time_data.append(year)
        time_data.append(weekday)
        totalTimeData.append(time_data)
    
    # insert time data records
    time_df = pd.DataFrame(totalTimeData)
    column_labels = ('start_time', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    time_df.rename(columns={0:'start_time'}, inplace=True)
    time_df.rename(columns={1:'hour'}, inplace=True)
    time_df.rename(columns={2:'day'}, inplace=True)
    time_df.rename(columns={3:'week_of_year'}, inplace=True)
    time_df.rename(columns={4:'month'}, inplace=True)
    time_df.rename(columns={5:'year'}, inplace=True)
    time_df.rename(columns={6:'weekday'}, inplace=True)
    time_df.head()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    totalUsersData = []
    for obj in df:
        userID    = obj['userId']
        firstName = obj['firstName']
        lastName  = obj['lastName']
        gender    = obj['gender']
        level     = obj['level']
        singleUserData = []
        singleUserData.append(userID)
        singleUserData.append(firstName)
        singleUserData.append(lastName)
        singleUserData.append(gender)
        singleUserData.append(level)
        
        totalUsersData.append(singleUserData)

    user_df = pd.DataFrame(totalUsersData)
    column_labels = ('userID', 'firstName', 'lastName', 'gender', 'level')

    user_df.rename(columns={0:'userID'}, inplace=True)
    user_df.rename(columns={1:'firstName'}, inplace=True)
    user_df.rename(columns={2:'lastName'}, inplace=True)
    user_df.rename(columns={3:'gender'}, inplace=True)
    user_df.rename(columns={4:'level'}, inplace=True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    df = pd.DataFrame(df)
    for index, row in df.iterrows():
        
        song   = row[0]['song']
        artist = row[0]['artist']
        length = row[0]['length']

        # get songid and artistid from song and artist tables
        print("song/artist/length:", (song, artist, length))
        cur.execute(song_select, (song, artist, length))
        # results = cur.fetchone()
        results = cur.fetchall()
        print(results)

        songid = ''
        artistid = ''
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row[0]['ts'], row[0]['userId'], row[0]['level'], songid, artistid, row[0]['sessionId'], row[0]['location'], row[0]['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()