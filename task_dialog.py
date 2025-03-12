from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton

class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowTitle("Задача")
        layout = QFormLayout()
        
        self.task_name = QLineEdit()
        self.description = QLineEdit()
        self.status = QComboBox()
        self.status.addItems(['В процессе', 'Завершена', 'Отменена'])
        self.project_id = QLineEdit()
        self.assignee_id = QLineEdit()
        
        layout.addRow("Название:", self.task_name)
        layout.addRow("Описание:", self.description)
        layout.addRow("Статус:", self.status)
        layout.addRow("ID проекта:", self.project_id)
        layout.addRow("ID сотрудника:", self.assignee_id)
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
        
        if task:
            self.task_name.setText(task.task_name)
            self.description.setText(task.description)
            self.status.setCurrentText(task.status)
            self.project_id.setText(str(task.project_id))
            self.assignee_id.setText(str(task.assignee_id))