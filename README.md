# Fontora — Free Font Library 🎨

**Fontora** is a beautiful, single-page font discovery and download website. Browse 550+ high-quality open-source fonts — including wedding calligraphy, **9 Indian languages** (ગુજરાતી, हिंदी, தமிழ், తెలుగು, ಕನ್ನಡ, മലയാളം, বাংলা, ਪੰਜਾਬੀ, ଓଡ଼ିଆ), scripts, serifs, sans-serifs, display, and monospace. Preview them with custom text/size/color, and download them instantly to your device — all 100% free for personal & commercial use.

![Fonts](https://img.shields.io/badge/fonts-550%2B-purple) ![Languages](https://img.shields.io/badge/Indian%20Languages-9-orange) ![Wedding](https://img.shields.io/badge/wedding-99%2B-pink) ![License](https://img.shields.io/badge/license-SIL%20OFL%20%2F%20Apache-green)

## ✨ Features

- **550+ curated fonts** across 15 categories:
  - 💍 **Wedding** (99) — elegant calligraphy, scripts, and serifs for invitations
  - 🇮🇳 **Hindi/Devanagari** (57) — हिंदी fonts including Noto, Tiro, Anek, Rajdhani, Teko, Baloo
  - 🇮🇳 **Gujarati** (25) — ગુજરાતી fonts including Noto, Anek, Baloo, Rasa, Mukta Vaani
  - 🇮🇳 **Telugu** (20) — తెలుగు fonts including Noto, Anek, Baloo Tammudu, Hind Guntur
  - 🇮🇳 **Tamil** (18) — தமிழ் fonts including Noto, Anek, Baloo Thambi, Catamaran, Hind Madurai
  - 🇮🇳 **Punjabi/Gurmukhi** (13) — ਪੰਜਾਬੀ fonts including Noto, Anek, Baloo Paaji, Tiro Gurmukhi
  - 🇮🇳 **Kannada** (12) — ಕನ್ನಡ fonts including Noto, Anek, Baloo Tamma, Tiro Kannada, Hind Mysuru
  - 🇮🇳 **Bengali** (15) — বাংলা fonts including Noto, Anek, Baloo Da, Hind Siliguri, Tiro Bangla
  - 🇮🇳 **Malayalam** (7) — മലയാളം fonts including Noto, Anek, Baloo Chettan, Gayathri, Manjari
  - 🇮🇳 **Odia** (6) — ଓଡ଼ିଆ fonts including Noto, Anek, Baloo Bhaina
  - ✒️ **Script** (73) — calligraphy, handwriting, brush
  - 🎨 **Display** (100) — decorative, retro, pixel, gothic
  - 📜 **Serif** (43) — elegant, classic, slab
  - 🔤 **Sans Serif** (46) — modern, clean, geometric
  - 💻 **Monospace** (20) — coding, terminal, typewriter
- **Indian Languages dropdown** — quickly filter to any of the 9 Indian languages, or select "All Indian Languages" to browse them together
- **Instant search** — find fonts by name or category in milliseconds
- **Live preview** — customize text, font size (14–120px), and colors
- **One-click download** — TTF/WOFF2 files saved directly to your device
- **Font detail modal** — character map, file info, large preview
- **Offline-ready** — all fonts are bundled locally in the `fonts/` folder
- **Fully responsive** — works on desktop, tablet, and mobile
- **Dark theme** with gradient accents and smooth animations

## 🚀 Quick Start

### Option 1: Open directly
Just open `index.html` in any modern web browser.

### Option 2: Local server (recommended)
```bash
cd fontora
python3 -m http.server 8080
# Then visit http://localhost:8080
```

## 📁 Project Structure

```
fontora/
├── index.html           # Main single-page website
├── fonts-data.js        # Font metadata (embedded)
├── fonts_manifest.json  # Full manifest with all font info
├── README.md            # This file
└── fonts/               # 282 font files (.ttf and .woff2)
    ├── lobster.ttf
    ├── great_vibes.ttf
    ├── dancing_script.ttf
    ├── cabin.woff2
    └── ...
```

## 🔍 How to Use

1. **Search** — type in the search bar to find fonts by name
2. **Filter** — click category pills (Script, Display, Serif, etc.)
3. **Preview** — type custom text, adjust size & colors in the preview bar
4. **Sort** — sort by name, category, or file size
5. **Download** — click the download button on any font card
6. **Detail view** — click a font card to see character map and large preview

## 📜 Licensing

All fonts are sourced from [Google Fonts](https://fonts.google.com/) and are licensed under either:
- **SIL Open Font License 1.1** (most fonts)
- **Apache License 2.0**

Both licenses allow free use for personal and commercial projects, including redistribution. See individual font license files for details.

## 🛠️ Technical Details

- **Pure HTML/CSS/JavaScript** — no build tools, frameworks, or dependencies
- **Font Loading API** — uses `FontFace` to load fonts on demand as you scroll
- **Intersection Observer** — fonts load lazily only when near the viewport
- **Vanilla JS** — fast, lightweight (~47KB HTML + 28KB data)
- **CSS Grid** — responsive card layout
- **Local file serving** — all fonts stored in the `fonts/` folder

## 🌐 Adding More Fonts

To add more fonts:
1. Add the `.ttf` or `.woff2` file to the `fonts/` folder
2. Add an entry to `fonts-data.js`:
```javascript
{"n":"Font Name","id":"font-id","f":"fonts/font_file.ttf","c":"category","fmt":"ttf","s":12345}
```
3. Refresh the page

Categories: `script`, `display`, `serif`, `sans-serif`, `monospace`

---

Made with 💜 for designers & developers
