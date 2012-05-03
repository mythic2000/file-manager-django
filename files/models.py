import shutil
import os
import glob
import subprocess
from datetime import datetime


def save_permissions(user, folder, path, settings):
    fullpath = "/home/%s/%s/%s/%s" % (user[0], user, folder, path)
    if not os.path.isdir(fullpath):
        return {"success": False, "status": "Path is not directory"}
    mode = settings.get("mode", "public")
    if mode == "public":
        try:
            os.remove(fullpath+"/.htaccess")
        except:
            pass
        try:
            os.remove(fullpath+"/.htpasswd")
        except:
            pass
        return {"success": True}
    if mode == "sso":
        contents = """        Order deny,allow
        Deny from all
        Satisfy any
        AuthType mod_auth_pubtkt
        TKTAuthLoginURL https://login.futurice.com/
        TKTAuthTimeoutURL https://login.futurice.com/?timeout=1
        TKTAuthUnauthURL https://login.futurice.com/?unauth=1
        TKTAuthToken "futu"
        TKTAuthToken "ext"
        Require valid-user"""
        open(fullpath+"/.htaccess", "w").write(contents)
        chown(user, fullpath+"/.htaccess")
        return {"success": True}
    if mode == "basicauth":
        contents = """AuthType Basic
AuthName "Protected files"
AuthUserFile %s
Require valid-user""" % (fullpath+"/.htpasswd")
        open(fullpath+"/.htaccess", "w").write(contents)
        chown(user, fullpath+"/.htaccess")
        p = subprocess.Popen(["htpasswd", "-cbs", fullpath+"/.htpasswd", settings.get("username"), settings.get("password")])
        p.wait()
        return {"success": True}

    return {"success": False, "status": "Invalid method"}



def get_file(user, folder, path, filename):
    fullpath = "/home/%s/%s/%s/%s/%s" % (user[0], user, folder, path, filename)
    return get_file_raw(fullpath)

def get_file_raw(file):
    type = "unknown"
    if os.path.isfile(file):
        type = "file"
    elif os.path.isdir(file):
        type = "dir"
    elif os.path.islink(file):
        type = "link"
    size = os.path.getsize(file)
    mtime = os.path.getmtime(file)
    mtime_readable = pretty_date(mtime)
    return {"full_path": file, "filename": os.path.basename(file), "size": size, "type": type, "mtime": mtime, "mtime_readable": mtime_readable}


def get_files(user, folder, path):
    fullpath = ("/home/%s/%s/%s/%s/" % (user[0], user, folder, path)).replace("//", "/")


    list_of_files = glob.glob("%s/*" % fullpath)
    files_final = []
    for file in list_of_files:
        files_final.append(get_file_raw(file))
    return files_final


def chown(user, fullpath):
    p = subprocess.Popen(["sudo", "/root/safe_chown.py", user, fullpath])
    p.wait()

def mkdir_file(user, folder, path, foldername):
    fullpath = "/home/%s/%s/%s/%s/%s" % (user[0], user, folder, path, foldername)
    if os.path.exists(fullpath):
        return {"success": False, "status": "File already exists"}
    os.mkdir(fullpath, 0771)
    chown(user, fullpath)
    return {"success": True}

def delete_file(user, folder, path):
    fullpath = "/home/%s/%s/%s/%s" % (user[0], user, folder, path)
    if os.path.exists(fullpath):
        try:
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
            else:
                os.remove(fullpath)
            return {"success": True}
        except Exception, e:
            return {"success": False, "status": "rm failed: %s" % fullpath, "err": str(e)}
    return {"success": False, "status": "No such file or directory"}

def upload_file(f, user, folder, path):
    fullpath = "/home/%s/%s/%s/%s/%s" % (user[0], user, folder, path, f.name)
    destination = open(fullpath, "wb")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    chown(user, fullpath)


# from http://stackoverflow.com/a/1551394/592174
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int or type(time) is float:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"