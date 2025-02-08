#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import sys

def show_help():
    help_text = """usage:
autodoc            - Generates a Doxygen configuration and runs Doxygen to generate a PDF.
autodoc details    - Process C files, add Doxygen documentation to functions that do not already have them.
autodoc clean      - Remove all added Doxygen documentation from the C files and the autodoc.pdf.
autodoc help       - Show this help guide."""
    print(help_text)

def generate_doxygen_config():
    print("Creating the Doxyfile config")
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
    for i in range(func_line, -1, -1):
        if content[i].strip().startswith("/*"):
            del content[i]
        elif content[i].strip().startswith("*/"):
            break
    return content

def is_doxygen_docs_present(lines, func_line):
    line = lines[func_line].strip()
    if not line:
        return False
    split_line = line.split()
    if len(split_line) < 2:
        return False
    function_name = split_line[1]
    function_name_pattern = re.compile(r"\b" + re.escape(function_name) + r"\b")

    for i in range(func_line, -1, -1):
        if lines[i].strip().startswith("/*"):
            return True
        elif lines[i].strip().startswith("*/"):
            break
    return False

def process_c_file(file_path, clean=False):
    with open(file_path, 'r') as file:
        content = file.readlines()
    updated_content = []
    function_pattern = re.compile(r"^\s*([a-zA-Z_][\w\s\*]+)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*$")

    for i, line in enumerate(content):
        updated_content.append(line)
        match = function_pattern.search(line)
        if match:
            return_type = match.group(1)
            function_name = match.group(2)
            params_str = match.group(3)
            params = [p.strip().split()[-1] for p in params_str.split(',') if p.strip() and ' ' in p.strip()]            
            if clean:
                updated_content = remove_doxygen_docs_from_function(updated_content, i)
            elif not is_doxygen_docs_present(updated_content, i):
                doxy_comment = add_doxygen_docs_to_function(function_name, params, return_type)
                updated_content.insert(updated_content.index(line), doxy_comment)
    return updated_content

def clean_up():
    if os.path.exists("Doxyfile"):
        os.remove("Doxyfile")
        print("Removed Doxyfile")

    if os.path.exists("doxygen_output"):
        shutil.rmtree("doxygen_output")
        print("Removed doxygen_output directory")

def run_doxygen():
    print("Building the autodoc pdf")
    with open('/dev/null', 'w') as devnull:
        subprocess.run(['doxygen', 'Doxyfile'], stdout=devnull, stderr=devnull)
        subprocess.run(['make', '-C', 'doxygen_output/latex'], stdout=devnull, stderr=devnull)
        subprocess.run(['mv', 'doxygen_output/latex/refman.pdf', './autodoc.pdf'], stdout=devnull, stderr=devnull)
    print("Autodoc PDF generated!")

def get_local_files():
    c_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.c'):
                c_files.append(os.path.join(root, file))
    return c_files

def clean_doc(c_files):
    for file_path in c_files:
        print(f"Cleaning up file: {file_path}")
        updated_content = process_c_file(file_path, clean=True)
        with open(file_path, 'w') as file:
            file.writelines(updated_content)
    clean_up()
    if os.path.exists("autodoc.pdf"):
        os.remove("autodoc.pdf")
        print("Removed autodoc.pdf")
    print("Cleanup completed!")

def add_details(c_files):
    clean_doc()
    for file_path in c_files:
        print(f"Processing file: {file_path}")
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
