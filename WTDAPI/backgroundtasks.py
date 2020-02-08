from background_task import background
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Bing




@background(schedule=60)
def scrapeQuicket():
    category_n = ['9', '13', '50', '61', '30', '12', '38', '62', '1', '63', '64', '2', '5']
    category_word = ['Arts & Culture', 'Business & Industry', 'Charity & Causes', 'Community',
                     'Family & Education', 'Food & Drink', 'Health & Wellness', 'Hobbies & Interests', 'Music',
                     'Occasion', 'Other', 'Science & Technology', 'Sports & Fitness']
    print(category_n[0])
    k = 0
    for word in category_word:
        print(k)
        for t in range(1, 3):
            url = 'https://www.quicket.com/events/south-africa/gauteng/' + str(t) + '/?categories=' + category_n[k]
            quicket(url, word)


def quicket(url, category):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    for event in soup.find_all("li"):
        title_elem = event.find('h3', class_='event-list-title')
        if title_elem:
            info_link = event.find('a', class_='image')
            image_link = event.find('img')
            company_elem = event.find('span', class_='text-inline')
            location_elem = event.find('div', class_='event-list-venue')
                # sleep(3)
            print(title_elem.text.strip())
            print(company_elem.text.strip())
            print(location_elem.text.strip())
            print(info_link.get('href'))
            print("https:" + image_link.get('src'))
            print(category)
