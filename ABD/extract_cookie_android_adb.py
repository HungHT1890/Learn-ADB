"""
import re
rawText = re.sub(r'[^\x20-\x7E]', '|', rawText)
Trong đó, `re.sub()` dùng để thay thế tất cả các chuỗi phù hợp với mẫu regex bằng chuỗi thay thế. Mẫu regex `[^\x20-\x7E]` 
sẽ tìm kiếm bất kỳ ký tự nào không nằm trong khoảng từ 0x20 đến 0x7E (khoảng này bao gồm tất cả các ký tự ASCII in được). Khi tìm thấy, nó sẽ thay thế bằng ký tự `|`.
"""

from re import findall , sub
from os import system 
from subprocess import check_output

CREATE_NO_WINDOW = 0x08000000

def get_devices():
    list_devices = []
    devices_checkout = str(check_output('adb devices' , creationflags = CREATE_NO_WINDOW , shell = True)).replace("b'List of devices attached",'').replace("'",'').split(r'\r\n')
    for device in devices_checkout:
        if device != '':
            list_devices.append(device.split('\\tdevice')[0])
    return list_devices


def get_cookie_android(device):
    print(f'Get cookie: {device}')
    auth = str(check_output(f"adb -s {device} pull /data/data/com.facebook.katana/app_light_prefs/com.facebook.katana/authentication auth.txt"))
    with open('auth.txt','r',encoding='utf-8', errors = 'ignore') as f:
        auth_file = f.read()
        auth_full = (sub(r'[^\x20-\x7E]','|',auth_file))
    try:
        system('del auth.txt')
    except Exception as f:
        pass
    if 'EAAAAU' in auth_full:
        regex_token = r'EAAAAU(.*?)username'
        token = 'EAAAAU' + findall(regex_token,auth_full)[0].strip().replace('|','')
        cookie_full = auth_full.split('n[')[1].split(']')[0]
        regex_cookie = r'{"name":"(.*?)","expires":"'
        find_cookie_str = findall(regex_cookie,cookie_full)
        cookie_data_list = []
        for cookie_value in find_cookie_str:
            name = cookie_value.split('","value":"')[0].strip()
            value =  cookie_value.split('","value":"')[1].strip()
            cookie_data_list.append(name + '=' + value)
        cookie = '; '.join(cookie_data_list)
        full_data_extracted = f'{cookie}|{token}'
        print(full_data_extracted)
        with open('cookie_token.txt','a',encoding='utf-8') as save_output_cookie_token:
            save_output_cookie_token.write(full_data_extracted + '\n')

if __name__ == '__main__':
    list_devices = get_devices()
    print(list_devices)
    for device in list_devices:
        try:
            get_cookie_android(device)
        except:
            pass
