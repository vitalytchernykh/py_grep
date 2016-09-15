#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

apath = 'c:/backup/otk'
astep = 5
atime = ''

# return file system objects list
def getFsoList(fso_path):

    import os, time

    files = [os.path.join(fso_path, f) for f in os.listdir(fso_path)]

    # sort list by time modified
    return sorted(files, key=lambda x: time.ctime(os.path.getmtime(x)))


# search first id in logs
def findFirstID(fso_list):

    import os
    from datetime import datetime

    line0 = ''

    for fso_name in fso_list:
	f = open(fso_name, 'r')
	for line in f:
	    if '<FDS source="bfcotk" type="paydoc"><DOCUMENTID>' in line:
		return line[47:58], datetime.strptime(line0[:8], '%H:%M:%S')
	    line0 = line
        f.close


def findNextID(fso_list, ftime):

    import os
    from datetime import datetime

    line0 = ''

    for fso_name in fso_list:
	f = open(fso_name, 'r')
	for line in f:
	    if '<FDS source="bfcotk" type="paydoc"><DOCUMENTID>' in line and datetime.strptime(line0[:8], '%H:%M:%S') > ftime:
		return line[47:58]
	    line0 = line
        f.close

#
def findSubStr(fso_name, atext):

    import os
    from datetime import datetime

    f = open(fso_name, 'r')
    global atime
    result = ''

    for line in f:
	if atext in line:
	    if 'Получатель сохранил сообщение' in line0:
	        result = result + str(datetime.strptime(line0[:8], '%H:%M:%S') - atime) + ' '
		atime = datetime.strptime(line0[:8], '%H:%M:%S')
	line0 = line
    f.close

    return result

# main module
def main():

    import os
    from datetime import datetime
    from datetime import timedelta

    global atime

    # get files list
    fso_list = getFsoList(apath)

    # output
    print '\n log files list (sorted by time modified):'
    for i in fso_list:
	print i    

    # search first id in logs
    alist = findFirstID(fso_list)

    # init first id+time in logs
    fid = alist[0]
    ftime =  alist[1]

    # output
    print '\n first message in logs:\nid: %s time: %s' % (fid, str(ftime)[11:19])

    adocs = []

    while fid:
	adocs.append(fid)
	fid = findNextID(fso_list, ftime)
	ftime = ftime + timedelta(minutes = astep)

    # output
    print '\n time step %s min (doc_id,paydoc_ibso,tiket_otk,frod_otk,ticket_ibso):' % astep

    for atext in adocs:
	aout = ''
        atime = datetime.strptime('00:00:00', '%H:%M:%S')
        if fso_list:
            for fso_item in fso_list:
                res = findSubStr(fso_item, atext)
		if res != '':
		    aout = aout + res
	print atext + ' ' + aout

if __name__ == '__main__':

    # main module call
    main()
