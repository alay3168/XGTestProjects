#! /bin/sh

rm facedet_v
version=$1
ln -s $version facedet_v

python demo.py
