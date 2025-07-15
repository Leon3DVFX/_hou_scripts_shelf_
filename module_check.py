#module_check.py
#Author: Leon3DVFX
#License: MIT
import hou 
def is_module_importable(m_name):
    try:
        __import__(m_name)
        return True
    except ImportError:
        return False
module_name = hou.ui.readInput('Write module name!')
if module_name[1] == '':
    hou.ui.displayMessage('Empty name')
else:
    if is_module_importable(module_name[1]):
        hou.ui.displayMessage(f'Module "{module_name[1]}" is IMPORTABLE')
    else:
        hou.ui.displayMessage(f'Module "{module_name[1]}" NOT found!')
