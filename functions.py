from passlib.hash import sun_md5_crypt as Sun


def checkEmpty(shadow):
    empty = False
    for case in shadow:
        if not case:
            empty = True
    return empty

