import asyncio
import asyncssh


async def generate_ssh_key_pair():
    key = asyncssh.generate_private_key('ssh-rsa')
    private_key = key.export_private_key('openssh')
    public_key = key.export_public_key('openssh')

    return private_key, public_key


async def main():
    private_key, public_key = await generate_ssh_key_pair()

    # Write private key to file
    with open('id_rsa', 'w') as private_file:
        private_file.write(private_key.decode())

    # Write public key to file
    with open('id_rsa.pub', 'w') as public_file:
        public_file.write(public_key.decode())

    print("Private Key has been saved to id_rsa")
    print("Public Key has been saved to id_rsa.pub")


if __name__ == "__main__":
    asyncio.run(main())
