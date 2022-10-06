import sys

class Printer():
    """Print updated data in a single line through loop iterations
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def getFiles(p):
    """Gets all the files inside a folder

    Args:
        p (str): Path of the folder

    Returns:
        list[str]: List containing all files absolute path
    """
    flist = p.glob('**/*')
    files = [x for x in flist if x.is_file()]
    return files