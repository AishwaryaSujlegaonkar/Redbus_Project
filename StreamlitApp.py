import sqlite3
import pandas as pd
import streamlit as st

# Establish database connection
def get_connection():
    return sqlite3.connect('RedbusDB.db')

conn = get_connection()

# Fetch filtered data
def fetch_data(filters):
    query = "SELECT * FROM bus_routes"
    conditions = []

    # Apply filters
    if filters['bustype'] != "All":
        if filters['bustype'] == "Seater":
            conditions.append("bustype LIKE '%Seater%'")
        elif filters['bustype'] == "Sleeper":
            conditions.append("bustype LIKE '%Sleeper%'")

    if filters['route_name'] != "All":
        conditions.append(f"route_name = '{filters['route_name']}'")

    if filters['price_range'] != "All":
        price_ranges = {
            "100-500": "price BETWEEN 100 AND 500",
            "500-1000": "price BETWEEN 500 AND 1000",
            "1000-2000": "price BETWEEN 1000 AND 2000",
            "2000+": "price >= 2000"
        }
        conditions.append(price_ranges[filters['price_range']])

    if filters['star_rating'] != "All":
        star_rating_ranges = {
            "1-2": "star_rating BETWEEN 1 AND 2",
            "2-3": "star_rating BETWEEN 2 AND 3",
            "3-4": "star_rating BETWEEN 3 AND 4",
            "4-5": "star_rating BETWEEN 4 AND 5"
        }
        conditions.append(star_rating_ranges[filters['star_rating']])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return pd.read_sql_query(query, conn)

# Custom HTML for RedBus Title
st.markdown(
    """
    <style>
    .title-container {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: #D13140;
        color: white;
        padding: 5px;
        width: 100%;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 30px;
        font-weight: bold;
        margin-left: 10px;
    }
    </style>
    <div class="title-container">
        <div class="title-text">RedBus</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for Filters
st.sidebar.header("Search Buses")

# Static options for "Bus Type" dropdown
bus_type_options = ["Select", "Seater", "Sleeper"]
routes = ["Select"] + pd.read_sql_query("SELECT DISTINCT route_name FROM bus_routes", conn)["route_name"].tolist()
price_options = ["Select", "100-500", "500-1000", "1000-2000", "2000+"]
star_rating_options = ["Select", "1-2", "2-3", "3-4", "4-5"]

# Create filter containers
with st.sidebar.container():
    selected_route = st.selectbox("Route", routes)

with st.sidebar.container():
    selected_bus_type = st.selectbox("Bus Type", bus_type_options)

with st.sidebar.container():
    selected_price = st.selectbox("Price Range", price_options)

with st.sidebar.container():
    selected_rating = st.selectbox("Minimum Rating", star_rating_options)

# Collect all selected filters
filters = {
    "route_name": selected_route,
    "bustype": selected_bus_type,
    "price_range": selected_price,
    "star_rating": selected_rating
}

# Add a "Search" button
if st.sidebar.button("Search"):
    # Fetch and display data only when the button is clicked
    data = fetch_data(filters)
    st.write("Available Buses")
    st.dataframe(data)
