import requests
import time
from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup as BS
import json
import PullToDB
import asyncio, aiohttp, sys

URLS = {
    1: 'https://pikabu.ru/new',
    2: 'https://pikabu.ru',
    3: 'https://pikabu.ru/best',
}
start_time = time.time()
all_posts = []
ua = user_agent()


async def gather_data(url, last_page, category):
    tasks = []
    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as session:
        for page in range(1, last_page + 1):
            task = asyncio.create_task(get_page_data(session, url, page, category))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_data(session, url, page, category):
    headers = {'user-agent': ua,
               'accept': '*/*'}
    async with session.get(url=url, headers=headers, params={"page": page}) as response:
        response_text = await response.text()
    all_posts.extend(get_my_data(response_text, category))
    print("Page", page, "from category", category, "is ready")


def find_last_page(html=None):
    soup = BS(html, 'html.parser')
    return soup.find(class_="stories-feed").get("data-page-last")


def get_my_data(html=None, category=1):
    all_stories = []
    soup = BS(html, 'html.parser')
    try:
        stories = soup.find(class_="stories-feed__container").find_all(class_="story__main")
    except Exception as err:
        print("Произошла ошибка при парсинге", err)
    # print(len(stories))
    # print(stories)
    one_story_data = {
        "news_id": None,
        "href": None,
        "author": None,
        "story_title": None,
        "story_block": None,
        "category": None
    }
    try:
        for story in stories:
            if story.find_all(class_="story-block_type_text") \
                    and not story.find_all(class_="story-block_type_image") \
                    and not story.find_all(class_="story-block_type_video") \
                    and not story.find_all(class_="story__sponsor"):
                one_story_data["news_id"] = story.find(class_="story__footer").find(class_="story__tools") \
                    .find(class_="story__share").get("data-story-id")
                one_story_data['href'] = story.find(class_="story__title").find("a").get("href")
                one_story_data["author"] = story.find(class_="story__user-link user__nick").get("data-name")
                one_story_data['story_title'] = story.find(class_="story__title").text
                one_story_data['story_block'] = story.find(class_="story-block_type_text").get_text('\n')
                one_story_data["category"] = category
                all_stories.append(one_story_data)

    except Exception as err:
        print("Произошла ошибка при парсинге", err)
    return all_stories


def open_page(url: str = None, param: dict = None) -> str:
    headers = {'user-agent': ua,
               'accept': '*/*'}
    answer = requests.get(url, headers=headers, params=param)
    if answer.status_code != 200:
        raise ConnectionError
    return answer.text


def make_clean_data(not_clean_data: list[dict, ...] = None) -> list[dict, ...]:
    clean_data = []
    for elem in not_clean_data:
        if elem not in clean_data:
            clean_data.append(elem)
    return clean_data


def save_json_file(clean_data: list[dict, ...] = None, category: int = 1) -> None:
    filename = "result_" + str(category) + ".json"
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(list(clean_data), file, indent=4, ensure_ascii=False)


async def main():
    for category, url in URLS.items():
        print("Категория N -", category, "-", url)
        text = open_page(url)
        last_page = int(find_last_page(text))
        print("Max page is -", last_page)
        await gather_data(url, last_page, category)
        # print(len(all_posts))
    clean_text = make_clean_data(all_posts)
    save_json_file(clean_text, 'all')
    PullToDB.bd_insert(clean_text)
    print("Work takes at all this time:", time.time() - start_time)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
