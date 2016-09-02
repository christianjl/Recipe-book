
def display_output(title, ingredients, instructions):

    recipe_text1 = '<html>\n<body>\n<center>\n<h1>{}</h1>\n<h2>Ingredients:</h2>\n<p>'.format(title)
    recipe_text2 = '<br />'.join(ingredients)
    recipe_text3 = '</p>\n<h2>Instructions</h2>\n<p>{}</p></center>\n</body>\n</html>'.format(instructions)

    recipe_text = recipe_text1 + recipe_text2 + recipe_text3

    return recipe_text
