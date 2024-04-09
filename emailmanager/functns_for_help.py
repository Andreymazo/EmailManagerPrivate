from email.header import decode_header
import imaplib
import quopri
import re
import subprocess
import chardet
import email
from config.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_SSL, EMAIL_USE_TLS, SECOND_EMAIL_HOST, SECOND_EMAIL_HOST_PASSWORD, SECOND_EMAIL_HOST_USER

charset_lst = ['utf-8', 'koi8-r', 'windows-1251',  'iso-8859-1', 'quoted-printable', 'unicode-escape']
# andrewmazo@yandex.ru, anfreymazo215@gmail.com

def dupl(data_2):##Ubiraem duplikati 
            index = 0
            a=[]
            while len(data_2) >index and data_2[index] not in a:
                   a.append(data_2[index])
                   index += 1
            index += 1
            # print(a)
            return a

def change_smth_in_file():
   with open ('config/settings.py', ) as f:
      subprocess.run('sed -n "699,907p" astrology/views.py > file.txt', shell=True)

      with open('file.txt', 'r+') as f:
            data = f.readlines()
            with open('file_in.txt', 'w') as ff:
                  for index_line,i in enumerate(data):
                    index_row1 = 0
                    index_row2 = 0
                    filter = ''
                    iii = ''
                    for j in range(len(i)):
                        iiii=''
                        while index_row1 + index_row2 <= len(i)-1:
                            while len(filter) > 15 and filter[-16:] == 'number_to_chek_2':
                                iii = iii[:-2]
                                iii = iii + '_3'
                                filter=''

                                index_row2 += 2
                                if index_row1 + index_row2 >= len(i)-1:# Тут для ых 10 строчек надо обойти, иначе +2 стразу прибавляет больше лена
                                    index_row2 -= 2
                            filter = ''.join([filter,i[index_row1]])
                            iii = ''.join([iii,i[index_row1]])   
                            index_row1 += 1

                            # iiii = iii + i[-index_row2+1:-1]
                        iiii = iii + i[-index_row2:]
                    ff.write(iiii)

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

def decoded_header(decoded_header_in):#Декодируем байты, применяем в заголовках (для заголовков(прям класс такой есть) - decode_header, для байтов надо эту функцию применять)
       decoded_text=''
       for part, encoding in decoded_header_in:
         if isinstance(part, bytes):
            charset_dict = chardet.detect(part)
            charset = charset_dict.get('encoding')
            decoded_text += part.decode(charset)
         else:
            decoded_text += part
       return  decoded_text

def parse_emails(imap_server, username, mail_pass):
    print('00000000000000000eeeeeeeeeeeee00000000000000000')
   #  mail_pass = EMAIL_HOST_PASSWORD#'tCdHZrMJA41mCchy3mxk'#
   #  username = EMAIL_HOST_USER#'andreymazo@mail.ru'#
   #  imap_server = EMAIL_HOST#'imap.mail.ru'#
    subprocess.run("sed 's/EMAIL_USE_TLS = False/EMAIL_USE_TLS = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
    subprocess.run("sed 's/EMAIL_USE_SSL = True/EMAIL_USE_SSL = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
    subprocess.run("sed 's/EMAIL_PORT = 465/EMAIL_PORT = 2525/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)

    print('imap_server, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL username mail_pass', imap_server, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL, username, mail_pass)
    imap = imaplib.IMAP4_SSL(imap_server)
    print(imap.login(username, mail_pass))
    imap.select("INBOX")
    _, msgnums = imap.uid('search', None, 'ALL')
    for msgnum in msgnums[0].split()[:1]:
       _, data = imap.fetch(msgnum, "(RFC822)")
       raw_email = data[0][1]
    
       print(f"Message number:  {msgnum}")
 
       message = email.message_from_bytes(raw_email)
       charset = message.get_content_charset()
       print('message.get_charset', message.get_content_charset())
       raw_email_string=str(raw_email)
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
       for part in email_message.walk():
         #  print('part.get_content_type()', part.get_content_type())
          if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            body = part.get_payload(decode=True)
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
            elif charset != 'windows-1251' or 'utf-8' :
                  if matched_str(body.decode(charset)):
                     print('++++++++++++++++++1111111111++++++++++++++++++++++', body.decode(charset))
                  elif not matched_str(body.decode(charset)):
                     print('++++++++++++++++++2222222222222222++++++++++++++++++++++', body.decode('unicode-escape'))
            elif charset == 'windows-1251' or 'utf-8':
               print('++++++++++++unicode_escape++++++++++++', body.decode('unicode-escape'))
            else:
               print('----------------------------------------------------------rrrrrrrrrrrrrr', body.decode(charset))
       
    imap.close()

def parse_emails_2(imap_server,username, mail_pass):
    mail_pass = SECOND_EMAIL_HOST_PASSWORD
    username = SECOND_EMAIL_HOST_USER
    imap_server = SECOND_EMAIL_HOST
    subprocess.run("sed 's/EMAIL_USE_TLS = True/EMAIL_USE_TLS = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
    subprocess.run("sed 's/EMAIL_USE_SSL = False/EMAIL_USE_SSL = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
    subprocess.run("sed 's/EMAIL_PORT = 465/EMAIL_PORT = 2525/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
    # print('imap_server, username, mail_pass, EMAIL_USE_TLS',imap_server, username,  mail_pass)#, EMAIL_USE_TLS)
    imap = imaplib.IMAP4_SSL(imap_server)#, ssl_context=ctx)
    print('22222222222222222222222222222222222jjjjjj2222222222222222s')
    print(imap.login(username, mail_pass))
   
    imap.select("INBOX")
    _, msgnums = imap.uid('search', None, 'ALL')
    for msgnum in msgnums[0].split()[:1]:
       _, data = imap.fetch(msgnum, "(RFC822)")
       raw_email = data[0][1]
       print(f"Message number:  {msgnum}")
       message = email.message_from_bytes(raw_email)
       charset = message.get_content_charset()
       print('message.get_charset', message.get_content_charset())
       raw_email_string=str(raw_email)
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
       for part in email_message.walk():
         #  print('part.get_content_type()', part.get_content_type())
          if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            body = part.get_payload(decode=True)
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
            elif charset != 'windows-1251' or 'utf-8' :
                  if matched_str(body.decode(charset)):
                     print('++++++++++++++++++1111111111++++++++++++++++++++++', body.decode(charset))
                  elif not matched_str(body.decode(charset)):
                     print('++++++++++++++++++2222222222222222++++++++++++++++++++++', body.decode('unicode-escape'))
            elif charset == 'windows-1251' or 'utf-8':
               print('++++++++++++unicode_escape++++++++++++', body.decode('unicode-escape'))
            else:
               print('----------------------------------------------------------rrrrrrrrrrrrrr', body.decode(charset))
       
    imap.close()

def get_variants(a):
      for i in a[0]:
         print(i[0][0])
         if a[0][0][0] == 'imap.mail.ru':
            print('888888888888888888888811111111111111111111111')
            subprocess.run("sed 's/EMAIL_USE_TLS = True/EMAIL_USE_TLS = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            subprocess.run("sed 's/EMAIL_USE_SSL = False/EMAIL_USE_SSL = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            subprocess.run("sed 's/EMAIL_PORT = 465/EMAIL_PORT = 2525/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            EMAIL_HOST_PASSWORD=i[2]
            print('EMAIL_HOST_PASSWORD', EMAIL_HOST_PASSWORD)
            EMAIL_HOST_USER=i[1]
            EMAIL_HOST=i[0]
            # return EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_HOST
            parse_emails(EMAIL_HOST,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
         if a[0][1][0] == 'imap.yandex.ru':
            print('enter yandex mmm')
            subprocess.run("sed 's/EMAIL_USE_TLS = True/EMAIL_USE_TLS = False/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            subprocess.run("sed 's/EMAIL_USE_SSL = False/EMAIL_USE_SSL = True/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            subprocess.run("sed 's/EMAIL_PORT = 465/EMAIL_PORT = 2525/i' config/settings.py>file_out && mv file_out config/settings.py ", shell=True)
            SECOND_EMAIL_HOST_PASSWORD=i[2]
            SECOND_EMAIL_HOST_USER=i[1]
            SECOND_EMAIL_HOST=i[0]
            parse_emails_2(SECOND_EMAIL_HOST,SECOND_EMAIL_HOST_USER,SECOND_EMAIL_HOST_PASSWORD)
        

      # get_variants([(1,2,3),(4,5,6)])