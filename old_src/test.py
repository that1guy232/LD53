import ast
import sys
import os
import builtins

class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.ignore_names = {"any", "all", "type"}
        self.builtin_names = set(dir(builtins))

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id not in self.builtin_names:
            class_name = node.func.id
            self.imports.add(f"from {class_name} import {class_name}")
        self.generic_visit(node)

class ClassExtractor(ast.NodeTransformer):
    def __init__(self, source_code):
        self.source_code = source_code
        self.class_names = []
        self.global_code_lines = []

    def visit_ClassDef(self, node):
        self.class_names.append(node.name)
        class_code_lines = []
        imports = []

        for base in node.bases:
            if isinstance(base, ast.Name):
                imports.append(f"from {base.id} import {base.id}")

        import_collector = ImportCollector()
        import_collector.visit(node)

        class_imports = set(imports) | import_collector.imports

        if class_imports:
            class_code_lines.append("\n".join(class_imports))

        for line_num in range(node.lineno - 1, node.end_lineno):
            class_code_lines.append(self.source_code.splitlines()[line_num])

        class_code = "\n".join(class_code_lines)
        output_directory = "output"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with open(os.path.join(output_directory, f"{node.name}.py"), "w") as file:
            file.write(class_code)

        return node

    def visit_Module(self, node):
        for item in node.body:
            if not isinstance(item, ast.ClassDef):
                start_line = item.lineno - 1
                end_line = item.end_lineno
                for line_num in range(start_line, end_line):
                    self.global_code_lines.append(self.source_code.splitlines()[line_num])
        self.generic_visit(node)

    def create_main_file(self, output_directory):
        with open(os.path.join(output_directory, "main.py"), "w") as main_file:
            for class_name in self.class_names:
                main_file.write(f"from {class_name} import {class_name}\n")
            main_file.write("\n")
            main_file.write("\n".join(self.global_code_lines))

def main(file_path):
    with open(file_path, "r") as file:
        source_code = file.read()
        tree = ast.parse(source_code)

    extractor = ClassExtractor(source_code)
    extractor.visit(tree)

    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    extractor.create_main_file(output_directory)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <python_file_path>")
    else:
        main(sys.argv[1])
