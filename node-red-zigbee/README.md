# Node-RED, MQTT & ZigBee Network Analysis

## Overview

This project implements an IoT data-processing workflow using **Node-RED, MQTT, and ZigBee**. The workflow processes ZigBee network traffic, extracts selected attributes, reconstructs routing-cost information, and supports data visualization and cloud integration through ThingSpeak.

## Technologies

- Node-RED
- MQTT
- ZigBee / ZigBee Cluster Library (ZCL)
- JavaScript
- ThingSpeak
- CSV data processing

## Implementation

The Node-RED flow includes:

1. **MQTT communication:** Generates message identifiers and processes incoming MQTT messages.
2. **ZigBee packet filtering:** Selects relevant ZigBee traffic and ZCL attributes.
3. **Attribute processing:** Identifies Active Power, RMS Current, and RMS Voltage attributes.
4. **Routing analysis:** Processes ZigBee Link Status information to reconstruct source–destination routing costs.
5. **Visualization:** Uses Node-RED dashboard charts and prepares HTTP requests for ThingSpeak.

## Repository Structure

```text
node-red-zigbee/
├── README.md
├── flows-public.json
└── results/
    ├── id_log_sample.csv
    ├── filtered_elems_sample.csv
    └── outgoing_cost_sample.csv
```

## Sample Results

| File | Description |
|---|---|
| `id_log_sample.csv` | Generated message identifiers and timestamps |
| `filtered_elems_sample.csv` | Selected ZigBee attribute-processing outputs |
| `outgoing_cost_sample.csv` | Reconstructed ZigBee routing costs |

The attribute-processing outputs demonstrate the filtering workflow; their numerical values should not be interpreted as independently validated physical measurements.

## Running the Flow

1. Install Node-RED and the required MQTT and dashboard nodes.
2. Configure an MQTT broker compatible with the flow settings.
3. Import `flows-public.json` into Node-RED.
4. Provide the ZigBee traffic dataset and update the local CSV file paths for your environment.
5. Configure a valid ThingSpeak write API key privately if using cloud integration.

**Note:** The flow was developed in a course environment and may require configuration changes to run on another system. The original course-provided dataset is not redistributed.

## Academic Context

Developed as part of an Internet of Things coursework project at Politecnico di Milano.
