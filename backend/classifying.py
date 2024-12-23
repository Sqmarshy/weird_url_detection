import torch
import torch.nn as nn
from feature_extraction import feature_extraction
import pandas as pd

class PhishingDetectionModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(PhishingDetectionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.bn2 = nn.BatchNorm1d(hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, 1)  # Single output for binary classification
        self.dropout = nn.Dropout(0.3)
        self.activation = nn.ReLU()  # Activation for hidden layers

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.fc3(x)  # Output logits (raw scores)
        return x

def run_modal(url):
    data = feature_extraction(url)
    input_size = data[0]
    features = data[1]
    hidden_size = 64

    model = PhishingDetectionModel(input_size, hidden_size)
    model.load_state_dict(torch.load("modal/best_model.pth", weights_only=True))
    model.eval()
    with torch.no_grad():
        outputs = model(features)
        probabilities = torch.sigmoid(outputs)  # Convert logits to probabilities
        prediction = (probabilities >= 0.5).int()
    return prediction