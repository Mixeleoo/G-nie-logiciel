from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QListWidget
from src.data_test.list_data_test import *


class TaskOngoingDisplay(QtWidgets.QListWidget):
    def __init__(self, taskpage, task_list):
        super(TaskOngoingDisplay, self).__init__(taskpage)

        self.setGeometry(QtCore.QRect(50, 40, 710, 570))

        # parametrage du font de la qlist
        font = QFont()
        font.setPointSize(15)
        self.setFont(font)

        # TODO Léo gérer récupération
        for t in task :
            if t["ongoing"]:
                item = QtWidgets.QListWidgetItem(t["name"])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.addItem(item)



class TaskFinishedDisplay(QtWidgets.QListWidget):
    def __init__(self, taskpage, task_list):
        super(TaskFinishedDisplay, self).__init__(taskpage)

        self.setGeometry(QtCore.QRect(50, 40, 710, 570))

        # parametrage du font de la qlist
        font = QFont()
        font.setPointSize(15)
        font.setStrikeOut(True)
        self.setFont(font)

        # TODO Léo gérer récupération
        for t in task :
            if t["ongoing"] == False :
                item = QtWidgets.QListWidgetItem(t["name"])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.addItem(item)
