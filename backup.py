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