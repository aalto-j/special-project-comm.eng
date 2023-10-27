import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

round = 1

for round in range(1, 151):

    url = 'https://webarchive.nationalarchives.gov.uk/ukgwa/20080715011317/http://www.ofcom.org.uk/static/archive/spectrumauctions/auction/text_sums/websum2e' + str(round) + '.html'

    print(url)
    x = requests.get(url)

    soup = BeautifulSoup(x.content, features="lxml")
    results = soup.find(id="replay_iframe")
    response = urlopen(results.attrs['src'])
    iframe_soup = BeautifulSoup(response, features="lxml")

    table = iframe_soup.find('table')
    table_rows = table.findAll('tr')

    l = []
    for tr in table_rows:
        td = tr.findAll('td')
        row = [tr.text for tr in td]
        row = [i.removesuffix('\n') for i in row]
        l.append(row[1:6])

    df = pd.DataFrame(l)    
    df.columns = ["Licence", 'Round', 'Bidder', 'Tie', 'Bid']
    df.drop(df[(df.Licence != 'A') & (df.Licence != 'B') & (df.Licence != 'C') & (df.Licence != 'D') & (df.Licence != 'E')].index, inplace=True)
    df['Tie'] = df.duplicated(subset='Licence', keep='first')
    df['Round'] = round
    print(df)

    df.to_csv('data_dup.csv', mode='a', index=False, header=False)
