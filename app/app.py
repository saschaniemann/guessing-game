"""Contains the page structure of our guessing game app."""

import streamlit as st

game_page = st.Page("_pages/game.py", title="Play", icon=":material/casino:")
stats_page = st.Page("_pages/stats.py", title="Stats", icon=":material/query_stats:")

pg = st.navigation([game_page, stats_page])
st.set_page_config(page_title="Guessing game", page_icon=":material/poker_chip:")
pg.run()
