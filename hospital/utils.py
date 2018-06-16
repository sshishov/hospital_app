import hashlib


def generate_choices(choices, algorithm='md5'):
    return tuple((hashlib.new(algorithm, choice.encode()).hexdigest(), choice) for choice in choices)
