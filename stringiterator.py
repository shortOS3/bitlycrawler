"""
Bitly crawler: StringIterator class.

The StringIterator is used as an iterable object to retrieve new strings to use as bitly addresses.
"""

__author__ = 'sendotux'


import string


class StringIterator(object):
    def __init__(self, init_string=[], length=7, loop=False):
        all_values = "*"+string.ascii_letters+string.digits
        self.__charlist = list([0 for x in range(length)])
        self.__ctoi = dict(zip(all_values, range(len(all_values))))
        self.__itoc = dict()
        self.__loop = loop
        for char in self.__ctoi:
            self.__itoc[self.__ctoi[char]] = char
        for char, itr in zip(init_string, range(len(init_string))):
            self.__charlist[itr] = self.__ctoi[char]

    def __iter__(self):
        return self

    def next(self):
        add = False
        self.__charlist[0] += 1
        for index in range(len(self.__charlist)):
            if add == True:
                self.__charlist[index] += 1

            if self.__charlist[index] >= 63:
                if not self.__loop and index == len(self.__charlist)-1:
                    raise StopIteration()
                else:
                    self.__charlist[index] = 1
                    add = True
            else:
                add = False

        return str(self)

    def __str__(self):
        returnstring = ""
        for num in self.__charlist:
            aux = self.__itoc[num]
            if aux != "*":
                returnstring = returnstring+aux
        return returnstring