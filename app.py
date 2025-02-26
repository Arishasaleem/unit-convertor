import streamlit as st
import time

def convert_units(category, from_unit, to_unit, value):
    conversions = {
        "Temperature": {
            "Celsius": lambda x: x,
            "Fahrenheit": lambda x: (x * 9/5) + 32,
            "Kelvin": lambda x: x + 273.15
        },
        "Length": {
            "Meters": lambda x: x,
            "Kilometers": lambda x: x / 1000,
            "Miles": lambda x: x * 0.000621371,
            "Feet": lambda x: x * 3.28084
        },
        "Weight": {
            "Kilograms": lambda x: x,
            "Grams": lambda x: x * 1000,
            "Pounds": lambda x: x * 2.20462
        },
        "Speed": {
            "Meters per second": lambda x: x,
            "Kilometers per hour": lambda x: x * 3.6,
            "Miles per hour": lambda x: x * 2.23694
        }
    }
    
    if category in conversions and from_unit in conversions[category] and to_unit in conversions[category]:
        base_value = conversions[category]["Meters"](value) if category == "Length" else conversions[category][from_unit](value)
        return conversions[category][to_unit](base_value)
    return None

st.set_page_config(page_title="Multi-Unit Converter", page_icon="🔄", layout="wide")
st.title("🔄 Multi-Unit Converter")
st.markdown("### Convert various units instantly with a sleek and modern UI!")

st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .stTextInput, .stSelectbox, .stNumberInput { border-radius: 10px; padding: 8px; }
    .stButton>button { background-color: #007BFF; color: white; padding: 10px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

category = st.selectbox("Select Category", ["Temperature", "Length", "Weight", "Speed"], key="category")
units = {
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Length": ["Meters", "Kilometers", "Miles", "Feet"],
    "Weight": ["Kilograms", "Grams", "Pounds"],
    "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour"]
}

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", units[category], key="from_unit")
with col2:
    to_unit = st.selectbox("To Unit", units[category], key="to_unit")

st.markdown("---")
value = st.number_input("Enter Value", min_value=0.0, format="%.2f", key="value")

# Live Conversion
if value:
    result = convert_units(category, from_unit, to_unit, value)
    if result is not None:
        st.success(f"✅ {value} {from_unit} = {result:.2f} {to_unit}")
    else:
        st.error("⚠ Conversion not possible!")

st.markdown("---")
# Conversion History
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("💾 Save Conversion"):
    st.session_state.history.append(f"{value} {from_unit} → {result:.2f} {to_unit}")
    time.sleep(0.5)
    st.success("✅ Conversion saved!")

if st.session_state.history:
    st.markdown("### 📜 Conversion History")
    for record in st.session_state.history[-5:]:
        st.write(f"🔹 {record}")
