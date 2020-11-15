from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QListWidget


class DataListItem():

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        del_button = QPushButton('del')
        del_button.setStyleSheet(
            "background-color: #eb5a46; border-radius: 5px; padding: 2px"
        )
        del_button.clicked.connect(parent.remove_item)
        add_button = QPushButton('add')
        add_button.setStyleSheet(
            "background-color: #90ee90; border-radius: 5px; padding: 2px"
        )
        add_button.clicked.connect(parent.add_to_item)
        add_button.clicked.connect(parent.update_data_list)
        label = QLabel(text)

        hwidget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(del_button)
        layout.addWidget(add_button)
        layout.addWidget(label)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        hwidget.setLayout(layout)
        vlayout = QVBoxLayout()
        vlayout.addWidget(hwidget)
        if(len(parent.data.replicate_files[index]) > 1):
            for j in range(1, len(parent.data.replicate_files[index]), 1):
                hlayout = QHBoxLayout()
                hlayout.addWidget(QLabel('-'))
                sub_del_button = QPushButton('del')
                sub_del_button.setStyleSheet(
                  "background-color: #eb5a46; border-radius: 5px; padding: 2px"
                )
                hlayout.addWidget(sub_del_button)
                sub_del_button.clicked.connect(
                    lambda: parent.remove_replicate(j)
                )
                hlayout.addWidget(QLabel(
                    parent.data.replicate_files[index][j].name.split('/')[-1]
                ))
                hlayout.addStretch()
                hlayout.setSizeConstraint(QLayout.SetFixedSize)
                subwidget = QWidget()
                subwidget.setLayout(hlayout)
                vlayout.addWidget(subwidget)
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.addStretch()
        vlayout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(vlayout)
        self.item.setSizeHint(self.widget.sizeHint())
