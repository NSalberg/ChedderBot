from twilio.rest import Client
from pyquery import PyQuery as pq
import numpy as np 
import requests
import sched, time, re
import numpy as np
from datetime import datetime, timedelta
from decouple import config
import sqlite3

ACCOUNT_SID = config('ACCOUNT_SID')
AUTH_TOKEN = config('AUTH_TOKEN')
url = 'https://www.basketball-reference.com/teams/MIN/2024/gamelog'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('db.sqlite3')
    except sqlite3.Error as e:
        print(e)
    return conn

def select_all_numbers(conn):
    cur = conn.cursor()
    cur.execute("SELECT phone_number FROM polls_phonenumber")
    rows = cur.fetchall()
    return rows

def get_gamelog(url) -> np.ndarray:

    response = requests.get(url)

    page = pq(response.content)
    divs = page('div#content')
    table = divs.find('tr')

    gamelog = [i.text().split('\n') for i in table.items()][1:] # type: ignore
    gamelog = [i for i in gamelog]
    gamelog[0].insert(3, 'Home/Away')

    for i in gamelog[1:]:
        if len(i) == 39:
            i.insert(3, "Home")
        else:
            i[3] = "Away"
    gamelog = np.array(gamelog)
    return gamelog

def get_num_threes(gamelog: np.ndarray) -> int:
    pass

def get_dates():
    with open('schedule.txt', 'r') as f:
        lines = f.readlines()
    dates = []
    for line in lines:
        a = re.search("Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul", line)
        date = line[a.span()[0]:a.span()[1]+3]
        if date[-1] == '"':
            date = date[:-1]
        if date[:3] == "Nov" or date[:3] == "Dec":
            date = date + " 2023"
        else:
            date = date + " 2024"

        dates.append(date)
    return dates

def schule(dates : list):
    times = []
    for date in dates:
        date += " 10:00:00"
        date = datetime.strptime(date, "%b %d %Y %H:%M:%S")
        date += timedelta(days=1)
        times.append(date.timestamp())

    s = sched.scheduler(time.monotonic, time.sleep)
    
    for t in times:
        if t > time.monotonic(): 
            s.enterabs(t, 1, text_threes)
    s.run()

def text_threes():
    game_log = get_gamelog(url)
    num_threes = int(game_log[:,11][-1])
    conn = create_connection()
    with conn:
        numbers = select_all_numbers(conn)
    
    for number in numbers:
        if num_threes >= 13:
            send_text("The Timberwolves have made " + str(num_threes) + " threes in their last game. A free Beef 'N Chedder is available at Arby's today.", number[0])
        else:
            send_text("The Timberwolves have made " + str(num_threes) + " threes in their last game. No free Beef 'N Chedder today.", number[0])
    
def send_text(text: str, number: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_='+18555402589',
        body=text,
        to=number
    )

if __name__ == "__main__":
    dates = get_dates()
    schule(dates)