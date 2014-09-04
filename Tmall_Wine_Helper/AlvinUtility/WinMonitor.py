import os, subprocess
import poplib
import email,string
import email.header
import imaplib
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header

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

    
    mailHost = 'smtp.163.com'
    mail_user = r'alvingong119'
    mail_postfix = r'163.com'
    mail_pwd = r'5%tgb8ik,'

    def smtpSend(self, toList, sub, content):
        me = 'Ming<{0}@{1}>'.format(self.mail_user,self.mail_postfix)
        msg = MIMEText(content, _subtype='html',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ';'.join(toList)
        try:
            s = smtplib.SMTP()
            s.connect(self.mailHost)
            s.login(self.mail_user, self.mail_pwd)
            s.sendmail(me, toList, msg.as_string())
            s.close()
            return True
        except Exception as e:
            print(str(e))
            return False
    
    def smtpSendWithFile(self, toList, sub, att):
        msg = MIMEMultipart()
        me = 'Ming<{0}@{1}>'.format(self.mail_user,self.mail_postfix)
        msg['Subject'] = Header(sub,'gb2312')
        msg['From'] = me
        msg['To'] = ','.join(toList)
        #with open(att,'rb') as fp:
        #    content = MIMEBase('application', 'octet-stream')
        #    content.set_payload(fp.read())
        with open(att,'rb') as fp:
            content = MIMEText(fp.read(), _subtype = 'plain', _charset = 'utf-8')
        #encoders.encode_base64(content)
        content.add_header('Content-Disposition', 'attachment', filename = att)
        msg.attach(content)
        composed = msg.as_string()
        try:
          s = smtplib.SMTP()
          s.connect(self.mailHost)
          s.login(self.mail_user, self.mail_pwd)
          s.sendmail(me, toList, composed)
          s.close()
          return True
        except Exception as e:
          print(str(e))
          return False

#monitor = WinMonitorClass()
#content = "This is only a test mail sent by Python. Click following link to go to <a href='http://www.baidu.com'>百度</a>"
##monitor.imapHelper()
#mailtoList = [r'gongming119@hotmail.com', r'gongming119@outlook.com',r'xiaoxiaoluo3@126.com']
#if monitor.smtpSend(mailtoList, "Hello SMTP!", content):
#    print("Send Successfully...")
#else:
#    print("Send Mail Failed!!!")