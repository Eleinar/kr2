from PySide6.QtWidgets import (
    QPushButton, QDialog, QFormLayout, QLineEdit,
    QDateEdit
)

from datetime import date

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.setWindowTitle("Сотрудник")
        layout = QFormLayout()
        
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.position = QLineEdit()
        self.salary = QLineEdit()
        self.hire_date = QDateEdit()
        self.hire_date.setDate(date.today())
        
        layout.addRow("Имя:", self.first_name)
        layout.addRow("Фамилия:", self.last_name)
        layout.addRow("Должность:", self.position)
        layout.addRow("Зарплата:", self.salary)
        layout.addRow("Дата приема:", self.hire_date)
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
        
        if employee:
            self.first_name.setText(employee.first_name)
            self.last_name.setText(employee.last_name)
            self.position.setText(employee.position)
            self.salary.setText(str(employee.salary))
            self.hire_date.setDate(employee.hire_date)