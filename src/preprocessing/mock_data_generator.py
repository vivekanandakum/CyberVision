import pandas as pd
import numpy as np
import os
from pathlib import Path

# Paths based on config.py
ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

def generate_global_threats():
    print("Generating mock Global Threats data...")
    n = 1000
    df = pd.DataFrame({
        "country": np.random.choice(["USA", "China", "India", "UK", "Germany"], n),
        "year": np.random.choice(range(2015, 2025), n),
        "attack_type": np.random.choice(["Phishing", "Ransomware", "DDoS", "Malware"], n),
        "target_industry": np.random.choice(["Finance", "Healthcare", "Government", "IT", "Retail"], n),
        "financial_loss_in_million_": np.random.uniform(0.1, 50.0, n),
        "number_of_affected_users": np.random.randint(100, 100000, n),
        "attack_source": np.random.choice(["Insider", "Nation State", "Hacker Group", "Unknown"], n),
        "security_vulnerability_type": np.random.choice(["Zero-Day", "Unpatched", "Misconfiguration"], n),
        "defense_mechanism_used": np.random.choice(["Firewall", "MFA", "Antivirus", "None"], n),
        "incident_resolution_time_in_hours": np.random.randint(1, 30, n)
    })
    # Rename to match standard raw names before cleaning
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    df.to_csv(RAW_DIR / "Global_Cybersecurity_Threats_2015-2024.csv", index=False)

def generate_cfr_incidents():
    print("Generating mock CFR Incidents data...")
    n = 1000
    df = pd.DataFrame({
        "title": [f"Incident {i}" for i in range(n)],
        "date": pd.date_range(start="2005-01-01", end="2020-12-31", periods=n).strftime("%Y-%m-%d"),
        "affiliations": np.random.choice(["State A", "State B", "Unknown"], n),
        "description": ["Description text"] * n,
        "response": ["Response text"] * n,
        "victims": np.random.choice(["Government", "Corporate", "Military"], n),
        "sponsor": np.random.choice(["State X", "State Y", "Unknown"], n),
        "type": np.random.choice(["Espionage", "Sabotage", "Denial of Service"], n),
        "category": np.random.choice(["Category A", "Category B"], n),
        "sources_1": ["http://source1.com"] * n,
        "sources_2": [""] * n,
        "sources_3": [""] * n
    })
    df.to_csv(RAW_DIR / "cyber-operations-incidents.csv", index=False)

def generate_vulnerabilities():
    print("Generating mock Vulnerabilities data...")
    n = 1000
    df = pd.DataFrame({
        "title": [f"CVE-202{i%10}-{i}" for i in range(n)],
        "date": pd.date_range(start="2015-01-01", end="2024-01-01", periods=n).strftime("%Y-%m-%d"),
        "severity": np.random.choice(["Low", "Medium", "High", "Critical"], n),
        "summary": ["Vulnerability summary text"] * n,
        "link": ["http://link.com"] * n
    })
    df.to_csv(RAW_DIR / "security_vulnerabilities.csv", index=False)

def generate_attack_signatures():
    print("Generating mock Attack Signatures data...")
    n = 1000
    df = pd.DataFrame({
        "timestamp": pd.date_range(start="2023-01-01", end="2023-12-31", periods=n).strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip_address": ["192.168.1.1"] * n,
        "destination_ip_address": ["10.0.0.1"] * n,
        "source_port": np.random.randint(1024, 65535, n),
        "destination_port": np.random.choice([80, 443, 22, 3389], n),
        "protocol": np.random.choice(["TCP", "UDP", "ICMP"], n),
        "packet_length": np.random.randint(40, 1500, n),
        "packet_type": np.random.choice(["SYN", "ACK", "FIN"], n),
        "traffic_type": np.random.choice(["HTTP", "DNS", "SSH"], n),
        "payload_data": ["malicious payload"] * n,
        "malware_indicators": ["IoC"] * n,
        "anomaly_scores": np.random.uniform(0.0, 100.0, n),
        "alertswarnings": ["Alert"] * n,
        "attack_type": np.random.choice(["DDoS", "SQLi", "XSS"], n),
        "attack_signature": np.random.choice(["Sig1", "Sig2", "Sig3"], n),
        "action_taken": np.random.choice(["Blocked", "Logged", "Ignored"], n),
        "severity_level": np.random.choice(["Low", "Medium", "High"], n),
        "user_information": ["user1"] * n,
        "device_information": ["Device A"] * n,
        "network_segment": ["Segment X"] * n,
        "geolocation_data": np.random.choice(["USA", "UK"], n),
        "proxy_information": ["Proxy A"] * n,
        "firewall_logs": ["Log"] * n,
        "idsips_alerts": ["IDS Alert"] * n,
        "log_source": np.random.choice(["Firewall", "Server"], n)
    })
    df.to_csv(RAW_DIR / "cybersecurity_attacks.csv", index=False)

def generate_malmem():
    print("Generating mock MalMem data...")
    n = 1000
    labels = np.random.choice([
        "Benign", 
        "Spyware-Zeus-1.raw", 
        "Ransomware-WannaCry-2.raw", 
        "Trojan-Emotet-3.raw", 
        "Spyware-TIBS-4.raw"
    ], n)
    df = pd.DataFrame({
        "label": labels,
        "feature_1": np.random.uniform(0, 1, n),
        "feature_2": np.random.uniform(0, 1, n)
    })
    df.to_csv(RAW_DIR / "Obfuscated-MalMem2022.csv", index=False)

if __name__ == "__main__":
    generate_global_threats()
    generate_cfr_incidents()
    generate_vulnerabilities()
    generate_attack_signatures()
    generate_malmem()
    print("Successfully generated all mock datasets in data/raw!")
