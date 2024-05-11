import streamlit as st
from navigation import landing, dashboard_yf, chart

# Streamlit pages
st.set_page_config(layout = 'wide')


pages = {
    'Home': landing.pageI,
    'Chart': chart.pageIII
}

selected_page = st.sidebar.radio("Navigation", pages.keys())
pages[selected_page]()