import datetime
import logging
import main
import concurrent.futures


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def process_url(url):
    # Remove leading/trailing whitespace and newline characters
    url = url.strip()
    response_data = main.get_response_data(url)
    place_name = main.get_place_name(response_data)
    main.scrap_data(response_data, place_name, url)


def run(event, context):
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    MAX_THREADS = 5

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_url, urls)

    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
