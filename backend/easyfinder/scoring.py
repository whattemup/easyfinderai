""""AI Lead Scoring Logic for EasyFinder""" 
import re from typing 
import Dict, Any, List, Tuple from .config 
import SCORING_CONFIG, HIGH_PRIORITY_THRESHOLD, MEDIUM_PRIORITY_THRESHOLD 

def validate_email(email: str) -> bool: """Validate email format""" 
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$' 
return bool(re.match(pattern, email)) 
if email else False 

def parse_budget(budget_str: str) -> float: """Parse budget string to float""" 
if not budget_str: 
return 0 # Remove currency symbols and commas 
cleaned = str(budget_str).replace('$', '').replace(',', '').strip() try: 
return float(cleaned) except ValueError: return 0 

def score_company_size(company_size: str) -> Tuple[int, str]: 
  
  """Score based on company size""" 
  size = company_size.lower().strip() 
if company_size else '' config = SCORING_CONFIG['company_size'] 

if size == 'enterprise': return config['enterprise'], 
  f\"Enterprise company (+{config['enterprise']} pts)\"el
  if size == 'medium': return config['medium'], 
  f\"Medium company (+{config['medium']} pts)\"el
  if size == 'small': return config['small'], 
  f\"Small company (+{config['small']} pts)\" 
  return 0, \"Unknown company size (0 pts)\" 
 

def score_budget(budget: float) -> Tuple[int, str]: """Score based on budget""" 
  thresholds = SCORING_CONFIG['budget_thresholds'] 

if budget >= thresholds['high']['min']: 
   pts = thresholds['high']['points'] 
   return pts, f\"High budget ${budget:,.0f} (+{pts} pts)\" 
elif budget >= thresholds['medium']['min']: 
   pts = thresholds['medium']['points'] 
   return pts, f\"Medium budget ${budget:,.0f} (+{pts} pts)\" 
return 0, f\"Low budget ${budget:,.0f} (0 pts)\" 
 

def score_industry(industry: str) -> Tuple[int, str]: """Score based on industry""" ind = industry.lower().strip() 
if industry else '' target_industries = SCORING_CONFIG['target_industries'] 

if any(target in ind for target in target_industries): 
   pts = SCORING_CONFIG['industry_points']['target'] 
   return pts, f\"Target industry: {industry} (+{pts} pts)\" 
pts = SCORING_CONFIG['industry_points']['other'] 
return pts, f\"Other industry: {industry} (+{pts} pts)\" 
 

def score_email(email: str) -> Tuple[int, str]: """Score based on email validity""" if validate_email(email): pts = SCORING_CONFIG['email_valid_points'] return pts, f"Valid email format (+{pts} pts)" return 0, "Invalid email format (0 pts)" 

def calculate_lead_score(lead: Dict[str, Any]) -> Dict[str, Any]: """ Calculate comprehensive lead score with breakdown 

Args: 
   lead: Lead data dictionary 
    
Returns: 
   Dictionary with score, priority, and breakdown 
\"\"\" 
score = 0 
breakdown = [] 
 
# Company size scoring 
size_score, size_reason = score_company_size(lead.get('company_size', '')) 
score += size_score 
breakdown.append({'category': 'Company Size', 'points': size_score, 'reason': size_reason}) 
 
# Budget scoring 
budget = parse_budget(lead.get('budget', '0')) 
budget_score, budget_reason = score_budget(budget) 
score += budget_score 
breakdown.append({'category': 'Budget', 'points': budget_score, 'reason': budget_reason}) 
 
# Industry scoring 
industry_score, industry_reason = score_industry(lead.get('industry', '')) 
score += industry_score 
breakdown.append({'category': 'Industry', 'points': industry_score, 'reason': industry_reason}) 
 
# Email validation scoring 
email_score, email_reason = score_email(lead.get('email', '')) 
score += email_score 
breakdown.append({'category': 'Email', 'points': email_score, 'reason': email_reason}) 
 
# Determine priority 
if score >= HIGH_PRIORITY_THRESHOLD: 
   priority = 'HIGH' 
elif score >= MEDIUM_PRIORITY_THRESHOLD: 
   priority = 'MEDIUM' 
else: 
   priority = 'LOW' 
 
return { 
   'score': min(score, 100),  # Cap at 100 
   'priority': priority, 
   'breakdown': breakdown, 
   'qualifies_for_outreach': score >= HIGH_PRIORITY_THRESHOLD 
} 
 

def batch_score_leads(leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]: """Score multiple leads and return with scoring data""" scored_leads = [] for lead in leads: scoring_result = calculate_lead_score(lead) scored_lead = {**lead, **scoring_result} scored_leads.append(scored_lead) return scored_leads "
