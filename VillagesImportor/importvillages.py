import pywikibot
import csv

def create_shan_villages():
    # Connect to Shan Wikipedia
    site = pywikibot.Site("shn", "wikipedia")
    
    with open('villages.csv', 'r', encoding='utf-8') as file:
        # Standard CSVs use commas, so we don't need to specify the delimiter
        reader = csv.DictReader(file) 
        
        for row in reader:
            # Mapped to your exact CSV headers
            shn_name = row.get('shn_name')
            
            # Skip if the village doesn't have a Shan name
            if not shn_name:
                continue 

            my_name = row.get('my_name', '')
            en_name = row.get('en_name', '')
            
            lat = row.get('lat', '')
            lon = row.get('lon', '')
            # Check if lat/lon are not empty (string is not empty)
            if lat and lon:
                coords_value = f"{{{{coord|{lat}|{lon}|region:MM|format=dms|display=inline,title}}}}"
            else:
                # If data is missing, we leave the note for manual editing
                coords_value = ""
                # Log this to the terminal so you know which villages need attention
                print(f"⚠️ Warning: Missing coordinates for {shn_name}. Added placeholder.")
   
            
            state = row.get('state', '') 
            district = row.get('district', '')
            township = row.get('township', '')
            village_tract = row.get('village_tract', '')
            village_pcode = row.get('village_pcode', '')
            households = row.get('households', '')
            male_pp = row.get('male_pp', '')
            female_pp = row.get('female_pp', '')
            total_pp = row.get('total_pp', '')
            ref = row.get('ref', '') 

            
            text = f"""{{{{Infobox settlement
| name = {shn_name}
| official_name = ဝၢၼ်ႈ{shn_name}
| settlement_type = [[ဝၢၼ်ႈၸိူဝ်းမီးၼႂ်း မိူင်းမျၢၼ်ႇမႃႇ|ဝၢၼ်ႈ]]
| subdivision_type = မိူင်း
| subdivision_name = {{{{ၸွမ်ပိဝ်|မိူင်းမျၢၼ်ႇမႃႇ}}}}
| subdivision_type1 = [[ၼႃႈလိၼ်ၽွင်းငမ်းဢုပ်ႉပိူင်ႇ မိူင်းမျၢၼ်ႇမႃႇ|ၸႄႈတိူင်း]]
| subdivision_name1 = {{{{ၸွမ်ပိဝ်|ၸႄႈမိူင်းမွၼ်း}}}}
| subdivision_type2 = [[ၸႄႈတွၼ်ႈၸိူဝ်းမီးၼႂ်း မိူင်းမျၢၼ်ႇမႃႇ|ၸႄႈတွၼ်ႈ]]
| subdivision_name2 = [[ၸႄႈတွၼ်ႈ{district}|{district}]]
| subdivision_type3 = [[ၸႄႈဝဵင်းၸိူဝ်းမီးၼႂ်း မိူင်းမျၢၼ်ႇမႃႇ|ၸႄႈဝဵင်း]]
| subdivision_name3 = [[ၸႄႈဝဵင်း{township}|{township}]]
| subdivision_type4 = [[ဢိူင်ႇၸိူဝ်းမီးၼႂ်း မိူင်းမျၢၼ်ႇမႃႇ|ဢိူင်ႇ]]
| subdivision_name4 = ဢိူင်ႇ{village_tract}
| pushpin_map = မိူင်းမၢၼ်ႈ
| pushpin_map_caption = ဢွင်ႈတီႈ ၼႂ်းမိူင်းမျၢၼ်ႇမႃႇ
| pushpin_label_position = bottom
| coordinates_region = MM
| coordinates = {coords_value}
| timezone = [[လၵ်းၸဵင်ၶၢဝ်းယၢမ်းမျၢၼ်ႇမႃႇ|MST]]
| utc_offset = +06:30
}}}}
'''{shn_name}''' ({{{{Langx|my|{my_name}}}}}၊ {{{{Langx|en|{en_name}}}}}) ၼႆႉ ပဵၼ်ဝၢၼ်ႈဢၼ်မီးၼႂ်း ဢိူင်ႇ{village_tract}၊ [[ၸႄႈဝဵင်း{township}]]၊ [[ၸႄႈတွၼ်ႈ{district}]]၊ [[ၸႄႈမိူင်းမွၼ်း]]၊ [[မိူင်းမျၢၼ်ႇမႃႇ]] ယဝ်ႉ။ ၶူတ်ႉဢွင်ႈတီႈဝၢၼ်ႈၼႆႉ ပဵၼ် {{{{formatnum:{village_pcode}}}}} ယဝ်ႉ။ ၸွမ်းၼင်ႇသဵၼ်ႈမၢႆႁူဝ်ႁိူၼ်း ပီ 2014 သေ တီႈ ဢိူင်ႇ{village_tract}ၼႆႉ ႁူဝ်ႁိူၼ်း မီး {households}၊ ႁူဝ်ၼပ်ႉၵူၼ်း ၸၢႆး {male_pp} ၵေႃႉ၊ ယိင်း {female_pp} ၵေႃႉ၊ ႁူမ်ႈၵၼ် မီးယူႇ {total_pp} ၵေႃႉယဝ်ႉ။ <ref>{{{{cite web|url=http://themimu.info/place-codes|title=Place codes (Pcodes)|work=Myanmar Information Management Unit|date=June 2020|access-date=21 December 2020|archive-date=21 November 2020|archive-url=https://web.archive.org/web/20201121081823/https://themimu.info/place-codes|url-status=dead}}}}</ref>

== ၽိုၼ်ဢိင် ==
{{{{reflist}}}}

{{{{ဢွင်ႈတီႈၼႃႈလိၼ်
|Centre ={shn_name}
|North     =
|Northeast =
|East      =
|Southeast =
|South     =
|Southwest =
|West      =
|Northwest =
}}}}
{{{{ၸႄႈဝဵင်း{township}}}}}
{{{{Mon-geo-stub}}}}
{{{{DEFAULTSORT:{shn_name}}}}}
[[ပိူင်ထၢၼ်ႈ:ဝၢၼ်ႈၸိူဝ်းမီးတီႈ ၸႄႈဝဵင်း{township}]]

"""
            # Create the page object
            page = pywikibot.Page(site, shn_name)
            
            if not page.exists():
                # Saving to Sandbox for testing SIITBot
                sandbox_page = pywikibot.Page(site, f"ဝၢၼ်ႈ{shn_name}၊ ၸႄႈဝဵင်း{township}")
                sandbox_page.text = text
                
                # Use the standard Shan IT/Wiki terminology for the edit summary
                sandbox_page.save(summary="Bot: ၵေႃႇသၢင်ႈၼႃႈလိၵ်ႈဝၢၼ်ႈမႂ်ႇ", botflag=True)
                print(f"Created page for: {shn_name}")
            else:
                with open("skipped_pages.log", "a", encoding="utf-8") as f:
                    f.write(f"{target_title}\n")
                print(f"⏭️ Skipped: {target_title}")

                

if __name__ == "__main__":
    create_shan_villages()