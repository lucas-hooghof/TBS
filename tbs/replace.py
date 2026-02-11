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

def TemplatedBuild(inst: Instance,dir):
    template = f"{dir}:\n\t$(MAKE) -C {dir} target={os.path.abspath(inst.env["target"])} prefix={inst.env["prefix"]}"
    return template

def NextSector(file):
    file.write("\n\n")

def StartReplacing(instance: Instance):
    if instance.configure == False:
        print("Skipping Replace of GenConf Mode")
        return

    Phony = ".PHONY: "
    allmmf: str  = "all: "
    with open("Makefile","w+") as mmf:
        for _,dir in enumerate(instance.templatedirs):
            files = glob.glob(f"{dir}/*.tbm")
            for _,file in enumerate(files):
                ReplaceFile(instance,file)
            Phony = Phony + f" {dir}"
            allmmf = allmmf + f" {dir}"
            mmf.write(TemplatedBuild(instance,dir))
            NextSector(mmf)
            mmf.write(allmmf)
            NextSector(mmf)
            mmf.write(Phony)
        
    