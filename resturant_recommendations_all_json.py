# get the data from s3
import pandas as pd
import boto3
import json
from sqlalchemy import create_engine
#import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle

# AWS S3 Credentials
ACCESS_KEY = "YOUR ACCESS KEY"
SECRET_KEY = "YOUR SECRET KEY"
BUCKET_NAME = "project-folder"
FOLDER_PREFIX = "Json files/"  # Path to JSON file in S3

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
# List all JSON files in the folder
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FOLDER_PREFIX)
# Check if the folder is empty
if 'Contents' not in response:
    print("❌ No JSON files found in S3 bucket.")
    exit()
# Extract all file keys
json_files = [obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".json")]
# Read all JSON files and extract data
restaurant_data = []
for file_key in json_files:
    print(f"📥 Downloading {file_key} from S3...")
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    data = json.loads(obj["Body"].read())
    for entry in data:
        if "restaurants" in entry:
            for restaurant in entry["restaurants"]:
                rest_info = restaurant["restaurant"]
                restaurant_data.append({
                    "id": rest_info.get("id"),
                    "name": rest_info.get("name"),
                    "location": rest_info["location"].get("locality_verbose", ""),
                    "city": rest_info["location"].get("city", ""),
                    "latitude": rest_info["location"].get("latitude", ""),
                    "longitude": rest_info["location"].get("longitude", ""),
                    "cuisines": rest_info.get("cuisines", ""),
                    "average_cost_for_two": rest_info.get("average_cost_for_two", ""),
                    "price_range": rest_info.get("price_range", ""),
                    "rating": rest_info["user_rating"].get("aggregate_rating", ""),
                    "votes": rest_info["user_rating"].get("votes", ""),
                    "has_table_booking": rest_info.get("has_table_booking", ""),
                    "has_online_delivery": rest_info.get("has_online_delivery", "")
                })

# Convert to DataFrame
df = pd.DataFrame(restaurant_data)
# display(df.head())
print(df.head())


# RDS Database Config
DB_USERNAME = "DB NAME"
DB_PASSWORD = "DB PWD"
DB_HOST = "DB HOST "  # Example: mydb.xxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT = "YOUR PORT"  # MySQL uses 3306, PostgreSQL uses 5432
DB_NAME = "restaurant_recommendations"


# Connect to RDS

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
# engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}")

with engine.connect() as conn:
    print("✅ Connected to MySQL RDS!")

try:
    df.to_sql(name="restaurants", con=engine, if_exists="replace", index=False)
    print("✅ Data uploaded successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    

# Load Data from RDS
query = "SELECT votes,latitude,longitude, rating, price_range, average_cost_for_two FROM restaurants"
df = pd.read_sql(query, engine)

# Handle missing values
df.dropna(inplace=True)

# Convert categorical data (location) into numerical features
# df = pd.get_dummies(df, columns=["location"], drop_first=True)

# Define Features (X) and Target (y)
X = df.drop(columns=["average_cost_for_two"])
y = df["average_cost_for_two"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(X_train.shape)  # Should print (num_samples, 664)
print(X_train.columns)  # See all the feature names used during training


# Evaluate Model
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", mean_squared_error(y_test, y_pred) ** 0.5)
# print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))
# Save Model
#joblib.dump(model, "D:\\python\\restaurant_app\\restaurant_price_model.pkl")
with open("/home/ubuntu/restaurant_app/restaurant_price_model.pkl", "wb") as f:
    pickle.dump(model, f)
# Save Feature Names for Future Use
feature_file = "/home/ubuntu/restaurant_app/feature_description.json"
with open(feature_file, "w") as f:
    json.dump(list(X_train.columns), f)

print("✅ Model saved as 'restaurant_price_model.pkl'")
