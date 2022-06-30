import requests
import time
from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup as BS
import json

URL = 'https://pikabu.ru'
start_time = time.time()


def find_last_page(html=None):
    soup = BS(html, 'html.parser')
    return soup.find(class_="stories-feed").get("data-page-last")


def get_my_data(html=None):
    all_stories = []
    soup = BS(html, 'html.parser')
    stories = soup.find(class_="stories-feed__container").find_all(class_="story__main")
    # print(len(stories))
    # print(stories)
    one_story_data = {
        "news_id": None,
        "href": None,
        "author": None,
        "story_title": None,
        "story_block": None,
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
                one_story_data['story_block'] = story.find(class_="story-block_type_text").text
                all_stories.append(one_story_data)
    except Exception:
        print("Произошла ошибка при парсинге")
    return all_stories


def open_page(url: str = None, param: dict = None) -> str:
    ua = user_agent()
    headers = {'user-agent': ua,
               'accept': '*/*'}

    answer = requests.get(url, headers=headers, params=param)
    if answer.status_code != 200:
        raise ConnectionError
    # print(answer.text)
    return answer.text


def save_json_file(not_clean_data: list[dict, ...] = None) -> None:
    with open("result_not_clean.json", "w", encoding='utf-8') as file:
        json.dump(not_clean_data, file, indent=4, ensure_ascii=False)
    clean_data = []
    for elem in not_clean_data:
        if elem not in clean_data:
            clean_data.append(elem)
            print(elem)
            print("*" * 20)
    with open("result.json", "w", encoding='utf-8') as file:
        json.dump(list(clean_data), file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    all_text = []
    text = open_page(URL)
    last_page = int(find_last_page(text))
    print(last_page)
    for page in range(1, 50): #last_page):
        html_text = open_page(URL, {"page": page})
        all_text.extend(get_my_data(html_text))
        print(len(all_text))
    save_json_file(all_text)
    print(all_text)
