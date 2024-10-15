import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st
import json
from streamlit_lottie import st_lottie

# LOADING HELLO LOTTIE
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load the hello lottie animation
lottie_hello = load_lottiefile("gifs/hello.json")
lottie_trophy = load_lottiefile("gifs/winner.json")
lottie_great = load_lottiefile("gifs/great.json")
lottie_bear = load_lottiefile("gifs/bear.json")
lottie_strong = load_lottiefile("gifs/strong.json")
lottie_energy = load_lottiefile("gifs/energy.json")
lottie_healthy = load_lottiefile("gifs/healthy.json")
lottie_sick = load_lottiefile("gifs/sick.json")
lottie_eyes = load_lottiefile("gifs/eyes.json")
lottie_learn = load_lottiefile("gifs/learn.json")
lottie_avocado = load_lottiefile("gifs/avocado.json")

# Get today's date and day of the week
today = datetime.now().date()
day_of_week = datetime.now().strftime('%A')

# DISPLAYING LOTTIE AND TEXT SIDE BY SIDE
col1, col2 = st.columns([1, 2])  # Adjust the proportions as needed

with col1:
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=200,
        width=200,
        key="hello"
    )

with col2:
    st.markdown(f"<h2 style='color: #FF6347; font-family: \"Comic Sans MS\", cursive;'>Hey there, superstar! It is Nutri Time {day_of_week}!</h2>", unsafe_allow_html=True)

# SETTING UP DATABASE CONNECTION
# Connect to the SQLite database (creates `kula_heroes.db` if it doesn’t exist)
conn = sqlite3.connect('kula_heroes.db')
cursor = conn.cursor()

# Create the food_logs table if it doesn’t exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    food_item TEXT,
    category TEXT,
    points INTEGER,
    user_id INTEGER
)
''')
conn.commit()

# LOADING DATA
# Load the static food item list from CSV
file_path = 'food_items.csv'
food_data = pd.read_csv(file_path)

# FILTERING DATA FOR FRUITS AND VEGETABLES
# Separate the data for fruits and vegetables
fruits = food_data[food_data['Category'] == 'Fruit']
vegetables = food_data[food_data['Category'] == 'Vegetable']

# DISPLAYING TITLE AND SUBHEADER

# Title and subheader with kid-friendly fonts
st.markdown(
    """
    <style>
    .kiddy-title {
        font-size: 36px;
        font-family: "Comic Sans MS", cursive, sans-serif;
        color: #FF6347;
        text-align: center;
    }
    .kiddy-subheader {
        font-size: 24px;
        font-family: "Comic Sans MS", cursive, sans-serif;
        color: #4bbc3b;
        text-align: center;
    }
    .stButton>button {
        font-size: 22px;
        font-family: "Comic Sans MS", cursive, sans-serif;
        background-color: #FF6347;
        color: white;
        border-radius: 15px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 style='color: #FF6347; font-family: \"Comic Sans MS\", cursive; text-align: center;'>Yipee! We love fruits and veggies!</h2>", unsafe_allow_html=True)

# SETTING UP SIDEBAR
# Sidebar with cover image and styled welcome message
st.sidebar.image('images/cover.webp', width=250)

# Styling "Nutri!" with large, colorful font
st.sidebar.markdown(
    "<h2 style='color: #FF6347; font-family: \"Comic Sans MS\", cursive; text-align: left;'>Welcome to Nutri-Superstars!</h2>",
    unsafe_allow_html=True
)

# Additional text in the sidebar in default styling
st.sidebar.write("This is a brief prototype of the Nutri-Superstars platform for the DISH Competition 2024 ")  
st.sidebar.write("Tackling the notorious Fruits & Veggies, the platform demonstrates how technology can be harnessed to make nutrition education more accessible and appealing to younger children.")
st.sidebar.write("Disclaimer: Only few examples included for demonstration purposes. This can be expanded to different aspects of nutrition and culture. Expert informed methodology and backend to be explained upon request.")

# FRUITS SECTION
st.markdown(f"<div class='kiddy-subheader'>🥑 Did you eat a fruit today? Which one?🍉</div>", unsafe_allow_html=True)

selected_fruits = []
for i in range(0, len(fruits), 5):  # Step through 5 items at a time for two rows
    fruit_row = st.columns([2, 2, 2, 2, 2])  # Adjust column width as needed

    for idx, row_item in enumerate(fruits.iloc[i:i+5].iterrows()):  # Process 5 items per row
        _, row_data = row_item
        fruit_name = row_data['Food'].lower()
        fruit_path = f'images/{fruit_name}.webp'

        # Assign each item to the correct column within the row
        with fruit_row[idx]:
            st.image(fruit_path, width=150)
            if st.checkbox(f"{row_data['Food']}", key=row_data['Food']):
                selected_fruits.append(row_data)

# Calculate total points for fruits and display message
fruit_points = sum([fruit['Points'] for fruit in selected_fruits])
st.write(f"<h3 style='color: #fe7f2d;'>{fruit_points} Fruity Points! 🍓</h3>", unsafe_allow_html=True)


# VEGETABLES SECTION
st.markdown(f"<div class='kiddy-subheader'>🥬 Great! And did you eat veggies today? Which ones?</div>", unsafe_allow_html=True)

selected_vegetables = []
for i in range(0, len(vegetables), 5):  # Step through 5 items at a time for two rows
    veg_row = st.columns([2, 2, 2, 2, 2])  # Adjust column width as needed

    for idx, row_item in enumerate(vegetables.iloc[i:i+5].iterrows()):  # Process 5 items per row
        _, row_data = row_item
        veg_name = row_data['Food'].lower()
        veg_path = f'images/{veg_name}.webp'

        # Assign each item to the correct column within the row
        with veg_row[idx]:
            st.image(veg_path, width=150)
            if st.checkbox(f"{row_data['Food']}", key=row_data['Food'] + '_veg'):
                selected_vegetables.append(row_data)

# Calculate total points for vegetables and display message
veg_points = sum([veg['Points'] for veg in selected_vegetables])
st.write(f"<h3 style='color: #8ac926;'>{veg_points} Veggie Points!🥦</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #FF6347; font-family: \"Comic Sans MS\", cursive; text-align: left;'>Now check if you are a Nutri-Ninja!</h2>", unsafe_allow_html=True)

# LOGGING AND TOTAL POINTS BUTTON
total_points = fruit_points + veg_points

# Create a button to see total points
if st.button("SEE TOTAL POINTS HERE!", help="Click to see your total points!", key="total_points_button"):
    if total_points > 0:
        # Log selected fruits to the database
        for _, fruit in pd.DataFrame(selected_fruits).iterrows():
            cursor.execute('''
                INSERT INTO food_logs (date, food_item, category, points, user_id)
                VALUES (?, ?, ?, ?, ?)
                ''', (today, fruit['Food'], fruit['Category'], fruit['Points'], 1))  # assuming 1 is a placeholder for user_id

        # Log selected vegetables to the database
        for _, veg in pd.DataFrame(selected_vegetables).iterrows():
            cursor.execute('''
                INSERT INTO food_logs (date, food_item, category, points, user_id)
                VALUES (?, ?, ?, ?, ?)
                ''', (today, veg['Food'], veg['Category'], veg['Points'], 1))

        conn.commit()

        # First row: Trophy, Total Points Message, Great Lottie
        trophy_col, message_col, great_col = st.columns([2, 3, 2])
        with trophy_col:
            st.markdown("<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>", unsafe_allow_html=True)
            st_lottie(
                lottie_trophy,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=190,
                width=190,
                key="total_trophy"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with message_col:
            st.markdown("<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>", unsafe_allow_html=True)
            st.write(f"<h2 style='color: #FF6347;'>Wow! You earned {total_points} points!</h2>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with great_col:
            st.markdown("<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>", unsafe_allow_html=True)
            st_lottie(
                lottie_great,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=220,
                width=220,
                key="great_lottie"
            )
            st.markdown("</div>", unsafe_allow_html=True)
 
    else:
        # Display the reminder message if no items were selected
        st.write("<h3 style='color: #9d4edd;'>Oh no! Remember to eat fruits and veggies tomorrow!</h3>", unsafe_allow_html=True)

# LEARNING SECTION
st.markdown("<h2 style='color: #9d4edd; font-family: \"Comic Sans MS\", cursive; text-align: left;'>Why are Fruits & Veggies Awesome?</h2>", unsafe_allow_html=True)

# Custom CSS for adjustable explanation font size
st.markdown(
    """
    <style>
    .explanation-text {
        font-size: 18px; /* Adjust font size as needed */
        font-family: "Comic Sans MS", cursive, sans-serif;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Benefit 1: Super Strong
strong_title_col, strong_lottie_col, strong_text_col = st.columns([2, 2, 2])
with strong_title_col:
    st.markdown("<h3 style='text-align: center; color: #4682B4;'>Makes You Super Strong! 💪</h3>", unsafe_allow_html=True)
with strong_lottie_col:
    st_lottie(
        lottie_strong,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=150,
        width=150,
        key="strong_lottie"
    )
with strong_text_col:
    st.markdown("<p class='explanation-text'>They give you strength to play, run, and jump!</p>", unsafe_allow_html=True)

# Benefit 2: Bright Eyes Power
eyes_title_col, eyes_lottie_col, eyes_text_col = st.columns([2, 2, 2])
with eyes_title_col:
    st.markdown("<h3 style='text-align: center; color: #FFA500;'>Bright Eyes Power! 👀</h3>", unsafe_allow_html=True)
with eyes_lottie_col:
    st_lottie(
        lottie_eyes,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=180,
        width=180,
        key="eyes_lottie"
    )
with eyes_text_col:
    st.markdown("<p class='explanation-text'>They help keep your eyes sharp and bright!</p>", unsafe_allow_html=True)

# Benefit 3: Gives You Energy
energy_title_col, energy_lottie_col, energy_text_col = st.columns([2, 2, 2])
with energy_title_col:
    st.markdown("<h3 style='text-align: center; color: #4682B4;'>Gives You Energy! ⚡</h3>", unsafe_allow_html=True)
with energy_lottie_col:
    st_lottie(
        lottie_energy,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=150,
        width=150,
        key="energy_lottie"
    )
with energy_text_col:
    st.markdown("<p class='explanation-text'>They boost your energy to stay active all day!</p>", unsafe_allow_html=True)

# Benefit 4: Protects You from Getting Sick
sick_title_col, sick_lottie_col, sick_text_col = st.columns([2, 2, 2])
with sick_title_col:
    st.markdown("<h3 style='text-align: center; color: #FFA500;'>Protects You from Getting Sick! 🛡️</h3>", unsafe_allow_html=True)
with sick_lottie_col:
    st_lottie(
        lottie_sick,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=120,
        width=120,
        key="sick_lottie"
    )
with sick_text_col:
    st.markdown("<p class='explanation-text'>They keep you healthy so you can have fun!</p>", unsafe_allow_html=True)

# Benefit 5: Makes You Happy and Healthy
healthy_title_col, healthy_lottie_col, healthy_text_col = st.columns([2, 2, 2])
with healthy_title_col:
    st.markdown("<h3 style='text-align: center; color: #4682B4;'>Makes You Happy and Healthy 😊</h3>", unsafe_allow_html=True)
with healthy_lottie_col:
    st_lottie(
        lottie_healthy,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=150,
        width=150,
        key="healthy_lottie"
    )
with healthy_text_col:
    st.markdown("<p class='explanation-text'>They help you stay happy and strong!</p>", unsafe_allow_html=True)

# Benefit 6: And Many, Many More!
avocado_title_col, avocado_lottie_col, avocado_text_col = st.columns([2, 2, 2])
with avocado_title_col:
    st.markdown("<h3 style='text-align: center; color: #FFA500;'>And Many, Many More! 🥑</h3>", unsafe_allow_html=True)
with avocado_lottie_col:
    st_lottie(
        lottie_avocado,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=200,
        width=200,
        key="avocado_lottie"
    )
with avocado_text_col:
    st.markdown("<p class='explanation-text'>Eating different ones keeps your body at its best!</p>", unsafe_allow_html=True)


# CULTURE SECTION
# Initialize a session state variable for refresh control
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0

# CULTURE SECTION #https://nutrition.co.ke/swahili-words-for-common-fruits/
st.markdown("<h2 style='color: #8ac926; font-family: \"Comic Sans MS\", cursive; text-align: center;'>Let's Play! What Do We Call it in Swahili?</h2>", unsafe_allow_html=True)

# Load the culture data from CSV
culture_data = pd.read_csv('culture.csv')

# Select a random fruit or vegetable
import random
random_item = culture_data.sample(1).iloc[0]
english_name = random_item['English']
swahili_name = random_item['Swahili']
image_path = f"images/{english_name.lower()}.webp"  # Assumes image filenames are lowercase English names

# Display the image and English name
col1, col2, col3 = st.columns([1, 2, 1])  # Center image in middle column
with col2:
    st.image(image_path, width=200)
    st.markdown(f"<h3 style='text-align: center; color: #4682B4;'>{english_name}</h3>", unsafe_allow_html=True)

# Add a button to reveal the Swahili name
if st.button("Reveal!"):
    st.markdown(f"<h3 style='text-align: center; color: #4682B4;'>In Swahili, we call it: {swahili_name}!</h3>", unsafe_allow_html=True)

# Button to load the next item by increasing the refresh counter
if st.button("Try Another One!"):
    st.session_state.refresh_counter += 1  # Increment the counter to refresh



# DANCE
st.markdown("<h2 style='color: #8ac926; font-family: \"Comic Sans MS\", cursive; text-align: center;'>Good Job! Time for the Nutri Dance!</h2>", unsafe_allow_html=True)

# Set up three columns for positioning
left_col, center_col, right_col = st.columns([2, 3.5, 1])

# Left column with placeholder text
with left_col:
    st.write("")  # Placeholder for positioning adjustments

# Center column with bear lottie
with center_col:
    st_lottie(
        lottie_bear,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=280,
        width=280,
        key="bear_dance"
    )

# Right column left empty to help with centering
with right_col:
    st.write("")  # Leave empty

# CLOSE DATABASE CONNECTION
conn.close()

