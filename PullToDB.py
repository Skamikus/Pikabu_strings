import psycopg2
import db_conn
from psycopg2 import extras

def initial_bd():
    try:
        connection = psycopg2.connect(
            host=db_conn.host,
            user=db_conn.user,
            password=db_conn.password,
            database=db_conn.db,
        )

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"Server version - {cursor.fetchone()}")

        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Posts(
                    id serial PRIMARY KEY,
                    story_id integer,
                    href varchar,
                    author varchar(100),
                    story_title varchar(255),
                    story_block text,
                    date_in TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    date_change TIMESTAMP,
                    posted bool DEFAULT False,
                    UNIQUE(story_id)
                );              
                """
            )
            connection.commit()
            print("[INFO] BD exist now")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def prepare_data(data):
    rezult = []
    for each in data:
        rezult.append((each["news_id"], each["href"], each["author"], each["story_title"], each["story_block"]))
    return rezult


def bd_insert(data):
    posts = prepare_data(data)
    try:
        connection = psycopg2.connect(
            host=db_conn.host,
            user=db_conn.user,
            password=db_conn.password,
            database=db_conn.db,
        )
        cursor = connection.cursor()
        extras.execute_values(cursor,
            """
            INSERT INTO Posts (story_id, href, author, story_title, story_block)
            VALUES %s ON CONFLICT DO NOTHING
            """, posts
        )
        connection.commit()
        cursor.close()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

if __name__ == '__main__':
    initial_bd()
    # was = [
    # {
    #     "news_id": "9234356",
    #     "href": "https://pikabu.ru/story/rossiya_snova_grubo_narushila__spektakl_v_dvukh_deystviyakh_9234356",
    #     "author": "zigfrid.n",
    #     "story_title": "\"Россия снова грубо нарушила!\" - спектакль в двух ",
    #     "story_block": "Действие первое - Россия принимает" },
    # {
    #     "news_id": "9234356",
    #     "href": "https://pikabu.ru/story/listaya_staryie_stranitsyi__9231788",
    #     "author": "deputy2022",
    #     "story_title": "Листая старые страницы ...",
    #     "story_block": "- Мама, а слон в зоопарке чей?- Государственный.- Значит и мой немножечко."
    # },]
    # # print(prepare_data(was))
    # bd_insert(was)