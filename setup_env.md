# TopoBrainX — Environment Setup Guide

This guide explains how to run the TopoBrainX project.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/ValentinaSanchezMelchor/TopoBrainX.git
cd TopoBrainX
```
## Docker: 

1. install Docker
2. run
```bash
docker compose up --build
```
 on the terminal

## Step 2: Create a Virtual Environment
python3.11 -m venv .venv
source .venv/bin/activate  # For Mac/Linux
.venv\Scripts\activate # For Windows

## Step 3: Install Python Dependencies
pip install -r requirements.txt

## Step 4: Download and Place JIDT
Download the JIDT .jar file from the official GitHub page:
👉 https://github.com/jlizier/jidt/releases

Then place the .jar file here:
```bash
dependencies/info_theory/jidt_interface/infodynamics.jar
```

