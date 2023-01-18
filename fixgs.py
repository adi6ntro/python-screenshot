# if image save from ps file to png file.
# like this message "FileNotFoundError: [Errno 2] No such file or directory: 'gs'"
# please do this:
# for mac os only
# brew install ghostscript
# brew link ghostscript
# run this file until get result in your terminal like this "GhostScript found in /usr/local/bin/gs"
# last, make sure to put this "os.environ["PATH"] += ":/usr/local/bin/gs"" in the beginning of your code


# this is the very first thing to do
import os
import subprocess
import shutil
#see is gs is avaible
if shutil.which("gs") is None:
    print("GhostScrip is not avaible, search for it")
    try:
        gs = subprocess.Popen(["which", "gs"], stdout=subprocess.PIPE)
        gs_path = gs.stdout.read()
        gs_path = gs_path.decode() if isinstance(gs_path, bytes) else gs_path
        print("GhostScript found in", gs_path)
        os.environ["PATH"] += ":" + os.path.dirname(gs_path)
    except Exception as e:
        raise Warning("GhostScrip not found, this program may fail")
else:
    if os.environ["PATH"].find("gs") == -1:
        gs = subprocess.Popen(["which", "gs"], stdout=subprocess.PIPE)
        gs_path = gs.stdout.read()
        gs_path = gs_path.decode() if isinstance(gs_path, bytes) else gs_path
        print("GhostScript found in", gs_path)
        os.environ["PATH"] += ":" + os.path.dirname(gs_path)
    else:
        print(os.environ["PATH"])
del subprocess
del shutil

# then everything else
