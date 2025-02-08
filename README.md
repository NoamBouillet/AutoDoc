# AutoDoc
A documentation builder for C-Makefile based projects

## Requirements
python3 and doxygen packages are going to be installed if you don't have them already.

## Install
```sh
curl -sLO https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/installing.sh && bash installing.sh
```
Installs the autodoc command by copying autodoc.py to an executable location.
Then, you can safely run
```sh
autodoc
```
to clean documentation you don't want, you can use
```sh
autodoc clean
```
Don't forget to add Doxygen files into your .gitignore, nobody wants to see that in your repository

## Uninstall

```sh
sudo rm -rf /usr/local/bin/autodoc
```

## Doxygen
If you want to learn about the doxygen documentation, go on [doxygen website](https://www.doxygen.nl/manual/docblocks.html).

