import streamlit as st
import pandas as pd
from datetime import datetime
from catdel.database import database as db

FIELDS = {
    'user_name': {'type': 'text_input', 'label': 'Your Name', 'placeholder': 'John Doe'},
    'user_email': {'type': 'text_input', 'label': 'Your Email', 'placeholder': 'john.doe@example.com'},
    'feature_title': {'type': 'text_input', 'label': 'Feature Title', 'placeholder': 'Enter the feature title'},
    'feature_description': {'type': 'text_area', 'label': 'Feature Description (required)', 'placeholder': 'Describe the feature'},
    'priority': {'type': 'selectbox', 'label': 'Priority', 'options': ['Low', 'Medium', 'High']}
}

def form(fields):
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    if not st.session_state['submitted']:
        with st.form(key='feature_request_form', clear_on_submit=True):
            form_data = {}
            for field, details in fields.items():
                if details['type'] == 'text_input':
                    form_data[field] = st.text_input(label=details['label'], placeholder=details['placeholder'])
                elif details['type'] == 'text_area':
                    form_data[field] = st.text_area(label=details['label'], placeholder=details['placeholder'])
                elif details['type'] == 'selectbox':
                    form_data[field] = st.selectbox(label=details['label'], options=details['options'])

            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not form_data['feature_description']:
                st.error('Feature Description is mandatory.')
            else:            
                feature_request = {field: form_data[field] for field in fields}
                feature_request['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                db.save_to_feature_request(feature_request)
                st.session_state['submitted'] = True
                st.success('Thank you for your feature request! You cannot resubmit the form.')
    else:
        st.warning('You have already submitted a feature request.')

def expander():
    with st.expander('📢 Have a Feature Request? Let Us Know!'):
        form(FIELDS)

@st.experimental_dialog('📢 Have a Feature Request? Let Us Know!')
def _modal():
    form(FIELDS)
    

def modal():
    if st.button('📢 Have a Feature Request? Let Us Know!', use_container_width=True):
        _modal()
