import subprocess
from django.core.management import BaseCommand
import os
from django.core.wsgi import get_wsgi_application

from emailmanager.management.commands.chek import parse_emails_2

def change_settigs_for_yandex_host():
   subprocess.run("sed 's/EMAIL_USE_TLS = True/EMAIL_USE_TLS = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)#Change one pattern to another
   subprocess.run("sed 's/EMAIL_USE_SSL = False/EMAIL_USE_SSL = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)#
   subprocess.run("sed 's/EMAIL_PORT = 465/EMAIL_PORT = 2525/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)#
  
   parse_emails_2()

  #  with open ('config/settings.py', ) as f:
        # subprocess.run('sed -n "180,181p" config/settings.py > file.txt', shell=True)# Копирование 180,181 строчки в файл
      # subprocess.run("sed '1,2d' file.txt>file_out && mv file_out file.txt ", shell=True) # Удаление с 1,2 строчки
        # subprocess.run("sed '180,181d' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)# Delete EMAIL_USE_TLS = True EMAIL_USE_SSL = False fm settings
        # subprocess.run("sed 's/EMAIL_USE_TLS = True/EMAIL_USE_TLS = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)#Change one pattern to another
        # subprocess.run("sed 's/EMAIL_USE_SSL = False/EMAIL_USE_SSL = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)#

      # subprocess.run("sed -n /EMAIL_USE_/p config/settings.py > file_out && mv file_out file_out.txt" , shell=True) # переносим строки с шаблоном в новый файл

      # subprocess.run(["sed", "-i", "/TLS/d", "file.txt"])#delete all lines that contain the word TLS 
      
      
# sed '1d' file.txt > tmpfile; mv tmpfile file.txt
    #   with open('file.txt', 'r+') as f:
    #         data = f.readlines()
    #         with open('file_in.txt', 'w') as ff:
    #               for index_line,i in enumerate(data):
    #                 index_row1 = 0
    #                 index_row2 = 0
    #                 index_row_fix_1 = 0
    #                 index_row_fix_2 = 0
    #                 filter1 = ''
    #                 filter2 = ''
    #                 iii_1 = ''
    #                 iii_2 = ''
                   
    #                 for j in range(len(i)):
    #                     # iiii_1 = 'EMAIL_USE_TLS = False'
    #                     # iiii_2 = 'EMAIL_USE_SSL = True'
    #                     iiii=''
    #                     # iiii_1 = iii_1
    #                     # iiii_2 = iii_2

    #                     while index_row1 + index_row_fix_1<= len(i)-1 and index_row2 + index_row_fix_2<= len(i)-1:
    #                         # if len(filter1) > 19 and filter1[-20:] == 'EMAIL_USE_TLS = False':
    #                         #     return ff.write(filter1[-20:])
                       
    #                         while len(filter1) > 19 and filter1[-20:] == 'EMAIL_USE_TLS = True' or  len(filter2) > 20 and filter2[-21:] == 'EMAIL_USE_SSL = False':
    #                             print('---------------------------')
    #                             # iii = iii[:-2]
    #                             # iii = iii + '_3'       
    #                             iii_1 = 'EMAIL_USE_TLS = False'
    #                             iii_2 = 'EMAIL_USE_SSL = True'
    #                             filter1 = ''
    #                             filter2 = ''
    #                             index_row_fix_1 += 5
    #                             index_row_fix_2 += 4
    #                             # if index_row1 + index_row_fix_1 >= len(i)-1:# Тут для ых 10 строчек надо обойти, иначе +2 стразу прибавляет больше лена
    #                             #     index_row_fix_1 -= 2
    #                             #     index_row_fix_2 -= 2
    #                         filter1 = ''.join([filter1,i[index_row1]])
    #                         filter2 = ''.join([filter2,i[index_row2]])
    #                         iii_1 = ''.join([iii_1,i[index_row1]])   
    #                         index_row1 += 1
    #                         iii_2 = ''.join([iii_2,i[index_row2]])
    #                         index_row2 += 1
    #                         if iii_1 == 'EMAIL_USE_TLS = False':
    #                             return ff.write(f'{iii_1}\nEMAIL_USE_SSL = True')# Надо вернуть в случае если TSL не True
    #                     # if iii_1 == 'EMAIL_USE_TLS = False' and iii_2 == 'EMAIL_USE_SSL = True':
    #                     #     return ff.write(iiii_1), ff.write(iiii_2)
    #                     # iiii_1 = iii_1
    #                     # iiii_2 = iii_2
    #                 return ff.write(iii_1), ff.write(iii_2)


class Command(BaseCommand):
    def handle(self, *args, **options):
        change_settigs_for_yandex_host()
