import requests
from bs4 import BeautifulSoup
import random

r = requests.get('https://robertsspaceindustries.com/community/devtracker')

soup = BeautifulSoup(r.text, 'html.parser')

time = soup.find_all('div', class_='devtracker-list')

devposts = {}

for tracker in time:
    topic = []
    urls = []
    post_time = []

    # get Threads URL
    links = tracker.find_all('a', class_='devpost')
    # get Threads age
    wrappers = tracker.find_all('div', class_='devpost-wrapper')

    for link, wrapper in zip(links, wrappers):
        ran = random.randrange(1,65340)
        title = wrapper.find('span', class_='thread').get_text()
        category = wrapper.find('span', class_='category').get_text()
        url = link.get('href')
        post_time = wrapper.find('span', class_='time').get_text()


        devposts[ran] = {
            'topic': title,
            'category': category,
            'urls': f'https://robertsspaceindustries.com{url}',
            'post_time': post_time,
        }

for k, v in devposts.items():
    print(f'{k} {v}\n')