import pprint
import quopri
from django.core.management import BaseCommand
from config import settings
from config.settings import BASE_DIR
import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
from django.core import mail
from django.core.mail import BadHeaderError, send_mail
import chardet

charset_lst = ['utf-8', 'koi8-r', 'windows-1251',  'iso-8859-1', 'quoted-printable', 'unicode-escape']
# andrewmazo@yandex.ru, anfreymazo215@gmail.com
def charset_variants(raw_email_string_f, charset_lst_f, message_f, raw_email_f):
       
       charset_f=''
       if len(matched_in_str(raw_email_string_f, charset_lst_f)):
         charset_f = matched_in_str(raw_email_string_f, charset_lst_f)[0] # Первое совпадение присваиваем charset
         # print('charset 1', charset_f)
       else:
         charset_f == message_f.get_content_charset() #  здесь по-сути присваеваем None
         # print('charset 2', charset_f)
       if charset_f:
         # print('charset 3', charset_f)
         if charset_f == 'quoted-printable': # Проеверяем если charset 'quoted-printable'
            raw_email_f=quopri.decodestring(raw_email_f)
         elif charset_f != 'quoted-printable':
            # print('charset 3.3', type(charset_f))
            # print(type(raw_email_f))
            # print(type(raw_email_string_f))
            raw_email_string_f = raw_email_f.decode(charset_f)
            return charset_f, raw_email_string_f, raw_email_f
       else:
         print('charset 4', charset_f)
         return charset_f, raw_email_string_f, raw_email_f# charset либо None, либо одна из шифровок, либо 'quoted-printable' 
       
def check_every_charset_str(body, charset_list):#body - string
   for i in charset_list:
         index = 0
         while not matched_str(decoded_header(decode_header(body))) and index <= len(charset_lst): # Индекс чтобы не впасть в бесконечность
            index += 1
         return decoded_header(decode_header(body))
   
def check_every_charset_bites(body, charset_list):#body - bites
   for i in charset_list:
         index = 0
         while not matched_str(body.decode(i)) and index <= len(charset_lst): # Индекс чтобы не впасть в бесконечность
            index += 1
         return(body.decode(i))
   
def matched_str(str_in): # Проверяем выводится ли русский или английский текст
  index = 0
  for i in str_in[0:10]:
   #   print('000000000000000   i.lower()', i.lower())
     if i.lower() in 'абвгдежзийклмнопрстуфхцчшщъыьэюя':# or i.lower() in 'abcdefghijklmnopqrstuvwxyz':
        index += 1
  if index >= 4:#Двигая индекс можно избегать ошибок, увеличивать вероятность правильной расшифровки. Откажемся от одновременной проверки на англ и русск языки, проще менять  ипроверять сначала одно потом другое
     return True
  return False

def matched_lsts(lst1, lst2):# Выводим первое вхождение списка в другой список
   for i,j in zip(lst1,lst2):
      if not i.upper()==j.upper():
         pass
      return j
   return None

def matched_in_str(str_for_match, lst_with_elements):#Выводит  список вошедших элементов в charset_lst
   new_lst1 = []
   new_lst2 = new_lst1
   for i in lst_with_elements:
      if i.lower() in str_for_match:
         new_lst1.append(i)
   return new_lst2

def decoded_header(decoded_header_in):
       decoded_text=''
       for part, encoding in decoded_header_in:
         if isinstance(part, bytes):
            charset_dict = chardet.detect(part)
            charset = charset_dict.get('encoding')
            decoded_text += part.decode(charset)
            
         else:
            decoded_text += part
       return  decoded_text

def parse_emails():
  # res = mail.send_mail(subject="Subject here",
  #   message="Here is the message.",
  #   from_email=settings.EMAIL_HOST_USER,
  #   recipient_list=["andreymazo@mail.ru"],
  #   fail_silently=False,
  #   auth_user=None,
  #   auth_password=None,
  #   connection=None,
  #   html_message=None,
  #   )
  
  # print(res)
    ###########################
#     from imap_tools import MailBox

# # get list of email bodies from INBOX folder
# with MailBox('imap.mail.com').login('test@mail.com', 'password', 'INBOX') as mailbox:
#     bodies = [msg.text or msg.html for msg in mailbox.fetch()]
    #####################################
    mail_pass = "NV37yjFSEbh0mCrLxnp1"
    username = "andreymazo@mail.ru"
    imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    print(imap.login(username, mail_pass))
    imap.select("INBOX")
    # print(imap.search(None, 'ALL'))
   #  _, msgnums = imap.search(None, 'ALL')
    _, msgnums = imap.uid('search', None, 'ALL')
    # print("444444444444444444444", len( msgnums[0]))
    for msgnum in msgnums[0].split()[10:18]:
       _, data = imap.fetch(msgnum, "(RFC822)")
      #  print(data[0])
       raw_email = data[0][1]
      #  print('raw_email', raw_email)
      #  message = email.message_from_bytes(raw_email)
      #  message = email.message_from_string
       print(f"Message number:  {msgnum}")
      #  print('message', message())
      #  print(f"To:  {message.get('To')}")
     #########################################################  
      #  raw_email = data[0][1]
       message = email.message_from_bytes(raw_email)
       charset = message.get_content_charset()
       print('message.get_charset', message.get_content_charset())
     
          
      # #  print("444444444444444444444",raw_email)
       raw_email_string=str(raw_email)
      #  print('raw_email_string[0:10], ', raw_email_string[0:7700])
      # #  print('raw_email_str', raw_email_str)

       match_result_1 = re.search('Content-Type: text/plain; charset="windows-1251"', raw_email_string)
       match_result_2 = re.search('Content-Type: text/plain; charset=UTF-8', raw_email_string)
       match_result_3 = re.search('Content-Type: application/msword', raw_email_string)
       match_result_4 = re.search('Content-Type: text/plain; charset=ISO-8859-1', raw_email_string)
       match_result_5 = re.search('Content-Transfer-Encoding: quoted-printable', raw_email_string)
       print(match_result_1)
       print(match_result_2)
       print(match_result_3)
       print(match_result_4)
       print(match_result_5)
       
       print('matched_in_str(raw_email_string, charset_lst', matched_in_str(raw_email_string, charset_lst)) # Серяем совпадения в raw_email_string charset_lst
       charset, raw_email_string, raw_email = charset_variants(raw_email_string, charset_lst, message, raw_email)
       email_message = email.message_from_string(raw_email_string)
       message = email.message_from_bytes(data[0][1])
       subject_msg = message['Subject']
       from_msg = message['From']
       to_message = message.get('To')
   
       letter_date = email.utils.parsedate_tz(message["Date"])
       print('letter_date', letter_date)
       letter_from = message["Return-path"] # e-mail отправителя
       message_id = message.get('Message-ID')
       print(f"Message number:  {msgnum}")
      #  print(f"To:  {decode_header(to_message)[0][0]+decode_header(to_message)[0][1]}")
       print(f"Date:  {message.get('Date')}")
       print('subject_msg', subject_msg)
       try:
         print('Subject msg', decoded_header(decode_header(subject_msg)))
       except TypeError as e:
          print(e)
       print('To msg', decoded_header(decode_header(to_message)))
       print('From msg', decoded_header(decode_header(from_msg)))
       print(f'Message-ID {message_id}')
      #  try:
      #    body = subject_msg[:14].lower()
      #    # print('type(body), body', type(body), body)
      #  except  TypeError as e:
      #     print(e)
      # #  print('subject_msg[2:8].lower()', subject_msg[2:8].lower() )
      #  try:
      #    # print('1111111111222222222222222subject_msg[2:13].lower() ',body.lower(), matched_in_str(body, charset_lst))
      #    charset_lst_for_subject = matched_in_str(body, charset_lst)
      #  except TypeError as e:
      #     print(e)
      #  try:   
      #     if len(charset_lst_for_subject):
      #         print(check_every_charset_str(body, charset_lst_for_subject))
            #  for i in charset_lst_for_subject:
            #     index = 0
            #     while not matched_str(body.decode(i)) and index <= len(charset_lst): # Индекс чтобы не впасть в бесконечность
            #        index += 1
            #  print(body.decode(i))
      #     if not len(charset_lst_for_subject):
      #          print(check_every_charset_str(body, charset_lst))
      #  except TypeError as e:
      #     print(e)
            #  print(f"Subject: {decoded_header(decode_header(subject_msg))}")
         # if subject_msg[2:8].lower() in charset_lst or subject_msg[2:13].lower() in charset_lst:
            
         #    print(f"Subject: {decoded_header(decode_header(subject_msg))}")#{decode_header(subject_msg)[0][0].decode(charset)}")
         # elif subject_msg[2:8].lower() not in charset_lst  or subject_msg[2:13].lower() not in charset_lst:
         #    print(f"Subject: {subject_msg}")   
      #  except TypeError as e:
      #    print(e)  
         
      #  try:     
      #    if to_message[2:8] in charset_lst:
      #          to_message = decoded_header(decode_header(to_message))
      #    elif to_message[2:8] not in charset_lst:
      #          print(f"To: {to_message}")
      #  except TypeError as e:
      #    print(e)  
        
      #  if from_msg[2:8].lower() in charset_lst:
      #       # print(f"From: {decode_header(from_msg)[0][0].decode(charset)}")
      #       print(f"From: {decoded_header(decode_header(from_msg))}")
      #  elif from_msg[2:8].lower() not in charset_lst:
      #    print(f"From: {from_msg}")
      #    print('letter_from (емэйл отправителя)', letter_from)
         
      
       
      #  if subject_msg[2:8] in charset_lst:
      #       print(f"Subject: {decode_header(subject_msg)[0][0].decode(charset)}")
      #  else:
      #       print(f"Subject: {subject_msg}")
         
      #  to_message = decoded_header(decode_header(to_message))
      #  print(f"To: {to_message}")
      #  print(f"From: {(from_msg)}")
      #  print('letter_from (емэйл отправителя)', letter_from)
      #  print(f'Message-ID {message_id}')
      #  decoded_text=''
      #  for part, encoding in decoded_header:
      #    if isinstance(part, bytes):
      #       decoded_text += part.decode(encoding or 'utf-8')
      #    else:
      #       decoded_text += part

      #  print('decoded_text', decoded_text)
      
      #  print(f"Subject:  {decode_header(subject_msg)[0][0].decode(charset)}")
      #  print(f"From:  {decode_header(from_msg)[0][0].decode(charset)}")
      #  if not subject_msg:
      #    print(f"Subject:  {decode_header(subject_msg)[0][0].decode(charset)}")
      #  else:
      #    print('Subject: None')
      #  imap.fetch(b'19', "(BODY[HEADER.FIELDS (Subject)])")
      #  if not from_msg:
      #    print(f"From:  {decode_header(from_msg)[0][0].decode(charset)}")
      #  else:
      #    print("From:  None")
       
       for part in email_message.walk():
          
          print('part.get_content_type()', part.get_content_type())
         #  if part.get_content_type()=='multipart/mixed':
         #    #  if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
         #       body = part.get_payload(decode=True)
         #       print('body', body)
          if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            # print(base64.decode((part.get_payload())))
            body = part.get_payload(decode=True)
            
            # print('body', body)
            # print('part.as_string()', part.as_string())
            # print('message.get_charset', message.get_content_charset())
            # charset = message.get_content_charset()
            # print(body)
            # print(body.decode(charset))
            # print('charset', charset)
            if charset == None:
               print('charset', charset)
               charset = [subject_msg[2:8], to_message[2:8], from_msg[2:8]]
               charset = matched_lsts(charset, charset_lst)
               print('charset', charset)
               for i in charset_lst:
                index = 0
                while not matched_str(body.decode(i)) and index <= len(charset_lst): # Индекс чтобы не впасть в бесконечность
                   index += 1
                print(body.decode(i))

               # if charset == 'windows-1251' or 'utf-8' :
               #    print('++++++++++++unicode_escape1++++++++++++', body.decode('unicode-escape'))
               # # charset = from_msg[2:8]
               # elif charset != 'windows-1251' or 'utf-8' :
               #    print('++++++++++++++++++++++++++++++++++++++++', body.decode(charset))
            elif charset != 'windows-1251' or 'utf-8' :
                  if matched_str(body.decode(charset)):
                     print('++++++++++++++++++1111111111++++++++++++++++++++++', body.decode(charset))
                  
                  elif not matched_str(body.decode(charset)):
                     # print('check_every_charset_bites(body, charset_lst)', check_every_charset_bites(body, charset_lst))
                     # print('body.decode(charset)[0:29]', matched_str(body.decode(charset)))
                     print('++++++++++++++++++2222222222222222++++++++++++++++++++++', body.decode('unicode-escape'))
            elif charset == 'windows-1251' or 'utf-8':
               print('++++++++++++unicode_escape++++++++++++', body.decode('unicode-escape'))
            # elif charset == 'utf-8':
            #    print('--------------------------------tttttttttttttttt', (body).decode('unicode_escape'))
            else:
               print('----------------------------------------------------------rrrrrrrrrrrrrr', body.decode(charset))
             
    imap.close()
  
class Command(BaseCommand):
   
    def handle(self, *args, **options):
    
      parse_emails()
      
      

#       import zipfile, re

# docx = zipfile.ZipFile('/path/to/file/mydocument.docx')
# content = docx.read('word/document.xml').decode('utf-8')
# cleaned = re.sub('<(.|\n)*?>','',content)
# print(cleaned)