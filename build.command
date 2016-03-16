#!/bin/bash

mkdir Documentation
mkdir -p Website/dist

rm -rf Documentation/*
rm -rf Website/dist/*
rm -rf docs/build/*

# Evoke Sphinx to create html and pdf documentation
cd docs
make html latexpdf
cd ..

# Copying pdf documentation to Documentation and Website
cp docs/build/latex/ursgal.pdf Documentation/
cp docs/build/latex/ursgal.pdf Website/dist/

# Copying html documentation to Documentation and Website
cp -R docs/build/html Documentation/html
cp -R docs/build/html/* Website/

rm -rf dist/*
# Creating Python packages
python3.4 setup.py sdist --formats=bztar,gztar,zip
# python3.4 setup.py sdist --formats=zip
cd dist
tar xvfj *.bz2
cd ..

# Copying packages to Website
cp dist/ursgal*.zip     Website/dist/ursgal.zip
cp dist/ursgal*.tar.bz2 Website/dist/ursgal.tar.bz2
