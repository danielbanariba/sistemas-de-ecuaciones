import os
from anytree import Node, RenderTree

def build_tree(root_path, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = []

    root_node = Node(os.path.basename(root_path))
    nodes = {root_path: root_node}

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filtrar directorios que deben ser ignorados
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for dirname in dirnames:
            dir_full_path = os.path.join(dirpath, dirname)
            nodes[dir_full_path] = Node(dirname, parent=nodes[dirpath])
        for filename in filenames:
            file_full_path = os.path.join(dirpath, filename)
            Node(filename, parent=nodes[dirpath])

    return root_node

def tree_to_markdown(node, level=0):
    indent = '  ' * level
    markdown = f"{indent}|- {node.name}\n"
    for child in node.children:
        markdown += tree_to_markdown(child, level + 1)
    return markdown

def main():
    root_path = '.'  # Change this to your target directory
    ignore_dirs = ['venv', '__pycache__', '.git', ".web", "Lib", "Include", "assets", ".", "Scripts", "env"]  # Add directories you want to ignore
    tree_root = build_tree(root_path, ignore_dirs)
    markdown_output = tree_to_markdown(tree_root)

    with open('directory_structure.md', 'w', encoding='utf-8') as f:
        f.write(markdown_output)

if __name__ == "__main__":
    main()