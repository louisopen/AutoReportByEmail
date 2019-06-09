#!/usr/bin/env python
#coding:utf-8
#You may need pip install psutil
import psutil
import datetime
import time
import platform

now_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))

#User Computer network name
string = platform.node()            #LOUIS-NB
print("Network ID: %s" % string)

# Python Version
#string = platform.python_version()  #3.6.6
#print("Python %s" % string)

# Python直譯器Build日期 
string = platform.python_build()    #('v3.6.6:4cf1f54eb7', 'Jun 27 2018 03:37:03')
print("Python build: %s" % string[0])

# Python直譯器訊息 
string = platform.python_compiler() #MSC v.1900 64 bit (AMD64)
print("Python architecture: %s" % string)

#OS版本
#string = platform.system()  #Windows or Linux or ...
#print(string)
#string = platform.system_alias()
#string = platform.version() # OS版本 10.0.18362
#print(string)
#string = platform.platform()        #Windows-10-10.0.18362-SP0
print("OS Version: %s %s" % (str(platform.system()), str(platform.version())) )

# System architecture
string = platform.architecture()    #(’32bit’, ‘WindowsPE’)
print("OS architecture: %s" % string[0])

#Processor身分
string = platform.processor()       #Intel64 Family 6 Model 78 Stepping 3, GenuineIntel
print("CPU processor family: %s" % string)

# 查看cpu的信息
print ("CPU Core: %s" % psutil.cpu_count(logical=False))
cpu = (str)(psutil.cpu_percent(1)) + '%'
print ("cup used rate: %s" % cpu)

# 查看内存信息,剩余内存.free  总共.total
free = str(round(psutil.virtual_memory().free/(1024.0*1024.0*1024.0), 2))
total = str(round(psutil.virtual_memory().total/(1024.0*1024.0*1024.0), 2))
memory = int(psutil.virtual_memory().total-psutil.virtual_memory().free)/float(psutil.virtual_memory().total)
print ("RAM容量: %s G" % total)
print ("可用RAM: %s G" % free)
print ("RAM使用率: %s %%" % int(memory*100))

# 系统启动时间
print ("系统開始時間: %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

# 系统用户
users_count = len(psutil.users())
users_list = ",".join([u.name for u in psutil.users()])
print ("當前有%s個用户，分别是: %s" % (users_count, users_list))

'''
#print ('-----------------------------本機網卡訊息-------------------------------------')
import socket
hostname = socket.gethostname()
addrs = socket.getaddrinfo(hostname,None)
#addrs = socket.getaddrinfo(hostname, port, family=0, type=0, proto=0, flags=0)
print("Network interface: ")
for item in addrs:
    print(item)
'''

#print ('---------------------------本機網卡訊息(MAC)----------------------------------')
print("Network MAC address: ")
from psutil import net_if_addrs
for k, v in net_if_addrs().items(): #區域網路*2 or Bluetooth...
    for item in v:
        macaddress = item[1]
        if ':' in macaddress and len(macaddress)==17: #符合數量及"-"(Windows) ":"(Linux)
            print(v[0].address +" "+ macaddress)    #in Linux
            #print(v[1].address +" "+ macaddress)   #in Windows

# 网卡，可以得到网卡属性，连接数，当前流量等信息
print ('-----------------------------網路信息-------------------------------------')
net = psutil.net_io_counters()
#print(net)         #目前網路訊息(太多了)
bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024/1024)
bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024/1024)
print ("網卡接收流量: %s 網卡发送流量: %s" % (bytes_rcvd, bytes_sent))
#print (psutil.net_connections())       #目前網路連線訊息(太多了)

'''
print ('-----------------------------磁盤信息in Windows---------------------------')
io = psutil.disk_partitions()
print ("系统磁盤信息: "+str(io))
for i in io:
    o = psutil.disk_usage(i.device)
    print ("總容量: "+str(int(o.total/(1024.0*1024.0*1024.0)))+"G")
    print ("已用容量: "+str(int(o.used/(1024.0*1024.0*1024.0)))+"G")
    print ("可用容量: "+str(int(o.free/(1024.0*1024.0*1024.0)))+"G")

print ('-----------------------------进程信息-------------------------------------')
# 查看系统全部进程
for pnum in psutil.pids():
    p = psutil.Process(pnum)
    print ("进程名 %-20s  内存利用率 %-18s 进程状态 %-10s 创建时间 %-10s "\
          % (p.name(), p.memory_percent(), p.status(),  p.create_time()))
'''