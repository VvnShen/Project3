import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.sidebar.title("Welcome Welcome!")
        st.sidebar.title("Feel free to 'shop' around!")
        app = st.sidebar.radio(
            'Let\'s go to: ',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()