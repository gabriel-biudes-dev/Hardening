import os, subprocess, hashlib
from general import *

drivename = '/dev/sda1'

def getClusters(text):
    """Get clusters from the debugfs command result

    Args:
        text (str): Debugfs result

    Returns:
        list[int]: List of cluster numbers
    """
    text = text.split(':')[1]
    text = text.split('-')
    if len(text) == 1:
        text[0] = int(text[0])
        return text
    clusters = []
    for x in range(int(text[1]) - int(text[0]) + 1):
        clusters.append(int(text[0]) + x)
    return clusters

def showMenu():
    """Show Slack Space application menu

    Returns:
        int: Choosen option
    """
    print('Choose an option:')
    print('\t1)Show file data')
    print('\t2)Write message on file slack space')
    print('\t3)Clear file slack space')
    answer = int(input('Option: '))
    return answer

def showData(clusters, filesize):
    """Show clusters data

    Args:
        clusters (list[int]): List of cluster numbers
        filesize (int): File size in bytes
    """
    drive = open(drivename, 'rb')
    i = 0
    for x in clusters:
        print(f'CLUSTER NUMBER {i + 1} ({x}):')
        drive.seek(x * 4096)
        info = str(drive.read(4096)).split("'")[1]
        print(info)
        i = i + 1
    print(f'Number of clusters: {len(clusters)}')
    drive.seek((clusters[-1] * 4096) + (filesize % 4096))
    slackstr = str(drive.read(4096 - filesize % 4096)).split("'")[1]
    hash_object = hashlib.md5(slackstr.encode())
    md5_hash = hash_object.hexdigest()
    print(f'File slack md5 hash: {md5_hash}')
    drive.close()

def writeData(message, clusters, filesize):
    """Write data in slack space

    Args:
        message (str): Message to be written
        clusters (list[int]): List of cluster numbers
        filesize (int): File size in bytes
    """
    if len(message) > (4096 - (filesize % 4096)):
        print(f'Message is too long (max size: {4096 - (filesize % 4096)} characters)')
        return
    drive = open(drivename, 'wb')
    drive.seek((clusters[-1] * 4096) + (filesize % 4096))
    drive.write(bytes(message, encoding='utf-8'))
    drive.close()
    print('Message written')

def clearSlack(clusters, filesize):
    """Clear file slack space

    Args:
        clusters (list[int]): List of cluster numbers
        filesize (int): File size in bytes
    """
    interations = 4096 - (filesize % 4096)
    drive = open(drivename, 'wb')

    for x in range(interations):
        drive.seek((clusters[-1] * 4096) + (filesize % 4096)+ x)
        drive.write(bytes(b'\x00'))
    drive.close()
    print('Slack space cleared')

def main():
    """Main function of Slack Space application
    """
    print('[WORKS ONLY ON LINUX]')
    print('[MUST RUN WITH SUDO]\n')
    filename = input('File name: ')
    filestat = os.stat(filename)
    fileino = filestat.st_ino
    filesize = filestat.st_size
    result = subprocess.run(['debugfs', '-R', 'stat <' +str(fileino)+'>', drivename], capture_output=True, encoding='utf-8')
    data = str(result.stdout)
    datalist = data.splitlines()
    clusters = getClusters(datalist[13])
    answer = showMenu()
    while(answer != 9):
        if answer == 1: showData(clusters, filesize)
        if answer == 2: writeData(input('Message: '), clusters, filesize)
        if answer == 3: clearSlack(clusters, filesize)
        answer = showMenu()

if __name__ == '__main__':
    main()