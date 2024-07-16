import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="Appointments", page_icon="📅")
st.markdown("Appointments")
st.sidebar.header("Appointments")
# Initialize a list to store appointments
if 'appointments_list' not in st.session_state:
    st.session_state.appointments_list = []

st.title("Appointments Page")

    # Sample appointment data entry form
st.header("Schedule an Appointment")
with st.form(key='appointment_form'):
    name = st.text_input("Patient Name")
    date = st.date_input("Appointment Date")
    time = st.time_input("Appointment Time")
    symptoms = st.text_area("Symptoms")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Append the new appointment to the list
    st.session_state.appointments_list.append({
        'Patient Name': name,
        'Date': date.strftime("%Y-%m-%d"),
        'Time': time.strftime("%H:%M"),
        'Symptoms': symptoms
    })
    st.success(f"Appointment scheduled for {name} on {date} at {time}.")

# Display the appointments table
if st.session_state.appointments_list:
    st.header("Scheduled Appointments")
    appointments_df = pd.DataFrame(st.session_state.appointments_list)
    st.dataframe(appointments_df)
