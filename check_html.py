with open('index.html', 'r') as f:
    c = f.read()

import re

print('=== Does extraGrid content exist? ===')
m = re.search(r"el\('extraGrid'\)\.innerHTML\s*=\s*`[\s\S]{0,400}", c)
if m:
    print(m.group(0)[:400])
else:
    print('NOT FOUND')
print()

print('=== First 3 onclick attributes in HTML ===')
for p in re.findall(r'onclick="[^"]+"', c)[:5]:
    print(repr(p))
print()

print('=== Is showDetail defined? ===')
print('function showDetail:', 'function showDetail' in c)
print('function openDetailNow:', 'function openDetailNow' in c)
print()

print('=== Are alerts still there? ===')
print('showDetail alert:', "alert('showDetail called" in c)
print('openDetailNow alert:', "alert('openDetailNow called" in c)
print()

print('=== Does the file have a syntax-breaking issue? ===')
# Try to find obvious problems
print('Broken <script> tags:', c.count('<script>'))
print('Broken </script> tags:', c.count('</script>'))
print()

print('=== File size ===')
print('Total characters:', len(c))
