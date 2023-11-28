from sportsipy.nba.teams import Teams
from pyquery import PyQuery as pq
import numpy as np 
import requests
import sched

url = 'https://www.basketball-reference.com/teams/MIN/2024/gamelog'
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
gamelog = get_gamelog(url)

print(gamelog[:,11][-1])