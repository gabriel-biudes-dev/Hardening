from pathlib import Path
from general import *
import shutil

class Dir:
    def __init__(self, name, content):
        """Class to represent a folder

        Args:
            name (str): Folder name
            content (list[obj]): List of FileClass objects
        """
        self.name = name
        self.content = content

class FileClass:
    def __init__(self, name, content):
        """Class to represent a file

        Args:
            name (str): File name
            content (list[int]): File content converted to bytes
        """
        self.name = name
        self.content = content

def showMenu():
    """Show the Folder Store application menu

    Returns:
        int: Choosen option
    """
    print('[MENU]')
    print('\t1)Save folder')
    print('\t2)Restore folder')
    print('\t3)Delete folder data')
    return int(input('Option: '))

def readfile(path):
    """Get file data

    Args:
        path (str): File data

    Returns:
        bytearray: File data in bytearray
    """
    with open(path, "rb") as f:
        return bytearray(f.read())

def saveFolder(name):
    """Save data from a folder in the txt file

    Args:
        name (str): Folder name
    """
    directory = Path().absolute()
    directory = directory / name
    files = getFiles(directory)
    f = open('data.txt', 'a')
    f.write('[START]\n')
    f.write(str(directory).split('\\')[-1] + '\n')
    for index,x in enumerate(files):
        msg = 'Saving file ' + str((index + 1)) + '/' + str(len(files))
        Printer(msg)
        f.write('[FILE]\n')
        data = readfile(x)
        name = str(x).split('\\')[-1]
        f.write(name + '\n')
        for x in data: f.write(str(x) + ' ')
        f.write('\n[ENDFILE]\n')
    f.write('[END]\n')
    f.close()
    shutil.rmtree(directory)
    print('\nFiles saved successfully\n')

def readData(i, foldername):
    """Read data from a folder stored in the txt file, starting from the Inth line

    Args:
        i (int): Lines to be skipped on the txt file
        foldername (str): Folder name

    Returns:
        list[obj]: List of FileClass objects
    """
    f = open('data.txt', 'r')
    lines = f.readlines()
    files = []
    filename = ''
    for index, x in enumerate(lines):
        if lines[index + i] == '[END]\n': break
        if lines[index + i] == '[ENDFILE]\n': continue
        if lines[index + i] == '[FILE]\n': continue
        if lines[index + i] == foldername + '\n': continue
        if lines[index + i - 1] == '[FILE]\n':
            filename = lines[index + i]
            filename = filename.replace('\n', '')
            continue
        files.append(FileClass(filename, lines[index + i]))
    for index, x in enumerate(files):
        files[index].content = files[index].content.split(' ')
        files[index].content.pop(-1)
        for z, y in enumerate(files[index].content):
            try:
                files[index].content[z] = int(files[index].content[z])
            except Exception: pass
    f.close()
    return files

def getFolder():
    """Recover data from a folder stored in the txt file
    """
    print('Loading data..')
    directories = []
    f = open('data.txt', 'r')
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '[START]\n':
            foldername = lines[index + 1]
            foldername = foldername.replace('\n', '')
            data = readData(index + 1, foldername)
            directories.append(Dir(foldername, data))
    f.close()
    print('Choose an option:')
    for index,x in enumerate(directories):
        print(f'{index + 1}){x.name}')
    position = int(input('Option:')) - 1
    p = Path(directories[position].name)
    p.mkdir(parents=True, exist_ok=True)
    p = p.absolute()
    for index,files in enumerate(directories[position].content):
        msg = 'Recovering file ' + str((index + 1)) + '/' + str(len(directories[position].content))
        Printer(msg)
        newname = p / files.name
        zx = open(newname, 'wb')
        zx.write(bytearray(files.content))
        zx.close()
    print('\nFiles recovered successfully\n')

def removeLine(start, rangee):
    """Remove lines from the txt file

    Args:
        start (int): Starting line
        rangee (int): Ammount of lines to be deleted
    """
    start = start - 1
    with open("data.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for index,l in enumerate(d):
            if index < start:
                f.write(l)
                continue
            if index >= start and index < (start + rangee): continue
            f.write(l)
        f.truncate()

def deleteFolder():
    """Delete folder inside the txt file
    """
    print('Loading data..')
    directories = []
    f = open('data.txt', 'r')
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '[START]\n':
            foldername = lines[index + 1]
            foldername = foldername.replace('\n', '')
            data = readData(index + 1, foldername)
            directories.append(Dir(foldername, data))
    f.close()
    print('Choose an option:')
    for index,x in enumerate(directories):
        print(f'{index + 1}){x.name}')
    position = int(input('Option:')) - 1
    f = open('data.txt', 'r')
    lines = f.readlines()
    count = 0
    start = 0
    filenumber = len(directories[position].content)
    print('Removing data..')
    for index,line in enumerate(lines):
        if line == '[START]\n': count = count + 1
        if (count - 1) == position: 
            start = index + 1
            break
    deleted = 3 + (4 * filenumber)
    removeLine(start, deleted)
    f.close()
    print('Data removed successfully')

def main():
    answer = showMenu()
    while answer != 9:
        if answer == 1: saveFolder(input('Folder name: '))
        if answer == 2: getFolder()
        if answer == 3: deleteFolder()
        answer = showMenu()

if __name__ == '__main__':
    main()