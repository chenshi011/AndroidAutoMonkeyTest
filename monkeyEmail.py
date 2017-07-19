#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
import os, json, time, re, base64, smtplib, threading
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from logging import thread
import subprocess
def _matchFiles(path, pattern):
    files = []
    for f in os.listdir(path):
        match = pattern.match(f)
        if match:
            if os.path.getsize(r'%s\%s' % (path , f)) > 0:
                files.append(f)
    return files

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    
def _addbase(path, files, filetype):
    mimes = []
    for f in files:
        with open(r'%s\%s' % (path , f), 'rb') as fil:
            mime = MIMEBase('text', filetype, filename=f)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=f)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(fil.read())
            encoders.encode_base64(mime)
            mimes.append(mime)    
    return mimes;        

def _sendEmail(from_addr, basepsd, msg, smtp_server='smtp.exmail.qq.com', to_addr):
    password =  base64.b64decode(basepsd)
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    
def _shell(shell_cmd):
    print "shell:%s" % shell_cmd
    subprocess.Popen(shell_cmd, shell=True)
    #os.system(shell_cmd)
    
abspath = os.path.split(os.path.realpath(__file__))[0] + "/"
with open(abspath + "monkeyEmail.json", 'r') as js:
    json_data = json.load(js)
with os.popen("adb devices") as shell:
    device_line = shell.read()  
devices = re.split(r'[\s]+', device_line)
print devices

time_s = time.strftime(json_data["time_format"],time.localtime(time.time()))    
print "time_s::%s" % time_s    
logs_path = json_data["logs_path"]
file_type = json_data["file_type"]
monkey_error = json_data["monkey_error_name"]
monkey_log = json_data["monkey_log_name"]
dirty = ['List', 'of', 'devices', 'attached', 'offline', 'device', '']
threads = []
for device in devices:
    if device in dirty:
        continue
    device_name = device.replace(":",".")
    adb_cmd = "adb -s %s shell monkey -p %s %s %d %d 2 > %s/%s_%s(%s).%s 1 > %s/%s_%s(%s).%s" % (device,json_data["pakeage"],json_data["param"],json_data["delay"],json_data["times"],logs_path,device_name,monkey_error,time_s,file_type,logs_path,device_name,monkey_log,time_s,file_type)
    thread = threading.Thread(target=_shell, args=(adb_cmd,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
run_time = long(json_data["delay"]) * long(json_data["times"]) / 1000 + 2    
print "time.sleep %s s" % str(run_time)    
time.sleep(run_time)    
print "now try match files"

time_s_match = time.strftime(json_data["time_format_match"],time.localtime(time.time()))   
pattern_error = re.compile('^%s\(%s' % (monkey_error , time_s_match))
pattern_log = re.compile('^%s\(%s' % (monkey_log , time_s_match))
mimes_error = _addbase(logs_path, _matchFiles(logs_path, pattern_error), file_type)
if len(mimes_error) > 0:
    print "have monkey error try send email"
    msg = MIMEMultipart()
    print "add monkey error files%s " % len(mimes_error)
    for mime_error in mimes_error:
        msg.attach(mime_error)
    mimes_log = _addbase(logs_path, _matchFiles(logs_path, pattern_log), file_type)
    print "add monkey log files %s " % len(mimes_log)
    for mime_log in mimes_log:
        msg.attach(mime_log)
    msg.attach(MIMEText(json_data["msg"], 'plain', 'utf-8'))
    from_user = monkey_error
    from_addr = json_data["from_addr"]
    to_addr = json_data["to_addr"]
    to_user = json_data["to_user"]
    msg['From'] = _format_addr(u'%s<%s>' % (from_user, from_addr))
    msg['To'] = _format_addr(u'%s<%s>' % (to_user, to_addr))
    msg['Subject'] = Header(u'来自%s的问候……' % from_user, 'utf-8').encode()
    _sendEmail(from_addr, json_data["password"], msg, json_data["smtp_server"], json_data["to_addr"])
else:
    print "no monkey error no need send email exit"    
