import os
import shutil

def CopyStatic():
    path = os.path.exists("static")
    d = os.listdir("static")
    shutil.rmtree("public")
    