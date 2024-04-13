import re


def to_snake_case(class_name):
    # Insert an underscore between two consecutive uppercase letters or lowercase followed by uppercase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", class_name)
    # Insert an underscore between lowercase and uppercase
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
