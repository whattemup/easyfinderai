""""CLI Entry Point for EasyFinder AI""" import sys from pathlib import Path from typing import Optional 

from .config import DATA_DIR from .ingestion import parse_csv_content, generate_sample_csv from .scoring import batch_score_leads from .outreach import batch_send_emails from .logging import activity_logger 

def print_header(): """Print application header""" print("\n" + "="*60) print(" EasyFinder AI - Enterprise Lead Management System") print(" Version 1.0.0") print("="*60 + "\n") 

def print_lead_summary(lead: dict): """Print a single lead summary""" print(f"\n 📊 {lead['name']} ({lead['company']})") print(f" Email: {lead['email']}") print(f" Score: {lead['score']}/100 | Priority: {lead['priority']}") print(f" Breakdown:") for item in lead.get('breakdown', []): print(f" • {item['reason']}") 

def process_leads_cli(csv_path: Optional[Path] = None): """Process leads from CSV file via CLI""" print_header() 

# Determine CSV path 
if csv_path is None: 
   csv_path = DATA_DIR / 'leads.csv' 
   if not csv_path.exists(): 
       print(\"ℹ️  No leads.csv found. Creating sample file...\") 
       csv_path.write_text(generate_sample_csv()) 
       print(f\"✅ Sample CSV created at: {csv_path}\") 
 
# Read CSV 
print(f\"\n📁 Reading leads from: {csv_path}\") 
try: 
   content = csv_path.read_text() 
except FileNotFoundError: 
   print(f\"❌ Error: File not found: {csv_path}\") 
   return 
 
# Parse CSV 
leads, error = parse_csv_content(content) 
if error: 
   print(f\"❌ Error parsing CSV: {error}\") 
   return 
 
print(f\"✅ Found {len(leads)} leads\n\") 
 
# Score leads 
print(\"🧠 Scoring leads...\") 
scored_leads = batch_score_leads(leads) 
 
# Display results 
print(\"\n\" + \"-\"*60) 
print(\"  LEAD SCORING RESULTS\") 
print(\"-\"*60) 
 
for lead in scored_leads: 
   print_lead_summary(lead) 
   activity_logger.log_lead_scored(lead['name'], lead['score'], lead['priority']) 
 
# Summary stats 
high = sum(1 for l in scored_leads if l['priority'] == 'HIGH') 
medium = sum(1 for l in scored_leads if l['priority'] == 'MEDIUM') 
low = sum(1 for l in scored_leads if l['priority'] == 'LOW') 
 
print(\"\n\" + \"-\"*60) 
print(\"  SUMMARY\") 
print(\"-\"*60) 
print(f\"  Total Leads: {len(scored_leads)}\") 
print(f\"  🔴 HIGH Priority: {high}\") 
print(f\"  🟡 MEDIUM Priority: {medium}\") 
print(f\"  🔵 LOW Priority: {low}\") 
 
# Send emails to qualified leads 
print(\"\n\" + \"-\"*60) 
print(\"  EMAIL OUTREACH (Mock Mode)\") 
print(\"-\"*60) 
 
email_results = batch_send_emails(scored_leads) 
 
print(f\"\n  Qualified for outreach: {email_results['qualified']}\") 
print(f\"  Emails sent (mock): {email_results['sent']}\") 
 
for detail in email_results['details']: 
   print(f\"\n  📧 {detail['lead_name']} ({detail['email']})\") 
   print(f\"     Status: {detail['result'].get('message', 'Sent')}\") 
   activity_logger.log_email_sent( 
       detail['lead_name'],  
       detail['email'],  
       detail['result'].get('mode', 'mock') 
   ) 
 
# Log processing summary 
activity_logger.log_leads_processed( 
   len(scored_leads), 
   email_results['qualified'], 
   email_results['sent'] 
) 
 
print(\"\n\" + \"=\"*60) 
print(\"  ✅ Processing Complete!\") 
print(\"=\"*60 + \"\n\") 
 

def main(): """Main CLI entry point""" csv_path = None if len(sys.argv) > 1: csv_path = Path(sys.argv[1]) 

process_leads_cli(csv_path) 
 

if name == "__main__": main() "
