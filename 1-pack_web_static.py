#!/usr/bin/python3
"""A module for Fabric script that generates a .tgz archive."""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    d_time = datetime.now()
    output = f"versions/web_static_{d_time.year}{d_time.month}{d_time.day}{d_time.hour}{d_time.minute}{d_time.second}.tgz"
    try:
        print(f"Packing web_static to {output}")
        local(f"tar -cvzf {output} web_static")
        size = os.stat(output).st_size
        print(f"web_static packed: {output} -> {size} Bytes")
    except Exception:
        output = None
    return output
