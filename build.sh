#!/bin/bash

DIRECTORY=
ASSETS=


createWorkSpace(){
	mkdir build -p
	cd build
}

buildProjet(){
	pyinstaller magic/sublLike.py
}

initGlobalVariable(){
	DIRECTORY=$(pwd)
	ASSETS="$DIRECTORY/dist/sublLike/customtkinter"
}

creatAssestDirectory(){
	mkdir -p $ASSETS
	echo "assets directory have been created succesfully"
}

copyAssetsFileFromLib(){
	cp "/usr/local/lib/python3.8/dist-packages/customtkinter/assets" -r "$ASSETS"
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
