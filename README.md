# IoT Networking & Embedded Systems

A collection of academic projects exploring **Internet of Things (IoT), embedded systems, low-power wireless communication, and network protocol analysis**.

Developed during my M.Sc. studies in Telecommunication Engineering at Politecnico di Milano.

## Research & Technical Focus

- Wireless and IoT communication protocols
- Energy-efficient embedded systems
- MQTT, CoAP, and ZigBee networking
- ESP32-based sensing and ESP-NOW communication
- IoT data processing and network analysis

## Projects

### 1. ESP32 Low-Power Wireless Sensing Node

**Directory:** [`esp32-low-power-node/`](esp32-low-power-node/)

Developed and simulated an ESP32-based sensing application integrating PIR motion detection, light sensing, ESP-NOW communication, and deep-sleep functionality.

The project includes baseline and optimized implementations for exploring low-power operation.

**Technologies:** ESP32, Arduino/C++, ESP-NOW, Wokwi

### 2. MQTT & CoAP Protocol Analysis

**Directory:** [`protocol-analysis/`](protocol-analysis/)

Developed Python-based traffic analysis scripts using TShark to investigate MQTT messaging behavior, including topic hierarchies, wildcard subscriptions, retained messages, and Last Will functionality, alongside CoAP request-response exchanges.

**Technologies:** Python, Wireshark/TShark, MQTT, CoAP

### 3. IoT Energy Consumption Analysis

**Directory:** [`energy-analysis/`](energy-analysis/)

Compared the modeled communication energy consumption of MQTT and CoAP using coursework assumptions and analytical calculations.

The analysis examines how protocol behavior and message transmission influence estimated energy requirements.

**Technologies:** MQTT, CoAP, analytical energy modeling

### 4. Node-RED, MQTT & ZigBee Network Analysis

**Directory:** [`node-red-zigbee/`](node-red-zigbee/)

Implemented a Node-RED workflow for MQTT-based processing of ZigBee network traffic, attribute filtering, routing-cost reconstruction, dashboard visualization, and ThingSpeak integration.

Includes an exported Node-RED flow and cleaned CSV sample outputs.

**Technologies:** Node-RED, MQTT, ZigBee, JavaScript, ThingSpeak

## Repository Structure

```text
iot-networking-and-embedded-systems/
├── README.md
├── esp32-low-power-node/
│   ├── README.md
│   ├── sketch.ino
│   ├── diagram.json
│   ├── wokwi-project.txt
│   └── optimized/
├── protocol-analysis/
│   ├── README.md
│   └── *.py
├── energy-analysis/
│   └── README.md
└── node-red-zigbee/
    ├── README.md
    ├── flows-public.json
    └── results/
```

## Tools & Technologies

| Category | Technologies |
|---|---|
| Embedded systems | ESP32, Arduino/C++, Wokwi |
| Wireless communication | ESP-NOW, ZigBee |
| Network protocols | MQTT, CoAP |
| Programming | Python, JavaScript, C++ |
| Network analysis | Wireshark, TShark |
| IoT integration | Node-RED, ThingSpeak |

## Academic Context

These projects were completed as part of Internet of Things coursework at **Politecnico di Milano**.

They reflect my interest in combining wireless networking, embedded computing, and energy-efficient system design.

## Author

**Razia Jafari**

M.Sc. Telecommunication Engineering — Politecnico di Milano

**Research interests:** Wireless Networks · Edge/IoT Systems · Networked Embedded Systems · Distributed Computing
