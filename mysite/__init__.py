import os

def print_tree(root, max_depth, level=0):
    if level > max_depth:
        return
    print("│   " * level + "├───" + os.path.basename(root))
    if os.path.isdir(root):
        for item in os.listdir(root):
            item_path = os.path.join(root, item)
            print_tree(item_path, max_depth, level + 1)

print_tree('.', 2)  # Замените 2 на нужный уровень глубины