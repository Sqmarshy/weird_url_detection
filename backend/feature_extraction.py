from sklearn.preprocessing import StandardScaler
import joblib
import torch
import pandas as pd
import numpy as np

def feature_extraction(url):
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
    res['nb_www'] = url.count('www')
    res['nb_com'] = url.count('com')
    res['nb_dslash'] = url.count('//')
    res['contains_ip'] = 1 if any(c.isdigit() for c in url.split('/')[2]) else 0
    res['has_https'] = 1 if url.startswith('https://') else 0
    res['nb_redirects'] = url.count('http://') + url.count('https://') - 1
    res['ratio_digits_to_letters'] = sum(c.isdigit() for c in url) / max(1, sum(c.isalpha() for c in url))

    df = pd.DataFrame([res])
    scaler = joblib.load('modal/scaler.pkl')
    features_scaled = scaler.transform(df)
    feature_tensor = torch.tensor(features_scaled, dtype=torch.float32)
    input_size = features_scaled.shape[1]
    return (input_size, feature_tensor)