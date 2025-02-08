# AutoDoc
A documentation builder for C projects

## Requirements
python3 and doxygen packages are going to be installed if you don't have them already.

## Install
```sh
curl -sLO https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/install.sh && bash install.sh
```
Then, you can safely run
```sh
autodoc
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

