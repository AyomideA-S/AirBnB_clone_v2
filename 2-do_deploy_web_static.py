#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.24.74.197", "52.91.117.197"]
env.user = "ubuntu"


def do_pack():
    """
        return the archive path if archive has generated correctly.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = f"versions/web_static_{date}.tgz"
    t_gzip_archive = local(f"tar -cvzf {archived_f_path} web_static")

    return archived_f_path if t_gzip_archive.succeeded else None


def do_deploy(archive_path):
    """
        Distribute archive.
    """
    if not os.path.exists(archive_path):
        return False
    archived_file = archive_path[9:]
    newest_version = f"/data/web_static/releases/{archived_file[:-4]}"
    archived_file = f"/tmp/{archived_file}"
    put(archive_path, "/tmp/")
    run(f"sudo mkdir -p {newest_version}")
    run(f"sudo tar -xzf {archived_file} -C {newest_version}/")
    run(f"sudo rm {archived_file}")
    run(f"sudo mv {newest_version}/web_static/* {newest_version}")
    run(f"sudo rm -rf {newest_version}/web_static")
    run("sudo rm -rf /data/web_static/current")
    run(f"sudo ln -s {newest_version} /data/web_static/current")

    print("New version deployed!")
    return True
