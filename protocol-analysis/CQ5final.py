import subprocess

# This is the path of tshark on my computer.
# Python will use it to read the packets inside the pcap file.
tshark = r"C:\Program Files\Wireshark\tshark.exe"

# This command tells tshark what to read and what information to extract.
# - It opens B.pcapng
# - It keeps only MQTT packets
# - It prints only the fields that are useful for CQ5
cmd = [
    tshark,
    "-r", "B.pcapng",          # read the capture file B.pcapng
    "-Y", "mqtt",              # keep only MQTT packets
    "-T", "fields",            # print only selected fields, not the full packet details
    "-e", "tcp.stream",        # TCP stream number, used to connect packets of the same session
    "-e", "mqtt.msgtype",      # MQTT message type, for example CONNECT or SUBSCRIBE
    "-e", "mqtt.clientid",     # client ID, usually present in CONNECT packets
    "-e", "mqtt.topic",        # topic, useful for SUBSCRIBE packets
    "-e", "mqtt.willtopic",    # Will Topic, present in CONNECT if a Last Will is set
    "-e", "mqtt.willmsg_text"  # text content of the Will Message
]

# This line runs the tshark command.
# The output is decoded into text and split into separate lines,
# so each line represents one packet with the extracted fields.
lines = subprocess.check_output(cmd).decode(errors="ignore").splitlines()

# These dictionaries are used to organize the data in a simple way.

# stream_client links each TCP stream to the correct client ID.
# This is useful because SUBSCRIBE packets often do not show the client ID directly.
stream_client = {}

# will_info stores, for each client, its Will Topic and Will Message.
# The format is:
# client ID -> (will topic, will message)
will_info = {}

# subscriptions stores the wildcard subscriptions of each client.
# The format is:
# client ID -> list of subscription topics
subscriptions = {}


# First pass: read CONNECT packets

# In this loop, we look for MQTT CONNECT packets.
# CONNECT packets are important because they contain:
# - the client ID
# - the Will Topic
# - the Will Message
for line in lines:
    # Each line is split by tabs because tshark prints fields separated by tabs
    p = line.split("\t")

    # If a line does not contain all expected fields, we skip it
    if len(p) < 6:
        continue

    # Assign each extracted field to a variable for easier reading
    stream, msgtype, client, topic, willtopic, willmsg = p

    # MQTT message type 1 means CONNECT
    if msgtype == "1":
        # If the client ID exists, save the relation between stream and client
        if client:
            stream_client[stream] = client

        # If the client has a Will Topic, save both topic and message
        if client and willtopic:
            will_info[client] = (willtopic, willmsg)


# Second pass: read SUBSCRIBE packets

# In this loop, we look for MQTT SUBSCRIBE packets.
# The goal is to save only the subscriptions that contain at least one wildcard.
for line in lines:
    # Again, split the line into fields
    p = line.split("\t")

    # Skip incomplete lines
    if len(p) < 6:
        continue

    # Assign the fields to variables
    stream, msgtype, client, topic, willtopic, willmsg = p

    # MQTT message type 8 means SUBSCRIBE
    # We also check that the stream is known, so we can link the subscription to a client
    if msgtype == "8" and stream in stream_client:
        # Get the correct client ID from the stream number
        client = stream_client[stream]

        # Keep only subscriptions that use at least one wildcard:
        # '+' for one topic level
        # '#' for multiple topic levels
        if topic and ("+" in topic or "#" in topic):
            # If this is the first subscription of this client, create an empty list
            if client not in subscriptions:
                subscriptions[client] = []

            # Add the wildcard subscription topic to that client
            subscriptions[client].append(topic)


# Function to compare subscription and topic

# This function checks whether a subscription topic matches a normal topic.
# It supports the MQTT wildcards:
# '+' = matches one level
# '#' = matches all remaining levels
def match(sub, topic):
    # Split the subscription and the topic into parts using "/"
    sub = sub.split("/")
    topic = topic.split("/")

    # Compare them level by level
    for i in range(len(sub)):
        # If we find '#', the subscription matches everything from this point
        if sub[i] == "#":
            return True

        # If the topic is shorter than the subscription, it cannot match
        if i >= len(topic):
            return False

        # If the subscription part is neither '+' nor equal to the topic part,
        # then the two topics do not match
        if sub[i] != "+" and sub[i] != topic[i]:
            return False

    # At the end, the match is valid only if both have the same number of levels
    return len(sub) == len(topic)


# Final step: find the receivers

# This set will store the clients that receive at least one Last Will message.
# A set is used to avoid counting the same client more than once.
receivers = set()

print("Matching subscribers:\n")

# Go through each subscriber
for client in subscriptions:
    # Check all wildcard subscriptions of that client
    for sub in subscriptions[client]:
        # Compare this subscription with every available Will Topic
        for sender in will_info:
            willtopic, willmsg = will_info[sender]

            # If the subscription matches the Will Topic,
            # then this client would receive that Last Will message
            if match(sub, willtopic):
                receivers.add(client)

                # Print the match so it can be checked manually
                print("Client:", client)
                print("Sub:", sub)
                print("Will Topic:", willtopic)
                print("Will Message:", willmsg if willmsg else "(empty)")
                print()

# Print the final answer:
# the number of unique subscribers that receive at least one Last Will message
print("CQ5 Answer =", len(receivers))