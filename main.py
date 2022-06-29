import requests
import time
from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup as BS

ua = user_agent()
HEADERS = {'user-agent': ua,
           'accept': '*/*'}

URL = 'https://pikabu.ru/best'
start_time = time.time()


def get_my_data(html=None):
    all_stories = []
    soup = BS(html, 'html.parser')
    stories = soup.find(class_="stories-feed__container").find_all(class_="story__main")
    print(len(stories))
    one_story_data = {
        "news_id": None,
        "href": None,
        "author": None,
        "story_title": None,
        "story_block": None,
    }

    for story in stories:
        if story.find_all(class_="story-block_type_text") \
                and not story.find_all(class_="story-block_type_image") \
                and not story.find_all(class_="story-block_type_video"):
            one_story_data["news_id"] = story.get("data-story-id")
            one_story_data['href'] = story.find(class_="story__title").find("a").get("href")
            one_story_data["author"] = story.get("data-profile")
            one_story_data['story_title'] = story.find(class_="story__title").text
            one_story_data['story_block'] = story.find(class_="story-block_type_text").text
            all_stories.append(one_story_data)

    return all_stories


if __name__ == '__main__':
    r = requests.get(URL, headers=HEADERS)
    rez = get_my_data(r.text)
    print(rez)
