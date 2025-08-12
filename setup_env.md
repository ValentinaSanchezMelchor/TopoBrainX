# TopoBrainX — Environment Setup Guide

This guide explains how to set up the Python and Java environment for running the TopoBrainX project.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/ValentinaSanchezMelchor/TopoBrainX.git
cd TopoBrainX
```

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

