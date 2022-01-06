import requests
import datetime
import time
import os
import sys

import cv2
import numpy as np
import torch

from torch.utils.data import Dataset, DataLoader
from torchvision.utils import make_grid, save_image

import matplotlib.pyplot as plt

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


class NFTDataset(Dataset):
    def __init__(self, root='data/'):
        self.data = []
        for img in os.listdir(root):
            self.data.append([os.path.join(root, img), 1])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, class_name = self.data[idx]
        pic = plt.imread(img_path) #[512, 512, 4]
        pic = cv2.resize(pic, (256, 256))

        pic_tensor = torch.from_numpy(pic)
        return pic_tensor
