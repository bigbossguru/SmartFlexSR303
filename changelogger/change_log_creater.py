import re
import os
key = input("enter keywords, which you want to delete\n".upper()+"example=['poz','hel','ams','ghe','havAB', 'ell', 'elesys','safety', ...]: ")
key = key.split() + ['merge','revert']
'''('poz','hel','ams','ghe','havAB', 'ell', 'merge','revert','elesys','safety')'''
with open('CHANGELOG_orig.md', encoding='utf-8', mode='r') as f:
    lines = f.readlines()
with open('CHANGELOG.md', encoding='utf-8', mode='w') as f:
    for line in lines:
        tmp = ''
        num_issues = [re.search(r'#\d{1,6}\s', line), re.search(r'#\d{1,6}\:\s', line)]
        try:
            tmp = num_issues[0].group(0) 
        except:
            pass

        try:
            tmp = num_issues[1].group(0) 
        except:
            pass

        flag_esc = False
        for esc in key:
            if esc in line.lower(): flag_esc=True
        if flag_esc: continue
        if "Signed" in line:
            continue
        else:
            line2 = line.replace(tmp, '')
            line2 = line2.replace('  ', ' ')
            f.write(line2)

with open('CHANGELOG.md', encoding='utf-8', mode='r') as f:
    lines = f.readlines()
with open('CHANGELOG.md', encoding='utf-8', mode='w') as f:
    f.write('# Changelog\n\n')
    for line in lines:
        idx = (line.rfind('-'))
        tmp_line = line[:idx]+'\n'+line[idx:]
        f.write(tmp_line)

os.remove('CHANGELOG_orig.md')
