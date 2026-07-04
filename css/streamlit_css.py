import streamlit as st

def load_css():
    return st.markdown('''
    <style>
        [data-testid="stExpander"] div {
            display: flex;
            justify-content: center;
            font-size: 18px;
        }
                
        [data-testid="stExpander"] details {
            padding-bottom: 20px;
        }
        
        [data-testid="stCaptionContainer"] p {
            font-size: 25px;
        }
                
    </style>

    ''', unsafe_allow_html=True)
