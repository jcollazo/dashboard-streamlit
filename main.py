import streamlit as st
from navigation import landing, dashboard_yf, chart

# Streamlit pages
st.set_page_config(layout = 'wide')
st.sidebar.image(
"https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
width=50)

pages = {
    '🏠 Main Page': landing.pageI,
    '📈 SPX Analytics': chart.pageIII
}

selected_page = st.sidebar.radio("Navigation", pages.keys())
pages[selected_page]()