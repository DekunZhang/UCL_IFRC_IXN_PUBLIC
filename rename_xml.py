import shutil
import os
import sys
import re

dr = sys.argv[1]

for root, dirs, files in os.walk(dr):
    for file in files:
        if re.search("\.xml", file):
            spl = root.split("/")
            newname = spl[-1]
            sup = "/".join(spl[:-1])
            shutil.move(f"{root}/{file}", f"{sup}/{newname}.xml")
            shutil.rmtree(root)
