import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os


class StoreComparatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Сравнение ID магазинов")
        self.root.geometry("900x700")

        # Переменные для хранения путей к файлам
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        # Переменные для режимов ввода
        self.input_mode_file1 = tk.BooleanVar(value=True)
        self.input_mode_file2 = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для выбора файлов
        files_frame = tk.LabelFrame(main_frame, text="Выбор файлов", padx=5, pady=5)
        files_frame.pack(fill=tk.X, pady=(0, 10))

        # Первый файл
        file1_main_frame = tk.LabelFrame(files_frame, text="Файл 1", padx=5, pady=5)
        file1_main_frame.pack(fill=tk.X, pady=2)

        # Режим ввода для первого файла
        mode_frame1 = tk.Frame(file1_main_frame)
        mode_frame1.pack(fill=tk.X, pady=(0, 5))

        tk.Radiobutton(mode_frame1, text="Загрузить из файла", variable=self.input_mode_file1, value=True,
                       command=self.toggle_input_mode_1).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame1, text="Ввести вручную", variable=self.input_mode_file1, value=False,
                       command=self.toggle_input_mode_1).pack(side=tk.LEFT, padx=(10, 0))

        # Фрейм для файла 1
        self.file1_file_frame = tk.Frame(file1_main_frame)
        self.file1_file_frame.pack(fill=tk.X, pady=2)

        tk.Label(self.file1_file_frame, text="Файл:", width=8, anchor="w").pack(side=tk.LEFT)
        tk.Entry(self.file1_file_frame, textvariable=self.file1_path, state="readonly").pack(side=tk.LEFT, fill=tk.X,
                                                                                             expand=True, padx=5)
        tk.Button(self.file1_file_frame, text="Обзор", command=self.browse_file1).pack(side=tk.RIGHT)

        # Фрейм для ручного ввода файла 1
        self.file1_text_frame = tk.Frame(file1_main_frame)
        self.file1_text_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        self.file1_text_frame.pack_forget()  # Скрываем по умолчанию

        tk.Label(self.file1_text_frame, text="Содержимое файла 1:").pack(anchor="w")
        self.file1_text_area = scrolledtext.ScrolledText(self.file1_text_frame, wrap=tk.WORD, height=8)
        self.file1_text_area.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Второй файл
        file2_main_frame = tk.LabelFrame(files_frame, text="Файл 2", padx=5, pady=5)
        file2_main_frame.pack(fill=tk.X, pady=2)

        # Режим ввода для второго файла
        mode_frame2 = tk.Frame(file2_main_frame)
        mode_frame2.pack(fill=tk.X, pady=(0, 5))

        tk.Radiobutton(mode_frame2, text="Загрузить из файла", variable=self.input_mode_file2, value=True,
                       command=self.toggle_input_mode_2).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame2, text="Ввести вручную", variable=self.input_mode_file2, value=False,
                       command=self.toggle_input_mode_2).pack(side=tk.LEFT, padx=(10, 0))

        # Фрейм для файла 2
        self.file2_file_frame = tk.Frame(file2_main_frame)
        self.file2_file_frame.pack(fill=tk.X, pady=2)

        tk.Label(self.file2_file_frame, text="Файл:", width=8, anchor="w").pack(side=tk.LEFT)
        tk.Entry(self.file2_file_frame, textvariable=self.file2_path, state="readonly").pack(side=tk.LEFT, fill=tk.X,
                                                                                             expand=True, padx=5)
        tk.Button(self.file2_file_frame, text="Обзор", command=self.browse_file2).pack(side=tk.RIGHT)

        # Фрейм для ручного ввода файла 2
        self.file2_text_frame = tk.Frame(file2_main_frame)
        self.file2_text_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        self.file2_text_frame.pack_forget()  # Скрываем по умолчанию

        tk.Label(self.file2_text_frame, text="Содержимое файла 2:").pack(anchor="w")
        self.file2_text_area = scrolledtext.ScrolledText(self.file2_text_frame, wrap=tk.WORD, height=8)
        self.file2_text_area.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # Папка для сохранения результатов
        output_frame = tk.Frame(files_frame)
        output_frame.pack(fill=tk.X, pady=(10, 2))

        tk.Label(output_frame, text="Сохранить в:", width=10, anchor="w").pack(side=tk.LEFT)
        tk.Entry(output_frame, textvariable=self.output_dir, state="readonly").pack(side=tk.LEFT, fill=tk.X,
                                                                                    expand=True, padx=5)
        tk.Button(output_frame, text="Обзор", command=self.browse_output_dir).pack(side=tk.RIGHT)

        # Кнопка запуска
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.run_button = tk.Button(button_frame, text="Сравнить файлы", command=self.compare_files, bg="#4CAF50",
                                    fg="white", font=("Arial", 10, "bold"))
        self.run_button.pack(pady=10)

        # Фрейм для результатов
        results_frame = tk.LabelFrame(main_frame, text="Результаты", padx=5, pady=5)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем вкладки для результатов
        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка для ID только в первом файле
        self.only_file1_frame = tk.Frame(notebook)
        notebook.add(self.only_file1_frame, text="Только в файле 1")

        self.result1_text = scrolledtext.ScrolledText(self.only_file1_frame, wrap=tk.WORD)
        self.result1_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Вкладка для ID только во втором файле
        self.only_file2_frame = tk.Frame(notebook)
        notebook.add(self.only_file2_frame, text="Только в файле 2")

        self.result2_text = scrolledtext.ScrolledText(self.only_file2_frame, wrap=tk.WORD)
        self.result2_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопки управления результатами
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(controls_frame, text="Копировать результат 1",
                  command=lambda: self.copy_result(self.result1_text)).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Копировать результат 2",
                  command=lambda: self.copy_result(self.result2_text)).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Сохранить в файл", command=self.save_results_to_file).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Очистить", command=self.clear_results).pack(side=tk.RIGHT, padx=5)

    def toggle_input_mode_1(self):
        """Переключение режима ввода для первого файла"""
        if self.input_mode_file1.get():
            self.file1_file_frame.pack(fill=tk.X, pady=2)
            self.file1_text_frame.pack_forget()
        else:
            self.file1_file_frame.pack_forget()
            self.file1_text_frame.pack(fill=tk.BOTH, expand=True, pady=2)

    def toggle_input_mode_2(self):
        """Переключение режима ввода для второго файла"""
        if self.input_mode_file2.get():
            self.file2_file_frame.pack(fill=tk.X, pady=2)
            self.file2_text_frame.pack_forget()
        else:
            self.file2_file_frame.pack_forget()
            self.file2_text_frame.pack(fill=tk.BOTH, expand=True, pady=2)

    def browse_file1(self):
        filename = filedialog.askopenfilename(
            title="Выберите первый файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file1_path.set(filename)

    def browse_file2(self):
        filename = filedialog.askopenfilename(
            title="Выберите второй файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file2_path.set(filename)

    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Выберите папку для сохранения результатов")
        if directory:
            self.output_dir.set(directory)

    def read_ids_from_file(self, file_path):
        """Читает ID магазинов из файла и возвращает их как множество."""
        with open(file_path, 'r', encoding='utf-8') as file:
            ids = set(line.strip() for line in file if line.strip())
        return ids

    def read_ids_from_text(self, text_content):
        """Читает ID магазинов из текста и возвращает их как множество."""
        lines = text_content.strip().split('\n')
        ids = set(line.strip() for line in lines if line.strip())
        return ids

    def write_ids_to_file(self, ids, output_file):
        """Записывает множество ID в файл, каждый ID на новой строке."""
        with open(output_file, 'w', encoding='utf-8') as file:
            for id_ in sorted(ids):
                file.write(f"{id_}\n")

    def copy_result(self, text_widget):
        """Копирует содержимое текстового виджета в буфер обмена."""
        try:
            content = text_widget.get(1.0, tk.END).strip()
            if content and content != "Нет уникальных ID":
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                # Обновляем буфер обмена
                self.root.update()
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена!")
            elif content == "Нет уникальных ID":
                messagebox.showwarning("Предупреждение", "Нет данных для копирования!")
            else:
                messagebox.showwarning("Предупреждение", "Нет данных для копирования!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать в буфер обмена: {str(e)}")

    def save_results_to_file(self):
        """Сохраняет результаты в отдельный файл"""
        try:
            # Получаем содержимое обоих результатов
            result1_content = self.result1_text.get(1.0, tk.END).strip()
            result2_content = self.result2_text.get(1.0, tk.END).strip()

            if not self.output_dir.get():
                messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для сохранения!")
                return

            # Создаем общий файл с результатами
            combined_file = os.path.join(self.output_dir.get(), "combined_results.txt")
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write("=== Только в файле 1 ===\n")
                f.write(result1_content if result1_content != "Нет уникальных ID" else "Нет уникальных ID")
                f.write("\n\n=== Только в файле 2 ===\n")
                f.write(result2_content if result2_content != "Нет уникальных ID" else "Нет уникальных ID")

            messagebox.showinfo("Успех", f"Результаты сохранены в файл:\n{combined_file}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def clear_results(self):
        """Очищает результаты."""
        self.result1_text.delete(1.0, tk.END)
        self.result2_text.delete(1.0, tk.END)
        messagebox.showinfo("Успех", "Результаты очищены!")

    def compare_files(self):
        """Основная функция сравнения файлов."""
        # Проверяем, что выбрана папка для сохранения результатов
        if not self.output_dir.get():
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для сохранения результатов!")
            return

        try:
            # Читаем ID из первого источника
            if self.input_mode_file1.get():
                # Из файла
                if not self.file1_path.get():
                    messagebox.showerror("Ошибка", "Пожалуйста, выберите первый файл!")
                    return
                ids_file1 = self.read_ids_from_file(self.file1_path.get())
            else:
                # Из текста
                text_content = self.file1_text_area.get(1.0, tk.END).strip()
                if not text_content:
                    messagebox.showerror("Ошибка", "Пожалуйста, введите содержимое первого файла!")
                    return
                ids_file1 = self.read_ids_from_text(text_content)

            # Читаем ID из второго источника
            if self.input_mode_file2.get():
                # Из файла
                if not self.file2_path.get():
                    messagebox.showerror("Ошибка", "Пожалуйста, выберите второй файл!")
                    return
                ids_file2 = self.read_ids_from_file(self.file2_path.get())
            else:
                # Из текста
                text_content = self.file2_text_area.get(1.0, tk.END).strip()
                if not text_content:
                    messagebox.showerror("Ошибка", "Пожалуйста, введите содержимое второго файла!")
                    return
                ids_file2 = self.read_ids_from_text(text_content)

            # Находим ID, которые есть только в первом файле
            only_in_file1 = ids_file1 - ids_file2

            # Находим ID, которые есть только во втором файле
            only_in_file2 = ids_file2 - ids_file1

            # Определяем пути для выходных файлов
            output_file1 = os.path.join(self.output_dir.get(), "only_in_file1.txt")
            output_file2 = os.path.join(self.output_dir.get(), "only_in_file2.txt")

            # Записываем результаты в файлы
            self.write_ids_to_file(only_in_file1, output_file1)
            self.write_ids_to_file(only_in_file2, output_file2)

            # Отображаем результаты в GUI
            self.result1_text.delete(1.0, tk.END)
            self.result2_text.delete(1.0, tk.END)

            # Заполняем первый результат
            if only_in_file1:
                for id_ in sorted(only_in_file1):
                    self.result1_text.insert(tk.END, f"{id_}\n")
            else:
                self.result1_text.insert(tk.END, "Нет уникальных ID")

            # Заполняем второй результат
            if only_in_file2:
                for id_ in sorted(only_in_file2):
                    self.result2_text.insert(tk.END, f"{id_}\n")
            else:
                self.result2_text.insert(tk.END, "Нет уникальных ID")

            # Показываем сообщение об успехе
            messagebox.showinfo(
                "Успех",
                f"Сравнение завершено!\n\n"
                f"Только в файле 1: {len(only_in_file1)} ID\n"
                f"Только в файле 2: {len(only_in_file2)} ID\n\n"
                f"Результаты сохранены в:\n{output_file1}\n{output_file2}"
            )

        except FileNotFoundError as e:
            messagebox.showerror("Ошибка", f"Файл не найден: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


def main():
    root = tk.Tk()
    app = StoreComparatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()