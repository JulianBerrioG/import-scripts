import os 
import platform

system = platform.system()
print(system)
def formatted_route(file_route):
    if system == 'Windows':
        return file_route.replace('/','\\')
    else:
        print('new',file_route.replace('\\','/'))
        return file_route.replace('\\','/')