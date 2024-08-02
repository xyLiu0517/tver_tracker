from datetime import datetime
import time
import requests
import constants

url = "https://platform-api.tver.jp/service/api/v2/callSeries/{}"
payload = {
    "platform_uid": "c4014298f3424f4cb4a610a36f758a1afb2a",
    "platform_token": "2kbqrox4u743yqav49gqo8gzkbz3bn0o5tg9a30o",
    "require_data": "mylist[series][{}],later,good,resume",
}
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6",
    "Origin": "https://tver.jp",
    "Priority": "u=1, i",
    "Referer": "https://tver.jp/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0",
    "X-Tver-Platform-Type": "web"
}

db_file_path = './favorites_temp_db/fake_db_{}.txt'
time_interval = 60 * 30  # 30 minutes

def get_favorite_count():
    # request favorite count information every half an hour
    while (1):
        for id, _ in constants.id_to_drama_name.items():
            cur_payload = payload
            cur_payload['require_data'] = cur_payload['require_data'].format(id)
            response = requests.get(
                url.format(id), 
                params=cur_payload, 
                headers=headers
            )
            if response.status_code != 200:
                print('Error connecting to Tver. Status code: {}'.format(
                    response.status_code))
                continue
            else:
                print("Successfully connect to Tver")
                favorite_count = response.json()['result']['content']['favoriteCount']
                print("Favorite count: ", favorite_count)

                # Open fake db and write the favorite count
                db_file = open(db_file_path.format(id), 'a')
                db_file.write('Time: {}, favorites: {}\n'
                            .format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), favorite_count))
                db_file.close()

        time.sleep(time_interval)

def get_episode_good_count():
    pass


if __name__ == '__main__':
    get_favorite_count()
