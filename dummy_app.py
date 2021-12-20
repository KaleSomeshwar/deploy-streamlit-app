""" Main function for the frame navigator application, Developed using Streamlit library """
import os
import streamlit as st

def main():

    st.sidebar.selectbox("Task", ["A", "B"])


if __name__ == '__main__':
    main()

