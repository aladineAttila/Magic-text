#!/bin/bash

DIRECTORY=
ASSETS=

createWorkSpace(){
	mkdir build -p
	cd build
}

buildProjet(){
	pyinstaller ../main.py
}

initGlobalVariable(){
	DIRECTORY=$(pwd)
	ASSETS="$DIRECTORY/dist/main/customtkinter/"
}

creatAssestDirectory(){
	mkdir -p $ASSETS
	echo "assets directory have been created succesfully"
}

copyAssetsFileFromLib(){
	sudo cp -r /usr/local/lib/python3*/dist-packages/customtkinter/assets $ASSETS
	echo "assets file have been copied succesfully"
}

main(){
	createWorkSpace
	buildProjet
	initGlobalVariable
	creatAssestDirectory
	copyAssetsFileFromLib
	echo "build finish!"
}

main
