from bs4 import BeautifulSoup
import requests


def parse(url):
    response = requests.get(url)
    return response


def parse_pull_requests(url):
    soup = BeautifulSoup(parse(url).content, 'html.parser')
    names = soup.findAll('td', class_='uname-cell')
    currely = soup.findAll('td', class_='uvalue-cell')

    for item in names:
        print(item.find('a', class_='uname').get_text(strip=True))
    print(len(names))

    for cur in currely:
        print(cur.get_text())
    print(len(currely))

    #
    # pull_requests_list = []
    #
    # for item in items:
    #     soup = BeautifulSoup(parse('https://github.com' + item.get('href')).content, 'html.parser')
    #
    #     reviewers = soup.find('form', class_='js-issue-sidebar-form').findAll('span', class_='css-truncate-target')
    #     assignees = soup.find('span', class_='css-truncate js-issue-assignees').get_text(strip=True)
    #
    #     reviewers_str = ''
    #     for reviewer in reviewers:
    #         reviewers_str += f'{reviewer.get_text(strip=True)}, '
    #
    #     pull_requests_list.append({
    #         'title': item.get_text(strip=True),
    #         'link': f'https://github.com/{item.get("href")}',
    #         'reviewers': reviewers_str,
    #         'assignees': assignees
    #
    #     })
    # return pull_requests_list
    #
parse_pull_requests('https://www.convert-me.com/ru/convert/currency/USD.html?u=USD&v=1')
def is_valid(url):
    return True if parse(url).status_code == 200 else False