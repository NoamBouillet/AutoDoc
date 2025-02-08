# AutoDoc
A documentation builder for C projects

## Requirements
You need pdflatex packages installed as the exact packages' names change for each distribution.  
python3, doxygen and graphviz packages are going to be installed if you don't have them already.

## Install
```sh
curl -sLO https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/install.sh && bash install.sh
```
To build the autodoc file, you can run
```sh
autodoc
```
To add documentation for every function, you can run
```sh
autodoc details
```
To clean documentation if you don't want it anymore, you can run
```sh
autodoc clean
```  
## Uninstall

```sh
sudo rm -rf /usr/local/bin/autodoc
```

## Doxygen
If you want to learn about the doxygen documentation, go on the [doxygen website](https://www.doxygen.nl/manual/docblocks.html).

