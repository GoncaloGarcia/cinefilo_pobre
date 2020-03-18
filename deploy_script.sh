#!/bin/bash

mkdir .deps
pip3 install -r requirements.txt --target=.deps
cp fetch_meo.py .deps
cp constants.py .deps
cd .deps
zip -r ../deploy_package.zip *
cd ..
rm -rf .deps
