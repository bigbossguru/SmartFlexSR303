import paramiko
import pathlib
import glob
import termcolor

# Const variables for makes config file
DHCP = 'dhcp'
STATIC = 'static'
DEFAULT_IP_PLC = '192.168.1.10'
DEFAULT_IP = ('192.168.2.1', '192.168.1.1', '10.0.0.1')
DEFAULT_NETWORK = ('192.168.2.0', '192.168.1.0', '10.0.0.0')
DEFAULT_NETMASK = '255.255.255.0'
DHCP_POOL_LO_HI_eth0 = ('10.0.0.100', '10.0.0.200')
DHCP_POOL_LO_HI_eth2 = ('192.168.1.100', '192.168.1.200')
DHCP_POOL_LO_HI_eth1 = ('192.168.2.100', '192.168.2.200')

# List remote path 
remotepath_tmp              = '/var/tmp/'
remotepath_config           = '/var/tmp/conf.cfg'
remotepath_openvpn1         = '/etc/init.d/openvpn1'
remotepath_openvpn1_elesys  = '/etc/openvpn1_elesys'
remotepath_openvpn1_up      = '/etc/openvpn1_up'
remotepath_openvpn1_down    = '/etc/openvpn1_down'
remotepath_openvpn1_tls     = '/etc/openvpn1_tls.cert'
remotepath_fwupdate         = '/var/tmp/SPECTRE-v3-LTE.bin'
remotepath_user_modules     = ('/var/tmp/nmap.tgz', '/var/tmp/webterm.tgz')
remotepath_backup           = '/var/tmp/from_conf.cfg'

# List for Bash commands
command_info_net    = 'ifconfig -a'
command_info        = 'status -h sys'
command_listing     = 'ls /var/tmp'
command_restore     = 'restore /var/tmp/conf.cfg'
command_reboot      = 'reboot -d 2'
encodes             = 'iso8859-1'
command_user_module = ('umupdate -a /var/tmp/nmap.tgz', 'umupdate -a /var/tmp/webterm.tgz', 'umupdate -a /var/tmp/')
command_private     = 'chmod +x'
command_permission  = 'chmod go-r'
command_backup      = 'backup -a > /tmp/from_conf.cfg'
command_fwupdate    = 'fwupdate -i /var/tmp/SPECTRE-v3-LTE.bin -n'

extra_option = "--tls-client --tls-auth /etc/openvpn1_tls.cert --tls-timeout 3600 --pull --key-direction 1 --verb 3"

# Connection SSH protocol
client_connection = paramiko.SSHClient()
client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def connection_user_ssh():
    stat_connection = None
    try:
        while True:
            try:
                ip_addr = input('\t\tEnter Router IP Address [192.168.1.1]: ')  # 192.168.1.1
                port = input('\t\tEnter auth port [22]: ')                      # 22
                username = input('\t\tEnter auth username [root]: ')            # 'root'
                passwd = input('\t\tEnter auth password [root]: ')              # 'root'

                if len(ip_addr) <= 4:   ip_addr = DEFAULT_IP[1]
                if len(port) <= 0:      port = '22'
                if len(username) <= 0:  username = 'root'
                if len(passwd) <= 0:    passwd = 'root'

                stat_connection = client_connection.connect(hostname=ip_addr, port=int(port), username=username, password=passwd)

                if stat_connection is None: 
                    termcolor.cprint('\n\t\t\t\t\tConnection Successful\n'.upper(), 'green')
                    client_connection_sftp = client_connection.open_sftp()
                    break
            except (ValueError, paramiko.AuthenticationException, UnboundLocalError, Exception, TypeError):
                print('\n\t[ERROR] Invalid value or Authentication failed (check input is correct). Try again\n')
                continue
            except TimeoutError:
                print('\n\t[ERROR] Timeout Error (check connections with smartFlex). Try again\n')
                continue
            except KeyboardInterrupt: return
        return stat_connection, client_connection_sftp
    except UnboundLocalError:
        return

# Send command 
def command_user_ssh(command, rem_path='', flag_data=False):
    stdin, stdout, stderr = client_connection.exec_command(command)
    if len(rem_path) > 3:
        stdin, stdout, stderr = client_connection.exec_command(command+' '+rem_path)
    if flag_data == True:
        data = stdout.read().decode(encodes)
        return data

#Control answear    
def control_answear(ask_msg, mode='y/n', ip=None):
    while True:
        conf_ans = input(ask_msg).lower()
        if (mode == 'y/n') and (conf_ans == 'y' or conf_ans == 'n' or len(conf_ans) == 0):
            return conf_ans
            break
        elif (mode == 'd') and (conf_ans == 'd' or len(conf_ans) == 0) and ip:
            return ip
            break
        elif (len(conf_ans) >= 6) and (conf_ans.count('.') == 3):
            return conf_ans
            break
        else:
            print((' '*9)+'[ERROR] Invalid value, Try again\n')

# Create Local Address
def local_path_str(name_file=''):
    if len(name_file) > 5:
        local_path = str(pathlib.Path.cwd()).replace('\\', '/') + '/' + name_file
        return local_path
    else:
        local_path = str(pathlib.Path.cwd()).replace('\\', '/')
        return local_path 

# Create openvpn files
def openvpn_file(id_elesys='not exist'):
    data_down = ['#!/bin/sh\n', '\n', 'led off\n']
    data_up = ['#!/bin/sh\n', '\n', 'led on\n']
    data_elesys = [id_elesys+'\n', 'elesys\n']
    with open('openvpn1_down', "w", newline='\n') as down:
        down.writelines(data_down)
    with open('openvpn1_up', "w", newline='\n') as up:
        up.writelines(data_up)
    with open('openvpn1_elesys', "w", newline='\n') as elesys:
        elesys.writelines(data_elesys)

# SET IP address ETH
def replace_string_conf (input_user, head_line, index_line):
    config = open(local_path_str('conf_tmp.cfg')).read().splitlines()
    config[index_line] = head_line+input_user
    open(local_path_str('conf_tmp.cfg'), 'w', newline='\n').write('\n'.join(config))

def replace_string_conf_v1(header_info, input_user=''):
    config = open(local_path_str('conf_tmp.cfg')).read().splitlines()
    config[header_info[1]] = header_info[0]+input_user
    open(local_path_str('conf_tmp.cfg'), 'w', newline='\n').write('\n'.join(config))

# Set NAT Of The Network
def replace_string_nat (input_user):
    conf = open(local_path_str('conf_tmp.cfg')).read().splitlines()
    j=1
    for i in range(641, 682, 4): #start number line and end number line in config file with step 4
        conf[i]=('NAT_PORT%d_IPADDR=' %j)+input_user
        j += 1
    open(local_path_str('conf_tmp.cfg'), 'w', newline='\n').write('\n'.join(conf))

# List names FW
def name_fw():
    j = 1
    names_fw = []
    for i in glob.glob('firmware\\*.bin'):
        names_fw.append(i.replace('\\', '/')) 
        print('\t\t\t\t'+'   ['+str(j)+'] -> '+' '+i.split("\\")[1])
        j += 1
    return names_fw

# List names user modules
def name_modules():
    j = 1
    names_modul = []
    for i in glob.glob('smartflex_modules\\*.tgz'): 
        names_modul.append(i.replace('\\', '/'))
        print('\t\t\t\t'+'   ['+str(j)+'] -> '+' '+i.split("\\")[1])
        j += 1
    return names_modul

def create_conf_cfg():
    with open('config\\orig_conf.cfg', "r") as conf:
        config = conf.readlines()
        with open('conf_tmp.cfg', "w", newline='\n') as copy_config:
            copy_config.writelines(config)

def create_conf_port_forwarding():
    with open('config\\nat_port_forward.cfg', 'r') as conf:
        config = conf.readlines()
        with open('conf_nat_port_forward.cfg', 'w') as copy_config:
            copy_config.writelines(config)
            status = conf.writable()
    return status

strHead_lineNum_conf = {
    0: ['ETH_BOOTPROTO=', 1],
    1: ['ETH_IPADDR=', 2],
    2: ['ETH_NETMASK=', 3],
    3: ['ETH_NETWORK=', 4],
    4: ['ETH_BRIDGED=', 5],
    5: ['ETH_DHCP_POOL_ENABLED=', 10],
    6: ['ETH_DHCP_POOL_LO=', 11],
    7: ['ETH_DHCP_POOL_HI=', 12],
    8: ['ETH2_BOOTPROTO=', 52],
    9: ['ETH2_IPADDR=', 53],
    10: ['ETH2_NETMASK=', 54],
    11: ['ETH2_NETWORK=', 55],
    12: ['ETH2_BRIDGED=', 56],
    13: ['ETH2_DHCP_POOL_ENABLED=', 61],
    14: ['ETH2_DHCP_POOL_LO=', 62],
    15: ['ETH2_DHCP_POOL_HI=', 63],
    16: ['ETH3_BOOTPROTO=', 103],
    17: ['ETH3_IPADDR=', 104],
    18: ['ETH3_NETMASK=', 105],
    19: ['ETH3_NETWORK=', 106],
    20: ['ETH3_BRIDGED=', 107],
    21: ['ETH3_DHCP_POOL_ENABLED=', 111],
    22: ['ETH3_DHCP_POOL_LO=', 112],
    23: ['ETH3_DHCP_POOL_HI=', 113],
    24: ['ETH3_DHCP_STAT_ENABLED=', 114],
    25: ['ETH3_DHCP_STAT_MAC1=', 115],
    26: ['ETH3_DHCP_STAT_IPADDR1=', 116],
    27: ['OPENVPN_ENABLED=', 781],
    28: ['OPENVPN_PORT=', 784],
    29: ['ETH2_DHCP_STAT_ENABLED=', 64],
    30: ['ETH2_DHCP_STAT_MAC1=', 65],
    31: ['ETH2_DHCP_STAT_IPADDR1=', 66],
    32: ['PPP_ENABLED=', 163],
    33: ['PPP_APN=', 164],
    34: ['PPP_USERNAME=', 165],
    35: ['PPP_PASSWORD=', 166],
    36: ['PPP_PING=', 178],
    37: ['PPP_PING_BIND=', 179],
    38: ['PPP_PING_IPADDR=', 180],
    39: ['PPP_PING_SINTVL=', 182],
    40: ['OPENVPN_PROTO=', 783],
    41: ['OPENVPN_REMOTE_IPADDR=', 785],
    42: ['OPENVPN_COMP=', 799],
    43: ['OPENVPN_CA_CERT=', 803],
    44: ['OPENVPN_LOCAL_CERT=', 805],
    45: ['OPENVPN_LOCAL_KEY=', 806],
    46: ['OPENVPN_EXTRA_OPTS=', 809]
}