# CoAP vs MQTT Communication Energy Analysis

This analysis compares the communication energy consumption of **CoAP** and **MQTT** in a battery-powered IoT scenario.

The system consists of:

- a temperature sensor transmitting one measurement every 2 minutes,
- a battery-powered actuator receiving the measurements,
- direct device-to-device communication using CoAP,
- gateway-based communication using MQTT.

## Energy Model

Communication energy is calculated from the number of transmitted and received bits:

```text
E_TX = N_bits × E_TX,bit
E_RX = N_bits × E_RX,bit
```

with:

```text
E_TX,bit = 50 nJ/bit
E_RX,bit = 58 nJ/bit
```

The sensor generates:

```text
30 communication cycles/hour
```

## CoAP

The CoAP implementation uses Confirmable messages.

Each communication cycle consists of:

```text
Sensor ── PUT ──> Actuator
Sensor <── ACK ── Actuator
```

The resulting communication energy is:

```text
Energy per cycle = 73.44 µJ
Energy per hour  = 2203.2 µJ
```

## MQTT

The MQTT scenario uses **QoS 1** and assumes that devices reconnect during each communication cycle.

Communication includes operations such as:

```text
CONNECT
CONNACK
PUBLISH
PUBACK
SUBSCRIBE
SUBACK
DISCONNECT
```

The resulting communication energy is:

```text
Energy per cycle = 301.92 µJ
Energy per hour  = 9057.6 µJ
```

## Comparison

| Protocol | Energy per Hour |
|---|---:|
| CoAP | 2203.2 µJ |
| MQTT | 9057.6 µJ |

Under these assumptions:

```text
MQTT energy / CoAP energy ≈ 4.1
```

Therefore, MQTT requires approximately **4.1× more communication energy** than CoAP in this particular scenario.

The difference mainly results from the additional connection, subscription, acknowledgment, and control-message overhead introduced by MQTT.

## Duty-Cycled Devices

Energy consumption alone does not determine the most appropriate protocol.

If the actuator remains asleep for long periods, direct CoAP communication requires the sensor and actuator to be active at compatible times.

MQTT introduces a broker between the devices:

```text
Sensor → MQTT Broker → Actuator
```

This decouples the sender and receiver in time. The sensor can communicate with the broker while the actuator is asleep, and the actuator can retrieve relevant information after waking.

This illustrates an important IoT design trade-off:

> The protocol with the lowest communication overhead is not necessarily the best choice when device duty cycles and asynchronous communication are considered.

## Key Concepts

**CoAP · MQTT · QoS · Low-Power IoT · Communication Energy · Duty Cycling · Asynchronous Communication · Protocol Overhead**
