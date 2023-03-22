from dotmap import DotMap
import pathlib
import re


def find_all_py(path:  str) -> list:
    """Find all python files of a directory

    Args:
        path (str): the directory of the files

    Returns:
        list: a list with all python file names
    """
    p = pathlib.Path(path)

    return list(p.glob("**/*.py"))

def qtd_tabs(x: int) -> str:
    return "  "*x

def inverte_barra(path: str) -> str:
    new_path = ""
    for i in path:
        if i != "\\":
            new_path += i
        else:
            new_path += "/"
    return new_path
        
def write_docgen_page(file_py: str, file, functions):
    path = file_py.__str__()
    page_name = path.split("\\")[-1]
    path = r"" + path
    path = inverte_barra(path)

    file.write(qtd_tabs(1) + "- page: " +'"' + page_name[:-3] + ".md"+ '"'+ "\n")
    file.write(qtd_tabs(2) + "source: " +'"'+ path +'"'+ "\n")
    file.write(qtd_tabs(2) + "functions:\n")
    for func in functions:
        file.write(qtd_tabs(3) + "-" + func + "\n")


def write_mkgendoc_header(file: str) -> None:

    file.write("sources_dir: docs\n")
    file.write("templates_dir: docs/templates\n")
    file.write("repo: https://github.com/PedroVerardo/automatic_documentation\n")
    file.write("version: master\n")
    file.write("pages:\n")


def search_all_funcs(file_py: str) -> list:
    funcs = []
    with open(file_py, "r") as f:
        for line in f:
            m = re.search("def .*[(]", line)
            if m != None:
                name_func = m.group(0)[3:-1]
                funcs.append(name_func)
    return funcs

def write_mkdoc(github_url: str, name: str, files_py:list):
    header = f'''site_name: {name}
repo_url: {github_url}
site_url: https://example.com/
theme:
    name: readthedocs
    highlightjs: true
    hljs_languages:
        - yaml
        - rust
nav:
    '''
    for file in files_py:
        path = file.__str__()
        page_name = path.split("\\")[-1]

        header += "\n"+qtd_tabs(2)+"- "+page_name[:-3] +".md"+ "\n"
    
    with open("mkdocs.yml","w") as f:
        f.write(header)

def main(arg: DotMap):
    files_py = find_all_py(arg.dir)
    with open("mkgendoc.yml", "w") as f:
        write_mkgendoc_header(f)
        for file_py in files_py:
            funcs = search_all_funcs(file_py)
            write_docgen_page(file_py, f, funcs)
    write_mkdoc(arg.repo_url,arg.name,files_py)


if __name__ == "__main__":
    arg = DotMap()
    arg.name = "Auto Doc"
    arg.repo_url = "https://github.com/PedroVerardo/automatic_documentation"
    arg.dir = "python_codes"
    files_py = find_all_py(arg.dir)
 
    main(arg)
