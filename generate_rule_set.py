import maxminddb
import json
import os  # 新增，用于创建目录

all_ip = { 'UNKNOWN': [] }

with maxminddb.open_database('./Merged-IP.mmdb') as reader:
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

# 确保输出目录存在
os.makedirs("ruleJson", exist_ok=True)
os.makedirs("ipsetNft", exist_ok=True)

for key, value in all_ip.items():
    # 写入 JSON 规则文件
    filename = f"ruleJson/geoip_{key}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        content = {"version": 4, "rules": [{ 'ip_cidr': value }]}
        json.dump(content, f, indent=2)

    if key == 'CN':
        ipv4_cidrs = []
        ipv6_cidrs = []
        for cidr in value:
            if ':' in cidr:
                ipv6_cidrs.append(cidr)
            else:
                ipv4_cidrs.append(cidr)
        
        # 写入 IPv4 文件
        if ipv4_cidrs:
            nft_v4_filename = "ipsetNft/geoipv4_CN.nft"
            cidr_v4_str = ", ".join(ipv4_cidrs)
            nft_v4_content = f"define cncidrs_ipv4 = {{ {cidr_v4_str} }}"
            with open(nft_v4_filename, 'w', encoding='utf-8') as nft_f:
                nft_f.write(nft_v4_content)
            print(f"nftables IPv4 rule file generated: {nft_v4_filename}")
        
        # 写入 IPv6 文件
        if ipv6_cidrs:
            nft_v6_filename = "ipsetNft/geoipv6_CN.nft"
            cidr_v6_str = ", ".join(ipv6_cidrs)
            nft_v6_content = f"define cncidrs_ipv6 = {{ {cidr_v6_str} }}"
            with open(nft_v6_filename, 'w', encoding='utf-8') as nft_f:
                nft_f.write(nft_v6_content)
            print(f"nftables IPv6 rule file generated: {nft_v6_filename}")
