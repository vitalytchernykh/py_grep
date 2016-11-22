#!/usr/bin/env python
# -*- coding: cp1251 -*-
#
# grep logs by max procedures timings, threads activities processed

# return file system objects list
def getFsoList(fso_path):

    import os, time

    files = [os.path.join(fso_path, f) for f in os.listdir(fso_path)]

    # sort list by file time modified
    return sorted(files, key=lambda x: time.ctime(os.path.getmtime(x)))

#
def miner(fso_list):
	
    import re
    from datetime import datetime
    from datetime import timedelta

    grape_di = {}
    result_li = []

    for fso_name in fso_list:
       f = open(fso_name, 'r')
       print (fso_name)
       for line in f:
           time_str = re.search(r'(^\d{2}:\d{2}:\d{2},\d{3})(.*\.)(0x\d{2}) - (В.*ходные) параметры вызова .*', line)
           if time_str:
               th_time = datetime.strptime(time_str.group(1), '%H:%M:%S,%f')
               th_num = int(time_str.group(3)[2:])
               th_queue = time_str.group(2)
               if time_str.group(4) == 'Входные':
                   if th_num not in grape_di.keys():
                       grape_di[th_num] = [[th_time, th_queue]]
                   else:
                       grape_di[th_num].append([th_time, th_queue])
               if time_str.group(4) == 'Выходные':
                  if th_num in grape_di.keys():
                       if grape_di[th_num] != []:
                           for i in range(len(grape_di[th_num]),0,-1):
                               if grape_di[th_num][i-1][1] == th_queue:
                                   last_time = grape_di[th_num][i-1][0]
                                   del grape_di[th_num][i-1]
                                   result_li.append(['{:%H:%M:%S}'.format(last_time), (th_time - last_time).seconds, th_num])
                                   break

    return sorted(result_li), max(grape_di.keys())


# --select max(proc_timing) from (init_time, proc_time, th_num) group by init_time, th_num
def group_by(in_list):

    from itertools import groupby

#    for key, group in groupby(in_list, lambda x: x[0]):
#        print (key)
#        print (max(group, key=lambda x: x[1]))

    return [[max(group, key=lambda x: x[1])] for key, group in groupby(in_list, lambda x: x[0])]

# convert to excel view
def to_excel(in_list, max_th):

    out_list = []

    for i in in_list:
        tmp = [i[0][0]] + [''] * (max_th+1)
        tmp[i[0][2]+1] = str(i[0][1])
        out_list.append(tmp)

    return out_list

# main module
def main():

#    inpath = 'c:/project1/grep/test4'
#    inpath = 'c:/project1/grep/test2'
    inpath = 'c:/project1/grep/in'

    # get files list
    in_fso_list = getFsoList(inpath)

    a,m = miner(in_fso_list)
#    print ('\nthis is extractor action!')
#    for i in a: print (i)

    b = group_by(a)
#    print ('\nthis is group by action!')
#    for i in b: print (i)
              
    c = to_excel(b,m)
    print ('\nthis is excel view!')
    for i in c: print (i)


if __name__ == '__main__':

    # main module call
    main()
