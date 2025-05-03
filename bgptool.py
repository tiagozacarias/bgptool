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
    "BGP Tool COT-CEMIG v1.9 - Built for DWDM and MERIT")
button_names = {d.OK: "Select", d.CANCEL: "Cancel",
                d.HELP: "Help", d.EXTRA: "Extra", d.TIMEOUT: "Timeout"}
search_status = []
key_state_satelite_link = []
key_state_main_link = []
key_state_dwdm = []
key_state_merit = []
address_rr_dwdm = ("192.168.2.10", "192.168.2.11")
address_rr_merit = ("192.168.2.12", "192.168.2.13")
# address_rr_dwdm = ("10.2.72.60", "10.2.78.6")
# address_rr_merit = ("10.2.72.208", "10.2.18.25")


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

                # read input file - Automation to Main Link - DWDM e MERIT
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

                # read input file - Automation to Satelite Link - DWDM e MERIT
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
    def proc_configs_dwdm():

        # DWDM Atributes
        dwdm_file_tmp = "tmp/configs_temp_dwdm.txt"
        dwdm_file_default = "tmp/configs_default_dwdm.txt"
        dwdm_file_automation = "tmp/configs_automation_dwdm.txt"

        # DWDM Objects
        configs_merit = classProcConfigs(
            dwdm_file_tmp, dwdm_file_default, dwdm_file_automation)
        configs_merit.create_peer_configs()

    def proc_configs_merit():

        # Merit Atributes
        merit_file_tmp = "tmp/configs_temp_merit.txt"
        merit_file_default = "tmp/configs_default_merit.txt"
        merit_file_automation = "tmp/configs_automation_merit.txt"

        # Merit Objects
        configs_merit = classProcConfigs(
            merit_file_tmp, merit_file_default, merit_file_automation)
        configs_merit.create_peer_configs()


class classMain:

    try:

        def __init__(self):

            pass

        def clear_tmp_files():

            test_file_exist = [
                "test -d tmp/configs_default_dwdm.txt tmp/configs_temp_dwdm.txt tmp/configs_automation_dwdm.txt tmp/configs_default_merit.txt tmp/configs_temp_merit.txt tmp/configs_automation_merit.txt || rm -rf tmp/*"]
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
        key_state_dwdm.clear()
        key_state_merit.clear()
        search_status.clear()
        classMain.clear_tmp_files()

        try:

            d.infobox("Bem Vindo(a) a ferramenta BGP Tool COT-CEMIG",
                      width=60, height=10)

            time.sleep(1)

            code, tags = d.checklist("Escolha uma das opções de comutação abaixo:",
                                     choices=[("Comutar para Link Satelital", "", False),
                                              ("Comutar para Link Terrestre",
                                               "", False),
                                              ],
                                     title="Menu de Comutação.",
                                     backtitle="BGP Tool COT-CEMIG v1.9 - Built for DWDM and MERIT", width=60, height=20,
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
        key_state_dwdm.clear()
        key_state_merit.clear()

        try:

            code, tags = d.checklist("Lista de Sites - COS DIGITAL - CEMIG:",
                                     choices=[("Baguari SE", "", False),
                                              ("Barao de Cocais SE 3", "", False),
                                              ("Barbacena SE 2", "", False),
                                              ("Barreiro SE 1", "", False),
                                              ("Bom Despacho SE 3", "", False),
                                              ("Braunas SE", "", False),
                                              ("Camargos UHE", "", False),
                                              ("Conselheiro Pena SE", "", False),
                                              ("Emborcacao SE", "--> Comuta também Theodomiro C Santiago SE (UHE Emborcacao)", False),
                                              # ("Gafanhoto UHE", "Sem Satelite", False),
                                              ("Guilman Amorim SE", "", False),
                                              # ("Igarape UTE", "Sem Satelite", False),
                                              ("Ipatinga SE 1", "", False),
                                              # ("Irape SE", "Sem Satelite", False),
                                              ("Irape UHE", "", False),
                                              ("Itabira SE 2", "", False),
                                              ("Itabira SE 4", "", False),
                                              ("Itajuba SE 3", "", False),
                                              # ("Itabira SE 5", "Sem Satelite", False),
                                              ("Itabirito SE 2", "", False),
                                              ("Itutinga SE 345KV", "", False),
                                              ("Itutinga UHE", "", False),
                                              ("Jaguara SE 500KV",
                                               "--> Comuta também Jaguara SE 345KV", False),
                                              ("Jeceaba SE", "", False),
                                              ("Joao Molevade SE 2", "", False),
                                              # ("Joao Molevade SE 4", "Sem Satelite", False),
                                              ("Juiz de Fora SE 1", "", False),
                                              ("Lafaiete SE 1", "", False),
                                              ("Mascarenhas SE", "", False),
                                              ("Mesquita SE", "", False),
                                              ("Montes Claros SE 2", "", False),
                                              ("Nova Lima SE 6", "", False),
                                              ("Nova Ponte SE",
                                               "--> Comuta também Nova Ponte UHE", False),
                                              ("Ouro Preto SE 2", "", False),
                                              ("Pimenta SE", "", False),
                                              ("Pirapora SE 2", "", False),
                                              ("Porto Estrela SE", "", False),
                                              # ("Queimado SE", "Validar Route Reflector esta apontado para o Merit", False),
                                              ("Rosal UHE", "", False),
                                              ("Sa Carvalho UHE", "", False),
                                              ("Sabara SE 3", "", False),
                                              ("Salto Grande SE", "", False),
                                              ("Santos Dumont SE 2", "", False),
                                              ("Sao Goncalo do Para SE", "", False),
                                              ("Sao Gotardo SE 2", "", False),
                                              ("Sao Simao SE", "", False),
                                              ("Sete Lagoas SE 4", "", False),
                                              ("Taquaril SE", "", False),
                                              ("Timoteo SE 1", "", False),
                                              ("Timoteo SE 2", "", False),
                                              ("Tres Marias SE", "", False),
                                              ("Tres Marias UHE", "", False),
                                              # ("Uberaba 1 SE", "Sem Satelite", False),
                                              # ("Uberlandia Radio SE", "Sem Satelite", False),
                                              # ("Valadares SE 1", "Sem Satelite", False),
                                              ("Valadares SE 2", "", False),
                                              # ("Valadares SE 6", "Sem Satelite", False),
                                              ("Varzea da Palma 1 SE", "", False),
                                              ("Varzea da Palma 4 SE", "", False),
                                              ("Vespasiano SE 2", "", False),
                                              ("Volta Grande SE", "", False)],
                                     title="Escolha a localidade para comutação.",
                                     backtitle="BGP Tool COT-CEMIG v1.9 - Built for DWDM and MERIT", width=70, height=30,
                                     help_button=True, help_tags=True, help_status=True, help_label="Ajuda", cancel_label="Sair", list_height=20, extra_button=True, extra_label="Voltar")

            if code == d.HELP:

                d.msgbox("Você precisa selecionar uma localidade com a tecla espaço e depois precionar a tecla \"ENTER\" para realizar a comutação conforme desejado.\
                          Neste menu é possível a seleção de múltiplos sites (COS-DIGITAL) para comutação.",
                         width=60, height=10)
                classMain.main_menu()

            elif code == d.OK and tags == []:

                d.infobox("Você precisa selecionar uma opção..",
                          width=40, height=10)
                time.sleep(2)
                classMain.main_menu()

            elif code == d.OK and tags != "[]":

                for iterate in tags:

                    get_peers = neighbor.peers_cemig_cos_digital.get(iterate)

                    if "DWDM" in get_peers:

                        key_state_dwdm.append(1)
                        # Regex - match ip addresses of peers BGP
                        t = re.compile(
                            r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}")
                        get_d = t.findall((str(get_peers)))

                        for peer in get_d:

                            # Write file for automation
                            file = open("tmp/configs_temp_dwdm.txt", "a")
                            str_peers = repr(peer).replace(
                                "'", "").replace("[", "").replace("]", "")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL in" "\n")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL out" "\n")

                            file.close()

                    if "MERIT" in get_peers:

                        key_state_merit.append(1)
                        # Regex - match ip addresses of peers BGP
                        t = re.compile(
                            r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}")
                        get_m = t.findall((str(get_peers)))

                        for peer in get_m:
                            # Write file for automation
                            file = open("tmp/configs_temp_merit.txt", "a")
                            str_peers = repr(peer).replace(
                                "'", "").replace("[", "").replace("]", "")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL in" "\n")
                            file.write("neighbor" " " + str_peers +
                                       " " "route-map DENY-ALL out" "\n")

                            file.close()

                # Sentence Oriented of Object
                if 1 in key_state_dwdm and 1 in key_state_merit:

                    classProcConfigs.proc_configs_merit()
                    classProcConfigs.proc_configs_dwdm()

                elif 1 in key_state_dwdm:

                    classProcConfigs.proc_configs_dwdm()

                elif 1 in key_state_merit:

                    classProcConfigs.proc_configs_merit()

                d.yesno("Tem certeza que deseja comutar o trafêgo da(s) localidade(s)?",
                        width=40, height=10)

                if code == d.OK:

                    d.set_background_title("Aguarde por favor.")

                    d.gauge_start()

                    d.gauge_update(10)
                    time.sleep(1)
                    d.gauge_update(40)

                    # Test File Automation
                    test_file_dwdm_exist = os.path.isfile(
                        "tmp/configs_automation_dwdm.txt")
                    test_file_merit_exist = os.path.isfile(
                        "tmp/configs_automation_merit.txt")

                    # Automation DWDM and MERIT
                    if test_file_dwdm_exist == True:

                        automation.device_list_dwdm.clear()

                        for ip in address_rr_dwdm:

                            device_telnet = "cisco_ios_telnet"
                            device_ssh = "cisco_ios_ssh"

                            automation.ProcessConnectionDwdm.test_connection(
                                ip, device_telnet, device_ssh)

                        file_cmd = "tmp/configs_automation_dwdm.txt"
                        send_cmd = None

                        automation.ProcessFetch.multithread_dwdm(
                            file_cmd, send_cmd)

                    if test_file_merit_exist == True:

                        automation.device_list_merit.clear()

                        for ip in address_rr_merit:

                            device_telnet = "cisco_ios_telnet"
                            device_ssh = "cisco_ios_ssh"

                            automation.ProcessConnectionMerit.test_connection(
                                ip, device_telnet, device_ssh)

                        file_cmd = "tmp/configs_automation_merit.txt"
                        send_cmd = None
                        automation.ProcessFetch.multithread_merit(
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
