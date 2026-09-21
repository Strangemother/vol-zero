import ast

# convert a file into another format using AST conversion.
import ast


def main(filename):

    source = ''
    with open(filename, 'r') as stream:
        source = stream.read()

    tree = ast.parse(source)
    step_tree(tree)


def step_tree(tree):
    pass

if __name__ == '__main__':
    filen = 'test_file.py'
    main(filen)
