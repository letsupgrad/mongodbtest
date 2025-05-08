import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

st.title("MongoDB Connection Test")

# --- MongoDB Connection ---
@st.cache_resource(show_spinner="Connecting to MongoDB...")
def get_mongo_client():
    try:
        uri = st.secrets["mongo"]["uri"]
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # Test the connection
        return client
    except ConnectionFailure as e:
        st.error(f"MongoDB Connection Failed: {e}")
        return None

# Use the client
client = get_mongo_client()

if client:
    db = client.get_default_database()  # Or client["master"]
    st.success("Connected to MongoDB!")

    # Example: List collections
    st.write("Collections in DB:")
    st.write(db.list_collection_names())

    # Example: Display one document
    col = db.get_collection("billboard")  # Replace with your collection
    doc = col.find_one()
    st.write("Sample Document:")
    st.json(doc)
