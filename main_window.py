from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QMessageBox
)
from models import create_connection, Employee, Task
from employee_dialog import EmployeeDialog
from task_dialog import TaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление сотрудниками и задачами")
        self.setMinimumSize(750, 400)
        self.session = create_connection()

        layout = QHBoxLayout()
        
        button_layout = QVBoxLayout()
        
        self.show_employees_btn = QPushButton("Показать сотрудников")
        self.show_employees_btn.clicked.connect(self.load_employees)
        button_layout.addWidget(self.show_employees_btn)
        
        self.show_tasks_btn = QPushButton("Показать задачи")
        self.show_tasks_btn.clicked.connect(self.load_tasks)
        button_layout.addWidget(self.show_tasks_btn)
        
        self.add_employee_btn = QPushButton("Добавить сотрудника")
        self.add_employee_btn.clicked.connect(self.add_employee)
        button_layout.addWidget(self.add_employee_btn)
        
        self.edit_employee_btn = QPushButton("Редактировать сотрудника")
        self.edit_employee_btn.clicked.connect(self.edit_employee)
        button_layout.addWidget(self.edit_employee_btn)
        
        self.add_task_btn = QPushButton("Добавить задачу")
        self.add_task_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_task_btn)
        
        self.edit_task_btn = QPushButton("Изменить статус задачи")
        self.edit_task_btn.clicked.connect(self.edit_task)
        button_layout.addWidget(self.edit_task_btn)
        
        self.table_widget = QTableWidget()
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_employees()

    def load_employees(self):
        try:
            self.table_widget.clear()
            employees = self.session.query(Employee).all()
            self.table_widget.setRowCount(len(employees))
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID", "Имя", "Фамилия", "Должность", "Зарплата", "Дата приема"]
            )
            
            for row, employee in enumerate(employees):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(employee.id)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(employee.first_name or ""))
                self.table_widget.setItem(row, 2, QTableWidgetItem(employee.last_name or ""))
                self.table_widget.setItem(row, 3, QTableWidgetItem(employee.position or ""))
                self.table_widget.setItem(row, 4, QTableWidgetItem(str(employee.salary or "")))
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(employee.hire_date or "")))
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки сотрудников: {str(e)}")

    def load_tasks(self):
        try:
            self.table_widget.clear()
            tasks = self.session.query(Task).all()
            self.table_widget.setRowCount(len(tasks))
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID", "Название", "Описание", "Статус", "ID проекта", "ID сотрудника"]
            )
            
            for row, task in enumerate(tasks):
                self.table_widget.setItem(row, 1, QTableWidgetItem(task.task_name or ""))
                self.table_widget.setItem(row, 2, QTableWidgetItem(task.description or ""))
                self.table_widget.setItem(row, 3, QTableWidgetItem(task.status or ""))
                self.table_widget.setItem(row, 4, QTableWidgetItem(str(task.project_id or "")))
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(task.assignee_id or "")))
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки задач: {str(e)}")

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec():
            try:
                employee = Employee(
                    first_name=dialog.first_name.text(),
                    last_name=dialog.last_name.text(),
                    position=dialog.position.text(),
                    salary=float(dialog.salary.text()),
                    hire_date=dialog.hire_date.date().toPython()
                )
                self.session.add(employee)
                self.session.commit()
                self.load_employees()
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {str(e)}")

    def edit_employee(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            try:
                employee_id = int(self.table_widget.item(current_row, 0).text())
                employee = self.session.query(Employee).get(employee_id)
                dialog = EmployeeDialog(self, employee)
                if dialog.exec():
                    employee.first_name = dialog.first_name.text()
                    employee.last_name = dialog.last_name.text()
                    employee.position = dialog.position.text()
                    employee.salary = float(dialog.salary.text())
                    employee.hire_date = dialog.hire_date.date().toPython()
                    self.session.commit()
                    self.load_employees()
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось изменить сотрудника: {str(e)}")

    def add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            try:
                task = Task(
                    task_name=dialog.task_name.text(),
                    description=dialog.description.text(),
                    status=dialog.status.currentText(),
                    project_id=int(dialog.project_id.text()),
                    assignee_id=int(dialog.assignee_id.text())
                )
                self.session.add(task)
                self.session.commit()
                self.load_tasks()
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить задачу: {str(e)}")

    def edit_task(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            try:
                task_id = int(self.table_widget.item(current_row, 0).text())
                task = self.session.query(Task).get(task_id)
                dialog = TaskDialog(self, task)
                dialog.task_name.setEnabled(False)
                dialog.description.setEnabled(False)
                dialog.project_id.setEnabled(False)
                dialog.assignee_id.setEnabled(False)
                if dialog.exec():
                    task.status = dialog.status.currentText()
                    self.session.commit()
                    self.load_tasks()
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось изменить задачу: {str(e)}")