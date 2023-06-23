#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["52.91.121.146", "3.85.136.181"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = f"versions/web_static_{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    return None if local(f"tar -cvzf {file} web_static").failed is True else file


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, f"/tmp/{file}").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}/").failed is True:
        return False
    if (
        run(
            f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/"
        ).failed
        is True
    ):
        return False
    if run(f"rm /tmp/{file}").failed is True:
        return False
    if (
        run(
            f"mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/"
        ).failed
        is True
    ):
        return False
    if (
        run(f"rm -rf /data/web_static/releases/{name}/web_static").failed
        is True
    ):
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    return (
        run(
            f"ln -s /data/web_static/releases/{name}/ /data/web_static/current"
        ).failed
        is not True
    )


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    return False if file is None else do_deploy(file)
