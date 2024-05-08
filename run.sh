#!/bin/bash

python preprocess.py && python newbbox.py && python yolo8split.py
git 