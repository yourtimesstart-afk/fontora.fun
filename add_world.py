import urllib.request, json, os, re, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

with open("fonts_manifest.json", "r", encoding="utf-8") as f:
    data = json.load(f)
existing_ids = {font["id"] for font in data["fonts"]}

# ===== WORLD LANGUAGE FONTS =====
# Format: (Name, id, category, repo_folder, filename_or_None_for_api)
# If filename is None, use Google Fonts CSS API for WOFF2

world_fonts = [
    # ===== ARABIC (العربية) =====
    ("Noto Naskh Arabic", "noto-naskh-arabic", "arabic", "notonaskharabic", "NotoNaskhArabic%5Bwght%5D.ttf"),
    ("Noto Kufi Arabic", "noto-kufi-arabic", "arabic", "notokufiarabic", "NotoKufiArabic%5Bwght%5D.ttf"),
    ("Amiri", "amiri", "arabic", "amiri", "Amiri-Regular.ttf"),
    ("Cairo", "cairo", "arabic", "cairo", "Cairo%5Bwght%5D.ttf"),
    ("Tajawal", "tajawal", "arabic", "tajawal", "Tajawal-Regular.ttf"),
    ("Almarai", "almarai", "arabic", "almarai", "Almarai-Regular.ttf"),
    ("Mada", "mada", "arabic", "mada", "Mada-Regular.ttf"),
    ("Lateef", "lateef", "arabic", "lateef", "Lateef-Regular.ttf"),
    ("Reem Kufi", "reem-kufi", "arabic", "reemkufi", "ReemKufi%5Bwght%5D.ttf"),
    ("Scheherazade New", "scheherazade-new", "arabic", "scheherazadenew", "ScheherazadeNew-Regular.ttf"),
    ("Markazi Text", "markazi-text", "arabic", "markazitext", "MarkaziText%5Bwght%5D.ttf"),
    ("Aref Ruqaa", "aref-ruqaa", "arabic", "arefruqaa", "ArefRuqaa-Regular.ttf"),
    ("Katibeh", "katibeh", "arabic", "katibeh", "Katibeh-Regular.ttf"),
    ("Rakkas", "rakkas", "arabic", "rakkas", "Rakkas-Regular.ttf"),
    ("Lemonada", "lemonada", "arabic", "lemonada", "Lemonada%5Bwght%5D.ttf"),
    ("Vibes", "vibes", "arabic", "vibes", "Vibes-Regular.ttf"),
    ("Changa Arabic", "changa-arabic", "arabic", "changa", "Changa%5Bwght%5D.ttf"),
    ("Mirza", "mirza", "arabic", "mirza", "Mirza-Regular.ttf"),
    ("Lalezar", "lalezar", "arabic", "lalezar", "Lalezar-Regular.ttf"),
    ("El Messiri", "el-messiri", "arabic", "elmessiri", "ElMessiri-Regular.ttf"),
    ("Jomhuria", "jomhuria", "arabic", "jomhuria", "Jomhuria-Regular.ttf"),
    ("Harmattan", "harmattan", "arabic", "harmattan", "Harmattan-Regular.ttf"),

    # ===== CHINESE SIMPLIFIED (简体中文) =====
    ("Noto Sans SC", "noto-sans-sc", "chinese", "notosanssc", None),
    ("Noto Serif SC", "noto-serif-sc", "chinese", "notoserifsc", None),
    ("ZCOOL XiaoWei", "zcool-xiaowei", "chinese", "zcoolxiaowei", "ZCOOLXiaoWei-Regular.ttf"),
    ("ZCOOL QingKe HuangYou", "zcool-qingke-huangyou", "chinese", "zcoolqingkehuangyou", "ZCOOLQingKeHuangYou-Regular.ttf"),
    ("ZCOOL KuaiLe", "zcool-kuaile", "chinese", "zcoolkuaile", "ZCOOLKuaiLe-Regular.ttf"),
    ("Ma Shan Zheng", "ma-shan-zheng", "chinese", "mashanzheng", "MaShanZheng-Regular.ttf"),
    ("Long Cang", "long-cang", "chinese", "longcang", "LongCang-Regular.ttf"),
    ("Liu Jian Mao Cao", "liu-jian-mao-cao", "chinese", "liujianmaocao", "LiuJianMaoCao-Regular.ttf"),
    ("Zhi Mang Xing", "zhi-mang-xing", "chinese", "zhimangxing", "ZhiMangXing-Regular.ttf"),
    ("ZCOOL KuaiLe", "zcool-kuaile2", "chinese", "zcoolkuaile", "ZCOOLKuaiLe-Regular.ttf"),

    # ===== CHINESE TRADITIONAL (繁體中文) =====
    ("Noto Sans TC", "noto-sans-tc", "chinese-trad", "notosanstc", None),
    ("Noto Serif TC", "noto-serif-tc", "chinese-trad", "notoseriftc", None),

    # ===== JAPANESE (日本語) =====
    ("Noto Sans JP", "noto-sans-jp", "japanese", "notosansjp", None),
    ("Noto Serif JP", "noto-serif-jp", "japanese", "notoserifjp", None),
    ("Klee One", "klee-one", "japanese", "kleeone", "KleeOne-Regular.ttf"),
    ("Zen Kaku Gothic New", "zen-kaku-gothic-new", "japanese", "zenkakugothicnew", "ZenKakuGothicNew-Regular.ttf"),
    ("Zen Maru Gothic", "zen-maru-gothic", "japanese", "zenmarugothic", "ZenMaruGothic-Regular.ttf"),
    ("Zen Old Mincho", "zen-old-mincho", "japanese", "zenoldmincho", "ZenOldMincho-Regular.ttf"),
    ("Zen Kurenaido", "zen-kurenaido", "japanese", "zenkurenaido", "ZenKurenaido-Regular.ttf"),
    ("Dela Gothic One", "dela-gothic-one", "japanese", "delagothicone", "DelaGothicOne-Regular.ttf"),
    ("Hina Mincho", "hina-mincho", "japanese", "hinamincho", "HinaMincho-Regular.ttf"),
    ("Kosugi Maru", "kosugi-maru", "japanese", "kosugimaru", "KosugiMaru-Regular.ttf"),
    ("Kosugi", "kosugi", "japanese", "kosugi", "Kosugi-Regular.ttf"),
    ("M PLUS Rounded 1c", "mplus-rounded-1c", "japanese", "mplusrounded1c", "MPLUSRounded1c-Regular.ttf"),
    ("M PLUS 1p", "mplus-1p", "japanese", "mplus1p", "MPLUS1p-Regular.ttf"),
    ("Rampart One", "rampart-one", "japanese", "rampartone", "RampartOne-Regular.ttf"),
    ("Reggae One", "reggae-one", "japanese", "reggaeone", "ReggaeOne-Regular.ttf"),
    ("RocknRoll One", "rocknroll-one", "japanese", "rocknrollone", "RocknRollOne-Regular.ttf"),
    ("Shippori Mincho", "shippori-mincho", "japanese", "shipporimincho", "ShipporiMincho-Regular.ttf"),
    ("Shippori Mincho B1", "shippori-mincho-b1", "japanese", "shipporiminchob1", "ShipporiMinchoB1-Regular.ttf"),
    ("Yuji Syuku", "yuji-syuku", "japanese", "yujisyuku", "YujiSyuku-Regular.ttf"),
    ("Yuji Boku", "yuji-boku", "japanese", "yujiboku", "YujiBoku-Regular.ttf"),
    ("Yuji Mai", "yuji-mai", "japanese", "yujimai", "YujiMai-Regular.ttf"),

    # ===== KOREAN (한국어) =====
    ("Noto Sans KR", "noto-sans-kr", "korean", "notosanskr", None),
    ("Noto Serif KR", "noto-serif-kr", "korean", "notoserifkr", None),
    ("Black Han Sans", "black-han-sans", "korean", "blackhansans", "BlackHanSans-Regular.ttf"),
    ("Do Hyeon", "do-hyeon", "korean", "dohyeon", "DoHyeon-Regular.ttf"),
    ("Gothic A1", "gothic-a1", "korean", "gothica1", "GothicA1-Regular.ttf"),
    ("Gugi", "gugi", "korean", "gugi", "Gugi-Regular.ttf"),
    ("Hi Melody", "hi-melody", "korean", "himelody", "HiMelody-Regular.ttf"),
    ("Jua", "jua", "korean", "jua", "Jua-Regular.ttf"),
    ("Kirang Haerang", "kirang-haerang", "korean", "kiranghaerang", "KirangHaerang-Regular.ttf"),
    ("Nanum Gothic", "nanum-gothic", "korean", "nanumgothic", "NanumGothic-Regular.ttf"),
    ("Nanum Myeongjo", "nanum-myeongjo", "korean", "nanummyeongjo", "NanumMyeongjo-Regular.ttf"),
    ("Nanum Pen Script", "nanum-pen-script", "korean", "nanumpenscript", "NanumPenScript-Regular.ttf"),
    ("Nanum Brush Script", "nanum-brush-script", "korean", "nanumbrushscript", "NanumBrushScript-Regular.ttf"),
    ("Noto Sans KR", "noto-sans-kr2", "korean", "notosanskr", None),
    ("Single Day", "single-day", "korean", "singleday", "SingleDay-Regular.ttf"),
    ("Song Myung", "song-myung", "korean", "songmyung", "SongMyung-Regular.ttf"),
    ("Stylish", "stylish", "korean", "stylish", "Stylish-Regular.ttf"),
    ("Sunflower", "sunflower", "korean", "sunflower", "Sunflower-Regular.ttf"),
    ("Gowun Dodum", "gowun-dodum", "korean", "gowundodum", "GowunDodum-Regular.ttf"),
    ("Gowun Batang", "gowun-batang", "korean", "gowunbatang", "GowunBatang-Regular.ttf"),
    ("IBM Plex Sans KR", "ibm-plex-sans-kr", "korean", "ibmplexsanskr", "IBMPlexSansKR-Regular.ttf"),

    # ===== THAI (ภาษาไทย) =====
    ("Noto Sans Thai", "noto-sans-thai", "thai", "notosansthai", "NotoSansThai-Regular.ttf"),
    ("Noto Serif Thai", "noto-serif-thai", "thai", "notoserifthai", "NotoSerifThai-Regular.ttf"),
    ("Chakra Petch", "chakra-petch", "thai", "chakrapetch", "ChakraPetch-Regular.ttf"),
    ("Kanit", "kanit", "thai", "kanit", "Kanit-Regular.ttf"),
    ("Mitr", "mitr", "thai", "mitr", "Mitr-Regular.ttf"),
    ("Pridi", "pridi", "thai", "pridi", "Pridi-Regular.ttf"),
    ("Sriracha", "sriracha", "thai", "sriracha", "Sriracha-Regular.ttf"),
    ("Maitree", "maitree", "thai", "maitree", "Maitree-Regular.ttf"),
    ("Athiti", "athiti", "thai", "athiti", "Athiti-Regular.ttf"),
    ("K2D", "k2d", "thai", "k2d", "K2D-Regular.ttf"),
    ("KoHo", "koho", "thai", "koho", "KoHo-Regular.ttf"),
    ("Mali", "mali", "thai", "mali", "Mali-Regular.ttf"),
    ("Niramit", "niramit", "thai", "niramit", "Niramit-Regular.ttf"),
    ("Pattaya", "pattaya", "thai", "pattaya", "Pattaya-Regular.ttf"),
    ("Charm", "charm", "thai", "charm", "Charm-Regular.ttf"),
    ("Charmonman", "charmonman", "thai", "charmonman", "Charmonman-Regular.ttf"),
    ("Thasadith", "thasadith", "thai", "thasadith", "Thasadith-Regular.ttf"),
    ("Itim", "itim", "thai", "itim", "Itim-Regular.ttf"),
    ("Bai Jamjuree", "bai-jamjuree", "thai", "baijamjuree", "BaiJamjuree-Regular.ttf"),
    ("Anuphan", "anuphan", "thai", "anuphan", "Anuphan-Regular.ttf"),
    ("Kadwa", "kadwa", "thai", "kadwa", "Kadwa-Regular.ttf"),
    ("Taviraj", "taviraj", "thai", "taviraj", "Taviraj-Regular.ttf"),
    ("Trirong", "trirong", "thai", "trirong", "Trirong-Regular.ttf"),
    ("Krub", "krub", "thai", "krub", "Krub-Regular.ttf"),
    ("Fahkwang", "fahkwang", "thai", "fahkwang", "Fahkwang-Regular.ttf"),

    # ===== VIETNAMESE (Tiếng Việt) =====
    ("Be Vietnam Pro", "be-vietnam-pro", "vietnamese", "bevietnampro", "BeVietnamPro-Regular.ttf"),
    ("Be Vietnam", "be-vietnam", "vietnamese", "bevietnam", "BeVietnam-Regular.ttf"),
    ("Saira", "saira", "vietnamese", "saira", "Saira-Regular.ttf"),
    ("Saira Condensed", "saira-condensed", "vietnamese", "sairacondensed", "SairaCondensed-Regular.ttf"),
    ("Saira Semi Condensed", "saira-semi-condensed", "vietnamese", "sairasemicondensed", "SairaSemiCondensed-Regular.ttf"),
    ("Saira Stencil One", "saira-stencil-one", "vietnamese", "sairastencilone", "SairaStencilOne-Regular.ttf"),
    ("Saira Extra Condensed", "saira-extra-condensed", "vietnamese", "sairaextracondensed", "SairaExtraCondensed-Regular.ttf"),

    # ===== CYRILLIC / RUSSIAN (Русский) =====
    ("PT Sans", "pt-sans", "cyrillic", "ptsans", "PTSans-Regular.ttf"),
    ("PT Serif", "pt-serif", "cyrillic", "ptserif", "PTSerif-Regular.ttf"),
    ("PT Mono", "pt-mono", "cyrillic", "ptmono", "PTMono-Regular.ttf"),
    ("PT Sans Caption", "pt-sans-caption", "cyrillic", "ptsanscaption", "PTSansCaption-Regular.ttf"),
    ("PT Sans Narrow", "pt-sans-narrow", "cyrillic", "ptsansnarrow", "PTSansNarrow-Regular.ttf"),
    ("PT Serif Caption", "pt-serif-caption", "cyrillic", "ptserifcaption", "PTSerifCaption-Regular.ttf"),
    ("Russo One", "russo-one", "cyrillic", "russoone", "RussoOne-Regular.ttf"),
    ("Ruslan Display", "ruslan-display", "cyrillic", "ruslandisplay", "RuslanDisplay-Regular.ttf"),
    ("Underdog", "underdog", "cyrillic", "underdog", "Underdog-Regular.ttf"),
    ("Yeseva One", "yeseva-one", "cyrillic", "yesevaone", "YesevaOne-Regular.ttf"),
    ("Cuprum", "cuprum", "cyrillic", "cuprum", "Cuprum-Regular.ttf"),
    ("Jura", "jura", "cyrillic", "jura", "Jura-Regular.ttf"),
    ("Istok Web", "istok-web", "cyrillic", "istokweb", "IstokWeb-Regular.ttf"),
    ("Open Sans Cyrillic", "open-sans", "cyrillic", "opensans", "OpenSans-Regular.ttf"),
    ("Roboto Cyrillic", "roboto", "cyrillic", "roboto", "Roboto-Regular.ttf"),
    ("Fira Sans", "fira-sans", "cyrillic", "firasans", "FiraSans-Regular.ttf"),
    ("Oswald Cyrillic", "oswald", "cyrillic", "oswald", "Oswald-Regular.ttf"),
    ("Playfair Display Cyrillic", "playfair-display", "cyrillic", "playfairdisplay", "PlayfairDisplay-Regular.ttf"),
    ("Rubik Cyrillic", "rubik", "cyrillic", "rubik", "Rubik-Regular.ttf"),
    ("Manrope", "manrope", "cyrillic", "manrope", "Manrope-Regular.ttf"),
    ("Jost", "jost", "cyrillic", "jost", "Jost-Regular.ttf"),
    ("Comfortaa Cyrillic", "comfortaa", "cyrillic", "comfortaa", "Comfortaa-Regular.ttf"),
    ("Pangolin", "pangolin", "cyrillic", "pangolin", "Pangolin-Regular.ttf"),
    ("Seymour One", "seymour-one", "cyrillic", "seymourone", "SeymourOne-Regular.ttf"),
    ("Bungee Cyrillic", "bungee", "cyrillic", "bungee", "Bungee-Regular.ttf"),
    ("Marck Script", "marck-script", "cyrillic", "marckscript", "MarckScript-Regular.ttf"),
    ("Bad Script", "bad-script", "cyrillic", "badscript", "BadScript-Regular.ttf"),
    ("Golos Text", "golos-text", "cyrillic", "golostext", "GolosText-Regular.ttf"),
    ("Tenor Sans", "tenor-sans", "cyrillic", "tenorsans", "TenorSans-Regular.ttf"),
    ("Anonymous Pro", "anonymous-pro", "cyrillic", "anonymouspro", "AnonymousPro-Regular.ttf"),
    ("PT Root UI", "pt-root-ui", "cyrillic", "ptrootui", "PTRootUI-Regular.ttf"),

    # ===== GREEK (Ελληνικά) =====
    ("Noto Sans Greek", "noto-sans-greek", "greek", "notosans", None),
    ("Noto Serif Greek", "noto-serif-greek", "greek", "notoserif", None),
    ("GFS Didot", "gfs-didot", "greek", "gfsdidot", "GFSDidot-Regular.ttf"),
    ("GFS Neohellenic", "gfs-neohellenic", "greek", "gfsneohellenic", "GFSNeohellenic-Regular.ttf"),
    ("GFS Bodoni", "gfs-bodoni", "greek", "gfsbodoni", "GFSBodoni-Regular.ttf"),
    ("GFS Artemisia", "gfs-artemisia", "greek", "gfsartemisia", "GFSArtemisia-Regular.ttf"),
    ("Kreon", "kreon", "greek", "kreon", "Kreon-Regular.ttf"),
    ("PlatNomor", "platnomor", "greek", "platnomor", "PlatNomor-Regular.ttf"),

    # ===== HEBREW (עברית) =====
    ("Noto Sans Hebrew", "noto-sans-hebrew", "hebrew", "notosanshebrew", "NotoSansHebrew%5Bwdth,wght%5D.ttf"),
    ("Noto Serif Hebrew", "noto-serif-hebrew", "hebrew", "notoserifhebrew", "NotoSerifHebrew-Regular.ttf"),
    ("Frank Ruhl Libre", "frank-ruhl-libre", "hebrew", "frankruhllibre", "FrankRuhlLibre-Regular.ttf"),
    ("Alef", "alef", "hebrew", "alef", "Alef-Regular.ttf"),
    ("Assistant Hebrew", "assistant", "hebrew", "assistant", "Assistant-Regular.ttf"),
    ("Heebo", "heebo", "hebrew", "heebo", "Heebo-Regular.ttf"),
    ("Rubik Hebrew", "rubik-hebrew", "hebrew", "rubik", "Rubik-Regular.ttf"),
    ("Open Sans Hebrew", "open-sans-hebrew", "hebrew", "opensanshebrew", "OpenSansHebrew-Regular.ttf"),
    ("Arimo Hebrew", "arimo", "hebrew", "arimo", "Arimo-Regular.ttf"),
    ("David Libre", "david-libre", "hebrew", "davidlibre", "DavidLibre-Regular.ttf"),
    ("Bellefair", "bellefair", "hebrew", "bellefair", "Bellefair-Regular.ttf"),
    ("Secular One", "secular-one", "hebrew", "secularone", "SecularOne-Regular.ttf"),
    ("Solitreo", "solitreo", "hebrew", "solitreo", "Solitreo-Regular.ttf"),
    ("Tinos Hebrew", "tinos", "hebrew", "tinos", "Tinos-Regular.ttf"),
    ("Varela Round Hebrew", "varela-round", "hebrew", "varelaround", "VarelaRound-Regular.ttf"),
    ("M PLUS Code Latin", "mplus-code-latin", "hebrew", "mpluscodelatin", "MPLUSCodeLatin-Regular.ttf"),
    ("Pridi Hebrew", "pridi-hebrew", "hebrew", "pridi", "Pridi-Regular.ttf"),

    # ===== KHMER (ភាសាខ្មែរ) =====
    ("Noto Sans Khmer", "noto-sans-khmer", "khmer", "notosanskhmer", "NotoSansKhmer-Regular.ttf"),
    ("Noto Serif Khmer", "noto-serif-khmer", "khmer", "notoserifkhmer", "NotoSerifKhmer-Regular.ttf"),
    ("Kantumruy Pro", "kantumruy-pro", "khmer", "kantumruypro", "KantumruyPro-Regular.ttf"),
    ("Kantumruy", "kantumruy", "khmer", "kantumruy", "Kantumruy-Regular.ttf"),
    ("Moul", "moul", "khmer", "moul", "Moul-Regular.ttf"),
    ("Moul Pali", "moulpali", "khmer", "moulpali", "MoulPali-Regular.ttf"),
    ("Angkor", "angkor", "khmer", "angkor", "Angkor-Regular.ttf"),
    ("Bayon", "bayon", "khmer", "bayon", "Bayon-Regular.ttf"),
    ("Bokor", "bokor", "khmer", "bokor", "Bokor-Regular.ttf"),
    ("Chenla", "chenla", "khmer", "chenla", "Chenla-Regular.ttf"),
    ("Content", "content", "khmer", "content", "Content-Regular.ttf"),
    ("Dangrek", "dangrek", "khmer", "dangrek", "Dangrek-Regular.ttf"),
    ("Fasthand", "fasthand", "khmer", "fasthand", "Fasthand-Regular.ttf"),
    ("Freehand", "freehand", "khmer", "freehand", "Freehand-Regular.ttf"),
    ("Hanuman", "hanuman", "khmer", "hanuman", "Hanuman-Regular.ttf"),
    ("Koulen", "koulen", "khmer", "koulen", "Koulen-Regular.ttf"),
    ("Metal", "metal", "khmer", "metal", "Metal-Regular.ttf"),
    ("Nokora", "nokora", "khmer", "nokora", "Nokora-Regular.ttf"),
    ("Odor Mean Chey", "odor-mean-chey", "khmer", "odormeanchey", "OdorMeanChey-Regular.ttf"),
    ("Preah Vihear", "preah-vihear", "khmer", "preahvihear", "PreahVihear-Regular.ttf"),
    ("Siemreap", "siemreap", "khmer", "siemreap", "Siemreap-Regular.ttf"),
    ("Suwannaphum", "suwannaphum", "khmer", "suwannaphum", "Suwannaphum-Regular.ttf"),
    ("Taprom", "taprom", "khmer", "taprom", "Taprom-Regular.ttf"),

    # ===== LAO (ລາວ) =====
    ("Noto Sans Lao", "noto-sans-lao", "lao", "notosanslao", "NotoSansLao-Regular.ttf"),
    ("Noto Serif Lao", "noto-serif-lao", "lao", "notoseriflao", "NotoSerifLao-Regular.ttf"),
    ("Noto Sans Lao Looped", "noto-sans-lao-looped", "lao", "notosanslaolooped", "NotoSansLaoLooped-Regular.ttf"),
    ("Phetsarath", "phetsarath", "lao", "phetsarath", "Phetsarath-Regular.ttf"),
    ("Lao Sans Pro", "lao-sans-pro", "lao", "laosanspro", "LaoSansPro-Regular.ttf"),

    # ===== MYANMAR / BURMESE (မြန်မာ) =====
    ("Noto Sans Myanmar", "noto-sans-myanmar", "myanmar", "notosansmyanmar", "NotoSansMyanmar-Regular.ttf"),
    ("Noto Serif Myanmar", "noto-serif-myanmar", "myanmar", "notoserifmyanmar", "NotoSerifMyanmar-Regular.ttf"),
    ("Padauk", "padauk", "myanmar", "padauk", "Padauk-Regular.ttf"),
    ("Padauk Book", "padauk-book", "myanmar", "padaukbook", "PadaukBook-Regular.ttf"),

    # ===== SINHALA (සිංහල) =====
    ("Noto Sans Sinhala", "noto-sans-sinhala", "sinhala", "notosanssinhala", "NotoSansSinhala-Regular.ttf"),
    ("Noto Serif Sinhala", "noto-serif-sinhala", "sinhala", "notoserifsinhala", "NotoSerifSinhala-Regular.ttf"),
    ("Abhaya Libre", "abhaya-libre", "sinhala", "abhayalibre", "AbhayaLibre-Regular.ttf"),
    ("Iskoola Pota", "iskoola-pota", "sinhala", "iskoolapota", "IskoolaPota-Regular.ttf"),

    # ===== TIBETAN (བོད་ཡིག) =====
    ("Noto Sans Tibetan", "noto-sans-tibetan", "tibetan", "notosanstibetan", "NotoSansTibetan-Regular.ttf"),
    ("Noto Serif Tibetan", "noto-serif-tibetan", "tibetan", "notoseriftibetan", "NotoSerifTibetan-Regular.ttf"),
    ("Jomolhari", "jomolhari", "tibetan", "jomolhari", "Jomolhari-Regular.ttf"),
    ("Jomolhari ID", "jomolhari-id", "tibetan", "jomolhariid", "JomolhariID-Regular.ttf"),
    ("Dzongkha", "dzongkha", "tibetan", "dzongkha", "Dzongkha-Regular.ttf"),

    # ===== GEORGIAN (ქართული) =====
    ("Noto Sans Georgian", "noto-sans-georgian", "georgian", "notosansgeorgian", "NotoSansGeorgian-Regular.ttf"),
    ("Noto Serif Georgian", "noto-serif-georgian", "georgian", "notoserifgeorgian", "NotoSerifGeorgian-Regular.ttf"),
    ("BPG Nino Mkhedruli", "bpg-nino-mkhedruli", "georgian", "bpgninomkhedruli", "BPGNinoMkhedruli-Regular.ttf"),
    ("BPG Banner", "bpg-banner", "georgian", "bpgbanner", "BPGBanner-Regular.ttf"),

    # ===== ARMENIAN (Հայերեն) =====
    ("Noto Sans Armenian", "noto-sans-armenian", "armenian", "notosansarmenian", "NotoSansArmenian-Regular.ttf"),
    ("Noto Serif Armenian", "noto-serif-armenian", "armenian", "notoserifarmenian", "NotoSerifArmenian-Regular.ttf"),
    ("Aramian", "aramian", "armenian", "aramian", "Aramian-Regular.ttf"),
    ("Arian AMU", "arian-amu", "armenian", "arianamu", "ArianAMU-Regular.ttf"),

    # ===== ETHIOPIC / AMHARIC (አማርኛ) =====
    ("Noto Sans Ethiopic", "noto-sans-ethiopic", "ethiopic", "notosansethiopic", "NotoSansEthiopic-Regular.ttf"),
    ("Noto Serif Ethiopic", "noto-serif-ethiopic", "ethiopic", "notoserifethiopic", "NotoSerifEthiopic-Regular.ttf"),
    ("Abyssinica SIL", "abyssinica-sil", "ethiopic", "abyssinicasil", "AbyssinicaSIL-Regular.ttf"),

    # ===== THAANA / DHIVEHI (ދިވެހި) =====
    ("Noto Sans Thaana", "noto-sans-thaana", "thaana", "notosansthaana", "NotoSansThaana-Regular.ttf"),

    # ===== TIFINAGH (Berber) =====
    ("Noto Sans Tifinagh", "noto-sans-tifinagh", "tifinagh", "notosanstifinagh", "NotoSansTifinagh-Regular.ttf"),

    # ===== CHEROKEE =====
    ("Noto Sans Cherokee", "noto-sans-cherokee", "cherokee", "notosanscherokee", "NotoSansCherokee-Regular.ttf"),

    # ===== CANADIAN ABORIGINAL =====
    ("Noto Sans Canadian Aboriginal", "noto-sans-canadian-aboriginal", "canadian", "notosanscanadianaboriginal", "NotoSansCanadianAboriginal-Regular.ttf"),

    # ===== OGHAM / RUNIC =====
    ("Noto Sans Ogham", "noto-sans-ogham", "ogham", "notosansogham", "NotoSansOgham-Regular.ttf"),
    ("Noto Sans Runic", "noto-sans-runic", "runic", "notosansrunic", "NotoSansRunic-Regular.ttf"),

    # ===== BRAILLE =====
    ("Noto Sans Symbols", "noto-sans-symbols", "symbols", "notosanssymbols", "NotoSansSymbols-Regular.ttf"),

    # ===== THAI additional popular =====
    ("Chonburi", "chonburi", "thai", "chonburi", "Chonburi-Regular.ttf"),
    ("Krub Thai", "krub-thai", "thai", "krub", "Krub-Regular.ttf"),
    ("Fahkwang Thai", "fahkwang-thai", "thai", "fahkwang", "Fahkwang-Regular.ttf"),

    # ===== MORE POPULAR LATIN (worldwide support) =====
    ("Inter", "inter", "latin", "inter", "Inter-Regular.ttf"),
    ("Nunito", "nunito", "latin", "nunito", "Nunito-Regular.ttf"),
    ("Source Sans 3", "source-sans-3", "latin", "sourcesans3", "SourceSans3-Regular.ttf"),
    ("Source Serif 4", "source-serif-4", "latin", "sourceserif4", "SourceSerif4-Regular.ttf"),
    ("Source Code Pro", "source-code-pro", "latin", "sourcecodepro", "SourceCodePro-Regular.ttf"),
    ("JetBrains Mono", "jetbrains-mono", "latin", "jetbrainsmono", "JetBrainsMono-Regular.ttf"),
    ("Fira Code", "fira-code", "latin", "firacode", "FiraCode-Regular.ttf"),
    ("IBM Plex Sans", "ibm-plex-sans", "latin", "ibmplexsans", "IBMPlexSans-Regular.ttf"),
    ("IBM Plex Serif", "ibm-plex-serif", "latin", "ibmplexserif", "IBMPlexSerif-Regular.ttf"),
    ("IBM Plex Mono", "ibm-plex-mono", "latin", "ibmplexmono", "IBMPlexMono-Regular.ttf"),
    ("Space Grotesk", "space-grotesk", "latin", "spacegrotesk", "SpaceGrotesk-Regular.ttf"),
    ("DM Sans", "dm-sans", "latin", "dmsans", "DMSans-Regular.ttf"),
    ("DM Serif Display", "dm-serif-display", "latin", "dmserifdisplay", "DMSerifDisplay-Regular.ttf"),
    ("Syne", "syne", "latin", "syne", "Syne-Regular.ttf"),
    ("Archivo Black", "archivo-black", "latin", "archivoblack", "ArchivoBlack-Regular.ttf"),
    ("Anton", "anton", "latin", "anton", "Anton-Regular.ttf"),
    ("Bebas Neue", "bebas-neue", "latin", "bebasneue", "BebasNeue-Regular.ttf"),
    ("Oswald", "oswald", "latin", "oswald", "Oswald-Regular.ttf"),
    ("Darker Grotesque", "darker-grotesque", "latin", "darkergrotesque", "DarkerGrotesk-Regular.ttf"),
    ("Plus Jakarta Sans", "plus-jakarta-sans", "latin", "plusjakartasans", "PlusJakartaSans-Regular.ttf"),
    ("Outfit", "outfit", "latin", "outfit", "Outfit-Regular.ttf"),
    ("Sora", "sora", "latin", "sora", "Sora-Regular.ttf"),
    ("Lexend", "lexend", "latin", "lexend", "Lexend-Regular.ttf"),
    ("Epilogue", "epilogue", "latin", "epilogue", "Epilogue-Regular.ttf"),
    ("Figtree", "figtree", "latin", "figtree", "Figtree-Regular.ttf"),
    ("Onest", "onest", "latin", "onest", "Onest-Regular.ttf"),
    ("Schibsted Grotesk", "schibsted-grotesk", "latin", "schibstedgrotesk", "SchibstedGrotesk-Regular.ttf"),
    ("Instrument Serif", "instrument-serif", "latin", "instrument-serif", "InstrumentSerif-Regular.ttf"),
    ("Instrument Sans", "instrument-sans", "latin", "instrument-sans", "InstrumentSans-Regular.ttf"),
    ("Geist", "geist", "latin", "geist", "Geist-Regular.ttf"),
    ("Geist Mono", "geist-mono", "latin", "geistmono", "GeistMono-Regular.ttf"),
    ("Bricolage Grotesque", "bricolage-grotesque", "latin", "bricolagegrotesque", "BricolageGrotesk-Regular.ttf"),
    ("Fraunces", "fraunces", "latin", "fraunces", "Fraunces-Regular.ttf"),
    ("Newsreader", "newsreader", "latin", "newsreader", "Newsreader-Regular.ttf"),
    ("Lora", "lora", "latin", "lora", "Lora-Regular.ttf"),
    ("Crimson Pro", "crimson-pro", "latin", "crimsonpro", "CrimsonPro-Regular.ttf"),
    ("Spectral", "spectral", "latin", "spectral", "Spectral-Regular.ttf"),
    ("BioRhyme", "biorhyme", "latin", "biorhyme", "BioRhyme-Regular.ttf"),
    ("BioRhyme Expanded", "biorhyme-expanded", "latin", "biorhymeexpanded", "BioRhymeExpanded-Regular.ttf"),
    ("Maven Pro", "maven-pro", "latin", "mavenpro", "MavenPro-Regular.ttf"),
    ("Overpass", "overpass", "latin", "overpass", "Overpass-Regular.ttf"),
    ("Overpass Mono", "overpass-mono", "latin", "overpassmono", "OverpassMono-Regular.ttf"),
    ("Encode Sans", "encode-sans", "latin", "encodesans", "EncodeSans-Regular.ttf"),
    ("Chivo", "chivo", "latin", "chivo", "Chivo-Regular.ttf"),
    ("Hind", "hind", "latin", "hind", "Hind-Regular.ttf"),
    ("Mukta", "mukta", "latin", "mukta", "Mukta-Regular.ttf"),
    ("Rajdhani", "rajdhani", "latin", "rajdhani", "Rajdhani-Regular.ttf"),
    ("Yantramanav", "yantramanav", "latin", "yantramanav", "Yantramanav-Regular.ttf"),
    ("Teko", "teko", "latin", "teko", "Teko-Regular.ttf"),
    ("Khand", "khand", "latin", "khand", "Khand-Regular.ttf"),
    ("Eczar", "eczar", "latin", "eczar", "Eczar-Regular.ttf"),
    ("Karma", "karma", "latin", "karma", "Karma-Regular.ttf"),
    ("Sumana", "sumana", "latin", "sumana", "Sumana-Regular.ttf"),
    ("Martel", "martel", "latin", "martel", "Martel-Regular.ttf"),
    ("Martel Sans", "martel-sans", "latin", "martelsans", "MartelSans-Regular.ttf"),
    ("Poppins", "poppins", "latin", "poppins", "Poppins-Regular.ttf"),
    ("Montserrat", "montserrat", "latin", "montserrat", "Montserrat-Regular.ttf"),
    ("Raleway", "raleway", "latin", "raleway", "Raleway-Regular.ttf"),
    ("Quicksand", "quicksand", "latin", "quicksand", "Quicksand-Regular.ttf"),
    ("Nunito Sans", "nunito-sans", "latin", "nunitosans", "NunitoSans-Regular.ttf"),
    ("Work Sans", "work-sans", "latin", "worksans", "WorkSans-Regular.ttf"),
    ("Exo 2", "exo-2", "latin", "exo2", "Exo2-Regular.ttf"),
    ("Dosis", "dosis", "latin", "dosis", "Dosis-Regular.ttf"),
    ("Josefin Sans", "josefin-sans", "latin", "josefinsans", "JosefinSans-Regular.ttf"),
    ("Titillium Web", "titillium-web", "latin", "titilliumweb", "TitilliumWeb-Regular.ttf"),
    ("Yanone Kaffeesatz", "yanone-kaffeesatz", "latin", "yanonekaffeesatz", "YanoneKaffeesatz-Regular.ttf"),
    ("Cabin", "cabin", "latin", "cabin", "Cabin-Regular.ttf"),
    ("Varela Round", "varela-round", "latin", "varelaround", "VarelaRound-Regular.ttf"),
    ("Varela", "varela", "latin", "varela", "Varela-Regular.ttf"),
    ("Cairo", "cairo-latin", "latin", "cairo", "Cairo-Regular.ttf"),
    ("Tajawal", "tajawal-latin", "latin", "tajawal", "Tajawal-Regular.ttf"),
    ("Changa", "changa-latin", "latin", "changa", "Changa-Regular.ttf"),
    ("Mada", "mada-latin", "latin", "mada", "Mada-Regular.ttf"),
]

# Filter
to_download = [f for f in world_fonts if f[1] not in existing_ids]
print(f"World fonts to download: {len(to_download)}")

results = list(data["fonts"])
new_count = 0
failed = []

def get_woff2_from_api(name):
    """Get WOFF2 URL from Google Fonts CSS API (for large CJK fonts)."""
    family = name.replace(" ", "+")
    for w in ["400", "400;700"]:
        url = f"https://fonts.googleapis.com/css2?family={family}:wght@{w}&display=swap"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=20)
            css = resp.read().decode("utf-8", errors="ignore")
            # Find the largest woff2 (usually the full font, not subset)
            blocks = css.split("@font-face")
            # For CJK, get the last block (often the full/latin)
            urls = re.findall(r'url\((https?://[^)]+\.woff2)\)', css)
            if urls:
                # Return first - API returns subset based on UA
                return urls[0]
        except Exception:
            continue
    return None

def dl(args):
    name, font_id, category, folder, filename = args
    out_name = font_id.replace("-", "_")
    
    if filename is None:
        # Use API for WOFF2 (large CJK fonts)
        woff2_path = os.path.join("fonts", out_name + ".woff2")
        if os.path.exists(woff2_path) and os.path.getsize(woff2_path) > 5000:
            return (name, font_id, category, "fonts/" + out_name + ".woff2", os.path.getsize(woff2_path), "exists")
        url = get_woff2_from_api(name)
        if url:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                resp = urllib.request.urlopen(req, timeout=60)
                content = resp.read()
                if len(content) > 5000:
                    with open(woff2_path, "wb") as f:
                        f.write(content)
                    return (name, font_id, category, "fonts/" + out_name + ".woff2", len(content), "downloaded")
            except Exception as e:
                return (name, font_id, category, None, 0, f"api-error: {e}")
        return (name, font_id, category, None, 0, "no-api-url")
    
    # TTF download from jsDelivr
    ttf_path = os.path.join("fonts", out_name + ".ttf")
    if os.path.exists(ttf_path) and os.path.getsize(ttf_path) > 5000:
        return (name, font_id, category, "fonts/" + out_name + ".ttf", os.path.getsize(ttf_path), "exists")
    
    for folder_type in ["ofl", "apache", "ufl"]:
        for sub in ["", "static", "variable"]:
            url = f"https://cdn.jsdelivr.net/gh/google/fonts@main/{folder_type}/{folder}"
            if sub:
                url += f"/{sub}"
            url += f"/{filename}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                resp = urllib.request.urlopen(req, timeout=30)
                content = resp.read()
                if len(content) > 5000:
                    with open(ttf_path, "wb") as f:
                        f.write(content)
                    return (name, font_id, category, "fonts/" + out_name + ".ttf", len(content), "downloaded")
            except Exception:
                continue
    
    # Fallback: API WOFF2
    woff2_path = os.path.join("fonts", out_name + ".woff2")
    url = get_woff2_from_api(name)
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=30)
            content = resp.read()
            if len(content) > 2000:
                with open(woff2_path, "wb") as f:
                    f.write(content)
                return (name, font_id, category, "fonts/" + out_name + ".woff2", len(content), "downloaded-woff2")
        except Exception:
            pass
    
    return (name, font_id, category, None, 0, "failed")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(dl, f): f for f in to_download}
    for future in concurrent.futures.as_completed(futures):
        name, font_id, category, filepath, size, status = future.result()
        if filepath:
            fmt = "woff2" if filepath.endswith(".woff2") else "ttf"
            results.append({
                "name": name, "id": font_id, "file": filepath,
                "size": size, "category": category, "format": fmt
            })
            if status.startswith("downloaded"):
                new_count += 1
                print(f"  ✓ {name} ({category}, {fmt}, {size//1024}KB)")
        else:
            failed.append({"name": name, "id": font_id, "category": category})
            print(f"  ✗ {name}: {status}")

# Deduplicate
seen = set()
deduped = []
for f in results:
    if f["id"] not in seen:
        seen.add(f["id"])
        deduped.append(f)

deduped.sort(key=lambda x: (x["category"], x["name"]))
with open("fonts_manifest.json", "w", encoding="utf-8") as f:
    json.dump({"fonts": deduped, "failed": failed, "total": len(deduped)}, f, indent=2, ensure_ascii=False)

# Regenerate data
fonts_js = [{"n":f["n"],"id":f["id"],"f":f["file"],"c":f["category"],"fmt":f.get("format","ttf"),"s":f["size"]} for f in deduped]
with open("fonts-data.js", "w", encoding="utf-8") as f:
    f.write("window.FONTS_DATA = ")
    json.dump(fonts_js, f, ensure_ascii=False, separators=(',', ':'))
    f.write(";")

cats = {}
for f in deduped:
    cats[f["category"]] = cats.get(f["category"], 0) + 1
print(f"\n=== New: {new_count} | Total: {len(deduped)} | Failed: {len(failed)} ===")
for cat in sorted(cats.keys()):
    print(f"  {cat:20s}: {cats[cat]:3d}")
print(f"\nTotal size: {sum(f['size'] for f in deduped)/(1024*1024):.0f} MB")
