from background_task import background
from .functions import quicket


@background(schedule=0)
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
            quicket(url, word,words)

