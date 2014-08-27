import os, subprocess
import poplib
import email,string
import email.header
import imaplib
import sys

class WinMonitorClass():

    def __init__(self):
        print('Monitor is running...')

    def netOkOrFail(self,addr=r'www.baidu.com'):
        fnull = open(os.devnull,'w')
        result = subprocess.Popen(['ping', addr, '-n', '1'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,\
            universal_newlines=True, shell=True)
        if result:
            print('Network OK')
            print(result.stdout.read())
            print('Return Code: {0}'.format(str(result.returncode)))
        else:
            print('Network Failed')
        fnull.close()

    def parseMailHeaders(self):
        p = poplib.POP3('pop3.163.com')
        p.user(r'alvingong119@163.com')
        p.pass_(r'5%tgb8ik,')
        #ret = p.stat()
        numMessages = len(p.list()[1])
        for i in range(numMessages):
            #for j in p.retr(i+1)[1]:
            #    print(j)
            hdr,message,octet = p.retr(i+1)
            #header = email.header.Header.decode_header('subject')
            #subject = headers.decode_header(mail['subject'])
            mail = email.message_from_string('\n'.join([x.decode('utf-8') for x in message]))
            subject = email.header.decode_header(mail['subject'])
            print(subject[0][0].decode('utf-8'))
            fromWho = email.header.decode_header(mail['from'])
            print(fromWho[1][0].decode('utf-8'))
        p.quit()

    def imapHelper(self):
        mail = imaplib.IMAP4('imap.163.com')
        mail.login(r'alvingong119@163.com','5%tgb8ik,')
        #mail.list()
        mail.select('inbox')
        typ, data = mail.search(None, 'UNSEEN')
        for num in data[0].split():
            #typ, data = mail.fetch(num, '(RFC822)')
            #mail.store(num, '-FLAGS','\SEEN')
            typ, data = mail.fetch(num, '(BODY.PEEK[HEADER])')
            mailText = data[0][1].decode('utf-8')
            message = email.message_from_string(mailText)
            subject = email.header.decode_header(message['subject'])
            subjectValue = subject[0][0].decode('utf-8') if subject[0][1] == 'utf-8' else subject[0][0]
            print(subjectValue)
            fromWho = email.utils.parseaddr(message['from'])[1]
            print('From {0}'.format(fromWho))
            #print('mail mssage %s\n%s\n' % (num,repr(data)))
        mail.close()
        mail.logout()

monitor = WinMonitorClass()
monitor.imapHelper()