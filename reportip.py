#!/usr/bin/python3
#coding=utf-8
#case study
#Subject 1: 每次開機檢查新的IP與舊的IP不一樣時發出郵件通知並存檔(Count Hostname CPU MAC SDcard Datetime last-IP now-IP), Counts(每次開機累進+1)
#Subject 2: 每次開機產生一條新紀錄(Count Hostname CPU MAC SDcard Datetime last-IP now-IP),當新的IP與舊的IP不一樣時發出郵件通知, Counts(每次開機累進+1)
#Subject 3: Linux系統定時(Cron)運行檢查新的IP與舊的IP不一樣時發出郵件通知並存檔(Count Hostname CPU MAC SDcard Datetime last-IP now-IP), Counts(每次開機累進+1)
#Finially 1: smtplib 電子郵件@gmail.com 與@outlook.com 驗證都OK, 但有些Server安全性設定會導致無法發送
#Finially 2: 電子郵件"附件"是可以自由選擇
#Finially 3: "每次開機"是指有網路(ethernet or wifi)情形下開機
import os, sys, stat, socket
import time, threading
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
import code

#smtpserver = "smtp.gmail.com"
smtpserver = "smtp-mail.outlook.com"
#username = "louisopen@gmail.com"
username = "auto_report@outlook.com"
#password = "Cxxxxxx8"       #小心密碼放在這裡
password = "cxxx1xx3"       #小心密碼放在這裡
#sender = "louisopen@gmail.com"
sender = "auto_report@outlook.com"
#receiver = ["louisopen@hotmail.com","louisopen@outlook.com","louisopen@gmail.com"]
receiver = ["louisopen@hotmail.com"]
subject = "[RPi]IP Changed to "    #主題固定一個分類抬頭
last_ip=''
now_ip='0.0.0.0'


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
    if sendEmail(emailip)==True:
        print("Successfully send the e-mail")
    else:
        print("Fail the E-mail sending")

#==========================================================================
def get_SDserial():
    xcombine = os.popen("udevadm info -a -n /dev/mmcblk0 | grep -i serial | grep -n [a-zA-Z0-9] | awk -F'==\"' '{print $2}' ").read().strip()
    xcombine = xcombine.split('x')[1]   #抓(保留)字符串x後面(右邊)的字串
    xcombine = xcombine.split('\"')[0]  #抓(保留)字符串\"前面(左邊)的字串
    return xcombine

def get_CPUserial():
    return os.popen("cat /proc/cpuinfo |grep -i serial | awk -F ' ' '{print $3}'").read().strip()

def get_mac_address():
    return os.popen("ifconfig | grep -i ether|head -n 1 | awk -F' ' '{print $2}' ").read().strip()	#去字串頭尾
    '''
    import uuid
    node = uuid.getnode()
    return uuid.UUID(int = node).hex[-12:]
    '''
def get_user():
    import getpass
    user_name = getpass.getuser()
    return user_name

def get_IP():  
    get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    get_s.connect(('8.8.8.8', 0))
    #myaddr = socket.gethostbyname(myname)
    ip = ('%s') % (get_s.getsockname()[0])
    get_s.close()
    return ip
    #return os.popen("sudo hostname -I").read().strip()

#==========================================================================
# IP問題要考慮好: IP有可能獲取不到(當網路並非必要項時), 或網路雖為必要項但卻無法取得IP, 都會有問題!!!
# 沒有網路情況下或還未取得IP或得不到IP下,表示獲取IP是不會成功的
#==========================================================================
def until_IP():
    global now_ip
    while(True):        #thrading loop
        try:
            #now_ip=get_IP()
            now_ip=os.popen("hostname -I").read().strip()
            print ('Now ip %s'%now_ip)
            if now_ip !='0.0.0.0' or now_ip !=' ':
                break   #close threading
        except:
            now_ip = '0.0.0.0'
            #break       #close threading
        time.sleep(2)
    print ('End of threading.')


def checkinformation():
    global last_ip, now_ip, subject
    Counts = 0       #初始值, power on times
    myname = socket.getfqdn(socket.gethostname())
    #print(platform.platform())  
    CPUserial = get_CPUserial()
    MAC = get_mac_address()
    #print(MAC)
    subject += str(CPUserial)+" ("+ MAC +") "+str(now_ip)   #for mail subject
    try:
        #print (file_path)
        ip_file = open(file_path)       #如果檔案不存在, 直接錯誤到except創建
        last_ip = ip_file.read().replace('\n',' ')    #"換行代碼全部置換成" "
        ip_file.close()
        line = last_ip.split(' ')       #用" "分離出每個字串(組)
        #last_ip = last_ip.split('\n')
        Counts = int(line[-9])          #"累進值"位置(最後筆)
        Counts +=1
        last_ip = line[-2]              #取最後一次(行)的紀錄IP (以空白為間格,最後筆)
        #print(last_ip)
        emailip = str(Counts)+" "+myname+" "+str(CPUserial)+" "+MAC+" "+str(get_SDserial())+" "+datetime.datetime.now().strftime('%y%m%d-%H%M%S ')+str(last_ip)+" "+str(now_ip)
        ip_file = open(file_path,"a")   #可以變更"w"(只保留最後一筆)
        ip_file.write(str(emailip +"\n"))   
        ip_file.close()

    except Exception as ex:
        print ("%s: " % ex)
        emailip = str(Counts)+" "+myname+" "+str(CPUserial)+" "+MAC+" "+str(get_SDserial())+" "+datetime.datetime.now().strftime('%y%m%d-%H%M%S ')+"0.0.0.0 "+str(now_ip)
        ip_file = open(file_path,"w")   #初始化第一筆資料或"a"保留所有的變化
        ip_file.write(str(emailip +"\n"))
        ip_file.close()
        os.chmod(file_path, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH) #-rw-rw-rw- Linux command
        #os.chmod(file_info, stat.S_IWGRP | stat.S_IWOTH) #-rw-r--r-- Linux command
        #event_to_email(emailip)    #test
    #print(emailip)
    return emailip  #last string

# file_path config Linux or Windows
#file_path = os.path.split(os.path.realpath(__file__))[0] + '\powerupip.log'   #windows path
#file_info = os.path.split(os.path.realpath(__file__))[0] + '\information.txt'   #windows path
#file_path = os.path.split(os.path.realpath(__file__))[0] + '/powerupip.log'   #Linux path
#file_info = os.path.split(os.path.realpath(__file__))[0] + '/information.txt'   #Linux path

file_path = os.path.join(os.getcwd(),'Powerup_count_'+str(get_SDserial())+'.log')
file_info = os.path.join(os.getcwd(),'information.txt')

#==========================================================================
if __name__ == '__main__':
    #code.interact(local=locals())   #for interact test used
    th=threading.Thread(target=until_IP)
    th.start()
    th.join()
    systeminfo = checkinformation()
    
    #last_ip = "192.168.0.0"    #try for email everytime (可以去除,Subject 1)
    #print ("%s  %s"%(last_ip,now_ip))
    if last_ip == now_ip:
        #emailip=''
        pass
    else:
        event_to_email(systeminfo)
    #print ("IP changed: %s" % format(systeminfo))
    
    print (systeminfo)  #It is result
    