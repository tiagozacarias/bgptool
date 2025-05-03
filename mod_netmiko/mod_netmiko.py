#!/usr/bin/env python3
# coding=UTF-8
# Author: Tiago Eduardo Zacarias
# Version: 1.4.0
# Date: 02-05-2025
# License: GPLv3

# EXTERNAL LIBS
import threading
from netmiko import ConnectHandler
import socket
import os
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException

# Vars
# Get Login
username = os.environ["USERNAME_NETMIKO"]
password = os.environ["PASSWORD_NETMIKO"]
enable_password = os.environ["PASSWORD_ENABLE_NETMIKO"]

# Devices
device_list_region_a = []
device_list_region_b = []

# Multithreads
threads = []


class ProcessConnectionDwdm:

    def __init__(self) -> None:
        pass

    def test_connection(ip, device_telnet, device_ssh):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout Socket
        s.settimeout(6)

        # Result Telnet
        result_telnet = s.connect_ex((ip, 23))
        s.close()

        if result_telnet == 0:

            device_list_region_a.append({"device_type": device_telnet, "ip": ip,
                                     "username": username, "password": password,
                                     "timeout": 50, "fast_cli": False, "global_delay_factor": 2,
                                     "session_log": "log.txt", "session_log_file_mode": "append"})
        else:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Timeout Socket
            s.settimeout(6)

            # Result SSH
            result_ssh = s.connect_ex((ip, 22))
            s.close()

            if result_ssh == 0:

                device_list_region_a.append({"device_type": device_ssh, "ip": ip,
                                         "username": username, "password": password,
                                         "timeout": 50, "fast_cli": False, "global_delay_factor": 2,
                                         "session_log": "log.txt", "session_log_file_mode": "append"})

            else:

                with open(f"tmp/{ip}.error", "w") as f:

                    print(
                        f"Unable to establish SSH or Telnet connection on: {ip}", file=f)
                    f.close()


class ProcessConnectionMerit:

    def __init__(self) -> None:
        pass

    def test_connection(ip, device_telnet, device_ssh):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout Socket
        s.settimeout(6)

        # Result Telnet
        result_telnet = s.connect_ex((ip, 23))
        s.close()

        if result_telnet == 0:

            device_list_region_b.append({"device_type": device_telnet, "ip": ip,
                                      "username": username, "password": password,
                                      "timeout": 50, "fast_cli": False, "global_delay_factor": 2,
                                      "session_log": "log.txt", "session_log_file_mode": "append"})
        else:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Timeout Socket
            s.settimeout(6)

            # Result SSH
            result_ssh = s.connect_ex((ip, 22))
            s.close()

            if result_ssh == 0:

                device_list_region_b.append({"device_type": device_ssh, "ip": ip,
                                          "username": username, "password": password,
                                          "timeout": 50, "fast_cli": False, "global_delay_factor": 2,
                                          "session_log": "log.txt", "session_log_file_mode": "append"})

            else:

                with open(f"tmp/{ip}.error", "w") as f:

                    print(
                        f"Unable to establish SSH or Telnet connection on: {ip}", file=f)
                    f.close()


class ProcessFetch:

    def __init__(self) -> None:
        pass

    def connect_and_fetch(cmd, send_cmd, router):
        try:

            connection = ConnectHandler(**router)

            if cmd == None:

                output = connection.send_command(send_cmd, read_timeout=10)

            elif cmd == "show run":

                # Method for Backup cisco
                output = connection.send_command(cmd, read_timeout=10)

            elif cmd == "display cur":

                # Method for Backup Huawei
                output = connection.send_command(
                    cmd, read_timeout=10)

            elif cmd == cmd:

                # Method for automation
                output = connection.send_config_from_file(
                    cmd, read_timeout=10)

            # Open File
            with open(f"tmp/{router['ip']}.txt", "w") as f:

                print(
                    f"Configuration output for {router['ip']}:\n{output}", file=f)
                f.close()

            connection.disconnect()

        except AuthenticationException:

            with open(f"tmp/{router['ip']}.error", "w") as f:

                print(
                    f"Authentication failed, please verify your credentials on: {router['ip']}", file=f)
                f.close()

        except NetMikoTimeoutException:

            with open(f"tmp/{router['ip']}.error", "w") as f:

                print(
                    f"Timeout on: {router['ip']}", file=f)
                f.close()

        except ValueError:

            with open(f"tmp/{router['ip']}.error", "w") as f:

                print(
                    f"Value Erro", file=f)
                f.close()

    def multithread_region_a(file_cmd, send_cmd):

        for router in device_list_region_a:
            th = threading.Thread(
                target=ProcessFetch.connect_and_fetch, args=(file_cmd, send_cmd, router,))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

    def multithread_region_b(file_cmd, send_cmd):

        for router in device_list_region_b:
            th = threading.Thread(
                target=ProcessFetch.connect_and_fetch, args=(file_cmd, send_cmd, router,))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()
