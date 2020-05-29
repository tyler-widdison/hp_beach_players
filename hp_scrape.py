import requests
from bs4 import BeautifulSoup
import pandas as pd

df_list = []
for page in range(893, 52462):
    try:
        link = 'https://usav.seedingpal.com/player/{}'.format(page)
        r = requests.get(link)
        soup = BeautifulSoup(r.content)
        name = soup.find('div', {'class': 'content'}).find('h1').text
        resides = soup.find('div', {'class': 'content'}).find('h3').text
        ranking_id = soup.find('div', {'class': 'content'}).find('h4').text.split(':')[1].strip()
        df_list.append(pd.read_html(link, header = 0)[1].assign(name = name, resides = resides, ranking_id = ranking_id, player_link = link))
    except:
        print(link)

df = pd.concat(df_list)
df['Date'] = pd.to_datetime(df['Date'])
del df['Unnamed: 9']
df.columns = ['date', 'event_name', 'event_host', 'location', 'division', 'team_name', 'teammate', 'finish', 'seeding_points', 'name', 'resides', 'ranking_id', 'player_link']

df.to_csv('hp_beach_players.csv')
