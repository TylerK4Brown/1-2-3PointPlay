import streamlit as st

def load_css_gamedisplay():
    return st.markdown('''
    <style>
        [data-testid="stExpander"] div {
            display: flex;
            justify-content: center;
            font-size: 15px;
        }
                
        [data-testid="stExpander"] details {
            padding-bottom: 20px;
        }
        
        [data-testid="stCaptionContainer"] p {
            font-size: 25px;
        }
                       
        [data-testid="stToast"] div {
            display: flex;
            align-items: center;
        }
    </style>

    ''', unsafe_allow_html=True)

# TODO: will eventually add some hacky CSS here that makes these buttons look a little larger
def load_css_buttons_homepage():
    return st.markdown('''
    <style>
        [data-testid="stButton"] p {
            font-size: 40px;
        }
                       
        [data-testid="stButton"] button {
            height: 100px;
            background-color: #2d60cf;
        }
                       
        [data-testid="stButton"] button:hover {
            background-color: #6481c1;
        }
                    
    </style>
    ''', unsafe_allow_html=True)
