from textnode import *
import os
from copy_static import copy_files_recursive
import shutil
from blocks import extract_title
from generate import *
import sys
dir_path_static = "static"
dir_path_public = "docs"

def main():
    basepath = sys.argv or "/"
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

   
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("content", "template.html", dir_path_public, basepath)

main()