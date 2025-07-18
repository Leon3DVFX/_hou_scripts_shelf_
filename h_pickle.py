#h_pickle.py
#Author: Leon3DVFX
#License: MIT
import hou, os

f_form = '.hpkl'
#Функция path_norm заменяет $HIP на текущий рабочий каталог, возвращает абс. нормализованый путь(str)
def path_norm(path):
    new_path = path
    if path.startswith('$HIP'):
        new_path = path.replace('$HIP',os.getcwd())
    return os.path.normpath(new_path)
#Класс FileSaver(описание устройства записи)
class FileSaver:
    def __init__(self, path, node):
        self._mode = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        self._path = path_norm(path+f_form)
        self._file = os.open(self._path,self._mode)
        try:
            os.write(self._file, node.asCode(recurse=True).encode('utf-8'))
        finally:
            os.close(self._file)
#Класс FileLoader(описание устройства загрузки)            
class FileLoader:
    def __init__(self,path):
        self._mode = os.O_RDONLY
        self._path = path_norm(path)
        self._file = os.open(self._path,self._mode)
        try:
            exec(os.read(self._file, os.path.getsize(self._path)).decode('utf-8'))
        finally:
            os.close(self._file)
#Первоначальный выбор        
m_start = hou.ui.displayMessage('Create or Load Hpkl?', buttons=('Create','Load','Close'),\
                                close_choice = -1, default_choice = 2)
#Инструкция на основе первоначального выбора
match m_start:
    case 0:#Сохранение файла
        sel_node = hou.ui.selectNode(title = 'Select container!')
        if sel_node in {'/obj', '/mat', '/shop','/img','/out','/stage','/tasks','/ch', None}:
            hou.ui.displayMessage('Operation interrupted')
        else:
            node = hou.node(sel_node)
            hpath = hou.ui.selectFile(title = 'Select directory and give file name',\
                                     file_type = hou.fileType.Directory)

            if hpath.endswith('/'):
                hou.ui.displayMessage('Operation interrupted')
            else:
                abs_path = path_norm(hpath)
                if os.path.exists(abs_path+f_form):
                    repl = hou.ui.displayMessage('This file are exist!\nReplace?',buttons=('YES','NO'))
                    if repl == 0:
                        file = FileSaver(abs_path, node)
                    else:
                        hou.ui.displayMessage('Operation interrupted')
                else:
                    file = FileSaver(abs_path, node)
    case 1:#Загрузка файл(ов)
        sel_files = hou.ui.selectFile(title = 'Select Hpkl file or files', multiple_select = True,\
                                      pattern = '*.hpkl')
        paths = sel_files.split(' ; ')
        for hpath in paths:
            abs_path = path_norm(hpath)
            FileLoader(abs_path)
    case _:#_ - если выбранное не соответствует ни одному образцу
        hou.ui.displayMessage('Operation interrupted')