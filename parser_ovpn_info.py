from bs4 import BeautifulSoup
import base64

def parser():
    path_ovpn_file = input("enter path where is ovpn file: ")
    TAGS_BETWEEN_EXTRACT_DATA = ["ca", "cert", "key", "tls-auth"]

    with open(path_ovpn_file, 'r') as f:  file_in_memory = f.read()

    info_data_from_file = dict()
    openvpn_file_shv = ""
    soup = BeautifulSoup(file_in_memory, "html.parser")
    for idx, attr in enumerate(TAGS_BETWEEN_EXTRACT_DATA):
        for key in soup.find_all(attr):
            key_tmp = key.string
            if idx == 3:
                openvpn_file_shv = str(key_tmp).strip('\n')
            else:
                info_data_from_file[attr] = str(key_tmp).strip('\n')
    
    # create opevvpn1_tls.cert file
    with open ('openvpn1_tls.cert', 'w') as f:
        f.writelines(openvpn_file_shv)
    
    # cutting cert certificate
    tmp_str = str(info_data_from_file['cert'])
    tmp_str = tmp_str[tmp_str.find('-----BEGIN CERTIFICATE-----'):]
    info_data_from_file['cert'] = tmp_str

    # encoding each certificate on the base64
    for key in TAGS_BETWEEN_EXTRACT_DATA[0:3]:
        str_bytes = str(info_data_from_file[key]).encode("ascii")
        base64_bytes = base64.b64encode(str_bytes)
        base64_str = base64_bytes.decode("ascii")
        info_data_from_file[key] = base64_str
    
    # print(info_data_from_file)
    return info_data_from_file
    