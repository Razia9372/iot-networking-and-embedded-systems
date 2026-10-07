import subprocess
import matplotlib.pyplot as plt

# Path to tshark on my computer.
# Python will use tshark to read the pcap files and extract MQTT information.
tshark = r"C:\Program Files\Wireshark\tshark.exe"

# This function analyzes one capture file at a time.
# Its goal is to count how many MQTT publish messages have:
# 1 layer, 2 layers, 3 layers, and so on.
def analyze(file_name):

    # This tshark command does the following:
    # - opens the selected pcap file
    # - forces port 1883 to be interpreted as MQTT
    # - keeps only MQTT PUBLISH packets going to the broker
    # - extracts only the topic field from those packets
    cmd = [
        tshark,
        "-r", file_name,                         # read the capture file
        "-d", "tcp.port==1883,mqtt",             # decode port 1883 as MQTT
        "-Y", "mqtt.msgtype==3 && tcp.dstport==1883",  # keep only PUBLISH messages sent to the broker
        "-T", "fields",                          # print only the selected fields
        "-e", "mqtt.topic"                       # extract the MQTT topic
    ]

    # Run the tshark command.
    # The result is converted into text and split line by line.
    # Each line contains one MQTT topic.
    topics = subprocess.check_output(cmd).decode(errors="ignore").splitlines()

    # Dictionary to count how many messages belong to each topic depth.
    # Example:
    # if a topic has 3 layers, then layers_count[3] is increased by 1.
    layers_count = {}

    # This variable stores the total number of valid publish messages found.
    total = 0

    # Check each topic extracted from the capture
    for topic in topics:
        topic = topic.strip()

        # Ignore empty lines, if any appear in the output
        if topic == "":
            continue

        # The number of layers in a topic is equal to:
        # number of "/" characters + 1
        # Example:
        # home/kitchen/temp -> 2 slashes -> 3 layers
        layers = topic.count("/") + 1

        # If this layer value has not appeared before, start from 0
        if layers not in layers_count:
            layers_count[layers] = 0

        # Increase the number of messages for this layer value
        layers_count[layers] += 1

        # Increase the total number of valid publish messages
        total += 1

    # Return:
    # - the dictionary with layer distribution
    # - the total number of publish messages
    return layers_count, total


# Analyze file A.pcapng
# layers_A stores the distribution of topic depths
# total_A stores the total number of publish messages in A
layers_A, total_A = analyze("A.pcapng")

# Analyze file B.pcapng
# layers_B stores the distribution of topic depths
# total_B stores the total number of publish messages in B
layers_B, total_B = analyze("B.pcapng")

# These are the values requested in CQ8a and CQ8b:
# total number of publish messages considered in each capture
print("CQ8a =", total_A)
print("CQ8b =", total_B)


# Prepare the data for plotting


# We need all possible layer values that appear in either file.
# For example, if A has layers {1,2,3} and B has {2,3,4},
# then all_layers becomes [1,2,3,4]
all_layers = sorted(set(layers_A) | set(layers_B))

# For each layer value, get the number of messages in A.
# If that layer does not appear in A, use 0.
values_A = [layers_A.get(x, 0) for x in all_layers]

# Do the same for file B.
values_B = [layers_B.get(x, 0) for x in all_layers]

# Create x-axis positions for the bars
x = list(range(len(all_layers)))

# Width of each bar
# A smaller width allows the bars of A and B to appear side by side
width = 0.35


# Create the histogram


# Set the figure size to make the plot readable in the report
plt.figure(figsize=(7, 4.5))

# Plot bars for A slightly to the left of each x position
plt.bar([i - width/2 for i in x], values_A, width=width, label="A.pcapng")

# Plot bars for B slightly to the right of each x position
# This way the two captures can be compared directly
plt.bar([i + width/2 for i in x], values_B, width=width, label="B.pcapng")

# Label for x-axis: number of layers in the topic
plt.xlabel("Number of topic layers")

# Label for y-axis: number of publish messages
plt.ylabel("Number of messages")

# Title of the figure
plt.title("MQTT Publish Messages to Local Broker")

# Show the actual layer values on the x-axis
plt.xticks(x, all_layers)

# No grid is used here to keep the figure cleaner for the report

# Show legend to distinguish the two files
plt.legend()

# Adjust spacing so labels and title fit well
plt.tight_layout()

# Save the figure as an image file for the report
plt.savefig("CQ8_histogram.png", dpi=300)

# Display the plot on screen
plt.show()