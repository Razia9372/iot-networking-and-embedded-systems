# Low-Power ESP32 Wireless Sensor Node

This project implements a low-power IoT sensor node based on the **ESP32**, combining motion detection, ambient-light sensing, wireless communication, and energy-aware operation.

The node uses:

- **PIR sensor** for motion detection
- **LDR/photoresistor** for ambient-light sensing
- **ESP-NOW** for wireless data transmission
- **Deep sleep** for reducing energy consumption
- **LED** for local status indication

## System Operation

The baseline implementation follows a repeated operating cycle:

```text
Sensor Reading → Message Creation → ESP-NOW Transmission → Idle → Deep Sleep
```

The ESP32 remains active only during sensing, communication, and local processing before entering deep sleep.

## Energy Analysis

Energy consumption was evaluated for the main operating states:

- Sensor reading
- Wireless transmission
- Idle operation
- Deep sleep

The energy of each state was estimated using:

```text
E = P × t
```

where the measured average power is combined with the duration of each operating state.

The analysis was used to identify opportunities for reducing unnecessary active time and wireless-radio usage.

## Optimized Implementation

An additional implementation is available in:

```text
optimized/
```

The optimized design moves toward **event-driven operation**.

Instead of periodically waking regardless of environmental conditions, the ESP32 can use the PIR motion sensor as a wake-up source and return to deep sleep after processing the event.

The optimization focuses on:

- reducing active time,
- avoiding unnecessary transmissions,
- activating wireless communication only when required,
- maximizing time spent in deep sleep,
- using motion-triggered wake-up.

## Hardware

The simulated system contains:

```text
ESP32 DevKit
├── PIR motion sensor
├── LDR / photoresistor
├── Status LED
└── ESP-NOW wireless interface
```

The hardware configuration and wiring are defined in `diagram.json`.

## Wokwi Simulation

Both implementations can be reproduced using the included Wokwi project files.

### Baseline

The baseline implementation is located in the root of this directory:

```text
sketch.ino
diagram.json
wokwi-project.txt
```

### Optimized

The event-driven implementation is located in:

```text
optimized/
```

and contains its own source code and Wokwi hardware configuration.

## Technologies

**ESP32 · C/C++ · ESP-NOW · Deep Sleep · PIR · LDR · Low-Power IoT · Embedded Systems · Wokwi**
