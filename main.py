import streamlit as st
from scraper import run_scraper, get_suggestions

st.set_page_config(page_title="Hotel Price Suggester", layout="wide")
st.title("🏨 Glasgow Hotel Price Suggester")

if st.button("🔄 Refresh Data"):
    with st.spinner("Scraping Booking.com..."):
        data = run_scraper()
        if data.empty:
            st.error("No data found. Try refreshing or check the scraper.")
        else:
            suggestions = get_suggestions(data)
            st.success("Data refreshed!")
            st.dataframe(suggestions)
            st.download_button("📥 Download CSV", suggestions.to_csv(index=False), "suggested_prices.csv")
