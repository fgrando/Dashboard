#!/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QCheckBox, QLineEdit, QHBoxLayout,
    QLabel, QPushButton, QDateTimeEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QBrush, QColor, QFont

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasklist.json")

class TaskViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskList v1.0")
        self.resize(700, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Filter bar
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filter tasks by text...")
        self.filter_edit.textChanged.connect(self.filter_tasks)
        self.layout.addWidget(self.filter_edit)

        # Task Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Date", "Text"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # Done
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)   # Date
        header.setSectionResizeMode(2, QHeaderView.Stretch)            # Text
        self.table.itemChanged.connect(self.handle_item_edit)
        self.layout.addWidget(self.table)

        # Add Task Form
        form_layout = QHBoxLayout()

        self.datetime_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.datetime_input.setCalendarPopup(True)
        form_layout.addWidget(QLabel("Date & Time:"))
        form_layout.addWidget(self.datetime_input)

        self.text_input = QLineEdit()
        form_layout.addWidget(QLabel("Task Text:"))
        form_layout.addWidget(self.text_input)

        self.add_button = QPushButton("&Add Task")
        self.add_button.clicked.connect(self.add_task)
        form_layout.addWidget(self.add_button)

        self.layout.addLayout(form_layout)

        # Load and display tasks
        self.all_tasks = self.load_tasks()
        self.populate_table()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w") as f:
                json.dump(self.all_tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def populate_table(self, filtered_tasks=None):
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        tasks = filtered_tasks if filtered_tasks is not None else self.all_tasks

        # Sort tasks by datetime (ascending)
        try:
            tasks = sorted(
                tasks,
                key=lambda task: datetime.strptime(task["datetime"], "%Y-%m-%d %H:%M")
            )
        except Exception as e:
            print("Error while sorting tasks:", e)

        for task in tasks:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Checkbox
            chk = QCheckBox()
            chk.setChecked(task.get("done", False))
            chk.stateChanged.connect(lambda _, r=row: self.toggle_complete(r))
            self.table.setCellWidget(row, 0, chk)

            # Date item
            date_str = task["datetime"]
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(date_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 1, date_item)

            # Text item
            text_item = QTableWidgetItem(task["text"])
            text_item.setFlags(text_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 2, text_item)

            # Expired tasks in red
            task_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            is_past = task_date < datetime.now()

            white_brush = QBrush(QColor("white"))
            red_brush = QBrush(QColor("red"))
            if is_past and not task.get("done", False):
                date_item.setForeground(white_brush)
                date_item.setBackground(red_brush)

            if task.get("done", False):
                font = text_item.font()
                font.setStrikeOut(True)
                text_item.setFont(font)

        self.table.blockSignals(False)

    def toggle_complete(self, row):
        chkbox = self.table.cellWidget(row, 0)
        is_checked = chkbox.isChecked()

        text_item = self.table.item(row, 2)
        font = text_item.font()
        font.setStrikeOut(is_checked)
        text_item.setFont(font)

        date = self.table.item(row, 1).text()
        text = self.table.item(row, 2).text()

        for task in self.all_tasks:
            if task["datetime"] == date and task["text"] == text:
                task["done"] = is_checked
                break

        self.save_tasks()

    def handle_item_edit(self, item):
        row = item.row()
        new_date = self.table.item(row, 1).text()
        new_text = self.table.item(row, 2).text()
        done = self.table.cellWidget(row, 0).isChecked()

        try:
            datetime.strptime(new_date, "%Y-%m-%d %H:%M")
        except ValueError:
            return  # Ignore invalid datetime format

        # Update task in the model
        if row < len(self.all_tasks):
            self.all_tasks[row]["datetime"] = new_date
            self.all_tasks[row]["text"] = new_text
            self.all_tasks[row]["done"] = done
            self.save_tasks()
            self.populate_table()

    def filter_tasks(self):
        keyword = self.filter_edit.text().lower()
        if not keyword:
            self.populate_table()
        else:
            filtered = [task for task in self.all_tasks if keyword in task["text"].lower()]
            self.populate_table(filtered)

    def add_task(self):
        text = self.text_input.text().strip()
        if not text:
            return  # ignore empty

        dt = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm")
        new_task = {
            "datetime": dt,
            "text": text,
            "done": False
        }

        self.all_tasks.append(new_task)
        self.save_tasks()
        self.populate_table()

        # Reset input
        self.text_input.clear()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TaskViewer()
    viewer.show()
    sys.exit(app.exec_())
