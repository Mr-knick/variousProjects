import tftpy

# Define the server address and the file to be downloaded
server = 'localhost'
filename = 'test.txt'
local_filename = 'C:\\Users\\brent\PycharmProjects\\simple\\downloaded_test.txt'

# Create a TFTP client
client = tftpy.TftpClient(server, 69)

# Download the file
client.download(filename, local_filename)
print(f"Downloaded {filename} to {local_filename}")