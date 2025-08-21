import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="viz_demo")

# Load data
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

st.header("Enter your inputs")

# Property type
property_type = st.selectbox('Property Type', sorted(df['property_type'].unique().tolist()))

# Sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# Bedrooms
bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

# Bathrooms
bathrooms = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

# Balcony
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

# Property age
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

# Built-up area with validation
built_up_area = float(st.number_input('Built Up Area (sq ft)', min_value=501, step=1))

# Yes/No mapping
yes_no_map = {"No": 0.0, "Yes": 1.0}

# Servant room
servant_room = yes_no_map[st.selectbox('Servant Room', ["No", "Yes"])]

# Store room
store_room = yes_no_map[st.selectbox('Store Room', ["No", "Yes"])]

# Furnishing type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# Luxury category
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# Floor category
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    # Backend validation for built_up_area
    if built_up_area <= 500:
        st.error("❌ Built-up area must be greater than 500 sq ft.")
    else:
        # Form a dataframe
        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category'
        ]
        data = [[
            property_type, sector, bedrooms, bathrooms, balcony,
            property_age, built_up_area, servant_room, store_room,
            furnishing_type, luxury_category, floor_category
        ]]
        one_df = pd.DataFrame(data, columns=columns)
        st.dataframe(one_df)

        # Prediction with safe handling for unknown categories
        try:
            base_price = np.expm1(pipeline.predict(one_df))[0]  # in crores
            low = base_price - 0.22
            high = base_price + 0.22

            st.success(f"💰 The price of the flat is between {round(low, 2)} cr and {round(high, 2)} cr")
        except ValueError as e:
            if "Found unknown categories" in str(e):
                st.error(f"⚠ Unknown category found in input: {e}")
            else:
                st.error(f"Error: {e}")

        # #predict
        # base_price = np.expm1(pipeline.predict(one_df))[0]
        # low = base_price - 0.22
        # high = base_price + 0.22

        # #display
        # st.text(f'The price of the flat is between {round(low,2)}cr and {round(high,2)}cr')

        # # # Prediction with safe handling for unknown categories
        # # try:
        # #     prediction = np.expm1(pipeline.predict(one_df))
        # #     st.success(f"💰 Predicted Price: ₹{prediction[0]:,.2f}")
        # # except ValueError as e:
        # #     if "Found unknown categories" in str(e):
        # #         st.error(f"⚠ Unknown category f
