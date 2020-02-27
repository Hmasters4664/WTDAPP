import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Bing
from time import sleep
from .models import Event
import re
from datetime import datetime
from .serializers import EventSerializer


def quicket(url, category,prov):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    for event in soup.find_all("li"):
        title_elem = event.find('h3', class_='event-list-title')
        if title_elem:
            info_link = event.find('a', class_='image')
            image_link = event.find('img')
            company_elem = event.find('span', class_='text-inline')
            location_elem = event.find('div', class_='event-list-venue')
            print(title_elem.text.strip())
            print(company_elem.text.strip())
            dt = date(company_elem.text.strip())
            print(location_elem.text.strip())
            print(info_link.get('href'))
            print("https:" + image_link.get('src'))
            print(category)
            event = Event(title=title_elem.text.strip(), date_string=company_elem.text.strip()
                          , info_link=info_link.get('href'), image_link="https:" + image_link.get('src'),
                          location=location_elem.text.strip(), province=prov, category=category, dates=dt)
            event.save()
            sleep(1)


def scrapeQuicket(words):
    category_n = ['9', '13', '50', '61', '30', '12', '38', '62', '1', '63', '64', '2', '5']
    category_word = ['Arts & Culture', 'Business & Industry', 'Charity & Causes', 'Community',
                     'Family & Education', 'Food & Drink', 'Health & Wellness', 'Hobbies & Interests', 'Music',
                     'Occasion', 'Other', 'Science & Technology', 'Sports & Fitness']
    print(category_n[0])
    k = 0
    for word in category_word:
        print(k)
        for t in range(1, 3):
            url = 'https://www.quicket.com/events/south-africa/'+words+'/' + str(t) + '/?categories=' + category_n[k]
            print(url)
            quicket(url, word,words)


def date(string):
    p = string.split(' ')
    now = datetime.now()
    if (p[0] != 'Runs'):
        p[1] = re.sub('\D', '', p[1])
        strz = p[2] + ' ' + p[1] + ' ' + p[3]
        #print(strz)
        datetime_object = datetime.strptime(strz, '%b %d %Y')
        #print(datetime_object)
    else:
        dt = p[3] + ' ' + p[2] + ' ' + str(now.year)
        datetime_object = datetime.strptime(dt, '%b %d %Y')
        #print(datetime_object)
    return datetime_object

