import pandas as pd

df = pd.read_csv('dataset_phishing.csv', encoding = 'unicode_escape')

urls = df['url']
a,b,c,d = [], [], [], []
for url in urls:
    a.append(1 if any(c.isdigit() for c in url.split('/')[2]) else 0)
    b.append(1 if url.startswith('https://') else 0)
    c.append(url.count('http://') + url.count('https://') - 1)
    d.append(sum(c.isdigit() for c in url) / max(1, sum(c.isalpha() for c in url)))

df['contains_ip'] = a
df['has_https'] = b
df['nb_redirects'] = c
df['ratio_digits_to_letters'] = d

df.to_csv('dataset_phishing.csv')