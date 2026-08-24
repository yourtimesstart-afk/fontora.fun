import urllib.request, json, os, re, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

with open("fonts_manifest.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_all_subset_urls(name):
    family = name.replace(" ", "+")
    for w in ["400", "400;700"]:
        url = f"https://fonts.googleapis.com/css2?family={family}:wght@{w}&display=swap"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=20)
            css = resp.read().decode("utf-8", errors="ignore")
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
            if subsets:
                return subsets
        except Exception:
            continue
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

# For every woff2 font in non-Indic categories, force download all subsets
world_cats = ['arabic','thai','hebrew','greek','georgian','armenian','tibetan',
              'cyrillic','vietnamese','latin','khmer','lao','myanmar','sinhala',
              'ethiopic','thaana','tifinagh','cherokee','canadian','ogham','runic','symbols']

results = list(data["fonts"])
updated = 0

def process_font(font):
    if font["category"] not in world_cats:
        return None
    if font.get("format") != "woff2":
        return None
    # Check if already has subsets
    if font.get("subsets") and len(font["subsets"]) > 1:
        return None
    
    base_id = font["id"].replace("-", "_")
    subsets = get_all_subset_urls(font["name"])
    if len(subsets) <= 1:
        return None
    
    subset_files = []
    for i, sub in enumerate(subsets):
        if sub["weight"] != "400":
            continue
        sub_filename = f"{base_id}_subset{i}.woff2"
        sub_path = os.path.join("fonts", sub_filename)
        if os.path.exists(sub_path) and os.path.getsize(sub_path) > 1000:
            size = os.path.getsize(sub_path)
        else:
            size = download_subset(sub["url"], sub_path)
        if size > 0:
            subset_files.append({"f": f"fonts/{sub_filename}", "range": sub["range"], "s": size})
    
    if subset_files:
        font["subsets"] = subset_files
        # The main file should be the first (usually latin) subset
        return font
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(process_font, f): f for f in results}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            updated += 1

print(f"Updated {updated} fonts with subsets")

# Save
with open("fonts_manifest.json", "w", encoding="utf-8") as f:
    json.dump({"fonts": results, "failed": [], "total": len(results)}, f, indent=2, ensure_ascii=False)

# Regenerate data
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

# Count subset files
subset_count = sum(1 for f in os.listdir("fonts") if "_subset" in f)
print(f"Subset files: {subset_count}")
print(f"fonts-data.js: {os.path.getsize('fonts-data.js')} bytes")
total_size = sum(
    f["size"] + sum(s.get("s",0) for s in f.get("subsets",[]))
    for f in results
)
print(f"Total size: {total_size/(1024*1024):.0f} MB")
