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
    
    # 新增：若国家代码为 CN，额外生成 nftables 集合文件
    if key == 'CN':
        nft_filename = "ipsetNft/geoip_CN.nft"
        # 将 CIDR 列表格式化为逗号分隔的字符串
        cidr_list_str = ", ".join(value)
        nft_content = f"define cncidrs = {{ {cidr_list_str} }}"
        with open(nft_filename, 'w', encoding='utf-8') as nft_f:
            nft_f.write(nft_content)
        print(f"nftables rule file generated: {nft_filename}")
