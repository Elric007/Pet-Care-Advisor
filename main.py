import requests
import streamlit as st
from openai import OpenAI


# Set up OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_SECRET_KEY"])

# Function to get responses from OpenAI
def get_advice(query, sysprompt, location=None):
    if location:
        location_prompt = f"Additionally, based on the location '{location}', provide recommendations for the nearest veterinary clinics and pet stores."
        sysprompt += location_prompt
    response = client.chat.completions.create(
        model="gpt-4o",
          messages=[{
              "role": "system",
              "content": sysprompt
          }, {
              "role": "user",
              "content": query
          }],
          max_tokens=1000)
    adviced = response.choices[0].message.content
    return adviced


sysprompt = """
You are a knowledgeable pet advisor. Your role is to provide expert advice on pet care, health, and behavior.

"""

st.title("Pet Care Advisor")

st.write("Welcome to the Pet Care Advisor! Ask me anything about pet care.")

query = st.text_input("Enter your pet care question:")
location = st.text_input("Enter your location:")

# Initialize session state
if "advice" not in st.session_state:
    st.session_state.advice = ""
if "location_advice" not in st.session_state:
    st.session_state.location_advice = ""

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Get Advice"):
        if query:
            st.session_state.advice = get_advice(query, sysprompt)
            st.session_state.location_advice = ""  # Reset location advice when new advice is generated
        else:
            st.write("Please enter a question to get advice.")

with col2:
    if st.button("Find Location"):
        if location:
            location_prompt = f"Based on the location '{location}', provide recommendations for the nearest veterinary clinics and pet stores."
            location_info = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": location_prompt
                }],
                max_tokens=1000
            ).choices[0].message.content
            st.session_state.location_info = location_info
        else:
            st.write("Please enter a location to get recommendations.")

if st.session_state.advice:
    st.write("**Advice:**")
    st.write(st.session_state.advice)

if st.session_state.location_advice:
    st.write("**Location-based Advice:**")
    st.write(st.session_state.location_advice)


