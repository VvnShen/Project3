import streamlit as st
import apps.latestPrice


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

        st.sidebar.title("ETHUSD Latest price:")
        if st.sidebar.button("Get/Refresh"):
            price=apps.latestPrice.latestPrice()
            st.sidebar.write(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{price}</p>', unsafe_allow_html=True)
            apps.latestPrice.get_historical_data_plot()
            st.sidebar.write("(from chainlink Kovan Testnet)")
        
    
