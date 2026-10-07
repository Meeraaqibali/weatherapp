import re

with open('index.html', 'r') as f:
    c = f.read()

new_fn = '''async function geocode(city) {
    const countryMap = {
      'pakistan': 'PK', 'india': 'IN', 'bangladesh': 'BD', 'usa': 'US',
      'united states': 'US', 'uk': 'GB', 'england': 'GB', 'america': 'US',
      'china': 'CN', 'uae': 'AE', 'dubai': 'AE', 'saudi': 'SA',
      'saudi arabia': 'SA', 'iran': 'IR', 'afghanistan': 'AF',
      'turkey': 'TR', 'canada': 'CA', 'australia': 'AU', 'germany': 'DE',
      'france': 'FR', 'japan': 'JP', 'indonesia': 'ID', 'malaysia': 'MY'
    };
    
    const query = city.trim();
    const lowerQuery = query.toLowerCase();
    
    let countryHint = null;
    let adminHint = null;
    let cityName = query;
    
    for (let name in countryMap) {
      if (lowerQuery.endsWith(' ' + name)) {
        countryHint = countryMap[name];
        cityName = query.slice(0, -(name.length + 1)).trim();
        break;
      }
    }
    
    const adminHints = ['sindh', 'punjab', 'balochistan', 'kpk', 'khyber pakhtunkhwa',
                        'gilgit', 'baltistan', 'kashmir', 'ajk', 'islamabad',
                        'maharashtra', 'gujarat', 'rajasthan', 'delhi', 'karnataka'];
    for (let hint of adminHints) {
      if (lowerQuery.includes(hint)) {
        adminHint = hint;
        cityName = cityName.replace(new RegExp(hint, 'i'), '').trim();
        if (['sindh','punjab','balochistan','kpk','khyber pakhtunkhwa','gilgit','baltistan','kashmir','ajk'].includes(hint) && !countryHint) {
          countryHint = 'PK';
        }
        if (['maharashtra','gujarat','rajasthan','delhi','karnataka'].includes(hint) && !countryHint) {
          countryHint = 'IN';
        }
        break;
      }
    }
    
    if (!cityName) cityName = query;
    
    let attempts = [cityName, cityName.replace(/\\s+/g, ''), cityName.split(' ')[0]];
    let allResults = [];
    
    for (let attempt of attempts) {
      const url = 'https://geocoding-api.open-meteo.com/v1/search?name=' + encodeURIComponent(attempt) + '&count=10&language=en&format=json';
      try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.results && data.results.length > 0) {
          allResults = allResults.concat(data.results);
        }
      } catch (e) { }
    }
    
    if (allResults.length === 0) throw new Error('City not found. Try a different spelling.');
    
    const seen = new Set();
    allResults = allResults.filter(r => { if (seen.has(r.id)) return false; seen.add(r.id); return true; });
    
    if (countryHint) {
      const countryMatch = allResults.filter(r => r.country_code === countryHint);
      if (countryMatch.length > 0) allResults = countryMatch;
    }
    
    if (adminHint) {
      const adminMatch = allResults.filter(r => r.admin1 && r.admin1.toLowerCase().includes(adminHint));
      if (adminMatch.length > 0) allResults = adminMatch;
    }
    
    if (!countryHint && !adminHint) {
      const pkResult = allResults.find(r => r.country_code === 'PK');
      if (pkResult) return pkResult;
    }
    
    allResults.sort((a, b) => (b.population || 0) - (a.population || 0));
    return allResults[0];
  }'''

pattern = re.compile(r'async function geocode\(city\) \{.*?\n  \}', re.DOTALL)
c = pattern.sub(new_fn, c)

with open('index.html', 'w') as f:
    f.write(c)
print('DONE - Smart search applied')
