import tkinter as tk
from tkinter import ttk, messagebox
from avl_tree import AVLTree
from tree_save import Tree_Save


class AVLVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AVL Tree Visualizer")
        self.geometry("1200x800")

        # Инициализация дерева и IO
        self.tree = AVLTree()
        self.tree_save_io = Tree_Save(self.tree)

        # Параметры отрисовки
        self.node_radius = 25
        self.level_gap = 60

        # Создание интерфейса
        self.create_widgets()

        # Загрузка и отрисовка
        self.load_tree_at_start(silent=True)
        self.update_tree()

        # Обработчик закрытия
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Создание интерфейса
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Панель управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Элементы управления
        ttk.Label(control_frame, text="Узел:").pack(side=tk.LEFT, padx=5)
        self.entry = ttk.Entry(control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Добавить", command=self.insert_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить", command=self.delete_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Очистить", command=self.clear_all_nodes).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Сохранить", command=self.save_tree).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Загрузить", command=self.load_tree).pack(side=tk.LEFT, padx=5)

        # Холст с прокруткой
        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame,
                                width=1160,
                                height=650,
                                bg="white",
                                scrollregion=(0, 0, 2000, 2000))

        # прокрутка холста
        h_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        # Размещение прокрутким
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_tree(self):
        success, msg = self.tree_save_io.load_from_file()
        if success:
            self.update_tree()
        messagebox.showinfo("Уведомление", msg)

    def load_tree_at_start(self, silent=True):
        success, msg = self.tree_save_io.load_from_file()
        if not silent:
            messagebox.showinfo("Уведомление", msg)
        return success

    def save_tree(self):
        success, msg = self.tree_save_io.save_to_file()
        messagebox.showinfo("Уведомление", msg)

    def clear_all_nodes(self):
        self.tree.clear()
        self.update_tree()

    def insert_node(self):
        try:
            key = int(self.entry.get())
            self.tree.insert(key)
            self.update_tree()
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")

    def delete_node(self):
        try:
            key = int(self.entry.get())
            self.tree.delete(key)
            self.update_tree()
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")

    def update_tree(self):
        self.canvas.delete("all")

        if not self.tree.root:
            return

        tree_depth = self.tree.get_depth()
        required_width = 60 * (1.7 ** tree_depth)
        required_height = (tree_depth + 2) * self.level_gap

        self.canvas.config(scrollregion=(0, 0, required_width, required_height))
        self.draw_node(self.tree.root, required_width // 2, self.level_gap, required_width // 4)

    def draw_node(self, node, x, y, dx):
        if node:
            if node.left:
                self.draw_line(x, y, x - dx, y + self.level_gap)
                self.draw_node(node.left, x - dx, y + self.level_gap, dx / 2)
            if node.right:
                self.draw_line(x, y, x + dx, y + self.level_gap)
                self.draw_node(node.right, x + dx, y + self.level_gap, dx / 2)

            self.canvas.create_oval(x - self.node_radius,
                                    y - self.node_radius,
                                    x + self.node_radius,
                                    y + self.node_radius,
                                    fill="lightgray",
                                    outline="black")

            self.canvas.create_text(x, y,
                                    text=f"{node.key}",
                                    font=("Times New Roman", 16, "bold italic"))

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1 + self.node_radius,
                                x2, y2 - self.node_radius,
                                width=2, fill="red")

    def on_closing(self):
        self.save_tree()
        self.destroy()


if __name__ == "__main__":
    app = AVLVisualizer()
    app.mainloop()
