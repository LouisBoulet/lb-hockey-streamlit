import altair as alt

def register_lexend_theme():
    # Register the custom theme
    alt.themes.register('lexend_theme', lambda: {
        'config': {
            'title': {
                'font': 'Lexend',
                'fontSize': 18,
                'fontWeight': 'bold',
            },
            'axis': {
                'labelFont': 'Lexend',
                'labelFontSize': 14,
                'labelFontWeight': 'bold',
                'titleFont': 'Lexend',
                'titleFontSize': 16,
                'titleFontWeight': 'bold',
            },
            'legend': {
                'labelFont': 'Lexend',
                'labelFontSize': 14,
                'labelFontWeight': 'bold',
                'titleFont': 'Lexend',
                'titleFontSize': 16,
                'titleFontWeight': 'bold',
            },
            'mark': {
                'font': 'Lexend',
                'fontSize': 14,
                'fontWeight': 'bold',
            },
            'text': {
                'font': 'Lexend',
                'fontSize': 40,  # Adjust font size if necessary
                'fontWeight': 'bold',
            }
        }
    })

    # Enable the theme
    alt.themes.enable('lexend_theme')

# Register the theme as a function
register_lexend_theme()
