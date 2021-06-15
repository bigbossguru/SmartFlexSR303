import os
import time
from libConfigSSH import *
from termcolor import colored, cprint
from parser_ovpn_info import parser

os.system('')
color_attention_msg = 'yellow'
color_successful = 'green'
indent = ' '*9

cprint('\t---------------------------------------------------------------------------------', 'green')
cprint('\t|                              SmartFlex script                                 |', 'green')
cprint('\t---------------------------------------------------------------------------------', 'green')
cprint('\t\t\t   **for default authorization press Enter**\n', color_attention_msg)
try:
    status_connection, client_connection_sftp = connection_user_ssh()
except TypeError: exit()

def main():
    try:
        if status_connection is None:
            print('\t---------------------------------------------------------------------------------')
            print('\t|                                  Information                                  |')
            print('\t---------------------------------------------------------------------------------\n')
            data_info = command_user_ssh(command=command_info, flag_data=True)
            str_info = str(data_info).split('\n')
            for i in str_info:
                print('\t\t'+i)

        print('\t---------------------------------------------------------------------------------')
        print('\t|                              Router options                                   |')
        print('\t---------------------------------------------------------------------------------\n')
        print('\t\tManual mode              - self configuration of the router    [mm]')
        print('\t\tNetwork info             - print information network status    [ni]')
        print('\t\tInstall user modules     - copies and installing modules       [um]')
        print('\t\tUpdate Firmware          - update firmware                     [up]')
        print('\t\tBackup config            - backup configuration and save local [bc]')
        # print('\t\tExtend nat port          - extend nat port forwarding          [np]')
        print('\t\tReboot router            - reboot smartFlex                    [re]')
        print('\t\tExit script              - exit from is this script            [ex]\n')

        user_ans_conf = input(indent+'Choose options and enter: ').lower()

        if user_ans_conf == 'mm':
            print('\t---------------------------------------------------------------------------------')
            print('\t|                                  Manual Mode                                  |')
            print('\t---------------------------------------------------------------------------------\n')
            create_conf_cfg()
            try:
                print(indent+'SET WAN ETH0:')
                cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                eth0_dhcp = control_answear(indent+'ETH0 Enabled DHCP Client [Y/n]: ')
                if eth0_dhcp == 'y' or len(eth0_dhcp) == 0:
                    replace_string_conf_v1(strHead_lineNum_conf.get(0), DHCP)
                    for i in range(1, 8):
                        if ((i==4) or (i==5)): replace_string_conf_v1(strHead_lineNum_conf.get(i), '0')
                        else:                  replace_string_conf_v1(strHead_lineNum_conf.get(i), '')

                elif eth0_dhcp == 'n':
                    for i in range(1, 8):
                        if ((i==4) or (i==5)): replace_string_conf_v1(strHead_lineNum_conf.get(i), '0')
                        else:                  replace_string_conf_v1(strHead_lineNum_conf.get(i), '')
                    eth0_ip_addr = control_answear(indent+'ETH0 IP Address (default=10.0.0.1)[d]: ','d', DEFAULT_IP[2])
                    if eth0_ip_addr == 'd':
                        replace_string_conf_v1(strHead_lineNum_conf.get(0), STATIC)
                        replace_string_conf_v1(strHead_lineNum_conf.get(1), DEFAULT_IP[2])
                        replace_string_conf_v1(strHead_lineNum_conf.get(2), DEFAULT_NETMASK)
                        replace_string_conf_v1(strHead_lineNum_conf.get(3), DEFAULT_NETWORK[2])
                        eth0_dhcp_server = control_answear(indent+'ETH0 Enabled DHCP Server [Y/n]: ','d')
                        if eth0_dhcp_server == 'y':
                            replace_string_conf_v1(strHead_lineNum_conf.get(5), '1')
                            if eth0_ip_addr == 'd' or eth0_ip_addr == DEFAULT_IP[2]:
                                replace_string_conf_v1(strHead_lineNum_conf.get(6), DHCP_POOL_LO_HI_eth0[0])
                                replace_string_conf_v1(strHead_lineNum_conf.get(7), DHCP_POOL_LO_HI_eth0[1])
                            else:
                                replace_string_conf_v1(strHead_lineNum_conf.get(6), eth0_ip_addr[:eth0_ip_addr.rfind('.')+1]+'100')
                                replace_string_conf_v1(strHead_lineNum_conf.get(7), eth0_ip_addr[:eth0_ip_addr.rfind('.')+1]+'200')
                        else:
                            replace_string_conf_v1(strHead_lineNum_conf.get(5), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(6), '')
                            replace_string_conf_v1(strHead_lineNum_conf.get(7), '')
                    else:
                        replace_string_conf_v1(strHead_lineNum_conf.get(0), STATIC)
                        replace_string_conf_v1(strHead_lineNum_conf.get(1), eth0_ip_addr)
                        replace_string_conf_v1(strHead_lineNum_conf.get(2), DEFAULT_NETMASK)
                        replace_string_conf_v1(strHead_lineNum_conf.get(3), eth0_ip_addr[:eth0_ip_addr.rfind('.')+1]+'0')
                        eth0_dhcp_server = control_answear(indent+'ETH0 Enabled DHCP Server [y/n]: ')
                        if eth0_dhcp_server == 'y':
                            replace_string_conf_v1(strHead_lineNum_conf.get(5), '1')
                            if eth0_ip_addr == 'd' or eth0_ip_addr == DEFAULT_IP[2]:
                                replace_string_conf_v1(strHead_lineNum_conf.get(6), DHCP_POOL_LO_HI_eth0[0])
                                replace_string_conf_v1(strHead_lineNum_conf.get(7), DHCP_POOL_LO_HI_eth0[1])
                            else:
                                replace_string_conf_v1(strHead_lineNum_conf.get(6), eth0_ip_addr[:eth0_ip_addr.rfind('.')+1]+'100')
                                replace_string_conf_v1(strHead_lineNum_conf.get(7), eth0_ip_addr[:eth0_ip_addr.rfind('.')+1]+'200')
                        else:
                            replace_string_conf_v1(strHead_lineNum_conf.get(5), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(6), '')
                            replace_string_conf_v1(strHead_lineNum_conf.get(7), '')
                print('\n')

                print(indent+'SET LAN ETH1:')
                cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                eth1_bridge      = control_answear(indent+'ETH1 Enabled BRIDGED [y/N]: ')
                eth1_dhcp_server = control_answear(indent+'ETH1 Enabled DHCP Server [Y/n]: ')
                if eth1_bridge == 'y':  eth1_ip_addr = control_answear(indent+'ETH1 IP Address (default=192.168.1.1)[D]: ','d', DEFAULT_IP[1])
                else:                   eth1_ip_addr = control_answear(indent+'ETH1 IP Address (default=192.168.2.1)[D]: ','d', DEFAULT_IP[0]) 
                if eth1_dhcp_server == 'n': 
                    eth1_dhcp = control_answear(indent+'ETH1 Enabled DHCP Client [y/n]: ')
                    if eth1_dhcp == 'y':
                        replace_string_conf_v1(strHead_lineNum_conf.get(8), DHCP)
                        for i in range(9, 16): replace_string_conf_v1(strHead_lineNum_conf.get(i), '')
                        if eth1_bridge == 'y': replace_string_conf_v1(strHead_lineNum_conf.get(12), '1')
                        else:                  replace_string_conf_v1(strHead_lineNum_conf.get(12), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(13), '0')

                elif eth1_dhcp_server == 'y' or len(eth1_dhcp_server) == 0:
                    replace_string_conf_v1(strHead_lineNum_conf.get(8), STATIC)
                    for i in range(9, 16): replace_string_conf_v1(strHead_lineNum_conf.get(i), '')
                    if eth1_bridge == 'y': replace_string_conf_v1(strHead_lineNum_conf.get(12), '1')
                    else:                  replace_string_conf_v1(strHead_lineNum_conf.get(12), '0')
                    replace_string_conf_v1(strHead_lineNum_conf.get(13), '0')
                    
                    if (eth1_ip_addr == 'd' or len(eth1_ip_addr) == 0) and (eth1_bridge != 'y' or len(eth1_bridge) == 0): 
                        replace_string_conf_v1(strHead_lineNum_conf.get(9), DEFAULT_IP[0])
                        replace_string_conf_v1(strHead_lineNum_conf.get(10), DEFAULT_NETMASK)
                        replace_string_conf_v1(strHead_lineNum_conf.get(11), DEFAULT_NETWORK[0])
                        replace_string_conf_v1(strHead_lineNum_conf.get(13), '1')
                        replace_string_conf_v1(strHead_lineNum_conf.get(14), DHCP_POOL_LO_HI_eth1[0])
                        replace_string_conf_v1(strHead_lineNum_conf.get(15), DHCP_POOL_LO_HI_eth1[1])
                    elif (eth1_ip_addr == 'd' or len(eth1_ip_addr) == 0) and (eth1_bridge == 'y'):
                        replace_string_conf_v1(strHead_lineNum_conf.get(9), DEFAULT_IP[1])
                        replace_string_conf_v1(strHead_lineNum_conf.get(10), DEFAULT_NETMASK)
                        replace_string_conf_v1(strHead_lineNum_conf.get(11), DEFAULT_NETWORK[1])
                        replace_string_conf_v1(strHead_lineNum_conf.get(13), '1')
                        replace_string_conf_v1(strHead_lineNum_conf.get(14), DHCP_POOL_LO_HI_eth2[0])
                        replace_string_conf_v1(strHead_lineNum_conf.get(15), DHCP_POOL_LO_HI_eth2[1]) 
                    elif len(eth1_ip_addr) > 4:
                        replace_string_conf_v1(strHead_lineNum_conf.get(9), eth1_ip_addr)
                        replace_string_conf_v1(strHead_lineNum_conf.get(10), DEFAULT_NETMASK)
                        replace_string_conf_v1(strHead_lineNum_conf.get(11), eth1_ip_addr[:eth1_ip_addr.rfind('.')+1]+'0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(13), '1')
                        if eth1_ip_addr == '192.168.1.1':
                            replace_string_conf_v1(strHead_lineNum_conf.get(14), DHCP_POOL_LO_HI_eth2[0])
                            replace_string_conf_v1(strHead_lineNum_conf.get(15), DHCP_POOL_LO_HI_eth2[1])
                        else:
                            replace_string_conf_v1(strHead_lineNum_conf.get(14), eth1_ip_addr[:eth1_ip_addr.rfind('.')+1]+'100')
                            replace_string_conf_v1(strHead_lineNum_conf.get(15), eth1_ip_addr[:eth1_ip_addr.rfind('.')+1]+'200')

                    if eth1_bridge.lower() == 'y': replace_string_conf_v1(strHead_lineNum_conf.get(12), '1')
                    else:                          replace_string_conf_v1(strHead_lineNum_conf.get(12), '0')
                print('\n')

                if eth1_bridge != 'y':
                    print(indent+'SET LAN EHT2:')
                    cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                    eth2_dhcp_server = control_answear(indent+'ETH2 Enabled DHCP Server [Y/n]: ')
                    eth2_ip_addr     = control_answear(indent+'IP Address ETH2 (default=192.168.1.1)[D]: ','d', DEFAULT_IP[1])
                    mac_addr_plc     = input(indent+'MAC Address PLC (format=00:00:00:00:00:00): ').upper()
                    ip_addr_plc      = control_answear(indent+'IP Address PLC (default=192.168.1.10)[D]: ','d', DEFAULT_IP_PLC)
                    if eth2_dhcp_server == 'n': 
                        eth2_dhcp = control_answear(indent+'ETH2 Enabled DHCP Client [y/n]: ')
                        if eth2_dhcp == 'y':
                            replace_string_conf_v1(strHead_lineNum_conf.get(16), DHCP)
                            for i in range(17, 27): replace_string_conf_v1(strHead_lineNum_conf.get(i), '')
                            if eth1_bridge == 'y':  replace_string_conf_v1(strHead_lineNum_conf.get(20), '1')
                            else:                   replace_string_conf_v1(strHead_lineNum_conf.get(20), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(21), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')

                    elif eth2_dhcp_server == 'y' or len(eth2_dhcp_server) == 0:
                        replace_string_conf_v1(strHead_lineNum_conf.get(16), STATIC)
                        for i in range(17, 27): replace_string_conf_v1(strHead_lineNum_conf.get(i), '')
                        if eth1_bridge == 'y':  replace_string_conf_v1(strHead_lineNum_conf.get(20), '1')
                        else:                   replace_string_conf_v1(strHead_lineNum_conf.get(20), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(21), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')

                        if ip_addr_plc == 'd' or len(ip_addr_plc) == 0: replace_string_nat(DEFAULT_IP_PLC)
                        elif len(ip_addr_plc) > 4:                      replace_string_nat(ip_addr_plc)

                        if eth2_ip_addr == 'd' or len(eth2_ip_addr) == 0:
                            replace_string_conf_v1(strHead_lineNum_conf.get(17), DEFAULT_IP[1])
                            replace_string_conf_v1(strHead_lineNum_conf.get(18), DEFAULT_NETMASK)
                            replace_string_conf_v1(strHead_lineNum_conf.get(19), DEFAULT_NETWORK[1])
                            replace_string_conf_v1(strHead_lineNum_conf.get(21), '1')
                            replace_string_conf_v1(strHead_lineNum_conf.get(22), DHCP_POOL_LO_HI_eth2[0])
                            replace_string_conf_v1(strHead_lineNum_conf.get(23), DHCP_POOL_LO_HI_eth2[1])

                            if len(mac_addr_plc) > 1: replace_string_conf_v1(strHead_lineNum_conf.get(24), '1')
                            else:                     replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(25), mac_addr_plc)
                            replace_string_conf_v1(strHead_lineNum_conf.get(26), '')
                            if (ip_addr_plc == 'd') or (len(ip_addr_plc) == 0) and (len(mac_addr_plc) > 4):
                                replace_string_conf_v1(strHead_lineNum_conf.get(26), DEFAULT_IP_PLC)
                            elif (len(ip_addr_plc) > 4) and (len(mac_addr_plc) > 4):
                                replace_string_conf_v1(strHead_lineNum_conf.get(26), ip_addr_plc)
                        
                        elif len(eth2_ip_addr) > 4:
                            replace_string_conf_v1(strHead_lineNum_conf.get(17), eth2_ip_addr)
                            replace_string_conf_v1(strHead_lineNum_conf.get(18), DEFAULT_NETMASK)
                            replace_string_conf_v1(strHead_lineNum_conf.get(19), eth2_ip_addr[:eth2_ip_addr.rfind('.')+1]+'0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(21), '1')
                            if eth2_ip_addr == DEFAULT_IP[0]:
                                replace_string_conf_v1(strHead_lineNum_conf.get(22), DHCP_POOL_LO_HI_eth1[0])
                                replace_string_conf_v1(strHead_lineNum_conf.get(23), DHCP_POOL_LO_HI_eth1[1])
                            else:
                                replace_string_conf_v1(strHead_lineNum_conf.get(22), eth2_ip_addr[:eth2_ip_addr.rfind('.')+1]+'100')
                                replace_string_conf_v1(strHead_lineNum_conf.get(23), eth2_ip_addr[:eth2_ip_addr.rfind('.')+1]+'200')
                            if (len(mac_addr_plc) > 0) and (len(ip_addr_plc) > 0):
                                replace_string_conf_v1(strHead_lineNum_conf.get(24), '1')
                            else: replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(25), mac_addr_plc)
                            replace_string_conf_v1(strHead_lineNum_conf.get(26), '')
                            if (ip_addr_plc == 'd') or (len(ip_addr_plc) == 0) and (len(mac_addr_plc) > 4):
                                replace_string_conf_v1(strHead_lineNum_conf.get(26), DEFAULT_IP_PLC)
                            elif (len(ip_addr_plc) > 4) and (len(mac_addr_plc) > 4):
                                replace_string_conf_v1(strHead_lineNum_conf.get(26), ip_addr_plc)
                            if (ip_addr_plc == 'd' or len(ip_addr_plc) == 0): replace_string_nat(DEFAULT_IP_PLC)
                            elif len(ip_addr_plc) > 4:                        replace_string_nat(ip_addr_plc)
                    replace_string_conf_v1(strHead_lineNum_conf.get(29), '0')
                    replace_string_conf_v1(strHead_lineNum_conf.get(30), '')
                    replace_string_conf_v1(strHead_lineNum_conf.get(31), '')

                else:
                    mac_addr_plc = input(indent+'MAC Address PLC (format=00:00:00:00:00:00): ').upper()
                    ip_addr_plc = control_answear(indent+'IP Address PLC (default=192.168.1.10)[D]: ','d', DEFAULT_IP_PLC)
                    replace_string_conf_v1(strHead_lineNum_conf.get(20), '1')
                    replace_string_conf_v1(strHead_lineNum_conf.get(21), '0')
                    replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')
                    replace_string_conf_v1(strHead_lineNum_conf.get(25), '')
                    replace_string_conf_v1(strHead_lineNum_conf.get(26), '')
                    if len(mac_addr_plc) > 4:
                        replace_string_conf_v1(strHead_lineNum_conf.get(29), '1')
                        replace_string_conf_v1(strHead_lineNum_conf.get(30), mac_addr_plc)
                        if (ip_addr_plc == 'd'): 
                            replace_string_nat(DEFAULT_IP_PLC)
                            replace_string_conf_v1(strHead_lineNum_conf.get(31), DEFAULT_IP_PLC)
                        elif len(ip_addr_plc) > 4: 
                            replace_string_nat(ip_addr_plc)
                            replace_string_conf_v1(strHead_lineNum_conf.get(31), ip_addr_plc)
                    else:
                        replace_string_nat('')
                        replace_string_conf_v1(strHead_lineNum_conf.get(20), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(21), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(24), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(29), '0')
                        replace_string_conf_v1(strHead_lineNum_conf.get(30), '')
                        replace_string_conf_v1(strHead_lineNum_conf.get(31), '')
                    cprint('\n\t\t\t**ETH1 BRIDGED with ETH2**', color_successful)
                print('\n')      

                print(indent+'SET OPENVPN:')
                cprint(indent+'**without OPENVPN press Enter**', color_attention_msg)
                print(indent+'GSM connection (mobile wan)  - con. GSM with Elesys server (TSC)          [1]')
                print(indent+'Public Sit (openvpn)         - con. Public Sit with Elesys server         [2]')
                print(indent+'Public Sit (openvpn) + GSM   - con. Public Sit and GSM with Elesys server [3]')
                print(indent+'SHV open VPN                 - con. SHV open VPN server                   [4]')
                print(indent+'Without OPENVPN              - without openvpn connection                 []')
                conn_openvpn = input(indent+'Choose mode and enter: ')
                if len(conn_openvpn) > 0:
                    if conn_openvpn == '1':
                        print(indent+'SET Mobile WAN:')
                        cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                        gsm_en = control_answear(indent+'Mobile WAN Enabled [Y/n]: ')
                        if gsm_en == 'y' or len(gsm_en) == 0:
                            replace_string_conf_v1(strHead_lineNum_conf.get(27), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(32), '1')
                            replace_string_conf_v1(strHead_lineNum_conf.get(33), 'op.elektroline')
                            replace_string_conf_v1(strHead_lineNum_conf.get(34), 'tsc03')
                            replace_string_conf_v1(strHead_lineNum_conf.get(35), 'tsc03')
                            replace_string_conf_v1(strHead_lineNum_conf.get(36), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(37), '0')
                            replace_string_conf_v1(strHead_lineNum_conf.get(38), '')
                            replace_string_conf_v1(strHead_lineNum_conf.get(39), '0')
                            print(indent+'SET Mobile WAN.............................................................OK')
                    if conn_openvpn == '2':
                        print(('\n')+indent+'SET OPENVPN:')
                        cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                        openvpn_en = control_answear(indent+'OPENVPN Enabled [Y/n]: ')
                        if openvpn_en == 'y' or len(openvpn_en) == 0:
                            port_openvpn = input(indent+'OPENVPN port: ')
                            replace_string_conf_v1(strHead_lineNum_conf.get(27), '1')
                            replace_string_conf_v1(strHead_lineNum_conf.get(28), port_openvpn)
                            replace_string_conf_v1(strHead_lineNum_conf.get(32), '0')
                            print(('\n')+indent+'SET OPENVPN1_ELESYS:')
                            elesys_id = input(indent+'Enter elesysID: ').upper()
                            openvpn_file(elesys_id)
                            copy_openvpn_files()

                    if conn_openvpn == '3':
                        print(indent+'SET OPENVPN:')
                        cprint(indent+'**upper case in [] is default setting press Enter**', color_attention_msg)
                        openvpn_en = control_answear(indent+'OPENVPN Enabled [Y/n]: ')
                        if openvpn_en == 'y' or len(openvpn_en) == 0:
                            port_openvpn = input(indent+'OPENVPN port: ')
                            replace_string_conf_v1(strHead_lineNum_conf.get(27), '1')
                            replace_string_conf_v1(strHead_lineNum_conf.get(28), port_openvpn)
                            replace_string_conf_v1(strHead_lineNum_conf.get(32), '1')
                            print(indent+'SET OPENVPN1_ELESYS:')
                            elesys_id = input(indent+'Enter elesysID: ').upper()
                            openvpn_file(elesys_id)
                            copy_openvpn_files()
                    
                    if conn_openvpn == '4':
                        info_data_from_conf = parser()
                        replace_string_conf_v1(strHead_lineNum_conf.get(27), '1')
                        replace_string_conf_v1(strHead_lineNum_conf.get(40), 'udp')
                        replace_string_conf_v1(strHead_lineNum_conf.get(28), '1194')
                        replace_string_conf_v1(strHead_lineNum_conf.get(41), 'shv.elektroline.cz')
                        replace_string_conf_v1(strHead_lineNum_conf.get(42), 'lzo')
                        replace_string_conf_v1(strHead_lineNum_conf.get(43), info_data_from_conf['ca'])
                        replace_string_conf_v1(strHead_lineNum_conf.get(44), info_data_from_conf['cert'])
                        replace_string_conf_v1(strHead_lineNum_conf.get(45), info_data_from_conf['key'])
                        replace_string_conf_v1(strHead_lineNum_conf.get(46), '"--tls-client --tls-auth /etc/openvpn1_tls.cert --tls-timeout 3600 --pull --key-direction 1 --verb 3"')
                        copy_openvpn_files(shv=True)

                backup_conf_from_router()
                time.sleep(5)
                user_modules_smartflex(set_auto=True)
                time.sleep(5)
                copy_update_config()
                time.sleep(5)
                reboot_router()

            except (IOError, OSError):
                print(indent+'[ERROR] System or I/O Error, Try again')
                time.sleep(2)
                exit()

        elif user_ans_conf == 'np':
            extend_nat_port_forwarding()

        elif user_ans_conf == 'um':
            user_modules_smartflex()

        elif user_ans_conf == 'up':
            status_update = update_firmware()
            if status_update == True:
                reboot_router(True)
            else:
                time.sleep(1)
                exit()

        elif user_ans_conf == 'bc':
            backup_conf_from_router()

        elif user_ans_conf == 're':
            reboot_router()

        elif user_ans_conf == 'ni':
            network_info()

        else:
            print("\n\t [INFO] Not option was selected or Choose 'exit' or Invalid input. Exit script!\n")
            try:
                client_connection.close()
                os.remove(local_path_str('conf_tmp.cfg'))
                os.remove(local_path_str('openvpn1_down'))
                os.remove(local_path_str('openvpn1_up'))
                os.remove(local_path_str('openvpn1_elesys'))
                os.remove(local_path_str('openvpn1_tls.cert'))
            except FileNotFoundError: pass
            input('\t\t\t**for exit script press Enter. Have a nice day**')
            exit()

        cprint('\n\t\t\t\t  Configuration was successful'.upper(), 'green')
        client_connection.close()
        try:
            os.remove(local_path_str('conf_tmp.cfg'))
            os.remove(local_path_str('conf_nat_port_forward.cfg'))
        except FileNotFoundError: pass
        input('\t\t\t**for exit script press Enter. Have a nice day**')
    except KeyboardInterrupt:
        return


def network_info():
    print('\t---------------------------------------------------------------------------------')
    print('\t|                              Info Network status                              |')
    print('\t---------------------------------------------------------------------------------\n')
    net_info = command_user_ssh(command=command_info_net, flag_data=True)
    print(net_info)

def copy_update_config():
    print('\t---------------------------------------------------------------------------------')
    print('\t|                    Transfer and Update config file to router                  |')
    print('\t---------------------------------------------------------------------------------\n')
    try:
        client_connection_sftp.put(local_path_str('conf_tmp.cfg'), remotepath_config)
        print(indent+'Transfer config file to router...............................................OK')
        time.sleep(1)
        status_exit = command_user_ssh(command_restore)
        print(indent+'Update configuration.........................................................OK')
    except (IOError, OSError):
        print(indent+'[ERROR] Does not transfered config file! Fatal Error. Try again')
        time.sleep(2)
        exit()

def backup_conf_from_router():
    print('\t---------------------------------------------------------------------------------')
    print('\t|                                  Backup config                                |')
    print('\t---------------------------------------------------------------------------------\n')
    try:
        tmp_loc_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop').replace('\\', '/')
        command_user_ssh(command_backup)
        print(indent+'Backup Configuration successfully............................................OK')
        print(indent+"Backup Configuration is your Desktop: ".upper()+colored(tmp_loc_path+"/from_conf.cfg", 'green'))
        client_connection_sftp.get(remotepath_backup, tmp_loc_path+'/from_conf.cfg')
    except (IOError, OSError):
        print('\n\tDoes not transfered config file! Fatal Error. Try again')
        time.sleep(2)
        exit()

def reboot_router(hide_head=False):
    if hide_head is False:
        print('\t---------------------------------------------------------------------------------')
        print('\t|                                  Reboot router                                |')
        print('\t---------------------------------------------------------------------------------\n')
    try:
        command_user_ssh(command_reboot)
        print(indent+'Reboot router................................................................OK')
    except (IOError, OSError):
        print('\n\tError. Try again')
        time.sleep(2)
        exit()

def copy_openvpn_files(shv=False):
    print('\t---------------------------------------------------------------------------------')
    print('\t|                         Copy openvpn1 files to router                         |')
    print('\t---------------------------------------------------------------------------------\n')
    if shv:
        try:
            client_connection_sftp.put(local_path_str('openvpn1_tls.cert'), remotepath_openvpn1_tls)
            print(indent+'Copy config file to router...................................................OK')
            time.sleep(2)
            command_user_ssh(command=command_permission, rem_path=remotepath_openvpn1_tls, flag_data=True)
            time.sleep(2)
            os.remove(local_path_str('openvpn1_tls.cert'))
        except (IOError, OSError):
            print('\n\tDoes not transfered openvpn files! Fatal Error. Try again')
            time.sleep(2)
            exit()
    else:
        try:
            client_connection_sftp.put(local_path_str('openvpn1_down'), remotepath_openvpn1_down)
            print(indent+'Copy config file to router...................................................OK')
            client_connection_sftp.put(local_path_str('openvpn1_up'), remotepath_openvpn1_up)
            print(indent+'Copy config file to router...................................................OK')
            client_connection_sftp.put(local_path_str('openvpn1_elesys'), remotepath_openvpn1_elesys)
            print(indent+'Copy config file to router...................................................OK')
            time.sleep(2)
            command_user_ssh(command=command_private, rem_path=remotepath_openvpn1_down, flag_data=True)
            time.sleep(2)
            command_user_ssh(command=command_private, rem_path=remotepath_openvpn1_up, flag_data=True)
            time.sleep(2)
            os.remove(local_path_str('openvpn1_down'))
            os.remove(local_path_str('openvpn1_up'))
            os.remove(local_path_str('openvpn1_elesys'))
        except (IOError, OSError):
            print('\n\tDoes not transfered openvpn files! Fatal Error. Try again')
            time.sleep(2)
            exit()

def user_modules_smartflex(set_auto=False):
    print('\t---------------------------------------------------------------------------------')
    print('\t|                              Install user modules                             |')
    print('\t---------------------------------------------------------------------------------\n')
    if set_auto == True:
        try:
            client_connection_sftp.put(local_path_str('smartflex_modules/nmap.tgz'), remotepath_user_modules[0])
            command_user_ssh(command_user_module[0])
            print(indent+'Installed NMAP modul.........................................................OK')
            time.sleep(2)
            client_connection_sftp.put(local_path_str('smartflex_modules/webterm.tgz'), remotepath_user_modules[1])
            command_user_ssh(command_user_module[1])
            print(indent+'Installed WEBTERM modul......................................................OK')
        except (FileNotFoundError, TypeError):
            print(indent+'[ERROR] Check for files in the directory(nmap.tgz, webterm.tgz etc)\n')
            return False

    else:
        list_user_mod = name_modules()
        try:
            id_name_modul = int(input(indent+'Choose user modules: '))
            if id_name_modul <= 10:
                client_connection_sftp.put((local_path_str(list_user_mod[id_name_modul-1])), (remotepath_tmp+list_user_mod[id_name_modul-1].split('/')[1]))
                command_user_ssh((command_user_module[2]+list_user_mod[id_name_modul-1].split('/')[1]))
                print(indent+'Installed'+' '+ str(list_user_mod[id_name_modul-1].split('/')[1]).upper() +' '+'modul......................................................OK')
            elif id_name_modul == 12:
                client_connection_sftp.put(local_path_str('smartflex_modules/nmap.tgz'), remotepath_user_modules[0])
                command_user_ssh(command_user_module[0])
                print(indent+'Installed NMAP modul..........................................................OK')
                time.sleep(1)
                client_connection_sftp.put(local_path_str('smartflex_modules/webterm.tgz'), remotepath_user_modules[1])
                command_user_ssh(command_user_module[1])
                print(indent+'Installed WEBTERM modul.......................................................OK')
        except (FileNotFoundError, TypeError, ValueError):
            print('\n\t[ERROR] Check for files in the directory or Invalid value\n')
            exit()

def update_firmware():
    print('\t---------------------------------------------------------------------------------')
    print('\t|                                 Update Firmware                               |')
    print('\t---------------------------------------------------------------------------------')
    list_name_fw = name_fw()
    try:
        id_name_fw = input('\n'+indent+'Choose firmware and enter number of index: ')
        client_connection_sftp.put(local_path_str(list_name_fw[int(id_name_fw)-1]), remotepath_fwupdate)
        print(indent+'Updating Firmware wait please....................................................')
        print(command_user_ssh(command=command_fwupdate, flag_data=True))
        return True
    except (FileNotFoundError, TypeError, ValueError, NameError):
        print("\n\t [ERROR] Does not exist binary file in the local directory, 'exit' script!\n")
        exit()

def extend_nat_port_forwarding():
    print('\t---------------------------------------------------------------------------------')
    print('\t|                                 Extend NAT Port                               |')
    print('\t---------------------------------------------------------------------------------\n')
    print('\t\tAppend new port  - append new nat port forwarding [a]')
    print('\t\tRemove port      - delete nat port forwarding     [d]\n')
    mode = input(indent+'Choose options and enter: ').lower()
    if mode in 'ad' and len(mode) > 0:
        create_conf_port_forwarding()
        private_port = input(indent+"Enter [PRIVATE PORT]: ")
        public_port = input(indent+"Enter [PUBLIC PORT]: ")
        ip_addr_plc = input(indent+"Enter IP Address: ")
        mode = "-A" if mode == 'a' else "-D"
        command_set_nat_port = f"iptables -t nat {mode} pre_nat -p tcp --dport {public_port} -j DNAT --to-destination {ip_addr_plc}:{private_port}"
        # set_port_forwarding = command_user_ssh(command=command_set_nat_port)
    else:
        print("\n\t[ERROR] Invalid value, 'exit' script!\n")
        time.sleep(2)
        exit()


if __name__ == "__main__":
    main()