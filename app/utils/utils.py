def read_file_and_close(file_path):
    with open(file_path, "r") as f:
        return f.read()


def read_lines_and_close(file_path):
    with open(file_path, "r") as f:
        return f.readlines()
