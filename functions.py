from passlib.hash import sun_md5_crypt as Sun

def checkEmpty(arrays):
    msg = False
    for case in arrays:
        if not case:
            msg = True
    return msg