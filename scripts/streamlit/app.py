import requests
import streamlit as st
from streamlit_option_menu import option_menu
import json
import time
from scripts import (make_video_details_comments, 
                     push_to_mongodb, 
                     check_if_exists)

# page configurations
st.set_page_config(
    page_title = "youtube data", 
    page_icon = ":bar_chart:"
)

with st.sidebar:
    selected = option_menu(
        menu_title = None,
        options = ["Home", "Data Scraper", "Analytics", "Help"], 
        icons = ["house", "youtube", "bar-chart-fill",  "question-circle-fill"]
    )
with st.container():
    if selected == "Data Scraper":
        st.markdown("""
                    <h1 class = "header">Data Scraper</h1>
                    """, unsafe_allow_html=True)
        left_column, right_column = st.columns(2)
        with right_column:
            options = ["channel name", "channel id"]
            default = 0
            name_or_id_select = st.selectbox(
                "Select an option",
                options,
                default
            )
            
        with left_column:
            channel_name_or_id = st.text_input("")

        if st.button("Scrape Data"):
            data = make_video_details_comments(channel_name_or_id, name_or_id_select)
            channel_name = data["channel_details"]["channel_name"]
            check_if_exists(channel_name)
            push_to_mongodb(data)
                
                