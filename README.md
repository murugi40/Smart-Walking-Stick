# Smart Walking Stick for the Visually Impaired

An assistive technology project that integrates multiple sensors and communication modules to aid visually impaired individuals in navigating their environment more safely and independently. The project combines real-time sensing, vibration feedback, and GSM-based emergency communication.

## 💡 Overview

This smart walking stick offers a robust enhancement to traditional mobility aids for the visually impaired. It uses ultrasonic distance measurement, ambient light sensing, and a GSM module for emergency alerts. The system is controlled by a Raspberry Pi Pico and programmed in MicroPython.

## 🔧 Hardware Components

| Component          | Description                                |
| ------------------ | ------------------------------------------ |
| Microcontroller    | Raspberry Pi Pico (RP2040)                 |
| Ultrasonic Sensors | HC-SR04 (x3 for multi-directional sensing) |
| Light Sensor       | LDR (Light Dependent Resistor)             |
| Vibration Motor    | Coin-type motor for tactile alerts         |
| GSM Module         | SIM800L for SMS communication              |
| Help Button        | Push button connected via GPIO             |
| Power Supply       | 9V battery with charging circuit           |

## ✨ Features

* **Obstacle Detection**: Front, left, and right obstacle sensing with distance-based feedback.
* **Tactile Feedback**: Vibration motor alerts the user with unique patterns based on sensor input.
* **Ambient Light Detection**: Differentiates between day/night or dark/light environments.
* **Emergency SOS Function**: Sends SMS with GPS location when help button is pressed.

## ⚙️ System Operation

1. Ultrasonic sensors continuously measure distances.
2. LDR measures ambient light to trigger vibration in low/high light conditions.
3. If obstacles are detected within preset safe distances, vibration alerts are triggered.
4. Pressing the help button sends an SMS with predefined location data via the GSM module.

## 🖼️ System Logic (Block Diagram)

```
[Ultrasonic Sensors]   
      │
[LDR Sensor]           → [Raspberry Pi Pico] → [Vibration Motor / GSM Module]
      │
[Help Button]         
```

## 🧪 How to Run the System

1. Wire all sensors and modules to the Raspberry Pi Pico as per the system design.
2. Flash the `main.py` firmware using Thonny or another MicroPython-compatible IDE.
3. Ensure the GSM module is powered and a SIM card with airtime is inserted.
4. Power the system using a 9V battery.
5. Verify system output via vibration or serial monitor.

## 📁 Repository Structure

```
Smart-Walking-Stick/
🔹 main.py                  # Core MicroPython code
🔹 README.md                # Project overview and instructions
🔹 hardware_schematics/     # Block diagrams, pinouts, CAD images, IDE output screenshots
```

## 📊 4.1. Collective Data Shown in the IDE Software

The system provides real-time data feedback during testing through the IDE (e.g., Thonny), reflecting sensor readings, light levels, and trigger status for emergency calls. These stages are documented using screenshots:

* `IDE Collective data 1.png` – Initial environment scan, no obstacle detected
* `IDE Collective data 2.png` – Obstacle detected by right sensor
* `IDE Collective data 3.png` – Multiple sensors triggered and light detected
* `IDE Collective data 4.png` – All sensors detect obstacles; alert active

These images are available in the `hardware_schematics/` folder for visual reference of testing outcomes.

### Theory Behind IDE Output Interpretation

The safe values are set before obtaining values from the IDE — in this case:

* **Ultrasonic sensors**: 50 cm safe distance on the right and left, 120 cm for height.
* **Light detection**: A threshold of 10,162. Any value below this is considered *darkness*, while above it indicates *presence of light*.

**Case 1**: All sensors detect objects out of the safe range → No action triggered. Light reading is below the threshold → Darkness indicated.

**Case 2**: Right-side sensor (Sensor 3) detects an object within range → Vibration motor activates → Obstacle detected on the right.

**Case 3**: More than one sensor detects objects within safe range, and light value exceeds threshold → System reports *obstacle(s)* and *light present*.

**Case 4**: All ultrasonic sensors detect objects within the safe range → System indicates obstacles in all directions with appropriate vibration response.

**Case 5**: Help button is pressed → The interface confirms button press and SMS message sent (if network is available).

## 📄 Notes

* Designed for urban and indoor environments.
* System reacts to light and obstacles to provide real-time navigation support.
* The SMS feature currently includes a hardcoded Google Maps link; future updates may include GPS modules for dynamic location data.

---

> *“Technology should empower, not exclude. This project demonstrates how simple hardware and code can transform lives.”*
