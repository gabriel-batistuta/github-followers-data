from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
class User:
    def __init__(self, params:dict):
        self.username = params['username']
        self.name = params['name']
        self.company = params['company']
        self.github_url = params['github_url']
        self.location = params['location']
        self.img = params['img']
        self.description = params['description']

def get_soup(link):
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get(link)

    content = driver.page_source

    if not content:
        raise Exception("bad request, {0}".format(content.status_code))
    else:
        return BeautifulSoup(content, 'html.parser')
    
def get_followers(link):

    followers = []

    site = get_soup(f'{link}?tab=followers')
    div = site.find_all('div', attrs={'class':'Layout-main'})
    div = div[1]
    div_all_folowers = div.find('div', attrs={'class':'position-relative'})
    div_all_folowers = div_all_folowers.find_all('div', attrs={'class':'d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted'})
    
    for div_follower in div_all_folowers:
        img = div_follower.find('img', attrs={'class':'avatar avatar-user'})['href']

        div_username = div_follower.find('a', attrs={'class':'d-inline-block no-underline mb-1'})
        github_url = 'https://github.com' + div_username['href']
        name = div_username.find('span', attrs={'class':'f4 Link--primary'}).text
        username = div_username.find('span', attrs={'class':'Link--secondary pl-1'}).text

        description = div_follower.find('div', attrs={'class':'color-fg-muted text-small mb-2'}).text

        company_div = div_follower.find('p', attrs={'class':'color-fg-muted text-small mb-0'})
        company = company_div.find('span', attrs={'class':'mr-3'}).text
        location = company_div.text.replace(company, '').strip()

        params = {
            'username': username,
            'name': name,
            'description': description,
            'company': company,
            'location':location,
            'img':img, 
            'github_url':github_url
        }

        user = User(params)
        followers.append(user)

    return followers

def write_followers_json(followers, profile):
    username = profile.replace('https://github.com')
    dct = {
        f'{username} followers': followers
    }

    with open('followers.json', 'w') as file:
        json.dump(dct, file, indent=4)