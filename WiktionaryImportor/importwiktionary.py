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
import os

# ==========================================
# SETTINGS
# ==========================================
# Set to False to skip existing pages and avoid overwriting human edits.
FORCE_OVERWRITE = True 
# ==========================================

def parse_definitions(def_col):
    """
    Parses definitions where [tag] triggers a new section.
    Automatically handles definitions starting with a tag.
    """
    # 1. Clean invisible characters and outer square brackets
    def_col = def_col.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '').replace('\u200e', '')
    def_col = def_col.strip()
    
    # 2. Split into segments based on [tag]
    # The parentheses in the pattern capture the tag itself so it appears in the list
    pattern = r'\[\s*(n|v|vt|vi|adj|adv|pron|noun|verb|adjective|adverb|pronoun)\.?\s*\]'
    split_parts = re.split(pattern, def_col, flags=re.IGNORECASE)
    
    results = []
    POS_MAP = {'n':'noun', 'v':'verb', 'vt':'verb', 'vi':'verb', 'adj':'adjective', 'adv':'adverb', 'pron':'pronoun'}
    
    # 3. If the first segment is not empty, it's a default noun section
    if split_parts[0].strip():
        results.append(('noun', split_parts[0].strip()))
    
    # 4. Iterate through pairs of (tag, definition)
    # The split_parts list looks like: ['text before', 'tag', 'text after', 'tag', 'text after']
    for i in range(1, len(split_parts), 2):
        tag = split_parts[i].lower()
        definition = split_parts[i+1].strip()
        
        # Map the tag to the correct Shan POS category
        mapped_pos = POS_MAP.get(tag, 'noun')
        results.append((mapped_pos, definition))
            
    return results

def get_en_wiktionary_data(word, pos_list):
    """Fetches IPA and templates for all unique POS tags found in the row."""
    en_site = pywikibot.Site("en", "wiktionary")
    page = pywikibot.Page(en_site, word)
    
    pronunciation_block = ""
    templates_dict = {}
    
    if not page.exists():
        return pronunciation_block, templates_dict
        
    text = page.text
    
    # 1. Fetch Pronunciation block
    pron_match = re.search(r'(={3,5})\s*Pronunciation\s*\1\n(.*?)(?=\n={2,5}[^=]|\Z)', text, re.DOTALL)
    if pron_match:
        pronunciation_block = pron_match.group(2).strip()
    else:
        fallback_match = re.search(r'\{\{IPA\|en\|([^}]+)\}\}', text)
        if fallback_match:
            pronunciation_block = f"* {{{{IPA|en|{fallback_match.group(1)}}}}}"
        
    # 2. Fetch Templates dynamically
    pos_short_map = {'noun': 'noun', 'verb': 'verb', 'adjective': 'adj', 'adverb': 'adv', 'pronoun': 'pron'}
    
    for pos in set(pos_list):
        short_pos = pos_short_map.get(pos, 'noun')
        template_pattern = r'\{\{en-' + short_pos + r'(?:\|[^}]*)?\}\}'
        template_match = re.search(template_pattern, text)
        if template_match:
            templates_dict[pos] = template_match.group(0)
            
    return pronunciation_block, templates_dict

def create_wiktionary_entries():
    shn_site = pywikibot.Site("shn", "wiktionary")
    shan_pos_names = {'noun': 'ႁိၵ်ႈ', 'verb': 'သၢင်ႈ', 'adjective': 'ၵမ်ႉႁိၵ်ႈ', 'adverb': 'ၵမ်ႉသၢင်ႈ', 'pronoun': 'ႁိိၵ်ႈတၢင်'}
    default_templates = {'noun': '{{en-noun}}', 'verb': '{{en-verb}}', 'adjective': '{{en-adj}}', 'adverb': '{{en-adv}}', 'pronoun': '{{en-pron}}'}
    
    with open('dictionary.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get('english_word')
            if not word: continue 

            # Parse exclusively from definition text
            parsed_blocks = parse_definitions(row.get('shan_definition', ''))
            required_pos_types = [block[0] for block in parsed_blocks]

            print(f"Fetching data for: {word}...")
            pronunciation, fetched_en_templates = get_en_wiktionary_data(word, required_pos_types)
            
            if not pronunciation: pronunciation = "<!-- ဢမ်ႇမီးသဵင်ဢွၵ်ႇ -->" 

            # Construct the Wikitext
            text = f"==ဢိင်းၵလဵတ်ႈ==\n\n===သဵင်ဢွၵ်ႇ===\n{pronunciation}\n\n"
            
            # Construct distinct sections for every parsed POS block
            for pos_type, shan_def in parsed_blocks:
                shan_pos = shan_pos_names.get(pos_type, "ႁိၵ်ႈ")
                en_template = fetched_en_templates.get(pos_type, default_templates.get(pos_type, "{{en-noun}}"))
                
                # --- NEW: Split the definition by the Shan comma (၊) into numbered list items ---
                def_items = [item.strip() for item in shan_def.split('၊') if item.strip()]
                formatted_defs = "\n".join([f"# {item}" for item in def_items])
                
                # Each section now gets its own header and list items
                text += f"==={shan_pos}===\n{en_template}\n\n{formatted_defs}\n\n"

            text += "===ၽိုၼ်ဢိင်===\n# {{VPS Ref}}\n"
            
            page = pywikibot.Page(shn_site, word)
            if not page.exists() or FORCE_OVERWRITE:
                page.text = text
                page.save(summary="Bot: မႄးမႂ်ႇ/ၵေႃႇသၢင်ႈ ၼႃႈလိၵ်ႈၶေႃႈၵႂၢမ်း", bot=True)
                print(f"✅ Saved: {word}")
            else:
                with open("skipped_words.log", "a", encoding="utf-8") as f:
                    f.write(f"{word}\n")
                print(f"⏭️ Skipped: {word}")

if __name__ == "__main__":
    if os.path.exists('dictionary.csv'):
        create_wiktionary_entries()
    else:
        print("❌ Error: 'dictionary.csv' file not found in the current directory.")