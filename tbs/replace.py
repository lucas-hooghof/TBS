from .inittbs import Instance
import shutil
import os
import glob

def ReplaceFile(instance: Instance, file: str):
    if instance.configure == False:
        print("Skipping Replace of GenConf Mode")
        return
    folder = os.path.dirname(os.path.abspath(file))
    makefile_path = os.path.join(folder, "Makefile")

    shutil.copy(file, makefile_path)

    with open(makefile_path, "r+") as template:
        lines = template.readlines()

        for i, line in enumerate(lines):
            for arg in instance.env:
                line = line.replace(f"%{arg}%", str(instance.env[arg]))
            lines[i] = line

        template.seek(0)
        template.truncate()
        template.writelines(lines)

def StartReplacing(instance: Instance):
    if instance.configure == False:
        print("Skipping Replace of GenConf Mode")
        return
    with open("Makefile","w+") as mmf:
        for _,dir in enumerate(instance.templatedirs):
            files = glob.glob(f"{dir}/*.tbm")
            for _,file in enumerate(files):
                ReplaceFile(instance,file)
            mmf.write(dir)
        
    