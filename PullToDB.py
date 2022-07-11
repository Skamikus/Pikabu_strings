import psycopg2
import db_conn
from psycopg2 import extras


def _initial_bd():
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
                """CREATE TABLE IF NOT EXISTS "Short_tales_category" (
                    id serial PRIMARY KEY,
                    title varchar(50));
                    CREATE TABLE IF NOT EXISTS "Short_tales_posts" (
                    id serial PRIMARY KEY,
                    story_id integer,
                    href varchar,
                    author varchar(100),
                    story_title varchar(255),
                    story_block text,
                    date_in TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    date_change TIMESTAMP,
                    posted bool DEFAULT True,
                    category_id integer REFERENCES "Short_tales_category" (id) ON DELETE SET NULL,
                    UNIQUE(story_id)
                    );
                """
            )
            connection.commit()
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO "Short_tales_category" (id, title) VALUES 
            (1, 'Свежее'),
            (2, 'Горячее'),
            (3, 'Лучшее')
            ON CONFLICT (id) DO NOTHING;  
            """)
            connection.commit()
            print("[INFO] BD exist now")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def _prepare_data(data):
    rezult = []
    for each in data:
        rezult.append(
            (each["news_id"], each["href"], each["author"], each["story_title"], each["story_block"], each["category"]))
    return rezult


def bd_insert(data: list[dict, ...]) -> None:
    posts = _prepare_data(data)
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
                              INSERT INTO "Short_tales_posts" (story_id, href, author, story_title, story_block, category_id)
                              VALUES %s ON CONFLICT DO NOTHING
                              """, posts
                              )
        connection.commit()
        cursor.close()
        print("[INFO] PostgreSQL work completed successfully")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            # print("[INFO] PostgreSQL connection closed")


if __name__ == '__main__':
    _initial_bd()
