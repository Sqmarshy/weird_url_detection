import re
from urllib.parse import urlparse
import tldextract
import requests

def feature_extraction(url):
    res = {}
    parsed_url = urlparse(url)
    domain_info = tldextract.extract(url)

    res['is_https'] = int(parsed_url.scheme == 'https')
    res['num_subdomains'] = len(domain_info.subdomain.split('.')) if domain_info.subdomain else 0
    res['num_digits'] = sum(c.isdigit() for c in url)
    res['num_special_chars'] = len(re.findall(r'[^\w\s]', url))
    res['num_obfuscated_chars'] = len(re.findall(r'%[0-9A-Fa-f]{2}', url))

    alpha_sequence = re.findall(r'[a-zA-Z]+', url)
    digit_sequence = re.findall(r'\d+', url)
    special_char_sequence = re.findall(r'[^\w\s]', url)
    total_sequence_len = sum(len(seq) for seq in (alpha_sequence + digit_sequence + special_char_sequence))
    res['char_continuation_rate'] = total_sequence_len / len(url) if len(url) > 0 else 0
    
    res['num_query_params'] = len(parsed_url.query.split('&')) if parsed_url.query else 0

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            html_content = response.text
            res['has_favicon'] = int('<link rel="icon"' in html_content or '<link rel="shortcut icon"' in html_content)
        else:
            res['has_favicon'] = 0
    except:
        res['has_favicon'] = 0
    return res

# Example Usage
url = "https://example.com/path?query=1"
features = feature_extraction(url)
print(features)