#!/usr/bin/env python
# -*- coding: cp1251 -*-
#

inpath = 'c:/temp/888/in'
outpath = 'c:/temp/888/out'
astep = 5

# return file system objects list
def getFsoList(fso_path):

    import os, time

    files = [os.path.join(fso_path, f) for f in os.listdir(fso_path)]

    # sort list by time modified
    return sorted(files, key=lambda x: time.ctime(os.path.getmtime(x)))


def findRequests(fso_list, search_str):

    import re
    from datetime import datetime
    from datetime import timedelta

    line0 = ''
    out_list = {}
    next_time = datetime.strptime('00:00:00', '%H:%M:%S')

    for fso_name in fso_list:
       f = open(fso_name, 'r')
       for line in f:
           if search_str in line and 'P_DOC:' not in line0:
               cur_time = line0[:8]
               if datetime.strptime(cur_time, '%H:%M:%S') > next_time:
       	           out_list[re.search(r'<DOCREF>.*</DOCREF>', line).group(0), cur_time] = []
                   next_time = datetime.strptime(cur_time, '%H:%M:%S') + \
			timedelta(minutes = astep)
           line0 = line
       f.close
    return out_list


def findAnswers(fso_list, in_list):

    import re
    from datetime import datetime
    from datetime import timedelta

    line0 = ''

    for fso_name in fso_list:
       f = open(fso_name, 'r')
       for line in f:
           for docref in in_list.keys():
               if docref[0] in line and 'Получено сообщение' in line0:
                   if 'BS_A_UPDATE_PAYDOCRU' in line:
                       in_list[docref].append([line0[:8], re.search(r'<NOTEFROMBANK>.*</NOTEFROMBANK>', line).group(0)])
                   if 'BS_A_STATEMENT' in line:
                       in_list[docref].append([line0[:8], 'BS_A_STATEMENT'])
           line0 = line
       f.close
    return in_list


# main module
def main():

    import os
    from datetime import datetime
    from datetime import timedelta

    # get files list
    in_fso_list = getFsoList(inpath)
    out_fso_list = getFsoList(outpath)

    a = findRequests(in_fso_list, 'x:BSMessage xmlns:x="BS_R_PAYDOCRU"')

    b = findAnswers(out_fso_list, a)

#    for k,v in b.items(): print (k,v)

    for k,v in b.items():
        s = ''
        for i in v:
            s = s + i[0] + ',' + i[1] + ',' 
        print (k[0], ',', k[1], ',', s)


if __name__ == '__main__':

    # main module call
    main()
