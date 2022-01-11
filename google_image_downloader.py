"""Google images downloading functions."""

import glob
import json
import random
import re
import urllib
from pathlib import Path

import requests
import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582 '
}


@st.cache(allow_output_mutation=True)
def get_matched_data(query='minecraft shaders 8k photo'):
    """Return matching data to the query."""
    params = {"q": query, "tbm": "isch", "ijn": "0", }
    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    all_script_tags = soup.select('script')
    # https://regex101.com/r/48UZhY/6
    matched_data = ''.join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>",
                                      str(all_script_tags)))
    matched_data = json.dumps(matched_data)
    matched_data = json.loads(matched_data)

    # https://regex101.com/r/pdZOnW/3
    matched_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",',
                              matched_data)

    matched_data_without_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '',
        str(matched_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                matched_data_without_thumbnails)

    return matched_images


def get_images_data(query, refresh):
    """Save a random image from suggested images."""
    matched_images = get_matched_data(query)
    Path(f'temp_images').mkdir(parents=True, exist_ok=True)

    if refresh:
        random.shuffle(matched_images)

    for index, image in enumerate(matched_images[:10]):
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        image = bytes(image, 'ascii').decode('unicode-escape')
        image = bytes(image, 'ascii').decode('unicode-escape')  # to fix the image

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', headers['User-Agent'])]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(image, f'temp_images/image_{index:02}.jpg')

    images = sorted(glob.glob('temp_images' + '/*.jpg'))
    resized_images = []

    for image in images:
        try:
            img = Image.open(image)
        except:
            continue
        resized_images.append(img)
    return resized_images


if __name__ == '__main__':
    QUERY = 'wow'
    _ = get_images_data(QUERY, False)
