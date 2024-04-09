import email
from email.header import decode_header
import imaplib
import re
from django.shortcuts import render
from django.template.response import TemplateResponse


from config.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from emailmanager.forms import HostChoice_1, HostChoice_2
from emailmanager.functns_for_help import charset_variants, decoded_header, dupl, get_variants, matched_in_str, matched_lsts, matched_str

def home(request):
    host_form_1 = HostChoice_1(request.POST)
    host_form_2 = HostChoice_2(request.POST)
   #  hosts = HostChoice.hosts.append(host_form)
    hosts = [] 

    context = {
        'host_form_1':host_form_1,
        'host_form_2':host_form_2,
      #   'hosts':hosts,
        
    }
    if request.method == "POST":
        if host_form_1.is_valid() and host_form_2.is_valid():
             host_1 = host_form_1.cleaned_data['host_1']
             host_2 = host_form_2.cleaned_data['host_2']
             email_1 = host_form_1.cleaned_data['email_1']
             email_2 = host_form_2.cleaned_data['email_2']
             password_1 = host_form_1.cleaned_data['password_1']
             password_2 = host_form_2.cleaned_data['password_2']
             hosts.append(((host_1, email_1, password_1), (host_2, email_2, password_2)))
            #  hosts = dupl(hosts)
             print(hosts)
             get_variants(hosts)
             context = {
        'host_form_1':host_form_1,
        'host_form_2':host_form_2,
        'hosts':hosts,
        'email_1': email_1,
        'email_2':email_2
        
            }
             return TemplateResponse(request, 'emailmanager/templates/emailmanager/home.html', context)
             
    else:
       host_form_1 = HostChoice_1()
       host_form_2 = HostChoice_2()

    return TemplateResponse(request, 'emailmanager/templates/emailmanager/home.html', context)
###########################
   # вывод формы по полям
   #  {{ host_form.non_field_errors }}
   #  <div class="fieldWrapper">
   #      {{ host_form.password }}
   #  </div>}
   
   #############################

charset_lst = ['utf-8', 'koi8-r', 'windows-1251',  'iso-8859-1', 'quoted-printable', 'unicode-escape']

def parse_emails():# на входе хост, емейл, пароль, отрезок емйлов спарсить, на выходе список мейлов - туплов

    mail_pass = EMAIL_HOST_PASSWORD
    username = EMAIL_HOST_USER
    imap_server = EMAIL_HOST
    imap = imaplib.IMAP4_SSL(imap_server)
    print(imap.login(username, mail_pass))
    imap.select("INBOX")
    _, msgnums = imap.uid('search', None, 'ALL')
    for msgnum in msgnums[0].split()[10:18]:
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