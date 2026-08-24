import urllib.request, json, os, re, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

with open("fonts_manifest.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Fonts that need all subsets downloaded (non-CJK world scripts)
# CJK will use CDN at runtime due to huge size
needs_subsets_cats = ['arabic','thai','hebrew','greek','georgian','armenian','tibetan','cyrillic','vietnamese','latin']
cjk_cats = ['chinese','chinese-trad','japanese','korean']

# For each font that needs subsets, fetch CSS API and download ALL woff2 files
def get_all_subset_urls(name):
    family = name.replace(" ", "+")
    url = f"https://fonts.googleapis.com/css2?family={family}:wght@400;700&display=swap"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=20)
        css = resp.read().decode("utf-8", errors="ignore")
        # Parse all @font-face blocks and extract url + unicode-range
        blocks = css.split("@font-face")
        subsets = []
        for block in blocks:
            woff2_urls = re.findall(r'url\((https?://[^)]+\.woff2)\)', block)
            weight_match = re.search(r'font-weight:\s*(\d+)', block)
            range_match = re.search(r'unicode-range:\s*([^;]+);', block)
            if woff2_urls:
                subsets.append({
                    "url": woff2_urls[0],
                    "weight": weight_match.group(1) if weight_match else "400",
                    "range": range_match.group(1).strip() if range_match else None
                })
        return subsets
    except Exception as e:
        return []

def download_subset(url, out_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=30)
        content = resp.read()
        if len(content) > 1000:
            with open(out_path, "wb") as f:
                f.write(content)
            return len(content)
    except Exception:
        pass
    return 0

# Process fonts
results = list(data["fonts"])
updated = 0
cjk_count = 0

for font in results:
    cat = font["category"]
    
    # Mark CJK fonts to use CDN
    if cat in cjk_cats:
        # Store the family name for CDN loading
        font["cdn"] = font["name"]
        cjk_count += 1
        continue
    
    # For non-Latin scripts, download all subsets
    if cat in needs_subsets_cats:
        # Check if we already have multiple subsets downloaded
        base_id = font["id"].replace("-", "_")
        existing_subsets = [f for f in os.listdir("fonts") if f.startswith(base_id + "_subset") and f.endswith(".woff2")]
        
        if not existing_subsets and font.get("format") == "woff2":
            # Download all subsets
            subsets = get_all_subset_urls(font["name"])
            if len(subsets) > 1:
                subset_files = []
                for i, sub in enumerate(subsets):
                    if sub["weight"] == "400":  # Only regular weight subsets
                        sub_filename = f"{base_id}_subset{i}.woff2"
                        sub_path = os.path.join("fonts", sub_filename)
                        size = download_subset(sub["url"], sub_path)
                        if size > 0:
                            subset_files.append({"f": f"fonts/{sub_filename}", "range": sub["range"], "s": size})
                
                if subset_files:
                    font["subsets"] = subset_files
                    updated += 1
                    if updated % 20 == 0:
                        print(f"  Updated {updated} fonts...")

print(f"\nCJK fonts (CDN): {cjk_count}")
print(f"Fonts with extra subsets: {updated}")

# Save manifest
with open("fonts_manifest.json", "w", encoding="utf-8") as f:
    json.dump({"fonts": results, "failed": [], "total": len(results)}, f, indent=2, ensure_ascii=False)

# Regenerate fonts-data.js with subset info
fonts_js = []
for f in results:
    entry = {
        "n": f["name"], "id": f["id"], "f": f["file"],
        "c": f["category"], "fmt": f.get("format", "ttf"), "s": f["size"]
    }
    if f.get("cdn"):
        entry["cdn"] = f["cdn"]
    if f.get("subsets"):
        entry["sub"] = f["subsets"]
    fonts_js.append(entry)

with open("fonts-data.js", "w", encoding="utf-8") as f:
    f.write("window.FONTS_DATA = ")
    json.dump(fonts_js, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";")

print(f"fonts-data.js: {os.path.getsize('fonts-data.js')} bytes")

# Stats
cats = {}
for f in results:
    cats[f["category"]] = cats.get(f["category"], 0) + 1
print(f"\nFinal: {len(results)} fonts")
for cat in sorted(cats.keys()):
    print(f"  {cat:20s}: {cats[cat]:3d}")
total_size = sum(
    f["size"] + sum(s.get("s",0) for s in f.get("subsets",[]))
    for f in results
)
print(f"Total size: {total_size/(1024*1024):.0f} MB")
