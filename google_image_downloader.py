"""Google images downloading functions."""

import glob
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
def download_images(query='minecraft shaders 8k photo'):
    """Return matching data to the query."""
    html = requests.get(f"https://www.google.com/search?tbm=isch&q={query}",
                        headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    images = soup.find_all('img')
    image_urls = []
    for image in images:
        src = image.get('src')
        image_urls.append(src)
    urls_without_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '',
        str(image_urls))
    urls_without_thumbnails = urls_without_thumbnails.replace("'", '').split(',')
    urls_without_thumbnails = [url for url in urls_without_thumbnails if not url.endswith('.gif')]
    return urls_without_thumbnails


def get_resized_images(query, refresh):
    """Save a random image from suggested images."""
    matched_images = download_images(query)
    Path(f'temp_images').mkdir(parents=True, exist_ok=True)

    if refresh:
        random.shuffle(matched_images)

    for index, image in enumerate(matched_images[:10]):
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
    _ = get_resized_images(QUERY, False)
