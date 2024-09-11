# Importance to Teamate Offence - Streamlit App Test

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import altair_lexend_theme
import streamlit.components.v1 as components
import json

##########################################################
## Page Configuration

st.set_page_config(page_title="Importance to Teammate Offence (LB-Hockey)", layout="centered", page_icon="https://i0.wp.com/lb-hockey.com/wp-content/uploads/2024/02/LB-Hockey-Logo-Done.png?w=960&ssl=1", initial_sidebar_state="auto", menu_items={})
background_color = '#0E1117'
text_color = '#F3F3F3'


##########################################################
## Import Data

season = '2023-24'
seasons = [f'{s}-{str(s+1)[-2:]}' for s in range(2021, int(season[:4])+1)]
@st.cache_data
def load_data(seasons):
    dfs = {}
    for s in seasons:
        dfs[s] = pd.read_excel('Importance to Teammate Offence Data.xlsx', s).set_index('Name')
    # Combine the data for easy access
    return pd.concat([dfs[df] for df in seasons[::-1]], keys=seasons[::-1], names=['Season'])
data_combined = load_data(seasons)


##########################################################
## Markdown Format

st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@700&display=swap');

    /* Apply Lexend font and bold to all text */
    html, body, [class*="css"] {{
        font-family: 'Lexend', sans-serif;
        font-weight: bold;
        background-color: {background_color};
        color: {text_color};
    }}
    
    /* Customize specific elements if needed */
    h1, h2, h3, h4, h5, h6, p, div, span, label, input, textarea, button {{
        font-family: 'Lexend', sans-serif !important;
        font-weight: bold !important;
    }}

    /* Ensure dropdown and other input elements use the font */
    .stSelectbox, .stTextInput, .stButton {{
        font-family: 'Lexend', sans-serif !important;
        font-weight: bold !important;
    }}
    
    </style>
""", unsafe_allow_html=True)


##########################################################
## Functions

@st.cache_data
def create_donut_chart(value, color):
    global background_color, text_color

    # Data for donut chart
    data = pd.DataFrame({
        'scale': ['empty', '%'],
        'value': [100 - value, value]})
    
    # Base chart with theta and color encoding, no legend
    base = alt.Chart(data).encode(
        theta=alt.Theta(field='value', type='quantitative', stack=True),
        color=alt.Color('scale:N', scale=alt.Scale(range=[color, background_color]), legend=None))

    # Donut chart with adjusted radius to prevent clipping
    pie = base.mark_arc(outerRadius=70, innerRadius=46).properties(width=160, height=160)
    
    # Center text
    text = alt.Chart(pd.DataFrame({'text': [value]})).mark_text(
        size=35,
        color=text_color,
        fontWeight='bold',
        align='center',
        font='Lexend'
    ).encode(
        text='text:N')
    
    donut_chart = pie + text

    return donut_chart

@st.cache_data
def mark(text=''):
    st.markdown(text, unsafe_allow_html=True)


##########################################################
## App Building

# Player selection dropdown
selected_player = st.selectbox("Select a Player", data_combined.index.get_level_values('Name').unique(), label_visibility='hidden')
players = list(data_combined.index.get_level_values('Name').unique())

# Filter seasons based on the selected player
available_seasons = data_combined.xs(selected_player, level='Name').index.get_level_values('Season').unique()
selected_season = st.selectbox("Select a Season", available_seasons, label_visibility='hidden')

# Filter data based on selected player and season
player_data = data_combined.loc[(selected_season, selected_player)]

# Placeholder for image URLs
player_headshot_url = 'https://assets.nhle.com/mugs/nhl/'+selected_season[:4]+str(int(selected_season[:4])+1)+'/'+player_data['Team']+'/'+str(player_data['playerID'])+'.png'
team_logo_url = "https://assets.nhle.com/logos/nhl/svg/"+player_data['Team']+"_light.svg"

# Define the dimensions and styles of headshot box
box_width = 300
box_height = 230
border_thick = 5
margin_left = 17
# Calculate parameters for elements within box
inbox_width, inbox_height = box_width-border_thick*2, box_height-border_thick*2
headshot_width = headshot_height = min(inbox_height*0.95, inbox_width*0.8)  # headshot has equal height & width
logo_width = headshot_width*0.35
horizontal_middle = margin_left + (box_width / 2) - headshot_height/2 - 2
inner_bottom = border_thick - 1
inner_top = - box_height + border_thick - 12
right_side = box_width + margin_left - border_thick - logo_width - 2

# Predefined color variables
hover_color = "#242434"
border_color = background_color
options_background = background_color
typebox_background = "#242434"
typebox_focus_border_color = "#85B7D9"
typebox_font_size = 20
droplist_font_size = 16
scroll_to_top_on_expand = True
font_family = 'Lexend'

# Initialize session state to capture selected player
if 'selected_player' not in st.session_state:
    st.session_state['selected_player'] = players[0]

dropdown_html_js = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family={font_family}:wght@700&display=swap'); /* Font injection */

    .dropdown-container {{
        position: relative;
        overflow: visible;
        z-index: 10;  /* Ensure dropdown appears above other elements */
        width: {box_width-10}px;
        padding: 0px 0px 0px 0px;
    }}

    .dropdown-input {{
        text-align: center;
        width: 100%;
        padding: 10px 10px 10px 10px;
        border-radius: 10px;
        border: 1px solid {border_color};
        font-family: {font_family}, sans-serif;
        font-size: {typebox_font_size}px;
        color: {text_color};
        background-color: {typebox_background};
        position: relative;
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;
        spellcheck: false;  /* Remove all spellcheck underlining */
        autocorrect: off;
        autocapitalize: none;
        highlight: none;
    }}

    .dropdown-input:focus {{
        outline: none;
        border-color: {typebox_focus_border_color};
        box-shadow: 0 0 0 0px rgba(30, 144, 255, 0.2);
    }}

    .dropdown-list {{
        border: 0px solid {border_color};
        border-radius: 10px;
        background-color: {options_background};
        max-height: 500px;
        overflow-y: scroll;
        position: absolute;
        top: 100%;  /* Ensure the options list starts directly below the typebox */
        left: 0;
        width: {box_width+12}px;
        z-index: 11;  /* Ensure dropdown options are above other elements */
        display: none;  /* Hide by default */
    }}
    
    .dropdown-item {{
        padding: 10px;
        font-family: {font_family}, sans-serif;
        font-size: {droplist_font_size}px;
        color: {text_color};
        cursor: pointer;
    }}

    .dropdown-item:hover,
    .dropdown-item.hover {{
        background-color: {hover_color};
    }}

    .dropdown-arrow {{
        position: absolute;
        right: -10px;
        top: 50%;
        transform: translateY(-50%);
        width: 12px;
        height: 12px;
        pointer-events: none;
        fill: {text_color};
        z-index: 12;
    }}

    .show2 {{
        display: block;
    }}
</style>

<div class="dropdown-container" id="dropdownContainer">
    <input id="dropdownInput" type="text" class="dropdown-input" oninput="filterDropdown()" onclick="toggleDropdown(event)" placeholder="Type to search..." value="{players[0]}">
    <div id="dropdownList" class="dropdown-list"></div>
    <svg class="dropdown-arrow" viewBox="0 0 10 5">
        <polyline points="0,0 5,5 10,0"></polyline>
    </svg>
</div>

<script>
    var players = {players};
    var previousSelection = "{players[0]}";
    var hoveredOption = null;

    function populateDropdown(filteredPlayers = players) {{
        var dropdown = document.getElementById('dropdownList');
        dropdown.innerHTML = '';

        var clonedPlayers = [...filteredPlayers];
        var selectedPlayerIndex = clonedPlayers.indexOf(previousSelection);
        if (selectedPlayerIndex !== -1) {{
            clonedPlayers.splice(selectedPlayerIndex, 1);
            dropdown.appendChild(createOptionElement(previousSelection));
        }}

        clonedPlayers.forEach(function(player) {{
            dropdown.appendChild(createOptionElement(player));
        }});
    }}

    function createOptionElement(player) {{
        var option = document.createElement('div');
        option.className = 'dropdown-item';
        option.textContent = player;

        if (player === previousSelection) {{
            option.classList.add('hover');
            hoveredOption = option;
        }}

        option.onclick = function() {{
            selectPlayer(player, option);
        }};

        option.onmouseover = function() {{
            if (hoveredOption) {{
                hoveredOption.classList.remove('hover');
            }}
            option.classList.add('hover');
            hoveredOption = option;
        }};

        return option;
    }}

    function filterDropdown() {{
        var input = document.getElementById('dropdownInput').value.toLowerCase();
        var filteredPlayers = players.filter(function(player) {{
            return player.toLowerCase().includes(input);
        }});
        populateDropdown(filteredPlayers);
        document.getElementById('dropdownList').classList.add('show2');
        
        if (filteredPlayers.length > 0) {{
            var dropdown = document.getElementById('dropdownList');
            var firstOption = dropdown.firstChild;
            if (hoveredOption) {{
                hoveredOption.classList.remove('hover');
            }}
            firstOption.classList.add('hover');
            hoveredOption = firstOption;
        }}
    }}

    function toggleDropdown(event) {{
        event.stopPropagation();
        var dropdown = document.getElementById('dropdownList');
        var inputBox = document.getElementById('dropdownInput');
        populateDropdown(players);

        dropdown.classList.toggle('show2');
        inputBox.setAttribute('spellcheck', 'false');

        if (dropdown.classList.contains('show2') && {str(scroll_to_top_on_expand).lower()}) {{
            dropdown.scrollTop = 0;
        }}
    }}

    function collapseDropdown() {{
        var inputBox = document.getElementById('dropdownInput');
        inputBox.value = previousSelection;
        inputBox.setAttribute('spellcheck', 'false');
        document.getElementById('dropdownList').classList.remove('show2');
    }}

    function selectPlayer(player, option) {{
        var dropdown = document.getElementById('dropdownList');
        var inputBox = document.getElementById('dropdownInput');
        inputBox.value = player;
        dropdown.classList.remove('show2');
        previousSelection = player;
        inputBox.setAttribute('spellcheck', 'false');
        if (hoveredOption) {{
            hoveredOption.classList.remove('hover');
        }}
    }}

    document.getElementById('dropdownInput').addEventListener('keydown', function(e) {{
        var dropdown = document.getElementById('dropdownList');
        var options = dropdown.getElementsByClassName('dropdown-item');

        if (dropdown.classList.contains('show2')) {{
            if (e.key === 'ArrowDown') {{
                if (hoveredOption && hoveredOption.nextSibling) {{
                    hoveredOption.classList.remove('hover');
                    hoveredOption = hoveredOption.nextSibling;
                    hoveredOption.classList.add('hover');
                    scrollIntoViewIfNeeded(hoveredOption, dropdown);
                }} else if (!hoveredOption && options.length > 0) {{
                    hoveredOption = options[0];
                    hoveredOption.classList.add('hover');
                    scrollIntoViewIfNeeded(hoveredOption, dropdown);
                }}
                e.preventDefault();
            }} else if (e.key === 'ArrowUp') {{
                if (hoveredOption && hoveredOption.previousSibling) {{
                    hoveredOption.classList.remove('hover');
                    hoveredOption = hoveredOption.previousSibling;
                    hoveredOption.classList.add('hover');
                    scrollIntoViewIfNeeded(hoveredOption, dropdown);
                }}
                e.preventDefault();
            }} else if (e.key === 'Enter') {{
                if (hoveredOption) {{
                    selectPlayer(hoveredOption.textContent, hoveredOption);
                    document.getElementById('dropdownInput').blur();
                }}
            }} else if (e.key === 'Escape') {{
                document.getElementById('dropdownInput').blur();
            }}
        }}
    }})

    function scrollIntoViewIfNeeded(option, container) {{
        var containerRect = container.getBoundingClientRect();
        var optionRect = option.getBoundingClientRect();
        if (optionRect.top < containerRect.top) {{
            container.scrollTop -= (containerRect.top - optionRect.top);
        }} else if (optionRect.bottom > containerRect.bottom) {{
            container.scrollTop += (optionRect.bottom - containerRect.bottom);
        }}
    }}
    
    function handleBlur() {{
        setTimeout(function() {{
            var dropdown = document.getElementById('dropdownList');
            if (dropdown.classList.contains('show2')) {{
                collapseDropdown();
            }}
        }}, 150);  // Specific ms delay to ensure the click event finishes first
    }}

    document.getElementById('dropdownInput').addEventListener('blur', handleBlur);

    populateDropdown();
</script>
"""

# Render the dropdown HTML
components.html(dropdown_html_js, height=300)



mark(f'''
<style>
/* Container styling */
.teal-box {{
    position: relative;
    background-color: #45818e;
    border: {border_thick}px solid #0c343d;
    border-radius: 10px;
    width: {box_width}px;
    height: {box_height}px;
    margin-left: {margin_left}px;
    z-index: 0;
}}

/* Player headshot styling */
.player-headshot {{
    position: absolute;
    bottom: {inner_bottom}px;
    left: {horizontal_middle}px;
    height: {headshot_height}px;
    z-index: 1;
}}

/* Team logo styling */
.team-logo {{
    position: absolute;
    top: {inner_top}px;
    left: {right_side}px;
    width: {logo_width}px;
    z-index: 2;
}}
</style>
''')

# Make all appear
mark(f'<div class="teal-box">')
mark(f'<img class="player-headshot" src="{player_headshot_url}" alt="{selected_player} Headshot">')
mark(f'<img class="team-logo" src="{team_logo_url}" alt="{player_data['Team']} Logo"> </div>')


# Donut charts for each centrality measure and text below them
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.altair_chart(create_donut_chart(player_data['Betweenness'], '#49c1b1'), use_container_width=True)
    mark('''
    <div style="text-align:center; margin-top:-30px;">
        <span style="font-size:24px;">FLOW</span><br>
        <span style="font-size:17px;">(Betweenness)</span>
    </div>
    ''')
with c2:
    st.altair_chart(create_donut_chart(player_data['PageRank'], '#45dac3'), use_container_width=True)
    mark('''
    <div style="text-align:center; margin-top:-30px;">
        <span style="font-size:24px;">INFLUENCE</span><br>
        <span style="font-size:17px;">(PageRank)</span>
    </div>
    ''')
with c3:
    st.altair_chart(create_donut_chart(player_data['Information'], '#9bd0b2'), use_container_width=True)
    mark('''
    <div style="text-align:center; margin-top:-30px;">
        <span style="font-size:24px;">EFFICIENCY</span><br>
        <span style="font-size:17px;">(Information)</span>
    </div>
    ''')
with c4:
    st.altair_chart(create_donut_chart(player_data['WeightedDegree'], '#3a978d'), use_container_width=True)
    mark('''
    <div style="text-align:center; margin-top:-30px;">
        <span style="font-size:24px;">VOLUME</span><br>
        <span style="font-size:17px;">(Weighted Degree)</span>
    </div>
    ''')

# Bottom text explainer & credits
mark(f''' 
<div style="text-align: center; font-size: 12.3px; margin-top:30px;">
<em>Positional percentile displayed inside pie chart, attribute measured below it, centrality measure in parentheses</em>
</div>
''')  
mark('''
<div style="margin-top:15px; font-size: 14px;">
<span style="text-align:left;">Data: MoneyPuck & Corey Sznajder's A3Z</span>
<span style="float:right;">Metrics & visualizations: lb-hockey.com</span>
</div>
''')
