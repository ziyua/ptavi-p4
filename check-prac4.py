#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script de comprobación de entrega de práctica

Para ejecutarlo, desde la shell: 
 $ python check-prac4.py repo_github

"""

import os
import random
import sys

if len(sys.argv) != 2:
    sys.exit("Usage : $ python check-prac4.py repo_github")

repo_git = sys.argv[1]

files = ['README.md',
         'LICENSE',
         '.gitignore',
         'client.py',
         'server.py',
         'register.libpcap',
         '.git']

aleatorio = str(int(random.random() * 1000000))

error = 0

print 
print "Clonando el repositorio " + repo_git + "\n"
os.system('git clone ' + repo_git + ' /tmp/' + aleatorio + ' > /dev/null 2>&1')
try:
    student_file_list = os.listdir('/tmp/' + aleatorio)
except OSError:
    error = 1
    print "Error: No se ha podido acceder al repositorio " + repo_git + "."
    print 
    sys.exit()

if len(student_file_list) != 7:
    error = 1
    print "Error: solamente hay que subir al repositorio los ficheros indicados en las guion de practicas, que son en total 7:"

for filename in files:
    if filename not in student_file_list:
        error = 1
        print "\tError: " + filename + " no encontrado. Tienes que subirlo al repositorio."

if not error:
    print "Parece que la entrega se ha realizado bien."
    print
    print "La salida de pep8 es: (si todo va bien, no ha de mostrar nada)"
    print
    os.system('pep8 --repeat --show-source --statistics /tmp/' + aleatorio + '/client.py /tmp/' + aleatorio + '/server.py')
print
