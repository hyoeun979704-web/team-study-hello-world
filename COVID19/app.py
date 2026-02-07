import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="2,195일간의 여정, 코로나19 연대기",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GitHub raw URL에서 원본 HTML 로드
html_url = "https://raw.githubusercontent.com/hyoeun979704-web/Covid-19_Project_bive-coding-team/main/COVID19/index.html"

# HTML 파일 읽기
import requests

response = requests.get(html_url)
html_content = response.text

# CSS, JS 경로를 GitHub raw URL로 변경
html_content = html_content.replace(
    'href="css/style.css"',
    'href="https://raw.githubusercontent.com/hyoeun979704-web/Covid-19_Project_bive-coding-team/main/COVID19/css/style.css"'
)
html_content = html_content.replace(
    'src="js/main.js"',
    'src="https://raw.githubusercontent.com/hyoeun979704-web/Covid-19_Project_bive-coding-team/main/COVID19/js/main.js"'
)
html_content = html_content.replace(
    'data/timeline.csv',
    'https://raw.githubusercontent.com/hyoeun979704-web/Covid-19_Project_bive-coding-team/main/COVID19/data/timeline.csv'
)
html_content = html_content.replace(
    'data/cities.csv',
    'https://raw.githubusercontent.com/hyoeun979704-web/Covid-19_Project_bive-coding-team/main/COVID19/data/cities.csv'
)

# 전체 HTML을 iframe으로 렌더링
components.html(html_content, height=5000, scrolling=True)
