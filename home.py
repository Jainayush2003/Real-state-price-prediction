# import streamlit as st

# st.set_page_config(

#     page_title= "Hello",
#     page_icon = "👋"
# )

# st.write("# Welome to streamlit")
# st.sidebar.success("select a demo above.")



import streamlit as st

# Page config
st.set_page_config(
    page_title="Real Estate Web App",
    page_icon="🏠",
    layout="wide"
)

# Main title
st.write("# 🏡 Welcome to the Real Estate Price Prediction App")

st.markdown(
    """
    This interactive web app helps you explore and predict real estate property prices 
    using **Machine Learning**. Navigate using the sidebar to try out different features:

    ### 📊 Analytics
    - Explore the dataset with visualizations  
    - Understand factors affecting property prices  

    ### 🎯 Recommender System
    - Get property recommendations based on your preferences  
    - Discover similar properties in chosen locations  

    ### 💰 Prediction
    - Enter details like location, size, and amenities  
    - Instantly predict the estimated property price  

    ---
    👈 Use the sidebar to get started!
    """
)


