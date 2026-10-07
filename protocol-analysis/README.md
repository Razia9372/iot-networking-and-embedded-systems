# IoT Protocol Traffic Analysis

This project analyzes IoT communication traffic using **Python, Wireshark/TShark, CoAP, and MQTT**.

The objective is to programmatically extract protocol information from packet captures and investigate request-response behavior, MQTT subscriptions, retained messages, Last Will messages, wildcard matching, and topic hierarchy.

## Tools and Technologies

- Python
- Wireshark / TShark
- CoAP
- MQTT
- Packet Capture Analysis
- Matplotlib

## CoAP Request-Response Analysis

`coap_request_response_analysis.py`

Extracts CoAP traffic using TShark and analyzes Confirmable POST and PUT requests.

The script:

- extracts CoAP message type, code, Message ID, and URI path,
- matches requests and responses using the CoAP Message ID (MID),
- identifies unsuccessful operations,
- groups results by resource and request method.

This demonstrates programmatic analysis of CoAP request-response behavior from captured network traffic.

## MQTT Wildcard and Last Will Analysis

`mqtt_wildcard_last_will_analysis.py`

Analyzes MQTT client sessions, wildcard subscriptions, and Last Will messages.

The script:

- associates TCP streams with MQTT client IDs,
- extracts Last Will topics and messages from CONNECT packets,
- identifies wildcard subscriptions,
- implements matching for `+` and `#`,
- determines which subscribers match published Last Will topics.

## MQTT Retained Message Analysis

`mqtt_retained_message_analysis.py`

Analyzes retained MQTT PUBLISH messages and identifies clients that remove retained values by publishing an empty payload with the retain flag enabled.

TCP streams are correlated with MQTT client IDs to identify the corresponding clients.

## MQTT Subscription Wildcard Analysis

`mqtt_subscription_wildcard_analysis.py`

Examines MQTT SUBSCRIBE packets and identifies subscriptions containing multiple wildcard operators.

Both MQTT wildcard types are considered:

- `+` — single-level wildcard
- `#` — multi-level wildcard

## MQTT Topic Hierarchy Analysis

`mqtt_topic_depth_analysis.py`

Analyzes the hierarchical structure of MQTT topics used in PUBLISH messages.

For each capture, the script:

1. extracts MQTT PUBLISH topics using TShark,
2. calculates the number of topic levels,
3. computes the distribution of topic depths,
4. compares traffic from different captures,
5. generates a histogram using Matplotlib.

## Running the Analysis

The scripts require:

- Python 3
- Wireshark/TShark
- Matplotlib (for topic-depth visualization)
- the corresponding packet-capture datasets

The packet captures used for the original analysis are **not distributed in this repository**.

The scripts currently assume a standard Windows Wireshark installation:

```python
tshark = r"C:\Program Files\Wireshark\tshark.exe"
```

This path can be modified according to the local TShark installation.

## Academic Context

This work was developed as part of an Internet of Things course and focuses on practical analysis of application-layer IoT protocols and captured network traffic.
