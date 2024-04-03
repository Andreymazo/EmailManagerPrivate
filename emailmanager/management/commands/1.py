from datetime import timedelta
from django.core.management import BaseCommand
from smtplib import SMTP, SMTP_SSL
from poplib import POP3, POP3_SSL
from imaplib import IMAP4, IMAP4_SSL
import argparse
import chardet

# s = r'\xed\xe5 \xff?xb\xff\xe5\xf2\xf1\xff \xef\xf0\xe8\xeb\xee\xe6\xe5\xed\xe8\xe5\xec'


# def parse():
def matched_in_str(str_for_match, lst_with_elements):#Выводит  список вошедших элементов в charset_lst
   new_lst1 = []
   new_lst2 = new_lst1
   for i in lst_with_elements:
      if i.lower() in str_for_match:
         new_lst1.append(i)
   print(new_lst2)
    # part = b'\xce\xed\xeb\xe0\xe9\xed \xe7\xe0\xea\xe0\xe7 \xed\xe0 \xf1\xe0\xe9\xf2\xe5 "\xc3\xe5\xee\xe3\xf0\xe0\xe4"'
    
    # a = chardet.detect(part)
    # print(a.get('encoding'))
    # print(part.decode('windows-1251'))
class Command(BaseCommand):
    def handle(self, *args, **options):
        # parse()
        raw_email_string = 'wfdvjhtgwkoi8-rlkbljhwnnytewindows-1251'
        charset_lst = ['utf-8', 'koi8-r', 'windows-1251',  'iso-8859-1', 'quoted-printable', 'unicode-escape']
        matched_in_str(raw_email_string,charset_lst)
    