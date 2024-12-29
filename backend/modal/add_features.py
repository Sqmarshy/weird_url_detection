import pandas as pd
import re
from urllib.parse import urlparse
import tldextract

df = pd.read_csv('modal\dataset_phishing.csv', encoding = 'unicode_escape')

urls = df['url']
a, b, c, d, e, f= [], [], [], [], [], []

for idx, url in enumerate(urls):
    parsed_url = urlparse(url)
    domain_info = tldextract.extract(url)
    a.append(int(parsed_url.scheme == 'https'))
    b.append(len(domain_info.subdomain.split('.')) if domain_info.subdomain else 0)
    c.append(sum(i.isdigit() for i in url))
    d.append(len(re.findall(r'[^\w\s]', url)))
    e.append(len(re.findall(r'%[0-9A-Fa-f]{2}', url)))

    alpha_sequence = re.findall(r'[a-zA-Z]+', url)
    digit_sequence = re.findall(r'\d+', url)
    special_char_sequence = re.findall(r'[^\w\s]', url)
    total_sequence_len = sum(len(seq) for seq in (alpha_sequence + digit_sequence + special_char_sequence))

    f.append(round(total_sequence_len / len(url) if len(url) > 0 else 0, 9))

df['is_https'] = a
df['num_subdomains'] = b
df['num_digits'] = c
df['num_special_chars'] = d
df['num_obfuscated_chars'] = e
df['char_continuation_rate'] = f

df.to_csv('dataset_phishing.csv')