import streamlit as st
from multiapp import MultiApp
from medbrief import home_page
from appointments import appointments_page

app = MultiApp()

# Add all your application pages here
app.add_app("Appointments", appointments_page)
app.add_app("Medbrief", home_page)


# The main app
app.run()