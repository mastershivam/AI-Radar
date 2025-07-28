def is_url_in_file(url, filepath):
    try:
        with open(filepath, "r") as f:
            return url in f.read()
    except FileNotFoundError:
        return False