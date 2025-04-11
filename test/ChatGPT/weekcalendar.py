from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
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
    sys.exit(app.exec())