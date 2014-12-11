"""
Bitly crawler: Crawler class.

The Crawler class is a worker that retrieves long urls from bitly links using the bitly API.
"""


__author__ = 'sendotux'

import threading
from stringiterator import *
from fileio import *
import time


class Crawler(threading.Thread):
    def __init__(self, process_num, lock, connection, prefix=None):
        threading.Thread.__init__(self)
        super(Crawler, self).__init__()
        self.__process_num = process_num
        self.__lock = lock
        self.__connection = connection
        self.__prefix = prefix
        self.__entries_processed = 0
        self.__exception_count = 0
        self.__retry_time = 5
        self.__active = True

    def run(self):
        data = []
        string_crawler = StringIterator(self.__prefix)
        print "Starting process:", self.__process_num, "With prefix:", string_crawler
        for char in string_crawler:
            try:
                temp = self.__connection.expand(shortUrl="http://bit.ly/"+char)
                if u'error' in temp[0]:
                    pass
                else:
                    data.append(temp[0])

                if len(data) >= 10:
                    self.__lock.acquire()
                    FileIO.write_urls(data)
                    FileIO.write_str_line(char, self.__process_num)
                    self.__lock.release()
                    data = []

                self.__entries_processed += 1
                self.__retry_time = 5

            except Exception, e:
                print "Exception detected on process:", self.__process_num
                print "Exception type:", type(e)
                print e
                if str(e)[0] is "'":
                    print "Additional info:"
                    print data
                    data = []

                self.__exception_count += 1

                print "Putting process", self.__process_num, "to sleep for", self.__retry_time, "seconds."
                time.sleep(self.__retry_time)
                if self.__retry_time < 900:
                    self.__retry_time *= 4
                else:
                    self.__retry_time = 900

                try:
                    self.__lock.release()
                except:
                    pass
                print "Process", self.__process_num, "awake again."

        print "Ending process:", self.__process_num, "Entries processed:", self.__entries_processed

    def get_proc_num(self):
        return self.__process_num

    def get_proc_count(self):
        return self.__entries_processed

    def get_proc_err(self):
        return self.__exception_count