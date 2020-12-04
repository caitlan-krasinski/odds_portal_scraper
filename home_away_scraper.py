from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


#Home/Away scrape
data = []
count = 0
#open website
driver.get('https://www.oddsportal.com/hockey/usa/nhl/results/#/page/1')
y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-main')))
table = driver.find_element_by_class_name('table-main')
rows = table.find_elements_by_tag_name('tr')
season = '2019/2020'

pages = driver.find_element_by_id('pagination')
for j in range(len(pages)):
    driver.get('https://www.oddsportal.com/hockey/usa/nhl/results/#/page/'+ str(j))
    y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-main')))
    table = driver.find_element_by_class_name('table-main')
    rows = table.find_elements_by_tag_name('tr')
    season = '2019/2020'
    
    
    for i in range(len(rows)):
        try:
            if ('#/page/'+ str(j)) in str(driver.current_url):
                #all rows in table
                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-main')))
                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'tournamentTable')))
                table = driver.find_element_by_class_name('table-main')
                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'tr')))
                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-dummyrow')))
                rowsx = driver.find_elements_by_tag_name('tr')
                rows2 = rowsx[i]
                
                #only want rows that have link
                if (rows2.get_attribute('class') == 'odd deactivate') or (rows2.get_attribute('class') == ' deactivate'):
                    count = count+1
                    col = rows2.find_elements_by_tag_name('td')[1]
                    #click link to view game
                    y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'a')))
                    link = col.find_elements_by_tag_name('a')[0].click()
                    
                    if str(driver.current_url) != 'https://www.oddsportal.com/hockey/usa/nhl-2016-2017/results/#/page/'+ str(j) +'/' :
                        y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'odds-data-table')))
                        y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'tbody')))
                        y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ul-nav')))
                        y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="bettype-tabs"]/ul')))
                        #navigate to home/away tab
                        tab = driver.find_elements_by_xpath('//*[@id="bettype-tabs"]/ul')
                        tab = driver.find_elements_by_class_name('ul-nav')[0]
                        y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="bettype-tabs"]/ul/li[3]/a')))
                        y = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="bettype-tabs"]/ul/li[3]/a')))
                        if len(tab.find_elements_by_xpath('//*[@id="bettype-tabs"]/ul/li[3]/a')) > 0:
                            tab.find_elements_by_xpath('//*[@id="bettype-tabs"]/ul/li[3]/a')[0].click()
                        
                        if "#home-" in str(driver.current_url):
                            #scrape
                            
                            y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-container')))
                            bookmakers = driver.find_elements_by_tag_name('tr')
                            date = driver.find_elements_by_tag_name('p')[1].text
                            game = driver.find_elements_by_tag_name('h1')[0].text.split('-') #split by - to get each team
                            team1 = game[0]
                            team2 = game[1]
                            bet_type = driver.find_elements_by_class_name('active')[2].text
                            print(j, count, date, team1, team2, bet_type)
                            
                            #get data for each bookmaker
                            for x in bookmakers:
                                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'table-container')))
                                y = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'name')))
                                colx = x.find_elements_by_class_name('name')
                                one = x.find_elements_by_tag_name('div')
                                if len(one)>2 and len(colx)>0:
                                    if(colx[0].text == ''):
                                        break
                                    else: 
                                        payout = x.find_elements_by_class_name('center')[0].text
                                        bookmaker = colx[0].text
                                        
                                        #navigate to location to initiate first popup window on hover
                                        hov = ActionChains(driver).move_to_element(one[1])
                                        hov.perform()
                                        if len(x.find_elements_by_xpath("//*[@id='tooltiptext']/strong")) == 2: 
                                            open_odd1 = x.find_element_by_xpath("//*[@id='tooltiptext']/strong[2]").text
                                            close_odd1 = one[1].text
                                        else:
                                            open_odd1 = one[1].text
                                            close_odd1 = float('nan')

                                        #navigate to location to initiate second popup window on hover
                                        hov = ActionChains(driver).move_to_element(one[2])
                                        hov.perform()
                                        if len(x.find_elements_by_xpath("//*[@id='tooltiptext']/strong")) == 2: 
                                            open_odd2 = x.find_element_by_xpath("//*[@id='tooltiptext']/strong[2]").text
                                            close_odd2 = one[2].text
                                        else:
                                            open_odd2 = one[2].text
                                            close_odd2 = float('nan')

                                        r = [j, season, date, bet_type, team1, team2, bookmaker, open_odd1, close_odd1,  open_odd2, close_odd2, payout] 
                                        data2.append(r)


                driver.get('https://www.oddsportal.com/hockey/usa/nhl/results/#/page/'+ str(j))
        except:
            print('error')
            continue
            
            
            
f = 'home_away.csv'
col_names = ['page number', 'season', 'date', 'bet_type', 'team1', 'team2', 'bookmaker', 'open_odd1', 'close_odd1',  'open_odd2', 'close_odd2', 'payout']

with open(f, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(col_names)
    writer.writerows(data2)
