with open('index.html', 'r') as f:
    c = f.read()

import re

print('=== 1. How many showDetail functions exist? ===')
print('showDetail definitions:', c.count('function showDetail'))
print('openDetailNow definitions:', c.count('function openDetailNow'))
print()

print('=== 2. What do the onclick attributes look like? ===')
patterns = re.findall(r'onclick="[^"]*showDetail[^"]*"', c)
for p in set(patterns):
    print(repr(p))
print()

print('=== 3. Show the current showDetail function ===')
m = re.search(r'function showDetail[\s\S]*?(?=\n\s*function |\n\s*const el|\n\s*el\()', c)
if m:
    print(m.group(0)[:800])
else:
    print('NOT FOUND')
print()

print('=== 4. Show the renderWeather first 20 lines ===')
m = re.search(r'function renderWeather\(\)[\s\S]{0,500}', c)
if m:
    print(m.group(0)[:500])
