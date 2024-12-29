import joblib
import torch
import pandas as pd
import re
from urllib.parse import urlparse
import tldextract

def feature_extraction(url):
    parsed_url = urlparse(url)
    domain_info = tldextract.extract(url)
    res = {}
    res['length_url'] = len(url)
    res['nb_dots'] = url.count('.')
    res['nb_hyphens'] = url.count('-')
    res['nb_at'] = url.count('@')
    res['nb_qm'] = url.count('?')
    res['nb_and'] = url.count('&')
    res['nb_eq'] = url.count('=')
    res['nb_underscore'] = url.count('_')
    res['nb_tilde'] = url.count('~')
    res['nb_percent'] = url.count('%')
    res['nb_slash'] = url.count('/')
    res['nb_star'] = url.count('*')
    res['nb_colon'] = url.count(':')
    res['nb_comma'] = url.count(',')
    res['nb_semicolumn'] = url.count(';')
    res['nb_dollar'] = url.count('$')
    res['nb_space'] = url.count(' ')
    res['nb_com'] = url.count('com')
    res['nb_dslash'] = url.count('//')
    res['contains_ip'] = 1 if any(c.isdigit() for c in url.split('/')[2]) else 0
    res['has_https'] = 1 if url.startswith('https://') else 0
    res['nb_redirects'] = url.count('http://') + url.count('https://') - 1
    res['ratio_digits_to_letters'] = sum(c.isdigit() for c in url) / max(1, sum(c.isalpha() for c in url))

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

    df = pd.DataFrame([res])
    scaler = joblib.load('modal/scaler.pkl')
    features_scaled = scaler.transform(df)
    feature_tensor = torch.tensor(features_scaled, dtype=torch.float32)
    input_size = features_scaled.shape[1]
    return (input_size, feature_tensor)