import ast

class PythonCodeParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)  

    def get_functions(self):
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = self._get_end_line(node)
                code = self._extract_code(start_line, end_line)
                functions.append({
                    'name': node.name,
                    'start_line': start_line,
                    'end_line': end_line,
                    'code': code
                })
        return functions

    def get_classes(self):
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                start_line = node.lineno
                end_line = self._get_end_line(node)
                code = self._extract_code(start_line, end_line)
                classes.append({
                    'name': node.name,
                    'start_line': start_line,
                    'end_line': end_line,
                    'code': code
                })
        return classes

    def get_if_statements(self):
        if_statements = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                start_line = node.lineno
                end_line = self._get_end_line(node)
                code = self._extract_code(start_line, end_line)
                if_statements.append({
                    'start_line': start_line,
                    'end_line': end_line,
                    'code': code
                })
        return if_statements

    def get_loops(self):
        loops = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.For, ast.While)):
                start_line = node.lineno
                end_line = self._get_end_line(node)
                code = self._extract_code(start_line, end_line)
                loops.append({
                    'start_line': start_line,
                    'end_line': end_line,
                    'code': code
                })
        return loops

    def get_imports(self):
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                imports.append({
                    'type': 'import',
                    'names': [n.name for n in node.names]
                })
            elif isinstance(node, ast.ImportFrom):
                imports.append({
                    'type': 'from',
                    'module': node.module,
                    'names': [n.name for n in node.names]
                })
        return imports

    def get_other_statements(self):
        statements = []
        for node in ast.walk(self.tree):
            # Extract assignments (e.g., a = 1)
            if isinstance(node, ast.Assign):
                targets = [ast.dump(target) for target in node.targets]
                value = ast.dump(node.value)
                statements.append({
                    'type': 'assign',
                    'targets': targets,
                    'value': value,
                    'line': node.lineno
                })
            # Extract expressions (e.g., print(10))
            elif isinstance(node, ast.Expr):
                statements.append({
                    'type': 'expr',
                    'value': ast.dump(node.value),
                    'line': node.lineno
                })
        return statements

    def _get_end_line(self, node):
        end_line = node.lineno
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            for n in node.body:
                if hasattr(n, 'lineno'):
                    end_line = max(end_line, n.lineno)
        return end_line

    def _extract_code(self, start_line, end_line):
        code_lines = self.code.splitlines()
        return "\n".join(code_lines[start_line - 1:end_line])

    def get_logical_parts(self):
        return {
            "functions": self.get_functions(),
            "classes": self.get_classes(),
            "if_statements": self.get_if_statements(),
            "loops": self.get_loops(),
            "imports": self.get_imports(),
            "other_statements": self.get_other_statements()
        }

    def display_logical_parts(self):
        parts = self.get_logical_parts()

        print("Imports:")
        for imp in parts["imports"]:
            print(f"{imp['type']} {imp.get('module', '')} {imp.get('names', '')}")
        print()

        print("Functions:")
        for func in parts["functions"]:
            print(f"Function {func['name']} (lines {func['start_line']}–{func['end_line']}):")
            print(func['code'])
            print()

        print("Classes:")
        for cls in parts["classes"]:
            print(f"Class {cls['name']} (lines {cls['start_line']}–{cls['end_line']}):")
            print(cls['code'])
            print()

        print("If Statements:")
        for stmt in parts["if_statements"]:
            print(f"If statement (lines {stmt['start_line']}–{stmt['end_line']}):")
            print(stmt['code'])
            print()

        print("Loops:")
        for loop in parts["loops"]:
            print(f"Loop (lines {loop['start_line']}–{loop['end_line']}):")
            print(loop['code'])
            print()

        print("Other Statements:")
        for stmt in parts["other_statements"]:
            print(f"{stmt['type']} (line {stmt['line']}):")
            print(f"Targets: {stmt.get('targets', '')} Value: {stmt.get('value', '')}")
            print()

        print("End of logical parts.\n")
        print("*"*25,"\n\n")