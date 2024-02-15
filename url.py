import concurrent.futures
import main
import time

def process_url(url):
    url = url.strip()
    response_data = main.get_response_data(url)
    place_name = main.get_place_name(response_data)
    main.scrap_data(response_data, place_name, url)

def run():
    start = time.time()
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    MAX_THREADS = 5

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_url, urls)
    
    end = time.time()
    print("time: ", (end - start))

run()