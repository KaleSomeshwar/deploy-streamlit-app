"""Google images visualisation application, Developed using Streamlit library."""

import streamlit as st

from google_image_downloader import get_resized_images


def main():
    """Google image visualiser."""
    st.set_page_config(layout="wide")
    refresh = st.sidebar.button('Refresh')
    query = st.sidebar.text_input('Memes', 'wow')
    query += ' memes'

    st.markdown(query)

    images = get_resized_images(str(query), refresh)

    st.image(images, width=300)


if __name__ == '__main__':
    main()
