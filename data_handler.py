import requests
import datetime
import time
import os
import sys

def API_request_Opensea(limit, data_folder):
    url = "https://api.opensea.io/api/v1/assets"
    counter = 0
    while(counter <= 10000):
        querystring = {"order_direction":"asc","offset":str(counter),"limit":str(limit),
                       'collection':'boredapeyachtclub'}
        response = requests.request("GET", url, params=querystring)

        if response.status_code==200:
            for key in response.json()['assets']:
                id = key['token_id']
                print('Downloading {}/10000'.format(id), end='\r')
                img_data = requests.get(key['image_url']).content
                save_path = os.path.join(data_folder, '{}.jpg'.format(id))

                with open(save_path, 'wb') as handler:
                    handler.write(img_data)
            counter += limit
        else:
            time.sleep(1)
            print('Downloading {}/10000 (sleeping...)'.format(counter), end='\r')

if __name__ == '__main__':
    API_request_Opensea(50, 'data/')
