import os
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QGridLayout, \
    QComboBox, QLineEdit, QListWidget, QAction, QMainWindow, QTabWidget, QTextEdit, QTableWidget, \
    QListWidgetItem, QTextBrowser
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QIcon
import html_print
import SQL_reader
import sqlite3


class CreateNewRecipe(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        self.recipe_name_label = QLabel('Title:')
        self.recipe_name_box = QLineEdit()
        self.ingredient_list_label = QLabel('Ingredients:')

        self.ingredient_list = QTableWidget(25, 1)
        self.ingredient_list.setColumnWidth(0, 350)
        self.ingredient_list.setHorizontalHeaderLabels(['Ingredients'])
        self.instructions_label = QLabel('Instructions:')
        self.instructions_box = QTextEdit()
        self.save_button = QPushButton('Add')
        self.save_button.clicked.connect(lambda: self.submit_recipe())

        self.setGeometry(600, 300, 500, 500)

        self.grid.addWidget(self.recipe_name_label, 0, 0)
        self.grid.addWidget(self.recipe_name_box, 0, 1)
        self.grid.addWidget(self.ingredient_list_label, 2, 0)
        self.grid.addWidget(self.ingredient_list, 2, 1)
        self.grid.addWidget(self.instructions_label, 3, 0)
        self.grid.addWidget(self.instructions_box, 3, 1)
        self.grid.addWidget(self.save_button, 4, 0, 1, 2)
        self.setLayout(self.grid)
        self.setWindowTitle('New Recipe')

    def submit_recipe(self):

        new_title = self.recipe_name_box.text()
        new_instructions = self.instructions_box.toPlainText()

        new_ingredient_list = []

        for i in range(25):
            new_ingredient = self.ingredient_list.item(i, 0)
            if new_ingredient is not None:
                new_ingredient_list.append(new_ingredient.text())

        new_ingredients = ';;'.join(new_ingredient_list)
        SQL_reader.add_new_recipe(new_title, new_ingredients, new_instructions)

        self.close()


def add_new_recipe():
    global new_recipe_window
    new_recipe_window = CreateNewRecipe()
    new_recipe_window.show()


class DisplayRecipe(QWidget):
    def __init__(self):
        super().__init__()
        self.text_area = QTextBrowser()


class EditRecipe(QWidget):
    def __init__(self):
        super().__init__()
        self.text_area = QTextBrowser()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        recipe_name_label = QLabel('Title:')
        recipe_name_box = QLineEdit()
        ingredient_list_label = QLabel('Ingredients')
        ingredient_list = QListWidget()
        instructions_label = QLabel('Instructions')
        instructions_box = QTextEdit()
        save_button = QPushButton('Save')

        self.grid.addWidget(recipe_name_label, 0, 0)
        self.grid.addWidget(recipe_name_box, 0, 1)
        self.grid.addWidget(ingredient_list_label, 1, 0)
        self.grid.addWidget(ingredient_list, 1, 1)
        self.grid.addWidget(instructions_label, 2, 0)
        self.grid.addWidget(instructions_box, 2, 1)
        self.grid.addWidget(save_button, 3, 0, 1, 2)
        self.setLayout(self.grid)


class DisplayWindow(QTabWidget):

    def __init__(self):
        super().__init__()
        self.tab1 = DisplayRecipe()
        self.tab2 = EditRecipe()

        self.addTab(self.tab1, 'Display')
        self.addTab(self.tab2, 'Edit')


class RecipeData(QWidget):
    def __init__(self):
        super().__init__()

        self.current_item = 0

        grid = QGridLayout()
        grid.setSpacing(15)

        # Widgets
        type_label = QLabel('Type:')
        type_label.setFixedWidth(250)
        type_combo_box = QComboBox(self)
        type_combo_box.setFixedWidth(250)
        combobox_items = ['All', 'Starter', 'Snacks', 'Breakfast', 'Lunch/Dinner']
        type_combo_box.addItems(combobox_items)
        search_label = QLabel('Search:')
        search_label.setFixedWidth(250)
        search_input = QLineEdit()
        search_input.setFixedWidth(250)
        self.list_box = QListWidget()
        self.list_box.setFixedWidth(250)

        # New recipe button
        self.new_recipe_button = QPushButton()
        self.new_recipe_button.setIcon(QIcon('add.png'))
        self.new_recipe_button.setIconSize(QSize(28, 28))
        self.new_recipe_button.setMaximumSize(32, 32)
        self.new_recipe_button.setStyleSheet("background-color: white")
        self.new_recipe_button.setStatusTip('Add New Recipe')
        self.new_recipe_button.clicked.connect(lambda: add_new_recipe())

        # Add to shopping list button
        self.add_to_shopping_button = QPushButton()
        self.add_to_shopping_button.setIcon(QIcon('shopping.png'))
        self.add_to_shopping_button.setIconSize(QSize(32, 32))
        self.add_to_shopping_button.setMaximumSize(32, 32)
        self.add_to_shopping_button.setStyleSheet("background-color: white")
        self.add_to_shopping_button.setStatusTip('Add Recipe To Shopping List')

        # Refresh data button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon('refresh.png'))
        self.refresh_button.setIconSize(QSize(26, 26))
        self.refresh_button.setMaximumSize(32, 32)
        self.refresh_button.setStyleSheet("background-color: white")
        self.refresh_button.setStatusTip('Refresh List')

        # Delete recipe button
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon('delete.png'))
        self.delete_button.setIconSize(QSize(28, 28))
        self.delete_button.setMaximumSize(32, 32)
        self.delete_button.setStyleSheet("background-color: white")
        self.delete_button.setStatusTip('Delete Recipe')
        self.delete_button.clicked.connect(lambda: self.delete_recipe())

        self.text_area = QTabWidget()
        # text_edit_area = EditRecipe()
        self.text_area.tab1 = QTextEdit()
        self.text_area.tab2 = EditRecipe()

        self.text_area.addTab(self.text_area.tab1, 'Display')
        self.text_area.addTab(self.text_area.tab2, 'Edit')

        # Layout of widgets on grid
        grid.addWidget(type_label, 0, 0,)
        grid.addWidget(type_combo_box, 1, 0)
        grid.addWidget(search_label, 2, 0)
        grid.addWidget(search_input, 3, 0)
        grid.addWidget(self.list_box, 4, 0)

        grid.addWidget(self.new_recipe_button, 0, 1)
        grid.addWidget(self.add_to_shopping_button, 1, 1)
        grid.addWidget(self.refresh_button, 2, 1)
        grid.addWidget(self.delete_button, 3, 1)

        grid.addWidget(self.text_area, 0, 2, 5, 1)

        self.setLayout(grid)

        self.populate_recipe_list()

    def populate_recipe_list(self):
        self.list_box.clear()
        recipe_names = SQL_reader.recipe_names()
        for name in recipe_names:
            QListWidgetItem(str(name), self.list_box)

        self.list_box.itemClicked.connect(self.show_recipe)

    def show_recipe(self, item):
        title, ingredients, instructions = SQL_reader.recipe_data(item.text())
        recipe_text = html_print.display_output(title, ingredients, instructions)
        self.text_area.tab1.setHtml(recipe_text)
        self.current_item = item.text()
        return

    def delete_recipe(self):
        SQL_reader.delete_function(self.current_item)
        self.populate_recipe_list()


class TabWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tab1 = RecipeData()
        #TODO
        #self.tab2 = ShoppingList()

        self.addTab(self.tab1, 'Recipes')
        #self.addTab(self.tab2, 'Shopping List')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_content = TabWindow()
        self.setCentralWidget(self.window_content)
        self.setGeometry(300, 300, 830, 600)
        self.setWindowTitle('Recipes')

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('Options')

        new_recipe = QAction('New Recipe', self)
        refresh = QAction('Refresh', self)
        exit_action = QAction('Exit', self)

        new_recipe.triggered.connect(lambda: add_new_recipe())
        refresh.triggered.connect(self.window_content.tab1.populate_recipe_list)

        file_menu.addAction(new_recipe)
        file_menu.addAction(refresh)
        file_menu.addAction(exit_action)

        new_recipe.setStatusTip('Add New Recipe')
        refresh.setStatusTip('Refresh Data To Display Newly Added Recipes')
        exit_action.setStatusTip('Exit application')

        self.statusBar()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
