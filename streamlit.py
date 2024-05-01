from dashboard.user_behavior import getTopCustomers
import streamlit as st
import pandas as pd
import os, sys
# Add parent directory to path to import modules from src
rpath = os.path.realpath('src')
print(rpath)
if rpath not in sys.path:
    sys.path.insert(0, rpath)

print(sys.path)
# from loader import SlackDataLoader
import utils as utils



# read_file = SlackDataLoader("./anonymized")


def main():
    st.set_page_config(page_title="Tell-co", layout="wide")
    
    col_left, col_right = st.columns((1, 1))
    col_left.title("Report")
    col_left.write("analysis report")
    st.sidebar.title("Sidebar ")
    options = get_sidebar()
    data = get_data()
  
    if options == "All Data":
        reply_counts(data)
    elif options == "User Behavior":
        getTopCustomers() 

def get_sidebar():
    selected_option = st.sidebar.selectbox("Select an option", ["All Data", "User Behavior", "Top Messages","Sender Counts"])
    return selected_option

def get_data():
    data = ""
    return data



def reply_counts(data):
   return  ""
    
main()