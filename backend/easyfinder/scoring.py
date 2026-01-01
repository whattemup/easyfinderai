def score_lead(lead: dict) -> int:
score = 0


size = lead.get("company_size", "").lower()
if size == "enterprise": score += 40
elif size == "medium": score += 25
elif size == "small": score += 10


budget = int(lead.get("budget", 0))
if budget > 50000: score += 30
elif budget > 25000: score += 15


industry = lead.get("industry", "").lower()
if industry in ["construction", "logistics", "equipment"]:
score += 20


if "@" in lead.get("email", ""):
score += 10


return min(score, 100)
