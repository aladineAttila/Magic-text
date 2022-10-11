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

copyPluginDirectory() {
	plugin_dir=$DIRECTORY/dist/main/
	mkdir $plugin_dir/plugin/
	cp -r ../plugin/colorshemes $plugin_dir/plugin/ && cp ../magic.png $plugin_dir
	echo "copy colorscheme and magic.png"
}

copyAssetsFileFromLib(){
	cp -r /usr/local/lib/python3*/dist-packages/customtkinter/assets $ASSETS
	echo "assets file have been copied succesfully"
}

main(){
	createWorkSpace
	buildProjet
	initGlobalVariable
	creatAssestDirectory
	copyAssetsFileFromLib
	copyPluginDirectory
	echo "build finish!"
}

main
