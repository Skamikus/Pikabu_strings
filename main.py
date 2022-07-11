import requests
import time
from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup as BS
import json
import PullToDB

URLS = {1: 'https://pikabu.ru/new',
        2: 'https://pikabu.ru',
        3: 'https://pikabu.ru/best',
        }
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
                one_story_data['story_block'] = story.find(class_="story-block_type_text").get_text('\n')
                all_stories.append(one_story_data)
    except Exception as err:
        print("Произошла ошибка при парсинге", err)
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


def make_clean_data(not_clean_data: list[dict, ...] = None) -> list[dict, ...]:
    clean_data = []
    for elem in not_clean_data:
        if elem not in clean_data:
            clean_data.append(elem)
            # print(elem)
            # print("*" * 20)
    return clean_data

def save_json_file(clean_data: list[dict, ...] = None, category: int = 1) -> None:
    filename = "result_"+ str(category)+ ".json"
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(list(clean_data), file, indent=4, ensure_ascii=False)

def main():
    for category, url in URLS.items():
        all_text = []
        print("Категория N -", category, " - ", url)
        text = open_page(url)
        last_page = int(find_last_page(text))
        print("Max page is -", last_page)
        for page in range(30, 50):
            html_text = open_page(url, {"page": page})
            all_text.extend(get_my_data(html_text))
            print("page =", page, "posts taken =", len(all_text))
        clean_text = make_clean_data(all_text)
        save_json_file(clean_text, category)
        PullToDB.bd_insert(clean_text, category)
        # print(all_text)


if __name__ == '__main__':
    main()


