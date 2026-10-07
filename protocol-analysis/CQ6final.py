import subprocess

# Path to tshark on my computer
tshark = r"C:\Program Files\Wireshark\tshark.exe"



# This command:
# - reads the file B.pcapng
# - keeps only MQTT PUBLISH messages
# - keeps only messages with retain flag = 1
# - extracts stream number, message length, and topic length
cmd1 = [
    tshark, "-r", "B.pcapng",
    "-Y", "mqtt.msgtype==3 && mqtt.retain==1 && (ip.dst==35.158.34.213 || ip.dst==18.192.151.104 || ip.dst==35.158.43.69)",
    "-T", "fields",
    "-e", "tcp.stream",
    "-e", "mqtt.len",
    "-e", "mqtt.topic_len"
]

# Run the command and store output line by line
result1 = subprocess.check_output(cmd1).decode().splitlines()

# This set will store streams where retained messages are deleted
streams = set()

# Go through each packet
for line in result1:
    parts = line.split('\t')

    # Skip incomplete lines
    if len(parts) < 3:
        continue

    stream, msg_len, topic_len = parts

    # Convert values to integers
    try:
        msg_len = int(msg_len)
        topic_len = int(topic_len)
    except:
        continue

    # In MQTT, a retained message is deleted when payload is empty
    # This happens when total length = topic length + 2
    if msg_len == topic_len + 2:
        streams.add(stream)



# This command extracts:
# - stream number
# - client ID from CONNECT messages
cmd2 = [
    tshark, "-r", "B.pcapng",
    "-Y", "mqtt.msgtype==1",
    "-T", "fields",
    "-e", "tcp.stream",
    "-e", "mqtt.clientid"
]

# Run the command
result2 = subprocess.check_output(cmd2).decode().splitlines()

# Dictionary to match each stream to its client ID
stream_to_client = {}

# Fill the dictionary
for line in result2:
    parts = line.split('\t')

    if len(parts) < 2:
        continue

    stream, client = parts
    stream_to_client[stream] = client


# This set will store unique client IDs
clients = set()

# For each stream where a retained message was deleted
for s in streams:
    # Check if we know the client for that stream
    if s in stream_to_client:
        clients.add(stream_to_client[s])

# Print final results
print("CQ6a =", len(clients))
print("Clients:", clients)