import urllib3
import re
import time
import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)

start = time.time()

def create_table(conn, cur):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS reviews2 (
        id SERIAL PRIMARY KEY,
        place_name VARCHAR(300),
        name VARCHAR(300),
        profile VARCHAR(300),
        rating SMALLINT,
        review TEXT
    );
    """
    cur.execute(create_table_query)
    conn.commit()

def get_response_data(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return response.data.decode('utf-8')

def get_next_request(response_data):
    pattern = r'(\w+)(\\u003d\\u003d|\\u003d)\"\]\]\]'
    matches = re.findall(pattern, response_data)

    if not matches:
        return None
    return matches[0][0]

def change_request(response_data, url):
    pattern = r'2s(.*?)!'
    next_xhr = get_next_request(response_data)
    new_url = re.sub(pattern, f'2s{next_xhr}!', url)
    new_response = get_response_data(new_url)
    return new_response

def get_ratings(response_data):
    pattern = r'\[\[[1-5]\]\]\,\[n|\[\[[1-5]\]\,n|\[\[[1-5]\]\,\[\"|\[\[[1-5]\]\]\,\[\[\"'
    matches = re.findall(pattern, response_data)

    return [match[2] for match in matches]

def get_reviews(response_data):
    pattern = r'\[\[[1-5]\],\[".*?"|\[\[[1-5]\]\],\[null|\[\[[1-5]\],null|\[\[[1-5]\]\]\,\[\[\"'
    matches = re.findall(pattern, response_data)

    for i in range(len(matches)):
        if ",[null" in matches[i]: 
            matches[i] = ''
        elif "],null" in matches[i]:
            matches[i] = ''
        matches[i] = re.sub(r'\[\[[1-5]\],\["', '', matches[i])
        matches[i] = re.sub(r'\[\[[1-5]\]\]\,\[\[\"', '', matches[i])
        matches[i] = matches[i][0:-1]

    return matches

def get_names(response_data):
    pattern = r'br100","[^"]+","https'
    matches = re.findall(pattern, response_data)

    for i in range(len(matches)):
        matches[i] = matches[i].replace('br100","', '')
        matches[i] = matches[i].replace('","https', '')

    return matches

def get_profiles(response_data):
    pattern = r'https://www\.google\.com/maps/contrib/[0-9]+/reviews\?hl\\u003dpt-BR|https://www\.google\.com/maps/contrib/[0-9]+/reviews\?hl\\u003den'
    return re.findall(pattern, response_data)

def get_place_name(response_data):
    pattern = r'[^"]*","pt"\]\],\[|[^"]*","en"\]\],\['
    matches = re.findall(pattern, response_data)
    if('","pt"]],[' in matches[0]):
        matches[0] = matches[0].replace('","pt"]],[', '')
    elif('","en"]],[' in matches[0]):
        matches[0] = matches[0].replace('","en"]],[', '')

    return matches[0]


def scrap_data(response_data, place_name, url):
    conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    create_table(conn, cur)
    iter_count = 1

    while True:
        print(iter_count)
        names = get_names(response_data)
        profiles = get_profiles(response_data)
        numbers = get_ratings(response_data)
        reviews = get_reviews(response_data)

        for i in range(len(names)):
            cur.execute("""
            SELECT COUNT(*) FROM reviews2 
            WHERE place_name = %s AND name = %s AND profile = %s AND rating = %s AND review = %s
            """, (place_name, names[i], profiles[i], numbers[i], reviews[i]))
            count = cur.fetchone()[0]

            if count == 0:
                cur.execute("""
                    INSERT INTO reviews (place_name, name, profile, rating, review)
                    VALUES (%s, %s, %s, %s, %s)
                """, (place_name, names[i], profiles[i], numbers[i], reviews[i]))


        if not get_next_request(response_data):
            break

        response_data = change_request(response_data, url)
        iter_count += 1

    conn.commit()
    cur.close()
    conn.close()


end = time.time()
print("Time: ", (end - start))
