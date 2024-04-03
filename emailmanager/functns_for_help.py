
from email.header import decode_header
import quopri

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