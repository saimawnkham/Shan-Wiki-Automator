import sys
import subprocess

# --- Auto-Dependency Installer ---
try:
    import requests
except ImportError:
    print("⚙️ 'requests' library not found. Auto-installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    print("✅ Installation complete!\n")

import pywikibot
import re
import csv

def get_en_wiktionary_data(word, pos_type):
    """Fetches the entire English pronunciation block and exact inflection template."""
    en_site = pywikibot.Site("en", "wiktionary")
    page = pywikibot.Page(en_site, word)
    
    pronunciation_block = ""
    en_template = ""
    
    if not page.exists():
        return pronunciation_block, en_template
        
    text = page.text
    
    # 1. Fetch the Entire Pronunciation Block
    # This regex finds the Pronunciation heading (=== or ====) and captures everything until the next heading
    pron_match = re.search(r'(={3,5})\s*Pronunciation\s*\1\n(.*?)(?=\n={2,5}[^=]|\Z)', text, re.DOTALL)
    
    if pron_match:
        pronunciation_block = pron_match.group(2).strip()
    else:
        # Fallback: If no dedicated heading is found, try to grab at least one IPA template
        fallback_match = re.search(r'\{\{IPA\|en\|([^}]+)\}\}', text)
        if fallback_match:
            pronunciation_block = f"* {{{{IPA|en|{fallback_match.group(1)}}}}}"
        
    # 2. Fetch Inflection Template
    pos_short_map = {
        'noun': 'noun',
        'verb': 'verb',
        'adjective': 'adj',
        'adverb': 'adv',
        'pronoun': 'pron'
    }
    short_pos = pos_short_map.get(pos_type, 'noun')
    
    template_pattern = r'\{\{en-' + short_pos + r'(?:\|[^}]*)?\}\}'
    template_match = re.search(template_pattern, text)
    
    if template_match:
        en_template = template_match.group(0)
        
    return pronunciation_block, en_template

def create_wiktionary_entries():
    shn_site = pywikibot.Site("shn", "wiktionary")
    
    with open('dictionary.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            word = row.get('english_word')
            if not word:
                continue 

            definition = row.get('shan_definition', '')
            pos_type = row.get('part_of_speech', '').strip().lower()

            print(f"Fetching data from en.wiktionary for: {word}...")
            pronunciation, fetched_en_template = get_en_wiktionary_data(word, pos_type)
            
            if not pronunciation:
                pronunciation = "<!-- ဢမ်ႇမီးသဵင်ဢွၵ်ႇ -->" 

            if pos_type == 'noun':
                shan_pos = "ႁိၵ်ႈ"
                default_en_template = "{{en-noun}}"
            elif pos_type == 'verb':
                shan_pos = "သၢင်ႈ"
                default_en_template = "{{en-verb}}"
            elif pos_type == 'adjective':
                shan_pos = "ၵမ်ႉႁိၵ်ႈ"
                default_en_template = "{{en-adj}}"
            elif pos_type == 'adverb':
                shan_pos = "ၵမ်ႉသၢင်ႈ"
                default_en_template = "{{en-adv}}"
            elif pos_type == 'pronoun':
                shan_pos = "ႁိိၵ်ႈတၢင်"
                default_en_template = "{{en-pron}}"
            else:
                shan_pos = "ႁိၵ်ႈ"
                default_en_template = "{{en-noun}}"

            final_en_template = fetched_en_template if fetched_en_template else default_en_template

            # Notice the asterisk (*) is removed before {pronunciation} 
            # because the imported block already contains bullet points.
            text = f"""==ဢိင်းၵလဵတ်ႈ==

===သဵင်ဢွၵ်ႇ===
{pronunciation}

==={shan_pos}===
{final_en_template}

# {definition}

===ၽိုၼ်ဢိင်===
# {{{{VPS Ref}}}}
"""
            page = pywikibot.Page(shn_site, word)
            
            if not page.exists():
                page.text = text
                page.save(summary="Bot: ၵေႃႇသၢင်ႈၼႃႈလိၵ်ႈၶေႃႈၵႂၢမ်းမႂ်ႇ", botflag=True)
                print(f"✅ Created: {word}")
            else:
                with open("skipped_words.log", "a", encoding="utf-8") as f:
                    f.write(f"{word}\n")
                print(f"⏭️ Skipped: {word}")

if __name__ == "__main__":
    create_wiktionary_entries()