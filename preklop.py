import typer
import paramiko
import re
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

username = os.getenv('username')
password = os.getenv('password')
f = open("not_valid_addresses.txt", "a")
f2 = open("not_connected_mks.txt", "a")
f3 = open("successful_vlan_change.txt", "a")

def main(ip: str = "", vlan: str = ""):
    if check_ip(ip):
       preklop(ip,vlan,username,password)
    else:
       print(f"Not a valid IPv4 address: {ip} .")
       now = str(datetime.now())
       log = now + ' Not a valid IPv4 address: ' + ip
       f.write('\n')
       f.write(log)

def check_ip(ip):
    regex_pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(regex_pattern, ip):
       return True
    else:
       return False

def preklop(ip, vlan, username, password):
   ssh_client = paramiko.SSHClient()
   ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
      ssh_client.connect(hostname=ip, username=username, password=password, banner_timeout=60)
      commands = [
         f'/interface vlan set [find name="TV"] vlan-id={vlan}','/interface vlan set [find name="IPTV"] vlan-id={vlan}','quit'   
      ]
      for i in commands:
         output = ssh_client.exec_command(i)
      print(f"preklopena vlana {vlan} na ip {ip}")
      now = str(datetime.now())
      log = now + ' preklopena vlan ' + vlan + ' na ip ' + ip
      f3.write('\n')
      f3.write(log)
   except paramiko.SSHException as e:
      print(str(e))
      now = str(datetime.now())
      log = now + ' cant reach mk ' + ip + ' ' + str(e)
      f2.write('\n')
      f2.write(log)
   except paramiko.BadHostKeyException as e:
      print(str(e))
      now = str(datetime.now())
      log = now + ' cant reach mk ' + ip + ' ' + str(e)
      f2.write('\n')
      f2.write(log)
   except paramiko.BadAuthenticationType as e:
      print(str(e))
      now = str(datetime.now())
      log = now + ' bad credentials ' + ip + ' ' + str(e)
      f2.write('\n')
      f2.write(log)
   finally:
      ssh_client.close()

typer.run(main)
