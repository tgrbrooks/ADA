# Global configuration for the app

# App style/options

main_background = 'QMainWindow {background-color: white;}'
error_background = 'QMainWindow {background-color: #f8d7da;}'
white_background = 'background-color: white;'

tab_style = """
QTabWidget {
  font-size: 12pt;
  font-weight: bold;
  font-family: Sans;
}

QTabWidget::pane {
  border-top: 0.2em solid #1e8235; 
  background: white;
} 

QTabBar::tab {
  background: #28a745; 
  padding: 0.3em 0.8em 0.3em 0.8em;
  color: white;
} 

QTabBar::tab:selected { 
  background: #1e8235; 
  margin-bottom: -0.1em; 
}
"""

scroll_style = """
QListWidget {
    border: 0.08em solid #1e8235;
}
QScrollBar:vertical {
    width: 0.3em;
}
QScrollBar::handle:vertical {
    background: #1e8235;
}
QScrollBar:horizontal {
    height: 0.3em;
}
QScrollBar::handle:horizontal {
    background: #1e8235; 
}
"""

dropdown_style = """
QComboBox {
    font-size: 14pt;
    font-weight: bold;
    font-family: Sans;
    color: #1e8235;
    border:  0.05em solid #1e8235;
    border-top-right-radius: 0.3em;
    border-bottom-right-radius: 0.3em;
    padding: 0.2em;
    selection-background-color: #1e8235;
    selection-color: white;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 1.5em;

    border-left-width: 0.08em;
    border-left-color: #1e8235;
    border-left-style: solid;
    border-top-right-radius: 0.3em;
    border-bottom-right-radius: 0.3em;
}
QComboBox:!editable, QComboBox::drop-down:editable {
    color: #1e8235;
    background: white;
    selection-background-color: #1e8235;
    selection-color: white;
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    color: #1e8235;
    background: white;
    selection-background-color: #1e8235;
    selection-color: white;
}
QComboBox::down-arrow {
    width: 0.3em;
    height: 0.3em;
    background: #1e8235;
}
QComboBox::item:selected {
    font-size: 14pt;
    font-weight: bold;
    font-family: Sans;
    padding: 0.4em;
    background-color: #1e8235;
    color: white;
}
"""

spinbox_style = """
QSpinBox {
    font-size: 14pt;
    font-weight: bold;
    font-family: Sans;
    color: #1e8235;
    border:  0.05em solid #1e8235;
    border-top-right-radius: 0.3em;
    border-bottom-right-radius: 0.3em;
    padding: 0.2em;
    padding-right: 1.2em; /* make room for the arrows */
}
QSpinBox::up-button {
    font-size: 14pt;
    subcontrol-origin: border;
    subcontrol-position: top right;
    border-top-right-radius: 0.3em;
    border:  0.05em solid #1e8235;
    width: 1.2em;
}
QSpinBox::up-button:pressed {
    background: #1e8235;
}
QSpinBox::up-arrow {
    width: 0.2em;
    height: 0.2em;
    background: #1e8235;
}
QSpinBox::down-button {
    font-size: 14pt;
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    border-bottom-right-radius: 0.3em;
    border:  0.05em solid #1e8235;
    width: 1.2em;
}
QSpinBox::down-button:pressed {
    background: #1e8235;
}
QSpinBox::down-arrow {
    width: 0.2em;
    height: 0.2em;
    background: #1e8235;
}
"""

default_font = 'font-size: 14pt;\
                font-family: Sans;'
default_font_bold = 'font-size: 14pt;\
                     font-weight: bold;\
                     font-family: Sans;\
                     color: #1e8235;'
small_font = 'font-size: 12pt;\
              font-family: Sans;\
              color: #1e8235;'
big_font = 'font-size: 28pt;\
            font-family: Sans;'
default_button_font = default_font +\
                       'color: white;'
default_button_font_bold = default_font +\
                       'color: white;\
                        font-weight: bold;'
big_button_font = big_font +\
                  'color: white;'


error_font = 'font-size: 14pt;\
              font-weight: bold;\
              font-family: Sans;\
              color: #721c25;'
default_label_font_bold = default_font +\
                       'color: #1e8235;\
                        font-weight: bold;'
label_style = default_label_font_bold +\
              'background-color: #e3fcec;\
               border: 0.05em solid #1e8235; \
               padding: 0.22em;'
              
top_label_style = label_style +\
                  'border-top-left-radius: 0.3em; \
                   border-top-right-radius: 0.3em;'

left_label_style = label_style +\
                  'border-top-left-radius: 0.3em; \
                   border-bottom-left-radius: 0.3em;'

round_label_style = label_style +\
                  'border-top-left-radius: 0.3em; \
                   border-top-right-radius: 0.3em;\
                   border-bottom-left-radius: 0.3em; \
                   border-bottom-right-radius: 0.3em;'

right_line_edit_style = default_font_bold +\
                  'border-top-right-radius: 0.3em; \
                   border-bottom-right-radius: 0.3em;\
                   border: 0.05em solid #1e8235;\
                   padding: 0.2em;'

#spin_box_style = default_font_bold +\
#                 'border: 0.08em solid #1e8235;\
#                  padding: 0.3em;'

#drop_down_style = default_font +\
#                  'border: 0.08em solid #1e8235;'

main_button_style = 'QPushButton {' +\
                    default_button_font + \
                    'background-color: #28a745;\
                     border-radius: 0.3em;\
                     padding: 0.2em;\
                     } QPushButton:pressed {' +\
                    default_button_font + \
                    'background-color: #1e8235;\
                     border-radius: 0.3em;\
                     padding: 0.2em;}'

big_button_style = 'QPushButton {' +\
                    big_button_font + \
                    'background-color: #28a745;\
                     border-radius: 0.2em;\
                     padding: 0.2em;\
                     } QPushButton:pressed {' +\
                    big_button_font + \
                    'background-color: #1e8235;\
                     border-radius: 0.2em;\
                     padding: 0.2em;}'
                    
delete_button_style = default_button_font +\
                      'background-color: #dc3545;\
                       border-radius: 0.5em;\
                       text-align: center;\
                       vertical-align: middle;\
                       padding: 0em 0.2em 0.2em 0.2em;'

add_button_style = default_button_font +\
                   'background-color: #28a745;\
                    border-radius: 0.5em;\
                    text-align: right;\
                    vertical-align: middle;\
                    padding: 0em 0.14em 0.2em 0.2em;'

list_style = 'QListWidget {' + white_background + '}'
list_item_style = 'border-bottom: 0.2em black;'

xaxis_units = ["seconds", "minutes", "hours", "days"]
info_options = ["none", "reactor", "profile", "title", "date", "time",
                "date+time"]
style_options = ["default", "greyscale", "colour blind", "pastel", "deep"]
font_options = ["sans-serif", "serif", "cursive", "fantasy", "monospace"]
table_row_options = ["profile", "reactor", "gradient", "time to",
                     "average of condition", "condition at time",
                     "fit parameter"]
fit_options = ["flat line", "linear", "quadratic", "exponential"]

# Width and height ratio
wr = 1.
hr = 1.

# Plotting default values

title = ''

# X axis config
xvar = ''
xname = ''
xunit = ''
xmin = -1
xmax = -1
xlog = False

# Y axis config
yvar = ''
yname = ''
yunit = ''
ymin = -1
ymax = -1
ylog = False
ynormlog = False

# Condition y axis config
condition_yvar = ''
condition_yname = ''
condition_yunit = ''
condition_ymin = -1
condition_ymax = -1
condition_ylog = False

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
