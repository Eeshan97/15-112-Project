import cx_Freeze
spritesheet = []
for i in range(1,7):
    spritesheet.append('dice (' + str(i)+').png')
executables = [
        #                   name of your game script
        cx_Freeze.Executable("Project.py")
]
cx_Freeze.setup(
        name = "Ludo",
        options = {"build_exe": {"packages":["pygame","time","random"],"include_files":["ludo.jpg"] + spritesheet + ["rules.txt"]}},
        description = "Ludo Game Install",
        executables = executables)
