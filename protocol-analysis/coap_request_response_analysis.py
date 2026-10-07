import subprocess  # lets us run tshark from inside Python

tshark = r"C:\Program Files\Wireshark\tshark.exe"  # full path to the tshark executable on Windows

# Build the tshark command that will read the capture file and extract only CoAP packets
cmd = [
    tshark,                         # the program to run
    "-r", "A.pcapng",               # read packets from the file A.pcapng
    "-Y", "coap",                   # display filter: keep only CoAP packets
    "-T", "fields",                 # print selected fields instead of full packet details
    "-e", "coap.type",              # extract the CoAP message type (CON, ACK, etc.)
    "-e", "coap.code",              # extract the CoAP code (request method or response code)
    "-e", "coap.mid",               # extract the CoAP message ID
    "-e", "coap.opt.uri_path"       # extract the URI path (resource name)
]

# Run tshark, decode the output as text, and split it into lines (one line per packet)
output = subprocess.check_output(cmd).decode(errors="ignore").splitlines()

# Dictionary to store request packets, using MID as the key
# Example: requests[mid] = ("POST", "sensor/temp")
requests = {}

# Dictionary to store response packets, again using MID as the key
# Example: responses[mid] = 132
responses = {}

# Go through each line produced by tshark
for line in output:
    parts = line.split("\t")  # tshark separates extracted fields with tabs

    # Skip lines that do not contain all four expected fields
    if len(parts) < 4:
        continue

    # Assign each extracted field to a variable for easier reading
    type_ = parts[0]          # CoAP message type
    code = parts[1]           # request method code or response code
    mid = parts[2]            # message ID
    resource = parts[3]       # URI path / resource name

    # Check if this packet is a request
    if type_ == "0":  # type 0 means CON (Confirmable message)
        if code == "2":  # code 2 means POST request
            requests[mid] = ("POST", resource)  # save method and resource under this MID
        elif code == "3":  # code 3 means PUT request
            requests[mid] = ("PUT", resource)   # save method and resource under this MID

    # Check if this packet is a response
    elif type_ == "2":  # type 2 means ACK (Acknowledgement)
        try:
            responses[mid] = int(code)  # save numeric response code for this MID
        except:
            pass  # ignore cases where the code cannot be converted to an integer

# Dictionary to group unsuccessful POST and PUT requests by resource
# Example:
# resources["sensor/temp"] = {"POST": {12, 15}, "PUT": {20}}
resources = {}

# Loop over all saved requests
for mid in requests:
    # Only continue if we also found a matching response with the same MID
    if mid in responses:
        # In CoAP, response codes >= 128 are response messages (often errors here, based on exercise logic)
        if responses[mid] >= 128:
            method, resource = requests[mid]  # get the request method and resource name

            # If this resource is not yet in the dictionary, create an entry for it
            if resource not in resources:
                resources[resource] = {"POST": set(), "PUT": set()}

            # Add this MID to the correct method set for that resource
            # A set is used to avoid counting the same MID more than once
            resources[resource][method].add(mid)

# This variable will count how many resources have the same number of unsuccessful POST and PUT requests
count = 0

# Go through each resource and compute the number of unsuccessful POSTs and PUTs
for r in resources:
    x = len(resources[r]["POST"])  # number of unique unsuccessful POST requests
    y = len(resources[r]["PUT"])   # number of unique unsuccessful PUT requests

    # Print the result for this resource
    print(r, "POST =", x, "PUT =", y)

    # If the two counts are equal and greater than zero, this resource satisfies CQ2
    if x == y and x > 0:
        count += 1

# Print the final CQ2 answer
print("\nCQ2 Answer =", count)
