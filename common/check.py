
import re


def check_phone(cont):
    if not cont:
        return False
    return re.match(r"^1[35678]\d{9}$", cont)


def check_num(cont):
    if not cont:
        return False
    return re.match(r"^\d+$", cont)


def check_id_num(cont):
    if not cont:
        return False
    return re.match(r"^(\d{14}|\d{17})(\d|[xX])$", cont)