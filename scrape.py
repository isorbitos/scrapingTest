import requests
from bs4 import BeautifulSoup
import pprint

def scan_pages(count):
    target_web = "https://news.ycombinator.com/"
    res = requests.get(target_web +'newest')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    for x in range(count):
        href = soup.select('.morelink')[0].get('href')
        print(href)
        nex_target = target_web +href
        print(nex_target)
        res = requests.get(nex_target)
        soup = BeautifulSoup(res.text, 'html.parser')
        links.extend(soup.select('.storylink'))
        subtext.extend(soup.select('.subtext'))

    return (links, subtext)

# print(soup.select('.morelink'))

def sort_stories_by_votes(hn):
    return list(reversed(sorted(hn, key=lambda item: item['votes'])))

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().split()[0])
            if points > 2:
                hn.append({'title': title, 'link':href, 'votes':points})
    return sort_stories_by_votes(hn)

my_reluts = scan_pages(2)

# print(my_reluts[1])

pprint.pprint(create_custom_hn(my_reluts[0], my_reluts[1]))