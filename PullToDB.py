import psycopg2
import db_conn

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
                    posted bool DEFAULT False
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


def bd_insert():
    pass


if __name__ == '__main__':
    initial_bd()