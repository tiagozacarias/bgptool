#!/usr/bin/env python3
# Author: Tiago Eduardo Zacarias
# Date: 23-09-2023
# Tool objective: Switch Traffic to satelital links and main links.
# coding=UTF-8
# License: GPLv3

# IMPORTS
import sys
import time
import locale
import subprocess

# IP Peers COS-DIGITAL - CEMIG

peers_cemig_cos_digital = {

    "Baguari SE": ("192.168.2.16", "192.168.2.17", "DWDM"),
    "Barao de Cocais SE 3": ("192.168.2.18", "192.168.2.19", "MERIT"),
    "Barbacena SE 2": ("10.209.1.22", "10.209.1.117", "DWDM"),
    "Barreiro SE 1": ("10.209.1.49", "10.209.1.118", "MERIT"),
    "Bom Despacho SE 3": ("10.209.1.32", "10.209.1.59","DWDM"),
    "Braunas SE": ("10.209.1.163", "DWDM"),
    "Camargos UHE": ("10.209.1.112", "MERIT"),
    "Conselheiro Pena SE": ("10.209.1.12", "10.209.1.119", "DWDM"),
    "Emborcacao SE": ("10.209.1.28", "10.209.1.120","10.209.1.62", "10.209.1.157","DWDM"),
    # "Gafanhoto UHE": ("10.232.130.7", "MERIT"), #Sem Satelite
    "Guilman Amorim SE": ("10.209.1.106", "10.209.1.122", "DWDM"),
    # "Igarape UTE": ("10.209.1.38", "DWDM"),#Sem Satelite
    "Ipatinga SE 1": ("10.209.1.16", "10.209.1.123", "DWDM"),
    # "Irape SE": ("10.209.1.60", "DWDM"), #Sem Satelite
    "Irape UHE": ("10.209.1.37", "10.209.1.58", "MERIT"),
    "Itabira SE 2": ("10.209.1.17", "10.209.1.124", "DWDM"),
    "Itabira SE 4": ("10.209.1.101", "10.209.1.125", "DWDM"),
    "Itajuba SE 3": ("10.209.1.48", "10.209.1.127", "MERIT"),
    # "Itabira SE 5": ("10.209.1.162", "DWDM"), #Sem Satelite
    "Itabirito SE 2": ("10.209.1.102", "10.209.1.126", "DWDM"),
    "Itutinga SE 345KV": ("10.209.1.42", "10.209.1.128", "MERIT"),
    "Itutinga UHE": ("10.209.1.113", "MERIT"),
    "Jaguara SE 500KV": ("10.209.1.30", "10.209.1.130", "10.209.1.129", "DWDM"),
    "Jeceaba SE": ("10.209.1.25", "10.209.1.131", "DWDM"),
    "Joao Molevade SE 2": ("10.209.1.15", "10.209.1.132", "DWDM"),
    # "Joao Molevade SE 4": ("10.209.1.160", ""),#Sem Satelite
    "Juiz de Fora SE 1": ("10.209.1.23", "10.209.1.133", "DWDM"),
    "Lafaiete SE 1": ("10.209.1.24", "10.209.1.134", "DWDM"),
    "Mascarenhas SE": ("10.209.1.13", "10.209.1.135", "DWDM"),
    "Mesquita SE": ("10.209.1.18", "10.209.1.136", "DWDM"),
    "Montes Claros SE 2": ("10.209.1.39", "10.209.1.137", "MERIT"),
    "Nova Lima SE 6": ("10.209.1.103", "10.209.1.139", "DWDM"),
    "Nova Ponte SE": ("10.209.1.43", "10.209.1.140", "10.209.1.61", "10.209.1.158", "DWDM"),
    "Ouro Preto SE 2": ("10.209.1.26", "10.209.1.141", "DWDM"),
    "Pimenta SE": ("10.209.1.45", "10.209.1.142", "DWDM"),
    "Pirapora SE 2": ("10.209.1.21", "10.209.1.143", "MERIT"),
    "Porto Estrela SE": ("10.209.1.19", "10.209.1.144", "DWDM"),
    # "Queimado SE": ("10.217.252.25", ""),# Validar Route Reflector esta apontado para o Merit
    "Rosal UHE": ("10.232.129.2", "DWDM"),# Link Principal pelo Satelite
    "Sa Carvalho UHE": ("10.209.1.114", "DWDM"),
    "Sabara SE 3": ("10.209.1.34", "10.209.1.145", "DWDM"),
    "Salto Grande SE": ("10.209.1.159", "DWDM"),
    "Santos Dumont SE 2": ("10.209.1.105", "10.209.1.146", "DWDM"),
    "Sao Goncalo do Para SE": ("10.209.1.46", "10.209.1.147", "MERIT"),
    "Sao Gotardo SE 2": ("10.209.1.47", "10.209.1.148", "DWDM"),
    "Sao Simao SE": ("10.209.1.27", "10.209.1.149", "DWDM"),
    "Sete Lagoas SE 4": ("10.209.1.35", "10.209.1.150", "MERIT"),
    "Taquaril SE": ("10.209.1.50", "10.209.1.151", "DWDM"),
    "Timoteo SE 1": ("10.209.1.20", "10.209.1.152", "DWDM"),
    "Timoteo SE 2": ("10.209.1.165", "DWDM"),
    "Tres Marias SE": ("10.209.1.40", "10.209.1.153", "MERIT"),
    "Tres Marias UHE": ("10.232.130.3", "MERIT"),
    # "Uberaba 1 SE": ("10.209.1.52", "DWDM"),#Sem Satelite
    # "Uberlandia Radio SE": ("10.209.1.51", "DWDM"), #Sem Satelite
    # "Valadares SE 1": ("10.209.1.53", "DWDM"), #Sem Satelite
    "Valadares SE 2": ("10.209.1.11", "10.209.1.121", "DWDM"),
    "Valadares SE 6": ("10.209.1.55", "DWDM"),
    "Varzea da Palma 1 SE": ("10.209.1.41", "10.209.1.154", "MERIT"),
    "Varzea da Palma 4 SE": ("10.209.1.166", "10.209.1.167", "MERIT"),
    "Vespasiano SE 2": ("10.209.1.36", "10.209.1.155", "MERIT"),
    "Volta Grande SE": ("10.209.1.44", "10.209.1.156", "DWDM")}
