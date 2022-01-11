#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# here --server.port needs to use same port that is forwarded in terminal and while
# running/creating the docker container, here 8501 port is forwarded.
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
