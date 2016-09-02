import sqlite3
import os

if os.path.isfile('recipe_data'):
    conn = sqlite3.connect('recipe_data')
    cur = conn.cursor()

else:
    conn = sqlite3.connect('recipe_data')
    cur = conn.cursor()
    cur.execute('CREATE TABLE recipes (title TEXT, ingredients TEXT, instructions TEXT)')


def recipe_names():
    cur.execute('SELECT title FROM recipes')
    recipe_list = cur.fetchall()

    recipe_name_list = []
    for item in recipe_list:
        recipe_name_list.append(item[0])

    return recipe_name_list


def recipe_data(selected_recipe):

    cur.execute('SELECT * FROM recipes WHERE title=?', (selected_recipe,))
    recipe = cur.fetchall()

    recipe_title = recipe[0][0]
    recipe_ingredients = recipe[0][1].split(';;')
    recipe_instructions = recipe[0][2]

    return recipe_title, recipe_ingredients, recipe_instructions


def add_new_recipe(title, ingredients, instructions):

    cur.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)',
                (title, ingredients, instructions))

    conn.commit()


def delete_function(item):
    try:
        cur.execute('DELETE FROM recipes WHERE title=?', (item,))
        conn.commit()
    except NameError:
        pass
