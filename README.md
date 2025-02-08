# AutoDoc
A documentation builder for C projects

## Requirements
You need pdflatex packages installed as the exact packages' names change for each distribution.  
python3, doxygen and graphviz packages are going to be installed if you don't have them already.

## Install
```sh
curl -sLO https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/install.sh && bash install.sh
```
Then, you can safely run to add basic documentation
```sh
autodoc
```
To build the pdf file, you can use
```sh
autodoc gen
```
To clean documentation if you don't want it anymore, you can use
```sh
autodoc clean
```
Don't forget to add the other Doxygen files into your .gitignore, nobody wants to see that in your repository.

## Uninstall

```sh
sudo rm -rf /usr/local/bin/autodoc
```

## Doxygen
If you want to learn about the doxygen documentation, go on the [doxygen website](https://www.doxygen.nl/manual/docblocks.html).

