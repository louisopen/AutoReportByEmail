#!/usr/bin/python
#coding=utf-8
#Python coding for Raspberry Pi Linux
#Subject 1: 每次開機產生一條紀錄(Times Hostname MAC Datetime last-IP now-IP),當新的IP與舊的IP不一樣時發出郵件通知, Times(每次開機累進+1)
#Subject 2: 每次開機檢查新的IP與舊的IP不一樣時發出郵件通知並存檔(Times Hostname MAC Datetime last-IP now-IP), Times(每次開機累進+1)
#Subject 3: Linux系統定時(Cron)運行檢查新的IP與舊的IP不一樣時發出郵件通知並存檔(Times Hostname MAC Datetime last-IP now-IP), Times(每次開機累進+1)
#Finially 1: smtplib 電子郵件@gmail.com 與@outlook.com 驗證都OK, 但有些安全性設定會導致無法發送
#Finially 2: 電子郵件"附件"是可以自由選擇
#Finially 3: "每次開機"是指有網路(ethernet or wifi)情形下開機
import os, sys, stat, socket
import time
import datetime
#import platform
import struct
import smtplib
#import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
#from email.mime.image import MIMEImage

#smtpserver = "smtp.gmail.com"
smtpserver = "smtp-mail.outlook.com"
#username = "louisopen@gmail.com"
username = "auto_report@outlook.com"
#password = "Cxxxxxx8"       #小心密碼放在這裡
password = "cxxx12xx"       #小心密碼放在這裡
#sender = "louisopen@gmail.com"
sender = "auto_report@outlook.com"
#receiver = ["louisopen@hotmail.com","louisopen@outlook.com","louisopen@gmail.com"]
receiver = ["louisopen@hotmail.com"]
subject = "[RPi3]IP Changed to "    #主題固定一個分類抬頭

# file_path config Linux or Windows
#file_path = os.path.split(os.path.realpath(__file__))[0] + '\powerupip.txt'   #windows path
#file_info = os.path.split(os.path.realpath(__file__))[0] + '\information.txt'   #windows path
file_path = os.path.split(os.path.realpath(__file__))[0] + '/powerupip.txt'   #Linux path
file_info = os.path.split(os.path.realpath(__file__))[0] + '/information.txt'   #Linux path
times = 0     #初始值
myname = socket.getfqdn(socket.gethostname())

def check_attached(msgRoot):
    try:
        # open the file to be sent  
        filename = "information.txt"
        attachment = open(file_info, "rb") 
        # instance of MIMEBase and named as attached 
        af = MIMEBase('application', 'octet-stream')  
        # To change the payload into encoded form 
        af.set_payload((attachment).read()) 
        # encode into base64 
        encoders.encode_base64(af)   
        af.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        msgRoot.attach(af)  
    except Exception as e:
        print(e)
        
def sendEmail(msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] =  subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
   
    check_attached(msgRoot) #如果沒有附件,可以刪除

    try:    #smtp郵件主機都有安全性管制,有些必須手動打開才能轉發郵件
        smtp = smtplib.SMTP(smtpserver,587)    #TLS 
        #type(smtp)
        smtp.ehlo()
        smtp.starttls()                        #TLS only
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msgRoot.as_string())
        smtp.quit()

        #smtpssl=smtplib.SMTP_SSL(smtpserver, 465) #SSL
        #type(smtpssl)
        #smtpssl.ehlo()
        #smtpssl.login(username, password)
        #smtpssl.sendmail(sender, receiver, msgRoot.as_string())
        #smtpssl.quit()
        return True
    except Exception as e:
        print(e)
        return False

def event_to_email(emailip):
    global subject
    subject += now_ip +" ("+ MAC +")"
    if sendEmail(emailip)==True:
        print("Successfully send the e-mail")
    else:
        print("Fail the E-mail sending")

def get_mac_address():
    import uuid
    node = uuid.getnode()
    return uuid.UUID(int = node).hex[-12:]

def getIP():  #沒有網路下,不會成功
    get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    get_s.connect(('8.8.8.8', 0))
    ip = ('%s') % (get_s.getsockname()[0])
    return ip

if __name__ == '__main__':
    #print(platform.platform())  
    MAC = get_mac_address()
    #print(MAC)
    now_ip = getIP()
    try:
        print (file_path)
        ip_file = open(file_path)
        last_ip = ip_file.read().replace('\n',' ')    #"換行代碼全部置換成" "
        ip_file.close()
        line = last_ip.split(' ')    #用" "分離出每個字串(組)
        #last_ip = last_ip.split('\n')
        times = int(line[-7])     #"累進值"位置(最後筆)
        times +=1
        last_ip = line[-2]      #取最後一次的紀錄IP (以空白為間格,最後筆)
        #print(last_ip)

        now_ip = getIP()
        emailip = str(times)+" "+myname+" "+MAC+" "+datetime.datetime.now().strftime('%m%d%H%M%S ')+str(last_ip)+" "+str(now_ip)
        print(emailip)

        ip_file = open(file_path,"a")   #可以變更"w"(只留最後筆,Subject 2,3)
        ip_file.write(str(emailip +"\n"))   
        ip_file.close()
        
        #last_ip = "192.168.0.0" #try for email everytime (可以去除,Subject 1)
        if last_ip != now_ip:
            #print ("IP changed: %s" % format(emailip))
            event_to_email(emailip)

    except Exception as ex:
        #print ("%s: " % ex)
        emailip = str(times)+" "+myname+" "+MAC+" "+datetime.datetime.now().strftime('%m%d%H%M%S ')+"0.0.0.0 "+str(now_ip)
        print(emailip)
        ip_file = open(file_path,"w")
        ip_file.write(str(emailip +"\n"))
        ip_file.close()
        os.chmod(file_path, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH) #-rw-rw-rw- Linux command
        #os.chmod(file_info, stat.S_IWGRP | stat.S_IWOTH) #-rw-r--r-- Linux command
        event_to_email(emailip)