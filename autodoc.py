#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import sys

def add_doxygen_docs_to_function(function_name, params, return_type):
    """Generates Doxygen documentation for the function."""
    docs = f"/**\n"
    docs += f" * @brief {function_name} function documentation\n"
    
    for param in params:
        docs += f" * @param {param} Description of {param}\n"
    docs += f" * @return Description of the return value (type: {return_type})\n"
    docs += f" */\n"
    return docs


def remove_doxygen_docs_from_function(lines, func_line):
    """Removes Doxygen documentation if present."""
    doxy_pattern = re.compile(r"/\*\*")
    start = None
    for i in range(func_line, len(lines)):
        line = lines[i].strip()
        if doxy_pattern.match(line):
            start = i
            break
    
    if start is not None:
        end = start
        while end < len(lines) and not lines[end].strip().endswith("*/"):
            end += 1
        
        if end < len(lines):
            return lines[:start] + lines[end+1:]
    
    return lines


def is_doxygen_docs_present(lines, func_line):
    """Checks if Doxygen documentation already exists for the function."""
    doxy_pattern = re.compile(r"/\*\*")
    function_name_pattern = re.compile(r"\b" + re.escape(lines[func_line].split()[1]) + r"\b")

    print("lalalala")
    for line in lines[:func_line]:
        if doxy_pattern.match(line.strip()):
            if function_name_pattern.search(line.strip()):
                return True
    return False


def process_c_file(file_path, clean=False):
    """Process a single C file, adding or removing Doxygen documentation for functions."""
    with open(file_path, 'r') as file:
        content = file.readlines()

    updated_content = []
    function_pattern = re.compile(r"(\w+\s+\w+)\s*(\w+)\s*\(([^)]*)\)\s*\n\s*{")

    for i, line in enumerate(content):
        updated_content.append(line)
        match = function_pattern.search(line)
        if match:
            return_type = match.group(1)
            function_name = match.group(2)
            params_str = match.group(3)
            params = [param.strip().split()[1] for param in params_str.split(',') if param.strip()]
            
            if clean:
                updated_content = remove_doxygen_docs_from_function(updated_content, i)
            elif not is_doxygen_docs_present(updated_content, i):
                doxy_comment = add_doxygen_docs_to_function(function_name, params, return_type)
                updated_content.insert(updated_content.index(line), doxy_comment)
    return updated_content


def generate_doxygen_config():
    """Generates the Doxygen configuration file."""
    config_content = """
# Doxygen configuration file

PROJECT_NAME           = "AutoDoc Project"
OUTPUT_DIRECTORY       = ./doxygen_output
FILE_PATTERNS          = *.c
EXTRACT_ALL            = YES
GENERATE_LATEX         = YES
LATEX_OUTPUT           = pdf
GENERATE_HTML          = NO
    """
    
    with open("Doxyfile", 'w') as config_file:
        config_file.write(config_content)


def run_doxygen():
    """Runs Doxygen to generate the documentation PDF."""
    subprocess.run(['doxygen', 'Doxyfile'])


def clean_up():
    """Cleans up all generated files."""
    if os.path.exists("Doxyfile"):
        os.remove("Doxyfile")
        print("Removed Doxyfile")

    if os.path.exists("doxygen_output"):
        shutil.rmtree("doxygen_output")
        print("Removed doxygen_output directory")


def show_help():
    """Displays the help guide."""
    help_text = """
Usage:
  autodoc          - Process C files, add Doxygen documentation, and generate the PDF.
  autodoc clean      - Remove all added Doxygen documentation from the C files.
  autodoc help       - Show this help guide.

This script recursively processes all C files in the current directory:
- It adds Doxygen comments to functions that do not already have them.
- It generates a Doxygen configuration and runs Doxygen to generate a PDF.

If 'clean' is specified, it removes all added Doxygen documentation from the C files.
"""
    print(help_text)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "clean":
            clean = True
        elif sys.argv[1] == "help":
            show_help()
            return
        elif len(sys.argv) > 2:
            print("Unknown argument. Use 'help' for usage.")
            return
    else:
        clean = False

    if clean:
        c_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.c'):
                    c_files.append(os.path.join(root, file))
        
        for file_path in c_files:
            print(f"Cleaning up file: {file_path}")
            updated_content = process_c_file(file_path, clean=True)
            with open(file_path, 'w') as file:
                file.writelines(updated_content)
        clean_up()
        print("Cleanup completed!")
        return

    c_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.c'):
                c_files.append(os.path.join(root, file))
    
    for file_path in c_files:
        print(f"Processing file: {file_path}")
        updated_content = process_c_file(file_path, clean=False)
        with open(file_path, 'w') as file:
            file.writelines(updated_content)
    
    generate_doxygen_config()
    run_doxygen()
    print("Doxygen PDF generated!")


if __name__ == "__main__":
    main()
