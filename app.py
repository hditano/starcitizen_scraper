import requests
from bs4 import BeautifulSoup
import random
import sqlite3
import os

r = requests.get('https://robertsspaceindustries.com/community/devtracker')

soup = BeautifulSoup(r.text, 'html.parser')

time = soup.find_all('div', class_='devtracker-list')

devposts = {}



con = sqlite3.connect('database.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS tracker(topic, category, url, post_time)")

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

        existing_urls = [url[0] for url in cur.execute("SELECT url FROM tracker").fetchall()]


        if devposts[ran]['urls'] in existing_urls:
            print(f'URL already exists {existing_urls}')
        else:
            print(f'Adding url {devposts[ran]['urls']}')
            cur.execute("INSERT INTO tracker VALUES (?, ?, ?, ?)", (devposts[ran]['topic'], devposts[ran]['category'], devposts[ran]['urls'], devposts[ran]['post_time']))
            con.commit()


# for item in existing_urls:
#     if temp_url in item:
#         cur.execute("DELETE FROM tracker WHERE url = ?", (temp_url,))
#         con.commit()
#         print(f'{temp_url} deleted')

# for i in existing_urls:
#     if temp_url in i:
#         print(f'Value {temp_url} exists')
#         cur.execute("DELETE FROM tracker WHERE url = ?", (temp_url,))
#         con.commit()
#         print(f'Deleted')
#     else:
#         print(f'Doesnt exist')
