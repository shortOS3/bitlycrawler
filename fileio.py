"""
Bitly crawler: FileIO class.

The FileIO class is used to read/write data on files (thread status and script output).
"""


__author__ = 'sendotux'


RESULT_FILE = "result.txt"
CHECK_FILE = "start.txt"


class FileIO(object):
    def __init__(self):
        pass

    @staticmethod
    def write_urls(obj, filename=RESULT_FILE):
        with open(filename, "ab+") as f:
            for line in obj:
                try:
                    f.write(str(line[u'short_url'].encode('utf-8'))+" "+str(line[u'long_url'].encode('utf-8'))+"\n")
                except Exception, e:
                    print "Cannot write line:", "["+str(line[u'short_url'])+","+str(line[u'long_url'])+"]"
            f.close()
        return 0

    @staticmethod
    def read_str(filename=CHECK_FILE):
        with open(filename, "rb") as f:
            retlist = f.readlines()
            for i in range(len(retlist)):
                retlist[i] = retlist[i][:-1]
        return retlist

    @staticmethod
    def write_str(writels, filename=CHECK_FILE):
        with open(filename, "wb") as f:
            for element in writels:
                f.write(element+"\n")

    @staticmethod
    def write_str_line(writestr, num, filename=CHECK_FILE):
            with open(filename, "rb+") as f:
                for i in range(num):
                    f.readline()
                f.write(writestr+"\n")