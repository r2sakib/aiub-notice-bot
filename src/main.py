# python 3.11.4

import requests
from bs4 import BeautifulSoup
from time import sleep
import bot

BASE_URL = 'https://www.aiub.edu/category/notices'
NOTICE_BASE_URL = 'https://www.aiub.edu'


def get_notices(html: str) -> list:
    """
    Extracts notice links from the HTML content of a AIUB webpage.

    Args:
        html (str): The HTML content of the webpage.

    Returns:
        list: A tuple containing two lists 
            - a list of notice links extracted from the HTML content and a list of corresponding notice titles.
    """
    soup = BeautifulSoup(html, 'html.parser')
    list_of_notices = soup.find('ul', class_='event-list')    
    list_of_links = list_of_notices.find_all('a', class_='info-link')
    list_of_titles = list_of_notices.find_all('h2', class_='title')

    links = []
    for a in list_of_links:
        links.append(a['href'])
    
    titles = []
    for a in list_of_titles:
        titles.append(a.text.strip())

    return (links, titles)


def check_new_notices(notices: tuple, new_notices: tuple) -> None:
    """
    Check for new notices and send a message if there are any.

    Args:
        notices (tuple): A tuple containing two lists, links and titles, of the old notices.
        new_notices (tuple): A tuple containing two lists, new_links and new_titles, of the new notices.

    Returns:
        None
    """
    links, titles = notices[0], notices[1]
    new_links, new_titles = new_notices[0], new_notices[1]

    if links != new_links:
        for i in range(len(new_links)-1):
            if new_links[i] not in links:
                message: str = bot.notice_message_formatter(new_titles[i], NOTICE_BASE_URL + new_links[i])
                bot.send_notice_message(message)
        return True


def main():
    """
    This function continuously checks the AIUB website for new notices every 60 seconds.
    If new notices are found, it calls the check_new_notices function send them to Telegram channel and prints logs to console.
    """
    html = requests.get(BASE_URL).text
    notices: tuple = get_notices(html)

    while True:
        new_html = requests.get(BASE_URL).text
        new_notices: tuple = get_notices(new_html)

        found_new_notices = check_new_notices(notices, new_notices)
        if found_new_notices:
            notices = new_notices
        
        print(f'Found new notices: {found_new_notices}\n {notices}')

        sleep(60)


if __name__ == '__main__':
    main()
