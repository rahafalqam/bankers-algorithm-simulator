# Banker's Algorithm Simulator

## Overview

This project was developed as part of the **Operating Systems (ENCS3390)** course.

It implements the **Banker's Algorithm** for deadlock avoidance using Python. The program manages resource allocation, verifies safe system states, processes resource requests and releases, and simulates process execution while preventing unsafe allocations. :contentReference[oaicite:2]{index=2}

---

## Features

- Banker's Algorithm implementation
- Deadlock avoidance
- Safe state verification
- Resource request handling (RQ)
- Resource release handling (RL)
- Safe sequence generation
- Process execution simulation
- System state visualization
- Input file support

---

## Supported Commands

| Command | Description |
|---------|-------------|
| `RQ` | Request resources |
| `RL` | Release resources |
| `*` | Display the current system state |
| `RUN` | Execute processes using a safe sequence |
| `EXIT` | Exit the program |

The application loads the initial system configuration from an input file and supports interactive resource management through these commands. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

---

## Repository Structure

```
.
├── bankers.py
├── input.txt
├── OSProjectTwoReport.pdf
└── README.md
```

---

## Running the Program

```bash
python bankers.py
```

or

```bash
python bankers.py input.txt
```

The program can run using the default input file or a custom input file supplied as a command-line argument. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

---

## Technologies

- Python 3
- Operating Systems
- Banker's Algorithm
- Deadlock Avoidance

---

## Course

**ENCS3390 – Operating Systems**

Faculty of Engineering & Technology  
Birzeit University

---

## Authors

- Rahaf Mahmoud
- Abdalrahman Abdullah
