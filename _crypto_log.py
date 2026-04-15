import os

# Clean up temp files
tmp = [r'D:\0_workspace\trae_2601\ymos\YMOS\_crypto_out.txt',
       r'D:\0_workspace\trae_2601\ymos\YMOS\_crypto_err.txt',
       r'D:\0_workspace\trae_2601\ymos\YMOS\_crypto_report.txt']
for f in tmp:
    if os.path.exists(f):
        os.remove(f)
        print('Removed:', os.path.basename(f))

# Update daily memory
mem_path = r'D:\0_workspace\trae_2601\ymos\YMOS\memory\2026-04-15.md'
with open(mem_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

new_section = '''
## 16:00 CST 加密监控报告（2026-04-15）
- 报告路径：`Eyes/监控数据/2026-04/crypto_monitor_20260415_1614.md`
- BTC $73,818（-1.01%）✅ 无异常波动（<5%）
- ETH $2,318（-2.52%）✅ 无异常波动（<5%）
- Fear & Greed：23（极度恐惧）
- 稳定币市值：$308.2B（CoinGecko）/ $318.2B（DeFiLlama）
- Funding Rate：BTC -0.0042%（中性），ETH +0.0013%（中性）
'''

if '16:00 CST' not in content:
    content += new_section

with open(mem_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Daily memory updated')
