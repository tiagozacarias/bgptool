#!/usr/bin/env python3
# Author: Tiago Eduardo Zacarias
# Date: 02-05-2025
# Tool objective: Switch Traffic to satelital links and main links.
# coding=UTF-8
# License: GPLv3

# IMPORTS
import sys
import time
import locale
import subprocess

# IP Peers

peers = {

    "SITE A": ("192.168.2.16", "192.168.2.17", "REGION_A"),
    "SITE B": ("192.168.2.18", "192.168.2.19", "REGION_A"),
    "SITE C": ("192.168.2.20", "192.168.2.21", "REGION_B"),
    "SITE D": ("192.168.2.22", "192.168.2.23", "REGION_A"),
    "SITE E ": ("192.168.2.24", "192.168.2.25","REGION_B"),
    )}
