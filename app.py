import json
import streamlit as st
import pandas as pd
import pickle
from sqlalchemy import create_engine


DB_USERNAME = "your admin"
DB_PASSWORD = "your pwd"
DB_HOST = "your DB ID"  # Example: mydb.xxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT = "Your Port NO"  # MySQL uses 3306, PostgreSQL uses 5432
DB_NAME = "restaurant_recommendations"

# Load model
with open("D:\\python\\restaurant_app\\restaurant_price_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load Feature Names for Prediction
feature_file = "D:\\python\\restaurant_app\\feature_description.json"
with open(feature_file, "r") as f:
    feature_names = json.load(f)


db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# Fetch restaurant data
query = "SELECT * FROM restaurants"
df = pd.read_sql(query, con=engine)

# Streamlit UI
st.title("🍽️ Restaurant Recommendation & Price Prediction")

# User Inputs
location = st.selectbox("📍 Select Location", sorted(df["location"].unique()))
#cuisine = st.selectbox("🍛 Select Cuisine", sorted(df["cuisines"].unique()))

available_cuisines = df[df["location"] == location]["cuisines"].unique()
cuisine = st.selectbox("🍛 Select Cuisine", sorted(available_cuisines))


# Filter Restaurants
filtered_df = df[(df["location"] == location) & (df["cuisines"].str.contains(cuisine, regex=False, na=False))]

if not filtered_df.empty:
    st.write(filtered_df[["name", "average_cost_for_two", "votes"]])
else:
    st.warning("⚠️ No restaurants found for this selection!")

# Predict Price
st.subheader("💰 Price Prediction")
votes = st.slider("🔢 Number of Votes", 0, 5000, 100)
price_range = st.selectbox("💲 Price Range (1-4)", [1, 2, 3, 4])

# Create Input DataFrame
if not filtered_df.empty:
    input_data = pd.DataFrame([[filtered_df.iloc[0]["latitude"], 
                                filtered_df.iloc[0]["longitude"], 
                                price_range, 
                                votes]], 
                              columns=["latitude", "longitude", "price_range", "votes"])

    # Ensure input data has all required features (fill missing columns with 0)
    for col in feature_names:
        if col not in input_data.columns:
            input_data[col] = 0  # Adding missing columns with default values

    # Reorder columns to match training format
    input_data = input_data[feature_names]

    # Predict Cost for Two
    if st.button("Predict Price"):
        pred = model.predict(input_data)
        st.success(f"💵 Estimated Cost for Two: ₹{int(pred[0])}")