import sys
import time
import random
import json
import asyncio
import aiohttp
import undetected_chromedriver
import requests

from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup as BS
from typing import Union
from multiprocessing import freeze_support

import PullToDB

URLS = {
    1: 'https://pikabu.ru/new',
    2: 'https://pikabu.ru',
    3: 'https://pikabu.ru/best',
}
WAS_ASYNC_PARSING = True
ua = user_agent()
HEADERS = {
    'user-agent': ua,
    'accept': '*/*',
}

# For future challenges
# your_proxy_url = {
#     'http': 'http://5.188.136.52:8080',
#     'https': 'https://84.204.40.154:8080',
#
# }

Posts_type = list[dict[str, Union[str, int]]]
all_posts: Posts_type = []


async def gather_each_category_data(url: str, last_page: int = 1, category: int = 1) -> None:
    """Creating and collecting tasks for a separate category with their execution in a separate function"""
    tasks = []
    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as session:
        for page in range(1, last_page + 1):
            task = asyncio.create_task(get_data_from_single_page(session, url, page, category))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_data_from_single_page(session: aiohttp.ClientSession, url: str, page: int, category: int):
    """Getting information from each page and sending it to parsing to extract data"""
    async with session.get(url=url, headers=HEADERS, params={'page': page}) as response:
        print(response.status)
        response_text = await response.text()
    all_posts.extend(parse_data_from_page(response_text, category))
    print(f'[INFO] Page {page}, from category {category} was parsed, posts at all = {len(all_posts)}')


def parse_data_from_page(html: str = '', category: int = 1) -> Posts_type:
    """ Extracting data from html response"""
    soup = BS(html, 'html.parser')
    try:
        stories = soup.find(class_='stories-feed__container').find_all(class_='story__main')
    except Exception as err:
        print('[ERROR] An error occurred while parsing, no page', err)
    one_story_data = {}
    stories_from_page = []
    try:
        for story in stories:
            if story.find_all(class_='story-block_type_text') \
                    and not story.find_all(class_='story-block_type_image') \
                    and not story.find_all(class_='story-block_type_video') \
                    and not story.find_all(class_='story__sponsor'):
                one_story_data['news_id'] = story.find(class_='story__footer') \
                    .find(class_='story__tools') \
                    .find(class_='story__share') \
                    .get('data-story-id')
                one_story_data['href'] = story.find(class_='story__title') \
                    .find('a').get('href')
                one_story_data['author'] = story.find(class_='story__user-link user__nick') \
                    .get('data-name')
                one_story_data['story_title'] = story.find(class_='story__title') \
                    .find(class_='story__title-link').text
                one_story_data['story_block'] = story.find(class_='story-block_type_text').get_text('\n')
                one_story_data['category'] = category

                stories_from_page.append(one_story_data)

    except Exception as err:
        print('[ERROR] An error occurred while parsing', err)
    return stories_from_page


def open_page_by_url(url: str = None) -> int:
    """Page opening"""
    answer = requests.get(url, headers=HEADERS)
    if answer.status_code != 200:
        raise ConnectionError(answer.status_code)
    return open_page_by_url(answer.text)


def find_last_page(html: str = None) -> int:
    """Search for the last page in a category"""
    soup = BS(html, 'html.parser')
    return int(soup.find(class_='stories-feed').get('data-page-last'))


def cleaned_from_duplicates_data(not_clean_data: Posts_type) -> Posts_type:
    """Elimination of duplicates in records, because pagination of the site works according to a separate logic.
     It is much easier and faster for me to remove duplicate records. """
    clean_data = []
    for elem in not_clean_data:
        if elem not in clean_data:
            clean_data.append(elem)
    return clean_data


def save_json_file(clean_data: Posts_type = None, category: Union[int, str] = 1, action: str = 'w') -> None:
    filename = f'result_{category}.json'
    with open(filename, action, encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


async def collect_all_data_from_Pikabu() -> None:
    """Pass through all categories with the collection of "raw" data"""
    for category, url in URLS.items():
        print(f'[INFO] Try to open category N - {category} from page: {url}')
        try:
            category_last_page = open_page_by_url(url)
            print(f'[INFO] Max page is - {category_last_page}')
            await gather_each_category_data(url, category_last_page, category)
        except:
            print('[ERROR] Try to opening the site due to protection against ddos attacks')
            WAS_ASYNC_PARSING = False
            parsing_with_chromedriver()
            break


def save_data_from_webdriver(driver=None, sleep: int = 2):
    """Saving data every 100 pages or when errors occur"""
    driver_need = True if driver else False
    if driver_need:
        driver_quit(driver)
    clean_data = cleaned_from_duplicates_data(all_posts)
    save_json_file(clean_data, 'all', 'a')
    PullToDB.insert_into_BD_data(clean_data)
    all_posts.clear()
    time.sleep(sleep)
    driver = get_webdriver() if driver_need else None
    print('[INFO] Posts and web cache was cleared')
    return driver


def get_data_from_category_with_webdriver(category_last_page: int, url: str, category: int):
    """" Collection using the webdriver of all information from the category page by page"""
    driver = get_webdriver()
    for page in range(1, category_last_page + 1):
        try:
            driver.get(f'{url}/?page={page}')
            all_posts.extend(parse_data_from_page(driver.page_source, category))
            if page % 100 == 0:
                driver = save_data_from_webdriver(driver)
            print(f'[INFO] Page {page}, from category {category} was parsed, collected posts = {len(all_posts)}')
        except Exception as ex:
            driver = save_data_from_webdriver(driver, 20)
            print('[ERROR] Timed out from renderer, restart driver {ex}')
    save_data_from_webdriver()
    driver_quit(driver)


def driver_quit(driver):
    """My function for correct Chromedriver stop and quit """
    if driver:
        try:
            driver.close()
        except Exception:
            print('[ERROR] Webdriver was stuck, QUIT only')
        finally:
            driver.quit()
        driver.quit()

def get_webdriver():
    """Getting new Chromedriver"""
    options = undetected_chromedriver.ChromeOptions()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = undetected_chromedriver.Chrome(options=options)
    driver.set_script_timeout(60)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(2)
    return driver


def parsing_with_chromedriver():
    """Pass through all categories with the collection of "raw" data with Chromedriver"""
    for category, url in URLS.items():
        print(f'[INFO] Try to open, with chromedriver, category N - {category} from page: {url}')
        try:
            driver = get_webdriver()
            driver.get(url)
            # time.sleep(3)
            category_last_page = find_last_page(driver.page_source)
            print(f'[INFO] Max page is - {category_last_page}')
            driver_quit(driver)
            get_data_from_category_with_webdriver(category_last_page, url, category)
        except Exception as ex:
            print(f'[ERROR] Error opening Category {ex}')
            driver_quit(driver)
            driver = get_webdriver()
    driver_quit(driver)


def main():
    start_time = time.time()
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(collect_all_data_from_Pikabu())
    if WAS_ASYNC_PARSING:
        clean_data = cleaned_from_duplicates_data(all_posts)
        save_json_file(clean_data, 'all')
        PullToDB.insert_into_BD_data(clean_data)
    print(f'[INFO] Work takes time: {time.time() - start_time}')


if __name__ == '__main__':
    freeze_support()
    main()

# Timed out receiving message from renderer: 300.000
