## streamlit_css.py
## Contains hacky CSS styling for the Streamlit application to make certain components look nicer
## Would probably be easier to just use React/Typescript, but to keep it Pythonic, this solution works nicely!
## The CSS styling applies to the entire page by simply calling these functions in the pages they need to be used in

import streamlit as st

# IN THIS load_css_gamedisplay() FUNCTION:
# data-testid="stExpander" div: the container for the text in the expander, makes the text larger and centered
# data-testid="stExpander" summary [data-testid="stMarkdownContainer"] p: pairs with the above changes to the div
# ^--- aligns the text in the expander to be centered, slight padding to the right, and allows for line breaks in the text
# data-testid="stExpander" details: the container for the expander, adds slight padding to the bottom of the expander
# data-testid="stExpander" summary [data-testid="stMarkdownContainer"] p: 
# data-testid="stCaptionContainer" p: makes the text in the caption of an image larger (score display in view_player_picks.py)
# data-testid="stToast" div: an attempt to center the toast, doesn't work for some reason
# data-testid="stButtonGroup" button: makes the buttons in the exapnder larger
# data-testid="stBaseButton-segmented_control" p: makes the text in the buttons larger
# data-testid="stButton" button: makes regular streamlit buttons larger
# data-testid="stMarkdownContainer" hr: adjusts the thickness and radius of the horizontal dividers in the app
def load_css_gamedisplay():
    return st.markdown('''
    <style>
        [data-testid="stExpander"] div {
            display: flex;
            justify-content: center;
            font-size: 20px;
        }
                
        [data-testid="stExpander"] details {
            padding-bottom: 5px;
        }

        [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {
            white-space: pre-line;
            padding: 0 40px 0 0;
            text-align: center;
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

# IN THIS load_css_buttons_homepage() FUNCTION:
# data-testid="stButton" p: makes the text in the buttons larger
# data-testid="stButton" button: makes the buttons larger, changes the background color, text color, border, and border radius
# data-testid="stButton" button:hover: changes the background color of the buttons when hovered over
def load_css_buttons_homepage():
    return st.markdown('''
    <style>
        [data-testid="stButton"] p {
            font-size: 21px;
        }
                       
        [data-testid="stButton"] button {
            height: 85px;
            background-color: #2d60cf;
            color: #ffffff;
            border: 0.1rem solid #ffffff;
            border-radius: 30px;
        }
                       
        [data-testid="stButton"] button:hover {
            background-color: #6481c1;
        }
                    
    </style>
    ''', unsafe_allow_html=True)

# IN THIS load_css_buttons_display_picks() FUNCTION:
# data-testid="stButton" button: makes the buttons larger
def load_css_buttons_display_picks():
    return st.markdown('''
    <style>     
    
        [data-testid="stButton"] button {
            height: 75px;
        }
        
    </style>
    ''', unsafe_allow_html=True)