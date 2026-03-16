import maxminddb
import json

all_ip = { 'UNKNOWN': [] }

with maxminddb.open_database('.\\Merged-IP.mmdb') as reader:
    for network, data in reader:
        ipstr = str(network)
        if 'country' in data:
            country_code = data['country']['iso_code']
            if not (country_code in all_ip):
                all_ip[country_code] = []
            all_ip[country_code].append(ipstr)
        else:
            all_ip['UNKNOWN'].append(ipstr)
            print('not found country: ' + ipstr)

print('Start write to file...')

for key, value in all_ip.items():
    filename = f"ruleJson/geoip_{key}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        content = {"version": 4, "rules": value}
        json.dump(content, f, indent=2)
