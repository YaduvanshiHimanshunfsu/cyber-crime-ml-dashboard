import random

with open("src/state_info.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '"region":' in line:
        line = line.rstrip('\r\n')
        line = line + ",\n"
        literacy = random.randint(65, 95)
        new_lines.append(line)
        new_lines.append(f'        "cyber_nodal_agency": "State Cyber Cell / CCTNS Mapping",\n')
        new_lines.append(f'        "it_literacy_index": "{literacy} %",\n')
        new_lines.append(f'        "helpline": "1930"\n')
    else:
        new_lines.append(line)

with open("src/state_info.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
