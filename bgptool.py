#!/usr/bin/env python3
# Author: Tiago Eduardo Zacarias
# Date: 02-05-2025
# Tool objective: Switch traffic to satelital links and main links.
# coding=UTF-8
# License: GPLv3


# EXTERNAL LIBS
from dialog import Dialog
import sys
import time
import locale
import subprocess
import re
import collections
import os

# CUSTOM LIBS
from bgp_peers import mod_peers as neighbor
from mod_netmiko import mod_netmiko as automation


# LOCALE
# locale.setlocale(locale.LC_ALL, '')

# VARS
d = Dialog(dialog="dialog")
main_title = d.set_background_title(
    "BGP Tool v1.9")
button_names = {d.OK: "Select", d.CANCEL: "Cancel",
                d.HELP: "Help", d.EXTRA: "Extra", d.TIMEOUT: "Timeout"}
search_status = []
key_state_satelite_link = []
key_state_main_link = []
key_state_region_a = []
key_state_region_b = []
address_rr_region_a = ("192.168.2.10", "192.168.2.11")
address_rr_region_b = ("192.168.2.12", "192.168.2.13")



# TODO
# Change module automation to netmiko.

# Version
_VersionInfo = collections.namedtuple(
    "VersionInfo", ("major", "minor", "micro", "releasesuffix"))


class VersionInfo(_VersionInfo):
    """Class used to represent the version of pythondialog.

    This class is based on :func:`collections.namedtuple` and has the
    following field names: ``major``, ``minor``, ``micro``,
    ``releasesuffix``.

    .. versionadded:: 2.14
    """

    def __str__(self):
        """Return a string representation of the version."""
        res = ".".join((str(elt) for elt in self[:3]))
        if self.releasesuffix:
            res += self.releasesuffix
        return res

    def __repr__(self):
        return "{0}.{1}".format(__name__, _VersionInfo.__repr__(self))


#: Version of pythondialog as a :class:`VersionInfo` instance.
#:
#: .. versionadded:: 2.14
version_info = VersionInfo(3, 5, 3, None)
#: Version of pythondialog as a string.
#:
#: .. versionadded:: 2.12
__version__ = str(version_info)


class error(Exception):
    """Base class for exceptions in pythondialog."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.complete_message()

    def __repr__(self):
        return "{0}.{1}({2!r})".format(__name__, self.__class__.__name__,
                                       self.message)

    def complete_message(self):
        if self.message:
            return "{0}: {1}".format(self.ExceptionShortDescription,
                                     self.message)
        else:
            return self.ExceptionShortDescription

    ExceptionShortDescription = "{0} generic exception".format("pythondialog")

# Initial Code


class classProcConfigs:

    def __init__(self, configs_temp, configs_default, configs_automation):

        self.configs_temp = configs_temp
        self.configs_default = configs_default
        self.configs_automation = configs_automation

    def create_peer_configs(self):

        for iterate in key_state_main_link:

            if iterate == 1:

                # read input file - Automation to Main Link - REGION_A  and REGION_B
                self.file_configs_default = open(self.configs_default, "w")
                # self.file_configs_default.write("configure terminal" "\n")
                self.file_configs_default.write("router bgp 266604" "\n")
                self.file_configs_default.write("address-family vpnv4" "\n")
                self.file_configs_default.close()

                self.file_configs_default = open(self.configs_default, "r")
                for linhas in self.file_configs_default:

                    self.file_configs_automation = open(
                        self.configs_automation, "a")
                    self.file_configs_automation.write(linhas)
                    self.file_configs_automation.close()

                self.file_configs_temp = open(self.configs_temp, "rt")
                self.data = self.file_configs_temp.read()
                self.data = self.data.replace(r"neighbor", "no neighbor")
                self.file_configs_temp.close()
                self.file_configs_automation = open(
                    self.configs_automation, "a")
                self.file_configs_automation.write(self.data)
                self.file_configs_automation.write("end" "\n")
                self.file_configs_automation.write("wr" "\n")
                # self.file_configs_automation.write("exit" "\n")
                self.file_configs_automation.close()

        for iterate in key_state_satelite_link:

            if iterate == 1:

                # read input file - Automation to Satelite Link - REGION_A e REGION_B
                self.file_configs_default = open(self.configs_default, "w")
                # self.file_configs_default.write("configure terminal" "\n")
                self.file_configs_default.write("router bgp 266604" "\n")
                self.file_configs_default.write("address-family vpnv4" "\n")
                self.file_configs_default.close()

                self.file_configs_default = open(self.configs_default, "r")

                for linhas in self.file_configs_default:

                    self.file_configs_automation = open(
                        self.configs_automation, "a")
                    self.file_configs_automation.write(linhas)
                    self.file_configs_automation.close()

                self.file_configs_temp = open(self.configs_temp, "rt")
                self.data = self.file_configs_temp.read()
                self.data = self.data.replace(r"neighbor", "neighbor")
                self.file_configs_temp.close()
                self.file_configs_automation = open(
                    self.configs_automation, "a")
                self.file_configs_automation.write(self.data)
                self.file_configs_automation.write("end" "\n")
                self.file_configs_automation.write("wr" "\n")
                # self.file_configs_automation.write("exit" "\n")
                self.file_configs_automation.close()

    # Oriented of objects
    def proc_configs_region_a():

        # REGION_A Atributes
        region_a_file_tmp = "tmp/configs_temp_region_a.txt"
        region_a_file_default = "tmp/configs_default_region_a.txt"
        region_a_file_automation = "tmp/configs_automation_region_a.txt"

        # REGION_A Objects
        configs_region_b = classProcConfigs(
            region_a_file_tmp, region_a_file_default, region_a_file_automation)
        configs_region_b.create_peer_configs()

    def proc_configs_region_b():

        # Merit Atributes
        region_b_file_tmp = "tmp/configs_temp_region_b.txt"
        region_b_file_default = "tmp/configs_default_region_b.txt"
        region_b_file_automation = "tmp/configs_automation_region_b.txt"

        # Merit Objects
        configs_region_b = classProcConfigs(
            region_b_file_tmp, region_b_file_default, region_b_file_automation)
        configs_region_b.create_peer_configs()


class classMain:

    try:

        def __init__(self):

            pass

        def clear_tmp_files():

            test_file_exist = [
                "test -d tmp/configs_default_region_a.txt tmp/configs_temp_region_a.txt tmp/configs_automation_region_a.txt tmp/configs_default_region_b.txt tmp/configs_temp_region_b.txt tmp/configs_automation_region_b.txt || rm -rf tmp/*"]
            subprocess.run(test_file_exist, shell=True)

    except (ValueError, IndexError):
        # raise "Erro de Index"
        pass

    except KeyboardInterrupt:

        pass

    def define_status():

        try:
            # Concatenation of search_status list elements for preview multiple selection of switching types.
            # Avoids inconsistency in automation.
            separador = ''
            result = [separador.join(search_status)]

            for iterate in result:

                t = re.compile(
                    r"Comutar para Link SatelitalComutar para Link Terrestre|Comutar para Link Satelital|Comutar para Link Terrestre")
                check = t.findall(iterate)[0]

            # print(check)
            if check == "Null":

                d.infobox(
                    "Você precisa selecionar uma das opções disponiveis..", width=40, height=10)
                time.sleep(2)
                classMain.commutation_menu()

            elif check == "Comutar para Link SatelitalComutar para Link Terrestre":

                d.infobox("Não é possível a escolha de multiplas opções neste menu.",
                          width=60, height=10)
                time.sleep(5)
                classMain.commutation_menu()

            elif check == "Comutar para Link Satelital":

                key_state_satelite_link.append(1)
                classMain.main_menu()

            elif check == "Comutar para Link Terrestre":

                key_state_main_link.append(1)
                classMain.main_menu()

        except (ValueError, IndexError):
            # raise "Erro de Index"
            pass

        except KeyboardInterrupt:

            pass

    def commutation_menu():

        # Clear status of options and temporary files
        key_state_main_link.clear()
        key_state_satelite_link.clear()
        key_state_region_a.clear()
        key_state_region_b.clear()
        search_status.clear()
        classMain.clear_tmp_files()

        try:

            d.infobox("Bem Vindo(a) a ferramenta BGP Tool ",
                      width=60, height=10)

            time.sleep(1)

            code, tags = d.checklist("Escolha uma das opções de comutação abaixo:",
                                     choices=[("Comutar para Link Satelital", "", False),
                                              ("Comutar para Link Terrestre",
                                               "", False),
                                              ],
                                     title="Menu de Comutação.",
                                     backtitle="BGP Tool  v1.9 - Built for REGION_A and REGION_B", width=60, height=20,
                                     help_button=True, help_tags=True, help_label="Ajuda", help_status=True, cancel_label="Sair")

            if code == d.HELP:

                d.msgbox("Você precisa selecionar uma das opções com a tecla espaço e depois precionar a tecla \"ENTER\" para concluir a seleção do tipo de comutação.\
                         Neste menu não é possível a seleção de multiplas opções, pois gera conflito na automação.",
                         width=60, height=10)
                classMain.commutation_menu()

            elif code == d.OK and tags != "[]":

                for iterate in tags:

                    search_status.append(iterate)

                classMain.define_status()

            elif code == d.TIMEOUT:

                d.infobox("Você deve selecionar uma opção")
                classMain.commutation_menu()

            elif code == d.ESC:

                d.msgbox(
                    "Você saiu do menu principal pressionando a tecla ESC.", width=40, height=10)
                classMain.commutation_menu()

            elif code == d.CANCEL:

                d.infobox("Saindo...", width=40, height=10)
                time.sleep(3)
                clear_shell = ["clear"]
                subprocess.run(clear_shell, shell=True)
                sys.exit(0)

            d.infobox(
                "Você precisa selecionar uma das opções disponiveis..", width=40, height=10)
            time.sleep(2)
            classMain.commutation_menu()

        except IndexError:

            pass

        except KeyboardInterrupt:

            pass

    def main_menu():

        # Clear variables and temporary files
        classMain.clear_tmp_files()
        key_state_region_a.clear()
        key_state_region_b.clear()

        try:

            code, tags = d.checklist("Lista de Sites:",
                                     choices=[("Site A", "", False),
                                              ("Site B", "", False),
                                              ("Site C", "", False),
                                              ("Site D", "", False),
                                              ("Site E", "", False)
                                             ],
                                     title="Escolha a localidade para comutação.",
                                     backtitle="BGP Tool  v1.9 - Built for REGION_A and REGION_B", width=70, height=30,
                                     help_button=True, help_tags=True, help_status=True, help_label="Ajuda", cancel_label="Sair", list_height=20, extra_button=True, extra_label="Voltar")

            if code == d.HELP:

                d.msgbox("Você precisa selecionar uma localidade com a tecla espaço e depois precionar a tecla \"ENTER\" para realizar a comutação conforme desejado.\
                          Neste menu é possível a seleção de múltiplos sites para comutação.",
                         width=60, height=10)
                classMain.main_menu()

            elif code == d.OK and tags == []:

                d.infobox("Você precisa selecionar uma opção..",
                          width=40, height=10)
                time.sleep(2)
                classMain.main_menu()

            elif code == d.OK and tags != "[]":

                for iterate in tags:

                    get_peers = neighbor.peers.get(iterate)

                    if "REGION_A" in get_peers:

                        key_state_region_a.append(1)
                        # Regex - match ip addresses of peers BGP
                        t = re.compile(
                            r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}")
                        get_d = t.findall((str(get_peers)))

                        for peer in get_d:

                            # Write file for automation
                            file = open("tmp/configs_temp_region_a.txt", "a")
                            str_peers = repr(peer).replace(
                                "'", "").replace("[", "").replace("]", "")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL in" "\n")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL out" "\n")

                            file.close()

                    if "REGION_B" in get_peers:

                        key_state_region_b.append(1)
                        # Regex - match ip addresses of peers BGP
                        t = re.compile(
                            r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}")
                        get_m = t.findall((str(get_peers)))

                        for peer in get_m:
                            # Write file for automation
                            file = open("tmp/configs_temp_region_b.txt", "a")
                            str_peers = repr(peer).replace(
                                "'", "").replace("[", "").replace("]", "")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL in" "\n")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL out" "\n")

                            file.close()

                # Sentence Oriented of Object
                if 1 in key_state_region_a and 1 in key_state_region_b:

                    classProcConfigs.proc_configs_region_b()
                    classProcConfigs.proc_configs_region_a()

                elif 1 in key_state_region_a:

                    classProcConfigs.proc_configs_region_a()

                elif 1 in key_state_region_b:

                    classProcConfigs.proc_configs_region_b()

                d.yesno("Tem certeza que deseja comutar o trafêgo da(s) localidade(s)?",
                        width=40, height=10)

                if code == d.OK:

                    d.set_background_title("Aguarde por favor.")

                    d.gauge_start()

                    d.gauge_update(10)
                    time.sleep(1)
                    d.gauge_update(40)

                    # Test File Automation
                    test_file_region_a_exist = os.path.isfile(
                        "tmp/configs_automation_region_a.txt")
                    test_file_region_b_exist = os.path.isfile(
                        "tmp/configs_automation_region_b.txt")

                    # Automation REGION_A and REGION_B
                    if test_file_region_a_exist == True:

                        automation.device_list_region_a.clear()

                        for ip in address_rr_region_a:

                            device_telnet = "cisco_ios_telnet"
                            device_ssh = "cisco_ios_ssh"

                            automation.ProcessConnectionDwdm.test_connection(
                                ip, device_telnet, device_ssh)

                        file_cmd = "tmp/configs_automation_region_a.txt"
                        send_cmd = None

                        automation.ProcessFetch.multithread_region_a(
                            file_cmd, send_cmd)

                    if test_file_region_b_exist == True:

                        automation.device_list_region_b.clear()

                        for ip in address_rr_region_b:

                            device_telnet = "cisco_ios_telnet"
                            device_ssh = "cisco_ios_ssh"

                            automation.ProcessConnectionMerit.test_connection(
                                ip, device_telnet, device_ssh)

                        file_cmd = "tmp/configs_automation_region_b.txt"
                        send_cmd = None
                        automation.ProcessFetch.multithread_region_b(
                            file_cmd, send_cmd)

                    d.gauge_update(80)
                    time.sleep(1)
                    d.gauge_update(100)  # work is done
                    time.sleep(2)

                    d.infobox("Comutação relizada com sucesso..",
                              width=40, height=10)
                    time.sleep(1)
                    classMain.main_menu()

                elif code == d.CANCEL:

                    d.infobox("Voltando para o menu principal..",
                              width=40, height=10)
                    time.sleep(1)
                    classMain.main_menu()

            elif code == d.TIMEOUT:

                d.infobox("Você deve selecionar uma opção",
                          width=40, height=10)

                classMain.main_menu()

            elif code == d.ESC:

                d.msgbox(
                    "Você saiu do menu principal pressionando a tecla ESC.", width=40, height=10)
                classMain.main_menu()

            elif code == d.CANCEL:

                d.infobox("Saindo...", width=40, height=10)
                time.sleep(3)
                clear_shell = ["clear"]
                subprocess.run(clear_shell, shell=True)

            elif code == "extra":

                classMain.commutation_menu()

            else:

                d.infobox(
                    "Você precisa selecionar um dos sites disponiveis..", width=40, height=10)
                time.sleep(2)
                classMain.main_menu()

        except IndexError:

            pass

        except KeyboardInterrupt:

            pass

        sys.exit(0)


if __name__ == '__main__':

    classMain.commutation_menu()
    __version__ = str(version_info)
    print(f"[dialog version:{__version__}]")
    print(f"[Bye-Bye!]")
