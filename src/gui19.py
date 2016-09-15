#!c:\Python34\python.exe
# -*- coding: cp1251 -*-

import sys
import os
import re
import random

try:
    # python 3
    from tkinter import *
    import tkinter.scrolledtext as tkst
    from tkinter.filedialog import askopenfilename, asksaveasfile
    from tkinter.messagebox import showerror
except ImportError:
    # python 2
    from Tkinter import *
    import ScrolledText as tkst
    from tkFileDialog import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.file_names = ''
        self.master.title("Грипалка курильщика")
        self.pack(fill = 'both', expand = 'true')

        menubar = Menu(self)
        self.master.config(menu=menubar)
        self.fileMenu = Menu(self, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.open_file)
        self.fileMenu.add_command(label="SaveFile", command=self.save_file)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=self.fileMenu)
        self.helpMenu = Menu(self, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.onExit)
        menubar.add_cascade(label="Help", menu=self.helpMenu)
        self.pack()
        
        toolbar = Frame(self, bd=1, relief=SOLID)
        self.grep_str = Entry(toolbar, relief=SUNKEN)
        self.grep_str.insert(0, 'ERROR Spoon')
        self.grep_str.pack(side=LEFT, padx=2, pady=2)
        self.grep_btn = Button(toolbar, relief=RAISED, text='grep', command=self.paste_log)
        self.grep_btn.pack(side=LEFT, padx=2, pady=2)
        self.clear_btn = Button(toolbar, relief=RAISED, text='clear', command=self.clear_log)
        self.clear_btn.pack(side=LEFT, padx=2, pady=2)
        self.err_btn = Button(toolbar, relief=RAISED, text='ERROR Spoon', command=self.err_str)
        self.err_btn.pack(side=LEFT, padx=2, pady=2)
        toolbar.pack(side=TOP, fill=X)

        self.log = tkst.ScrolledText(self, wrap= 'word')
        self.log.tag_configure('info1', background='#F3F781')
        self.log.tag_configure('info2', background='#A9F5A9')
        self.log.tag_configure('info3', background='#D8D8D8')
        self.log.tag_configure('err', background='#F78181')
        self.log.tag_configure('s_str', background='#90C3D4')
        self.log.pack(fill = 'both', expand = 'true')

        self.status_bar = Label(self, bd=1, relief=SUNKEN, anchor=W, text='none')
        self.status_bar.pack(side=BOTTOM, fill = 'both', expand = False)


    def onExit(self):
        self.quit()

    def clear_log(self):
        self.log.delete(1.0, END)

    def paste_log(self):
        None

    def err_str(self):
        self.grep_str.delete(0, END)
        self.grep_str.insert(INSERT, 'ERROR Spoon')

    def add_color(self, s, search_str):
        match = { search_str: 's_str',
                  'Выходные параметры вызова': 'info1',
                  'Получено сообщение': 'info1',
                  'Получатель сохранил сообщение': 'info2',
                  'Очередь ошибок сохранила сообщение': 'info2',
                  'Источник успешно удалил переданное сообщение': 'info3',
                  'ERROR Spoon': 'err'
                }

        out = []
        for item in match.keys():
            m1 = re.finditer(item, s)
            out = out + [(m.start(), m.group(), match[item]) for m in m1]

        out = sorted(out)
        pos = 0

        for i in range(len(out)):
            if s[pos:out[i][0]]: self.log.insert('end', s[pos:out[i][0]], '')
            self.log.insert('end', out[i][1], out[i][2])
            pos = out[i][0]+len(out[i][1])
        self.log.insert('end', s[pos:], '')

    def open_file(self):
        self.file_names = askopenfilename(multiple=1,
                                         filetypes=(('All files', '*.*'), ('log files', '*.log;*.txt')))
        if self.file_names:
            try:
                None #self.status_bar.config(text=self.file_names)
            except:                     # <- naked except is a bad idea
                showerror('Open Source File', "Failed to read file\n'%s'" % self.file_names)
        self.clear_log()

    def save_file(self):

        file_names = asksaveasfile(mode='w',defaultextension=".txt")

        if file_names:
            file_names.write(self.log.get("1.0", END ))
            file_names.close


def paste_log(obj):
    is_block = False
    block_str = ''
    prev_line = ''
    search_str = obj.grep_str.get()
    obj.clear_log()

    fso_list = [(f, os.stat(os.path.join('', f)).st_mtime) for f in obj.file_names]

    for f_name in sorted(fso_list, key=lambda tup: tup[1], reverse = False):
        obj.log.insert('end', '\n---\n'+f_name[0]+'\n---\n', '')
        with open (f_name[0], 'r') as f:
            for line in f:
                if re.match('^\d{2}:\d{2}:\d{2},\d{3}', line):
                    if 'Выполняем Rollback() у получателя' in line \
                              or 'Перенаправляем сообщение получателю' in line \
                                          or 'Очередь ошибок сохранила сообщение' in line:
                        block_str = block_str + line
                        continue
                    if block_str:
                        if search_str in block_str: obj.add_color(block_str, search_str)
                    block_str = ''
                block_str = block_str + line
            prev_line = line
    obj.status_bar.config(text=str(len(fso_list)) + ' file(s) processed')


Application.paste_log = paste_log
root = Tk()
app = Application(master=root)
app.mainloop()

