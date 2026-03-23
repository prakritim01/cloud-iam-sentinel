from app.core.scanner import scan_iam_policy

with open("sample_policies/vulnerable.json") as f:
    data = f.read()

threats, score = scan_iam_policy(data)
print(score, threats)