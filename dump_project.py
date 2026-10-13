import os
import sys
import fnmatch

# Configurações de exclusão
IGNORE_DIRS = {"venv", "__pycache__", ".git"}   # pastas fixas a ignorar
IGNORE_FILES = {"__init__.py", ".env", "settings.json"}  # arquivos fixos a ignorar
IGNORE_PATTERNS = {"*.log", "*.tmp", "*.md"}  # padrões glob adicionais

def load_gitignore(root_dir):
    """Carrega padrões do .gitignore se existir na pasta raiz."""
    gitignore_path = os.path.join(root_dir, ".gitignore")
    patterns = set()
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.add(line)
    return patterns

def should_ignore_file(filename, rel_path, gitignore_patterns, output_file):
    """Verifica se o arquivo deve ser ignorado por nome, padrão, .gitignore ou se é o próprio arquivo de saída."""
    if os.path.abspath(rel_path) == os.path.abspath(output_file):
        return True
    if filename in IGNORE_FILES:
        return True
    for pattern in IGNORE_PATTERNS.union(gitignore_patterns):
        if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def is_text_file(filepath, rel_path, gitignore_patterns, output_file):
    """Verifica se o arquivo é de texto (ignora binários e arquivos proibidos)."""
    filename = os.path.basename(filepath)
    if should_ignore_file(filename, filepath, gitignore_patterns, output_file):
        return False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except:
        return False

def build_treeview(root_dir, gitignore_patterns, output_file):
    """Cria a representação da estrutura de diretórios em formato treeview."""
    tree_lines = []

    def walk(dir_path, prefix=""):
        entries = sorted(os.listdir(dir_path))
        for i, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            rel_path = os.path.relpath(path, root_dir)

            # Ignora pastas e arquivos configurados
            if os.path.isdir(path) and (entry in IGNORE_DIRS or any(fnmatch.fnmatch(rel_path, p) for p in gitignore_patterns)):
                continue
            if os.path.isfile(path) and should_ignore_file(entry, path, gitignore_patterns, output_file):
                continue

            connector = "└── " if i == len(entries) - 1 else "├── "
            tree_lines.append(f"{prefix}{connector}{entry}")
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
                walk(path, new_prefix)

    tree_lines.append(f"{os.path.basename(root_dir)}/")
    walk(root_dir)
    return "\n".join(tree_lines)

def dump_project(root_dir):
    # Normaliza caminho relativo para absoluto
    root_dir = os.path.abspath(root_dir)

    if not os.path.isdir(root_dir):
        print(f"Erro: pasta '{root_dir}' não existe.")
        return

    # Nome do arquivo de saída
    base_name = os.path.basename(root_dir.rstrip(os.sep))
    output_file = os.path.join(root_dir, f"_dump_{base_name}.md")

    # Carrega padrões do .gitignore
    gitignore_patterns = load_gitignore(root_dir)

    with open(output_file, "w", encoding="utf-8") as out:
        # Passo 2: Estrutura de diretórios
        out.write(f"### 📂 Estrutura de Diretórios (base: {root_dir})\n\n")
        out.write("```text\n")
        out.write(build_treeview(root_dir, gitignore_patterns, output_file))
        out.write("\n```\n\n")

        # Passo 3: Conteúdo dos arquivos de texto
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove pastas ignoradas da varredura
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_dir)

                if is_text_file(filepath, rel_path, gitignore_patterns, output_file):
                    out.write(f"### 📄 {rel_path}:\n\n")
                    out.write("```text\n")
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"[Erro ao ler arquivo: {e}]")
                    out.write("\n```\n\n")

    print(f"Dump gerado em: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python dump_project.py <pasta_inicial>")
    else:
        dump_project(sys.argv[1])
