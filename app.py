import streamlit as st
from cv_page import cv_page
from rag.rag_page import rag_page

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "cv"

if st.session_state.page == "cv":
    cv_page()
else:
    rag_page()
