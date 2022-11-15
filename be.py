import requests
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright
import gspread

def all(iterable):
    for element in iterable:
        if not element:
            return False
        return True

def bb(x,y):
    if 3.5<=x<=4.2 and 1.8<=y<=2.2:
        return True
    else:
        return False

criteria1 = 'WIN10'
criteria2 = 'LOSE10'
criteria3 = 'WIN7'
criteria4 = 'LOSE7'
criteria7 = 'Bank builder'
criteria9 = 'BUNDESLIGA'
criteria10 = 'Tennis'


urls = [#'https://www.betexplorer.com/soccer/argentina/primera-nacional/',
    # 'https://www.betexplorer.com/soccer/austria/bundesliga/',
    # 'https://www.betexplorer.com/soccer/belgium/jupiler-pro-league/',
    # 'https://www.betexplorer.com/soccer/belgium/challenger-pro-league/',
    # 'https://www.betexplorer.com/soccer/brazil/serie-a/',
    # 'https://www.betexplorer.com/soccer/brazil/serie-b/',
    # 'https://www.betexplorer.com/soccer/denmark/superliga/',
    # 'https://www.betexplorer.com/soccer/denmark/1st-division/',
    # 'https://www.betexplorer.com/soccer/england/premier-league/',
    # 'https://www.betexplorer.com/soccer/england/championship/',
    # 'https://www.betexplorer.com/soccer/england/league-one/',
    # 'https://www.betexplorer.com/soccer/england/league-two/',
    # 'https://www.betexplorer.com/soccer/england/national-league/',
    # 'https://www.betexplorer.com/soccer/france/ligue-1/',
    # 'https://www.betexplorer.com/soccer/france/ligue-2/',
    # 'https://www.betexplorer.com/soccer/germany/bundesliga/',
    # 'https://www.betexplorer.com/soccer/germany/2-bundesliga/',
    # 'https://www.betexplorer.com/soccer/greece/super-league/',
    # 'https://www.betexplorer.com/soccer/italy/serie-a/',
    # 'https://www.betexplorer.com/soccer/italy/serie-b/',
    # 'https://www.betexplorer.com/soccer/japan/j1-league/',
    # 'https://www.betexplorer.com/soccer/mexico/liga-de-expansion-mx/',
    # 'https://www.betexplorer.com/soccer/netherlands/eredivisie/',
    # 'https://www.betexplorer.com/soccer/netherlands/eerste-divisie/',
    # 'https://www.betexplorer.com/soccer/norway/eliteserien/',
    # 'https://www.betexplorer.com/soccer/norway/obos-ligaen/',
    # 'https://www.betexplorer.com/soccer/poland/ekstraklasa/',
    # 'https://www.betexplorer.com/soccer/scotland/premiership/',
    # 'https://www.betexplorer.com/soccer/scotland/championship/',
    # 'https://www.betexplorer.com/soccer/scotland/league-one/',
    # 'https://www.betexplorer.com/soccer/scotland/league-two/',
    # 'https://www.betexplorer.com/soccer/spain/laliga/',
    # 'https://www.betexplorer.com/soccer/spain/laliga2/',
    # 'https://www.betexplorer.com/soccer/sweden/allsvenskan/',
    # 'https://www.betexplorer.com/soccer/sweden/superettan/',
    # 'https://www.betexplorer.com/soccer/switzerland/super-league/',
    # 'https://www.betexplorer.com/soccer/usa/mls/',
    'https://www.betexplorer.com/tennis/atp-singles/next-gen-finals-milan/'
    ]

#send requests to different leagues
for url in urls:
    r = requests.get(url).text
    soup = bs(r,'html.parser')
    match_tables = soup.find('table', class_='table-main table-main--leaguefixtures h-mb15')
    try:
        matches = match_tables.find_all('a', class_='in-match')
    except:
        matches = ''
    if matches:
        for match in matches:
            fixture = 'https://www.betexplorer.com' + match.get('href')
            #use playwright to render javascript of each fixture page
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(fixture)
                try:
                    page.locator('div#match-results-home li.wrap-header__list__item.semilong').click()
                    page.locator("li.option").nth(2).click()
                    page.locator('div#match-results-away li.wrap-header__list__item.semilong').click()
                    page.locator("li.option").nth(2).click()
                    page.wait_for_load_state('domcontentloaded')
                except:
                    pass
                html = page.inner_html('div.columns')
                try:
                    page.locator("text=O/U").click()
                    try:
                        page.wait_for_load_state('domcontentloaded')
                        ou_html = page.inner_html('table#sortable-8 tfoot#match-add-to-selection')
                        ou_soup = bs(ou_html, 'html.parser')
                        if ou_soup:
                            over2_odds = ou_soup.find_all('td', class_='table-main__detail-odds')
                            over2 = float(over2_odds[0].text)
                            under2 = float(over2_odds[1].text)
                    except:
                        pass
                    #criteria7
                    if bb(draw_odds,over2):
                        criteria.append(criteria7)
                except:
                    pass
                wl_soup = bs(html, 'html.parser')
                #extracting the data
                try:
                    match = wl_soup.find('span', class_='list-breadcrumb__item__in').text.replace('-','vs')
                except:
                    match = ''
                try:
                    breadcrumbs = wl_soup.find_all('a', class_='list-breadcrumb__item__in')
                except:
                    breadcrumbs = ''
                if breadcrumbs:
                    sport = breadcrumbs[1].text
                    country = breadcrumbs[2].text
                    league = breadcrumbs[3].text
                try:
                    time_info = wl_soup.find('p', class_='list-details__item__date').text
                except:
                    pass
                if time_info:
                    date,time = time_info.split('-')
                try:
                    average_odds = wl_soup.find('tfoot',{'id':'match-add-to-selection'})
                    odds = average_odds.find_all('td', class_='table-main__detail-odds')
                    home_odds = float(odds[0].text)
                    draw_odds = float(odds[1].text)
                    away_odds = float(odds[2].text)
                    home_results = wl_soup.find('div', {'id':'match-results-home'})

                    if home_odds:
                        #criteria9
                        if league == 'Bundesliga 2022/2023' and country == 'Germany':
                            if home_odds > 2.7:
                                criteria.append(criteria9)
                    #criteria10
                    if away_odds:
                        if sport == 'Tennis':
                            if home_odds > 1.44 and away_odds > 1.94:
                                criteria.append(criteria10)
                except:
                    pass
                home_form = []
                try:
                    for i in  home_results.find_all('i'):
                        home_form_list = ''.join(i['class']).strip(), i.text
                        hfl = home_form_list[0]
                        other,hf = hfl.rsplit('_',1)
                        home_form.append(hf)
                except:
                    pass
                try:
                    away_results = wl_soup.find('div', {'id':'match-results-away'})
                    away_form = []
                    for i in  away_results.find_all('i'):
                        away_form_list = ''.join(i['class']).strip(), i.text
                        afl = away_form_list[0]
                        other,af = afl.rsplit('_',1)
                        away_form.append(af)
                except:
                    pass
                
                criteria = []
                if sport == 'Soccer':
                    if home_form:
                        #Criteria 1, 2, 3 and 4
                        if not 'w' in home_form[1:11] and home_form[0] == 'w':
                            criteria.append(criteria1)
                        if not 'w' in home_form[1:9] and home_form[0] == 'w':
                            criteria.append(criteria3)
                        if not 'l' in home_form[1:11] and home_form[0] == 'l':
                            criteria.append(criteria2)
                        if not 'l' in home_form[1:9] and home_form[0] == 'l':
                            criteria.append(criteria4)
                    if away_form:
                        if not 'w' in away_form[1:11] and away_form[0] == 'w':
                            criteria.append(criteria1)
                        if not 'w' in away_form[1:9] and away_form[0] == 'w':
                            criteria.append(criteria3)
                        if not 'l' in away_form[1:11] and away_form[0] == 'l':
                            criteria.append(criteria2)
                        if not 'l' in away_form[1:9] and away_form[0] == 'l':
                            criteria.append(criteria4)
                        
                    
                if criteria:
                    bets = {'Date':date,'Match':match,'League':league,'Strategy':criteria,'odd1':home_odds,'oddx':draw_odds,'odd2':away_odds,'odds over2.5':over2}
                    gc = gspread.service_account(filename='creds.json')
                    sh = gc.open('test').sheet1
                    sh.append_row([str(bets['Date']), str(bets['Match']), str(bets['League']), str(bets['Strategy']), float(bets['odd1']), float(bets['oddx']), float(bets['odd2']), float(bets['odds over2.5'])])

                    print(bets)


'''
wins_losses = ['w', 'l', 'l', 'l', 'd', 'l', 'l', 'l', 'd', 'l', 'l', 'l', 'd', 'd', 'd']

if not 'w' in wins_losses[1:12]:
    print("No wins in last 10 games!")
'''