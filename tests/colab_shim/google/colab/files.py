import os
def upload():
    out = {}
    for p in filter(None, os.environ.get("HECON_SHIM_UPLOAD", "").split(os.pathsep)):
        out[os.path.basename(p)] = open(p, "rb").read()
    print("stand-in upload: %d file(s)" % len(out)); return out
def download(path):
    print("stand-in download: " + str(path))
