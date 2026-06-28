import pandas as pd

def generate_navbox_from_csv(file_path):
    # Use the parameter variable 'file_path' inside the function
    df = pd.read_csv(file_path)
    
    # Ensure the columns match your spreadsheet headers
    # Adjust 'village_tract' and 'shn_name' if your headers differ
    
    # 1. Pull the static info from the first row to use in the 'above' field
    first_row = df.iloc[0]
    ts = first_row['township']
    dist = first_row['district']
    
    # 2. Use those variables in your f-string
    navbox = f"""{{{{Navbox
| name= ၸႄႈဝဵင်း{ts}
| title= [[ၸႄႈဝဵင်း{ts}]]
| state= {{{{{{state| autocollapse}}}}}}
| listclass= hlist
| above = '''ၸႄႈတွၼ်ႈ''':[[ၸႄႈတွၼ်ႈ{dist}]] '''ဝဵင်း''': [[ဝဵင်း{ts}]]
"""
    
    # Group by village_tract to create groups
    grouped = df.groupby('village_tract')
    
    group_idx = 1
    for tract, group in grouped:
        # Get the township and district from the first row of the group
        # Assuming these are constant for all rows in this group/tract
        first_row = group.iloc[0]
        ts = first_row['township']
        dist = first_row['district']
        
        navbox += f"|group{group_idx} = ဢိူင်ႇ{tract}\n|list{group_idx} =\n"
        
        for _, row in group.iterrows():
            village = row['shn_name']
            # Now use the variables 'ts' and 'dist' inside your f-string
            navbox += f"* [[ဝၢၼ်ႈ{village}၊ ၸႄႈဝဵင်း{ts}|{village}]]\n"
        
        navbox += "\n"
        group_idx += 1
        
    navbox += """}}<noinclude>
{{collapsible option}}
[[Category:ထႅမ်းပလဵတ်ႉ မိူင်းမျၢၼ်ႇမႃႇ]]
</noinclude>"""
    return navbox

# Generate and print
print(generate_navbox_from_csv('villages.csv'))