#!/usr/bin/python
# -*- coding: cp1251 -*-

# Грипалка здорового человека

f_name = '20160311_05'
find_str = '73731051901'

prev_line = ''
is_block = False

import sys

with open (f_name, 'r') as f:
    for line in f:

	# error block
        if is_block:
            block_str = block_str + line
            if 'Очередь ошибок сохранила сообщение' in prev_line:
                is_block = False
                if find_str in line: print (block_str)
        else:
            if 'ERROR Spoon' in prev_line:
                block_str = prev_line
                is_block = True
            # regular lines
            if find_str in line: print (prev_line + line)

        prev_line = line
