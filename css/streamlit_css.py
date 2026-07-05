import streamlit as st

def load_css_gamedisplay():
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

# TODO: will eventually add some hacky CSS here that makes these buttons look a little larger
def load_css_buttons_homepage():
    return st.markdown('''
    <style>
        [data-testid="stBidiComponentIsolated"] {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100px;
            font-size: 30px;
        }
    </style>
    ''', unsafe_allow_html=True)
