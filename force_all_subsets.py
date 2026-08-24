import urllib.request, json, os, re, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

with open("fonts_manifest.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_all_subset_urls(name):
    family = name.replace(" ", "+")
    url = f"https://fonts.googleapis.com/css2?family={family}:wght@400&display=swap"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=20)
        css = resp.read().decode("utf-8", errors="ignore")
        blocks = css.split("@font-face")
        subsets = []
        for block in blocks:
            woff2_urls = re.findall(r'url\((https?://[^)]+\.woff2)\)', block)
            range_match = re.search(r'unicode-range:\s*([^;]+);', block)
            if woff2_urls:
                subsets.append({
                    "url": woff2_urls[0],
                    "range": range_match.group(1).strip() if range_match else None
                })
        return subsets
    except Exception:
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

world_cats = ['arabic','thai','hebrew','greek','georgian','armenian','tibetan',
              'cyrillic','vietnamese','latin','khmer','lao','myanmar','sinhala',
              'ethiopic','thaana','tifinagh','cherokee','canadian','ogham','runic','symbols']

results = list(data["fonts"])
updated = 0
skipped = 0

def process_font(font):
    if font["category"] not in world_cats:
        return ("skip", None)
    if font.get("format") != "woff2":
        return ("skip", None)
    
    base_id = font["id"].replace("-", "_")
    
    # Count existing subsets
    existing = [f for f in os.listdir("fonts") if f.startswith(base_id + "_subset") and f.endswith(".woff2")]
    
    # If we already have >1 subset, skip (already done)
    if len(existing) > 1:
        return ("skip", font)
    
    # Otherwise, fetch and download all
    subsets = get_all_subset_urls(font["name"])
    if len(subsets) <= 1:
        return ("skip", font)
    
    subset_files = []
    for i, sub in enumerate(subsets):
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
        return ("updated", font)
    return ("skip", font)

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(process_font, f): f for f in results}
    for future in concurrent.futures.as_completed(futures):
        status, font = future.result()
        if status == "updated":
            updated += 1
        else:
            skipped += 1

print(f"Updated: {updated}, Skipped: {skipped}")

with open("fonts_manifest.json", "w", encoding="utf-8") as f:
    json.dump({"fonts": results, "failed": [], "total": len(results)}, f, indent=2, ensure_ascii=False)

fonts_js = []
for f in results:
    entry = {"n": f["name"], "id": f["id"], "f": f["file"],
             "c": f["category"], "fmt": f.get("format","ttf"), "s": f["size"]}
    if f.get("cdn"): entry["cdn"] = f["cdn"]
    if f.get("subsets"): entry["sub"] = f["subsets"]
    fonts_js.append(entry)

with open("fonts-data.js", "w", encoding="utf-8") as f:
    f.write("window.FONTS_DATA = ")
    json.dump(fonts_js, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";")

subset_count = sum(1 for f in os.listdir("fonts") if "_subset" in f)
print(f"Subset files: {subset_count}")
print(f"fonts-data.js: {os.path.getsize('fonts-data.js')} bytes")
