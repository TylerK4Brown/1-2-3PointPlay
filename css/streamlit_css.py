import streamlit as st

def load_css_gamedisplay():
    return st.markdown('''
    <style>
        [data-testid="stExpander"] div {
            display: flex;
            justify-content: center;
            font-size: 20px;
        }
                
        [data-testid="stExpander"] details {
            padding-bottom: 20px;
        }
        
        [data-testid="stCaptionContainer"] p {
            font-size: 20px;
        }
                       
        [data-testid="stToast"] div {
            display: flex;
            align-items: center;
        }
        
        [data-testid="stButtonGroup"] button {
            height: 55px;
        }
        
        [data-testid="stBaseButton-segmented_control"] p {
            font-size: 20px;
        }
        
        [data-testid="stButton"] button {
            height: 75px;
        }
                       
        [data-testid="stMarkdownContainer"] hr {
            border: 0.01rem solid #3b3b3b;
            border-radius: 5px;
        }
    </style>

    ''', unsafe_allow_html=True)

# TODO: will eventually add some hacky CSS here that makes these buttons look a little larger
def load_css_buttons_homepage():
    return st.markdown('''
    <style>
        [data-testid="stButton"] p {
            font-size: 30px;
        }
                       
        [data-testid="stButton"] button {
            height: 125px;
            background-color: #2d60cf;
            color: #ffffff;
        }
                       
        [data-testid="stButton"] button:hover {
            background-color: #6481c1;
        }
                    
    </style>
    ''', unsafe_allow_html=True)
    
def load_css_buttons_display_picks():
    return st.markdown('''
    <style>     
    
        [data-testid="stButton"] button {
            height: 75px;
        }
        
    </style>
    ''', unsafe_allow_html=True)