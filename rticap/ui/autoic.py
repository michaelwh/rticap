import os
f=os.popen("ls")
for line in f.readlines():
    if len(line) >= 4:
        if line[len(line)-4:len(line)-1] == ".ui":
            command = "pyside-uic -o " + line[0:len(line)-4] + ".py" + " " + line
            print command
            out = os.popen("pyside-uic -o " + line[0:len(line)-4] + ".py" + " " + line)
            print out.readlines()
