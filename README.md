# 🗂️ Dump Project Script

Este script em **Python** gera um único arquivo Markdown contendo:

1. A **estrutura de diretórios** do projeto (treeview).
2. O **conteúdo concatenado** de todos os arquivos de texto, ignorando binários e arquivos configurados para exclusão.

É útil para enviar projetos para análise por IA quando não é possível compactar ou enviar arquivos `.py` separadamente.

---

## 🚀 Funcionalidades

- Gera um arquivo `_dump_<nome_da_pasta>.md` **na mesma pasta onde o script está localizado**.
- Inclui a **treeview** da estrutura de diretórios.
- Concatena o conteúdo de arquivos de texto em blocos Markdown.
- Ignora:
  - Pastas configuradas (`IGNORE_DIRS`).
  - Arquivos específicos (`IGNORE_FILES`).
  - Padrões glob (`IGNORE_PATTERNS`).
  - Regras do `.gitignore` (se existir).
  - O próprio arquivo de saída.
  - O próprio script em execução.

---

## 📦 Instalação

Clone o repositório e certifique-se de ter o Python 3 instalado.

```bash
git clone https://github.com/gtnasser/dump_project.git
cd dump_project.git
```

## 🛠️ Uso

Execute o script passando a pasta inicial como parâmetro:
```bash
python dump_project.py /caminho/para/seu/projeto
```

Exemplo com caminho relativo:
```bash
python dump_project.py ./frontend
```

O resultado será um arquivo _dump_<nome_da_pasta>.md na pasta onde o script está localizado.
Assim, você pode rodar o utilitário em qualquer projeto e o resultado sempre ficará junto do script executado, sem alterar o projeto analisado.

---

⚙️ Configuração de Exclusões

Você pode personalizar as listas de exclusão diretamente no script:

```python
IGNORE_DIRS = {"venv", "__pycache__", ".git"}   # pastas fixas a ignorar
IGNORE_FILES = {".env", "settings.json", ".gitignore", "__init__.py"}  # arquivos fixos a ignorar
IGNORE_PATTERNS = {"*.log", "*.tmp", "*.md"}  # padrões glob adicionais
```

Além disso, o script respeita as regras do `.gitignore` da pasta raiz do projeto.
