import json

def scan_iam_policy(policy_text):
    threats = []
    score = 100

    try:
        policy = json.loads(policy_text)
    except:
        return [{"Severity": "CRITICAL", "Rule": "Invalid JSON", "Description": "Malformed policy format."}], 0

    statements = policy.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]

    for stmt in statements:
        # We generally only care about analyzing "Allow" statements for over-permissiveness
        effect = stmt.get("Effect", "Allow")
        if effect != "Allow":
            continue 

        actions = stmt.get("Action", [])
        resources = stmt.get("Resource", [])
        condition = stmt.get("Condition", {})

        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]

        # Rule 1: Full Admin Access (The one you already had)
        if "*" in actions and "*" in resources:
            threats.append({
                "Severity": "CRITICAL", 
                "Rule": "Full Access", 
                "Description": "Unrestricted wildcard access to all resources."
            })
            score -= 40

        # Rule 2: Privilege Escalation Risks
        # Catching permissions that let a user create other users or escalate their own privileges
        iam_risks = ["iam:PassRole", "iam:CreateUser", "iam:CreateAccessKey", "iam:PutUserPolicy", "iam:AttachUserPolicy"]
        if any(risk in actions for risk in iam_risks):
            threats.append({
                "Severity": "HIGH", 
                "Rule": "Privilege Escalation", 
                "Description": "Policy allows creating or modifying IAM users/roles, risking privilege escalation."
            })
            score -= 30

        # Rule 3: Missing MFA for sensitive actions
        # Checking if 'aws:MultiFactorAuthPresent' is enforced in the conditions
        mfa_enforced = False
        if condition:
            # Look through all condition operators (StringEquals, Bool, etc.)
            for operator, checks in condition.items():
                if isinstance(checks, dict) and "aws:MultiFactorAuthPresent" in checks:
                    # Usually configured as "aws:MultiFactorAuthPresent": "true"
                    if str(checks.get("aws:MultiFactorAuthPresent")).lower() == "true":
                        mfa_enforced = True

        # If it's a powerful policy but doesn't require MFA, flag it
        is_powerful = "*" in actions or any(a.startswith("iam:") or a.startswith("s3:Delete") for a in actions)
        if is_powerful and not mfa_enforced:
             threats.append({
                 "Severity": "MEDIUM", 
                 "Rule": "Missing MFA", 
                 "Description": "Powerful actions are allowed without requiring Multi-Factor Authentication."
             })
             score -= 15

    # Ensure score doesn't drop below 0
    return threats, max(score, 0)