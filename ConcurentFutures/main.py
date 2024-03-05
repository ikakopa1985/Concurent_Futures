import concurrent.futures
import requests
import time
import json

start = time.perf_counter()

base_url = 'https://dummyjson.com/products/'
n = 100
processNumber = 8
thead = 20

th = []
threadPoolRunResults = []
processPools = []
processPoolsResults = []

urls_list = [base_url + str(item) for item in range(1, n)]


def request_url(url):
    response = requests.get(url)
    response_text = response.content.decode('utf-8')
    return json.loads(response_text)


def thread_pool_run(pp):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadPoolRunResults.append(list(executor.map(request_url, urls_list[(pp * thead):((pp * thead) + thead)])))
    return threadPoolRunResults


def process_pools_run():
    final_result = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pp in range(0, processNumber):
            processPools.append(executor.submit(thread_pool_run, pp))
        for pp in range(0, processNumber):
            final_result = final_result + (processPools[pp].result())
    with open('response.json', 'w') as json_file:
        json.dump(final_result, json_file, indent=4)
    finish = time.perf_counter()
    print(f'Done!  in  {finish - start}s', end=' ')


if __name__ == '__main__':
    process_pools_run()
