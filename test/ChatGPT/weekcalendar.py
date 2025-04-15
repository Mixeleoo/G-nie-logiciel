'''from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QDate
import sys

class WeekView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semaine en vue calendrier")

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(1, 7)  # 1 ligne, 7 colonnes (jours de la semaine)
        self.layout.addWidget(self.table)

        self.btn_next = QPushButton("Semaine suivante")
        self.btn_prev = QPushButton("Semaine précédente")
        self.layout.addWidget(self.btn_prev)
        self.layout.addWidget(self.btn_next)

        self.current_date = QDate.currentDate()
        self.update_week_view()

        self.btn_next.clicked.connect(self.next_week)
        self.btn_prev.clicked.connect(self.prev_week)

    def update_week_view(self):
        start_of_week = self.current_date.addDays(-(self.current_date.dayOfWeek() - 1))  # Lundi
        for i in range(7):
            day = start_of_week.addDays(i)
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(day.toString("dddd")))
            self.table.setItem(0, i, QTableWidgetItem(day.toString("dd/MM/yyyy")))

    def next_week(self):
        self.current_date = self.current_date.addDays(7)
        self.update_week_view()

    def prev_week(self):
        self.current_date = self.current_date.addDays(-7)
        self.update_week_view()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WeekView()
    w.show()
    sys.exit(app.exec())'''

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt6.QtCore import QDate
import calendar


class WeeklyCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendrier Hebdomadaire")
        self.resize(800, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label de la semaine
        self.weekLabel = QLabel()
        layout.addWidget(self.weekLabel)

        # Tableau : 7 colonnes pour Lundi à Dimanche, 10 lignes d'exemple
        self.table = QTableWidget(10, 7)
        layout.addWidget(self.table)

        # Entêtes de colonnes
        self.set_week_headers(QDate.currentDate())

        # Exemple de données : ajout d’un événement le lundi matin
        self.table.setItem(0, 0, QTableWidgetItem("Réunion"))

    def set_week_headers(self, current_date: QDate):
        """Définit les en-têtes de colonnes selon la semaine courante."""
        week_start = current_date.addDays(-current_date.dayOfWeek() + 1)  # Lundi
        self.weekLabel.setText(f"Semaine du {week_start.toString('dd MMM yyyy')}")

        day_names = list(calendar.day_name)  # ['Monday', 'Tuesday', ...]
        french_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

        for i in range(7):
            day = week_start.addDays(i)
            header = f"{french_days[i]}\n{day.toString('dd/MM')}"
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(header))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeeklyCalendar()
    win.show()
    sys.exit(app.exec())
