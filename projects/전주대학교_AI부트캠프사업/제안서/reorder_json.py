import json

filepath = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\전주대학교_AI부트캠프사업\제안서\content.json"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for track in data.get("tracks", []):
    for mod in track.get("modules", []):
        new_items = []
        for item in mod.get("items", []):
            # Create a new dict with the specific order: detail, method, hours
            new_item = {
                "detail": item.get("detail", ""),
                "method": item.get("method", ""),
                "hours": item.get("hours", "")
            }
            new_items.append(new_item)
        mod["items"] = new_items

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Key order in content.json updated successfully.")
