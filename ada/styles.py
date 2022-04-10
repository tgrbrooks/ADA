# App style
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
    background-color: white;
}
QListWidget::item
{
    background: white; 
}
QListWidget::item:selected
{
    background: white;
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

list_style = """
QListWidget {
    background-color: white;
}
QListWidget::item
{
    background: white; 
}
QListWidget::item:selected
{
    background: white;
}
"""
list_item_style = 'border-bottom: 0.2em black;'

toolbar_style = """
QToolBar {
    background: white;
    border: none;
    spacing: .5em;
}
QToolBar QToolButton{
    background-color: #28a745;
    border-radius: 0.2em;
    padding: 0.2em;
}
QToolBar QToolButton:hover{
    background-color: #1e8235;
    border-radius: 0.2em;
    padding: 0.2em;
}
"""

default_font = 'font-size: 14pt;\
                font-family: Sans;\
                color: #1e8235;'
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

right_label_style = label_style +\
                  'border-top-right-radius: 0.3em; \
                   border-bottom-right-radius: 0.3em;'

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

mid_line_edit_style = default_font_bold +\
                   'border: 0.05em solid #1e8235;\
                   padding: 0.2em;'

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
                       border-radius: 0.4em;\
                       text-align: center;\
                       vertical-align: middle;\
                       padding: 0em 0.2em 0.2em 0.2em;'

add_button_style = default_button_font +\
                   'background-color: #28a745;\
                    border-radius: 0.4em;\
                    text-align: right;\
                    vertical-align: middle;\
                    padding: 0em 0.14em 0.2em 0.2em;'
