#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import sys

GREEN="\033[1;32m"
BLUE="\033[1;34m"
RESET="\033[0m"

def show_help():
    help_text = f"""usage:
    autodoc            - Generates a Doxygen configuration and runs Doxygen to generate a PDF.
    autodoc details    - Process C files, add Doxygen documentation to functions that do not already have them.
    autodoc clean      - Remove all added Doxygen documentation from the C files and the autodoc.pdf.
    autodoc help       - Show this help guide."""
    print(help_text)

def generate_doxygen_config():
    print(f"{BLUE}Creating the Doxyfile config{RESET}")
    config_content = """# Doxygen configuration file

PROJECT_NAME           = "Auto Documentation"
OUTPUT_DIRECTORY       = ./doxygen_output
INPUT                  = ./
RECURSIVE              = YES
FILE_PATTERNS          = *.c
EXTRACT_ALL            = YES
GENERATE_LATEX         = YES
LATEX_OUTPUT           = latex
PDF_HYPERLINKS         = YES
USE_PDFLATEX           = YES
LATEX_BATCHMODE        = YES
GENERATE_HTML          = NO"""
    with open("Doxyfile", 'w') as config_file:
        config_file.write(config_content)

def add_doxygen_docs_to_function(function_name, params, return_type):
    doxy_comment = f"/**\n"
    doxy_comment += f" * @brief {function_name} function documentation\n"
    for param in params:
        if param != "void":
            doxy_comment += f" * @param {param} Description of {param}\n"
    if return_type != "void":
        doxy_comment += f" * @return {return_type} Description of the return value\n"
    doxy_comment += f" */\n"
    return doxy_comment

def remove_doxygen_docs_from_function(content, func_line):
    i = func_line - 1
    while i >= 0:
        if re.match(r"\s*/\*\*", content[i]):
            del content[i:func_line]
            break
        i -= 1
    return content

def is_doxygen_docs_present(lines, func_line):
    i = func_line - 1
    while i >= 0:
        if re.match(r"\s*/\*\*", lines[i]):
            return True
        i -= 1
    return False

def process_c_file(file_path, clean=False):
    with open(file_path, 'r') as file:
        content = file.readlines()
    updated_content = []
    function_pattern = re.compile(r"^\s*([a-zA-Z_][\w\s\*]+)\s+([a-zA-Z_][\w]*)\s*\(([^)]*)\)\s*(\{)?\s*$")

    for i, line in enumerate(content):
        updated_content.append(line)
        match = function_pattern.match(line)
        if match:
            return_type = match.group(1).strip()
            function_name = match.group(2).strip()
            params_str = match.group(3).strip()
            params = [p.strip().split()[-1] for p in params_str.split(',') if p.strip() and ' ' in p.strip()]
            if clean:
                updated_content = remove_doxygen_docs_from_function(updated_content, len(updated_content) - 1)
            elif not is_doxygen_docs_present(updated_content, len(updated_content) - 1):
                doxy_comment = add_doxygen_docs_to_function(function_name, params, return_type)
                updated_content.insert(len(updated_content) - 1, doxy_comment)
    return updated_content

def clean_up():
    if os.path.exists("Doxyfile"):
        os.remove("Doxyfile")
        print(f"{GREEN}✔ Removed Doxyfile{RESET}")

    if os.path.exists("doxygen_output"):
        shutil.rmtree("doxygen_output")
        print(f"{GREEN}✔ Removed doxygen_output directory{RESET}")

def run_doxygen():
    print(f"{BLUE}Building the autodoc PDF...{RESET}")
    with open('/dev/null', 'w') as devnull:
        subprocess.run(['doxygen', 'Doxyfile'], stdout=devnull, stderr=devnull)
        subprocess.run(['make', '-C', 'doxygen_output/latex'], stdout=devnull, stderr=devnull)
        subprocess.run(['mv', 'doxygen_output/latex/refman.pdf', './autodoc.pdf'], stdout=devnull, stderr=devnull)
    print(f"{GREEN}✔ Autodoc PDF generated!{RESET}")

def get_local_files():
    c_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.c'):
                c_files.append(os.path.join(root, file))
    return c_files

def clean_doc(c_files):
    for file_path in c_files:
        print(f"{BLUE}Cleaning up file: {file_path}{RESET}")
        updated_content = process_c_file(file_path, clean=True)
        with open(file_path, 'w') as file:
            file.writelines(updated_content)
    clean_up()
    if os.path.exists("autodoc.pdf"):
        os.remove("autodoc.pdf")
        print(f"{GREEN}✔ Removed autodoc.pdf{RESET}")
    print(f"{GREEN}✔ Cleanup completed!{RESET}")

def add_details(c_files):
    for file_path in c_files:
        print(f"{BLUE}Processing file: {file_path}{RESET}")
        updated_content = process_c_file(file_path, clean=False)
        with open(file_path, 'w') as file:
            file.writelines(updated_content)

def handle_options(c_files):
    length = len(sys.argv)
    if length > 2:
        print("Unknown argument. Use 'help' for usage.")
        exit(1)
    if length == 1:
        if not c_files:
            print("The directory is empty... What are you doing?")
            exit(1)
        return
    option = sys.argv[1]
    if option == "help":
        show_help()
        exit(0)
    if option != "clean" and option != "details":
        print("Unknown argument. Use 'help' for usage.")
        exit(1)
    if not c_files:
        print("The directory is empty... What are you doing?")
        exit(1)
    if option == "clean":
        clean_doc(c_files)
        exit(0)
    add_details(c_files)
    exit(0)

def main():
    c_files = get_local_files()
    handle_options(c_files)
    generate_doxygen_config()
    run_doxygen()
    return clean_up()

if __name__ == "__main__":
    main()
