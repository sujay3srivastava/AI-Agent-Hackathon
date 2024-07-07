import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize a list to store appointments
appointments_list = []



def appointments_page():
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
        appointments_list.append({
            'Patient Name': name,
            'Date': date.strftime("%Y-%m-%d"),
            'Time': time.strftime("%H:%M"),
            'Symptoms': symptoms
        })
        st.success(f"Appointment scheduled for {name} on {date} at {time}.")

    # Display the appointments table
    if appointments_list:
        st.header("Scheduled Appointments")
        appointments_df = pd.DataFrame(appointments_list)
        st.dataframe(appointments_df)


# This function is to prevent the appointments_list from resetting on every rerun
def main():
    if 'appointments_list' not in st.session_state:
        st.session_state.appointments_list = []
    global appointments_list
    appointments_list = st.session_state.appointments_list
    appointments_page()


# Call the main function to initialize the session state
main()