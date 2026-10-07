import subprocess

# Path of tshark on the computer
tshark = r"C:\Program Files\Wireshark\tshark.exe"

# CQ7 is on file B.pcapng.
# We want to find MQTT SUBSCRIBE requests whose topic has
# at least two wildcards, and we also want to print those requests.

# This command:
# 1. opens B.pcapng
# 2. keeps only MQTT SUBSCRIBE packets
# 3. extracts the frame number and the topic
cmd = [
    tshark,
    "-r", "B.pcapng",             # read the capture file
    "-Y", "mqtt.msgtype == 8",    # keep only SUBSCRIBE messages
    "-T", "fields",               # print only selected fields
    "-e", "frame.number",         # packet number in Wireshark
    "-e", "mqtt.topic"            # subscribed topic
]

# Run the command and store the output line by line
output = subprocess.check_output(cmd).decode(errors="ignore").splitlines()

# This variable stores the final answer
count = 0

print("Requests with at least two wildcards:\n")

# Check each subscribe request
for line in output:
    parts = line.split("\t")

    # Make sure both frame number and topic exist
    if len(parts) < 2:
        continue

    frame_number = parts[0]
    topic = parts[1]

    # Count wildcards in the topic
    plus_count = topic.count("+")
    hash_count = topic.count("#")
    wildcards = plus_count + hash_count

    # If the topic has at least two wildcards,
    # print the request and count it
    if wildcards >= 2:
        count += 1
        print("Frame", frame_number, "->", topic)

# Print the final result
print("\nCQ7 Answer =", count)
