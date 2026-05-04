import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Предопределённые задачи
        self.default_tasks = [
            {"name": "Прочитать статью", "type": "study"},
            {"name": "Сделать зарядку", "type": "sport"},
            {"name": "Написать отчёт", "type": "work"},
            {"name": "Повторить конспект", "type": "study"},
            {"name": "Пробежка 5 км", "type": "sport"},
            {"name": "Позвонить клиенту", "type": "work"},
            {"name": "Выучить 10 новых слов", "type": "study"},
            {"name": "Отжимания 50 раз", "type": "sport"},
            {"name": "Собрать встречу", "type": "work"}
        ]

        # Хранилище всех задач (для фильтрации)
        self.all_tasks = self.default_tasks.copy()
        self.filtered_tasks = self.all_tasks.copy()

        # История задач
        self.history = []

        # Загрузка истории из JSON
        self.load_history()

        # Создание GUI
        self.create_widgets()

        # Обновление списка истории
        self.update_history_display()

    def create_widgets(self):
        # Рамка для генерации задачи
        gen_frame = ttk.LabelFrame(self.root, text="Генератор задачи", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.task_label = ttk.Label(gen_frame, text="Нажмите 'Сгенерировать задачу'", font=("Arial", 12))
        self.task_label.pack(pady=5)

        ttk.Button(gen_frame, text="Сгенерировать задачу", command=self.generate_task).pack(pady=5)

        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр по типу", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="Все", variable=self.filter_var, value="all", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Radiobutton(filter_frame, text="Учёба", variable=self.filter_var, value="study", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Radiobutton(filter_frame, text="Спорт", variable=self.filter_var, value="sport", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Radiobutton(filter_frame, text="Работа", variable=self.filter_var, value="work", command=self.apply_filter).pack(side="left", padx=5)

        # Рамка добавления новой задачи
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Название задачи:").grid(row=0, column=0, padx=5, pady=5)
        self.new_task_entry = ttk.Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Тип задачи:").grid(row=1, column=0, padx=5, pady=5)
        self.new_task_type = ttk.Combobox(add_frame, values=["study", "sport", "work"], state="readonly")
        self.new_task_type.set("study")
        self.new_task_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить задачу", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=10)

        # Рамка истории задач
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(history_frame, height=12)
        self.history_listbox.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопка очистки истории
        ttk.Button(self.root, text="Очистить историю", command=self.clear_history).pack(pady=5)

    def generate_task(self):
        if not self.filtered_tasks:
            messagebox.showwarning("Нет задач", "Нет задач для выбранной категории.")
            return

        task = random.choice(self.filtered_tasks)
        task_name = task["name"]
        task_type = task["type"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.task_label.config(text=f"Текущая задача: {task_name} [{task_type.upper()}]")

        # Добавляем в историю
        self.history.append({
            "task": task_name,
            "type": task_type,
            "timestamp": timestamp
        })

        self.save_history()
        self.update_history_display()

    def apply_filter(self):
        filter_type = self.filter_var.get()
        if filter_type == "all":
            self.filtered_tasks = self.all_tasks.copy()
        else:
            self.filtered_tasks = [t for t in self.all_tasks if t["type"] == filter_type]

    def add_task(self):
        new_name = self.new_task_entry.get().strip()
        new_type = self.new_task_type.get()

        # Проверка на пустую строку
        if not new_name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым.")
            return

        # Проверка на дубликат (опционально)
        if any(t["name"].lower() == new_name.lower() for t in self.all_tasks):
            messagebox.showwarning("Предупреждение", "Такая задача уже существует.")
            return

        self.all_tasks.append({"name": new_name, "type": new_type})
        self.apply_filter()  # обновляем фильтрованный список
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{new_name}' добавлена.")

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.history):  # новые сверху
            self.history_listbox.insert(tk.END, f"{entry['timestamp']} — {entry['task']} [{entry['type'].upper()}]")

    def save_history(self):
        with open("tasks_history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists("tasks_history.json"):
            try:
                with open("tasks_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("История очищена", "Все задачи удалены из истории.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()