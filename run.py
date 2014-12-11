"""
Bitly crawler: run script.

Bitly Crawler python script for Security of Systems and Networks course at MSc System and Network Engineering.

Script runs without arguments.

Input/Output files (default values):

- start.txt: Must contain as lines as threads are intended to be used. Each line specifies the starting string for
that thread.
- result.txt: Contains the output from the script in the format: <<short url> <*space*> <long url>>
"""

__author__ = 'sendotux'

import bitly_api
import socket
import select
from crawler import *

THREAD_NUMBER = 8
IP = "0.0.0.0"
PORT = 8008


def create_workers(connection):
    print "Creating workers..."
    worker_list = list()
    character_list = FileIO.read_str()
    worker_list.append(Crawler(0, lock, connection, character_list[0]))
    for i in range(1, THREAD_NUMBER):
        starting_character = character_list[i]
        worker_list.append(Crawler(i, lock, connection, starting_character))
    print "Workers created."
    return worker_list


def start_workers(worker_list):
    print "Starting workers..."
    for worker in worker_list:
        worker.start()
    print "Workers started."


def stop_workers(worker_list):
    print "Stopping workers..."
    for worker in worker_list:
        worker.terminate()
    print "Workers stopped."


def join_workers(worker_list):
    print "Joining workers..."
    for worker in worker_list:
        worker.join()
    print "Workers joined."


def enable_networking(worker_list):
    print "Starting networking..."
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind((IP, PORT))
    server.listen(1)

    inputs = [server]
    outputs = []
    extra = []
    print "Networking started."

    while inputs:
        inp, out, ext = select.select(inputs, outputs, extra, 1)
        for entry in inp:
            if entry is server:
                new_conn, addr = entry.accept()
                inputs.append(new_conn)
            else:
                data = entry.recv(2)
                if data:
                    print data
                    if data == "00":
                        start_workers(worker_list)
                        entry.send("10")

                    if data == "01":
                        returnstring = ""
                        for worker in worker_list:
                            name = worker.get_proc_num()
                            proc = worker.get_proc_count()
                            err = worker.get_proc_err()
                            line = "Process: "+str(name)+" || Is alive: "+str(worker.is_alive())+\
                                   " || Queries processed: "+str(proc)+" || Exceptions: "+str(err)
                            print line
                            returnstring = returnstring+line+"\n"
                        entry.send("11"+str(len(returnstring)).zfill(8)+returnstring)

                    if data == "02":
                        for element in inputs:
                            inputs.remove(element)
                        stop_workers(worker_list)
                        entry.send("12")

                else:
                    entry.close()
                    inputs.remove(entry)

if __name__ == "__main__":
    token = raw_input("Insert access token ID:")
    connection1 = bitly_api.Connection(access_token=token)

    lock = threading.Lock()

    start_time = time.time()
    print "Starting time:", start_time

    worker_list1 = create_workers(connection1)
    time.sleep(1)
    start_workers(worker_list1)
    enable_networking(worker_list1)
    join_workers(worker_list1)
    end_time = time.time()

    print "Ending time:", end_time
    print "Elapsed time:", end_time - start_time
