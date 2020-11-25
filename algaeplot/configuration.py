# Global configuration for the app

# App style/options

main_background = 'background-color: #6c757d;'

default_font = 'font-size: 14pt;\
                font-family: SansSerif;'
default_font_bold = 'font-size: 14pt;\
                     font-weight: bold;\
                     font-family: SansSerif;'
small_font = 'font-size: 12pt;\
              font-family: SansSerif;'
big_font = 'font-size: 28pt;\
            font-family: SansSerif;'
default_button_font = default_font +\
                       'color: white;'
default_button_font_bold = default_font +\
                       'color: white;\
                        font-weight: bold;'
big_button_font = big_font +\
                  'color: white;'

label_style = default_button_font_bold +\
              'background-color: #6c757d;\
               padding: 5px;'
              
top_label_style = label_style +\
                  'border-top-left-radius: 5px; \
                   border-top-right-radius: 5px;'

left_label_style = label_style +\
                  'border-top-left-radius: 5px; \
                   border-bottom-left-radius: 5px;'

round_label_style = label_style +\
                  'border-top-left-radius: 5px; \
                   border-top-right-radius: 5px;\
                   border-bottom-left-radius: 5px; \
                   border-bottom-right-radius: 5px;'

right_line_edit_style = default_font_bold +\
                  'border-top-right-radius: 5px; \
                   border-bottom-right-radius: 5px;\
                   border: 2px solid #6c757d;\
                   padding: 3px;'

spin_box_style = default_font_bold +\
                 'border: 2px solid #6c757d;\
                  padding: 3px;'

drop_down_style = default_font +\
                  'border: 1px solid #6c757d;'

main_button_style = 'QPushButton {' +\
                    default_button_font + \
                    'background-color: #007bff;\
                     border-radius: 5px;\
                     padding: 2px;\
                     } QPushButton:pressed {' +\
                    default_button_font + \
                    'background-color: #003cff;\
                     border-radius: 5px;\
                     padding: 2px;}'

big_button_style = 'QPushButton {' +\
                    big_button_font + \
                    'background-color: #007bff;\
                     border-radius: 5px;\
                     padding: 2px;\
                     } QPushButton:pressed {' +\
                    big_button_font + \
                    'background-color: #003cff;\
                     border-radius: 5px;\
                     padding: 2px;}'
                    
delete_button_style = default_button_font_bold +\
                      'background-color: #dc3545;\
                       border-radius: 8px;\
                       text-align: center;\
                       vertical-align: middle;\
                       padding: 2px;'
add_button_style = default_button_font_bold +\
                   'background-color: #28a745;\
                    border-radius: 8px;\
                    text-align: right;\
                    vertical-align: middle;\
                    padding: 2px;'

list_item_style = 'border-bottom: 2px black;'

xaxis_units = ["seconds", "minutes", "hours", "days"]
info_options = ["none", "reactor", "profile", "title", "date", "time",
                "date+time"]
style_options = ["default", "greyscale", "colour blind", "pastel", "deep"]
font_options = ["sans-serif", "serif", "cursive", "fantasy", "monospace"]
table_row_options = ["profile", "reactor", "gradient", "time to",
                     "average of condition", "condition at time",
                     "fit parameter"]
fit_options = ["flat line", "linear", "quadratic", "exponential"]

# Plotting default values

title = ''

# X axis config
xvar = ''
xname = ''
xunit = ''
xmin = -1
xmax = -1

# Y axis config
yvar = ''
yname = ''
yunit = ''
ymin = -1
ymax = -1

# Condition y axis config
condition_yvar = ''
condition_yname = ''
condition_yunit = ''
condition_ymin = -1
condition_ymax = -1

# Data config
smooth = False
align = False
y_alignment = -1
auto_remove = False
remove_above = -1
remove_below = -1
downsample = -1
condition_average = -1
show_events = False

# Measurement config
cursor = False
# Legend config
legend = False
condition_legend = False
legend_title = ''
condition_legend_title = ''
label_names = []
condition_label_names = []
extra_info = 'none'
condition_extra_info = 'none'
only_extra = False
condition_only_extra = False

# Style config
style = ''
font_style = ''
title_size = -1
legend_size = -1
label_size = -1
line_width = -1
axis_colour = -1
grid = False

# Stats config
std_err = False
