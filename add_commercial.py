import urllib.request, json, os, re, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"

with open('fonts_manifest.json') as f:
    data = json.load(f)
existing_ids = {f['id'] for f in data['fonts']}

# Popular commercial-use free fonts from Google Fonts (OFL/Apache - safe for Etsy, Canva, books, weddings)
new_fonts = [
    # Wedding scripts
    ("Alex Brush","alex-brush","wedding","alexbrush","AlexBrush-Regular.ttf"),
    ("Allura","allura","wedding","allura","Allura-Regular.ttf"),
    ("Great Vibes","great-vibes","wedding","greatvibes","GreatVibes-Regular.ttf"),
    ("Parisienne","parisienne","wedding","parisienne","Parisienne-Regular.ttf"),
    ("Italianno","italianno","wedding","italianno","Italianno-Regular.ttf"),
    ("Sacramento","sacramento","wedding","sacramento","Sacramento-Regular.ttf"),
    ("Sofia","sofia","wedding","sofia","Sofia-Regular.ttf"),
    ("Satisfy","satisfy","wedding","satisfy","Satisfy-Regular.ttf"),
    ("Mr De Haviland","mr-de-haviland","wedding","mrdehaviland","MrDeHaviland-Regular.ttf"),
    ("Mrs Saint Delafield","mrs-saint-delafield","wedding","mrssaintdelafield","MrsSaintDelafield-Regular.ttf"),
    ("Mrs Sheppards","mrs-sheppards","wedding","mrssheppards","MrsSheppards-Regular.ttf"),
    ("MonteCarlo","montecarlo","wedding","montecarlo","MonteCarlo-Regular.ttf"),
    ("Petit Formal Script","petit-formal-script","wedding","petitformalscript","PetitFormalScript-Regular.ttf"),
    ("WindSong","windsong","wedding","windsong","WindSong-Regular.ttf"),
    ("Yesteryear","yesteryear","wedding","yesteryear","Yesteryear-Regular.ttf"),
    ("Berkshire Swash","berkshire-swash","wedding","berkshireswash","BerkshireSwash-Regular.ttf"),
    ("Bilbo","bilbo","wedding","bilbo","Bilbo-Regular.ttf"),
    ("Bilbo Swash Caps","bilbo-swash-caps","wedding","bilboswashcaps","BilboSwashCaps-Regular.ttf"),
    ("Caveat","caveat","wedding","caveat","Caveat%5Bwght%5D.ttf"),
    ("Cedarville Cursive","cedarville-cursive","wedding","cedarvillecursive","CedarvilleCursive-Regular.ttf"),
    ("Cherry Swash","cherry-swash","wedding","cherryswash","CherrySwash-Regular.ttf"),
    ("Condiment","condiment","wedding","condiment","Condiment-Regular.ttf"),
    ("Dawning of a New Day","dawning-of-a-new-day","wedding","dawningofanewday","DawningofaNewDay-Regular.ttf"),
    ("Engagement","engagement","wedding","engagement","Engagement-Regular.ttf"),
    ("Felipa","felipa","wedding","felipa","Felipa-Regular.ttf"),
    ("Grand Hotel","grand-hotel","wedding","grandhotel","GrandHotel-Regular.ttf"),
    ("Kaushan Script","kaushan-script","wedding","kaushanscript","KaushanScript-Regular.ttf"),
    ("Kristi","kristi","wedding","kristi","Kristi-Regular.ttf"),
    ("La Belle Aurore","la-belle-aurore","wedding","labelleaurore","LaBelleAurore-Regular.ttf"),
    ("League Script","league-script","wedding","leaguescript","LeagueScript-Regular.ttf"),
    ("Leckerli One","leckerli-one","wedding","leckerlione","LeckerliOne-Regular.ttf"),
    ("Lobster Two","lobster-two","wedding","lobstertwo","LobsterTwo-Regular.ttf"),
    ("Lovers Quarrel","lovers-quarrel","wedding","loversquarrel","LoversQuarrel-Regular.ttf"),
    ("Merienda","merienda","wedding","merienda","Merienda-Regular.ttf"),
    ("Molle","molle","wedding","molle","Molle-Regular.ttf"),
    ("Niconne","niconne","wedding","niconne","Niconne-Regular.ttf"),
    ("Norican","norican","wedding","norican","Norican-Regular.ttf"),
    ("Over the Rainbow","over-the-rainbow","wedding","overtherainbow","OvertheRainbow-Regular.ttf"),
    ("Pacifico","pacifico","wedding","pacifico","Pacifico-Regular.ttf"),
    ("Quintessential","quintessential","wedding","quintessential","Quintessential-Regular.ttf"),
    ("Rancho","rancho","wedding","rancho","Rancho-Regular.ttf"),
    ("Redressed","redressed","wedding","redressed","Redressed-Regular.ttf"),
    ("Rochester","rochester","wedding","rochester","Rochester-Regular.ttf"),
    ("Rock Salt","rock-salt","wedding","rocksalt","RockSalt-Regular.ttf"),
    ("Rouge Script","rouge-script","wedding","rougescript","RougeScript-Regular.ttf"),
    ("Sail","sail","wedding","sail","Sail-Regular.ttf"),
    ("Shadows Into Light","shadows-into-light","wedding","shadowsintolight","ShadowsIntoLight-Regular.ttf"),
    ("Stalemate","stalemate","wedding","stalemate","Stalemate-Regular.ttf"),
    ("The Girl Next Door","the-girl-next-door","wedding","thegirlnextdoor","TheGirlNextDoor-Regular.ttf"),
    ("Vibur","vibur","wedding","vibur","Vibur-Regular.ttf"),
    ("Waiting for the Sunrise","waiting-for-the-sunrise","wedding","waitingforthesunrise","WaitingfortheSunrise-Regular.ttf"),
    ("Walter Turncoat","walter-turncoat","wedding","walterturncoat","WalterTurncoat-Regular.ttf"),
    ("Arizonia","arizonia","wedding","arizonia","Arizonia-Regular.ttf"),
    ("Arapey","arapey","serif","arapey","Arapey-Regular.ttf"),
    # Book/serif
    ("Cardo","cardo","serif","cardo","Cardo-Regular.ttf"),
    ("EB Garamond","eb-garamond","serif","ebgaramond","EBGaramond-Regular.ttf"),
    ("Cormorant Garamond","cormorant-garamond","serif","cormorantgaramond","CormorantGaramond-Regular.ttf"),
    ("Cormorant","cormorant","serif","cormorant","Cormorant-Regular.ttf"),
    ("Cormorant Infant","cormorant-infant","serif","cormorantinfant","CormorantInfant-Regular.ttf"),
    ("Cormorant SC","cormorant-sc","serif","cormorantsc","CormorantSC-Regular.ttf"),
    ("Cormorant Unicase","cormorant-unicase","serif","cormorantunicase","CormorantUnicase-Regular.ttf"),
    ("Cormorant Upright","cormorant-upright","serif","cormorantupright","CormorantUpright-Regular.ttf"),
    ("Crimson Text","crimson-text","serif","crimsontext","CrimsonText-Regular.ttf"),
    ("Crimson Pro","crimson-pro","serif","crimsonpro","CrimsonPro-Regular.ttf"),
    ("Libre Baskerville","libre-baskerville","serif","librebaskerville","LibreBaskerville-Regular.ttf"),
    ("Libre Caslon Display","libre-caslon-display","serif","librecaslondisplay","LibreCaslonDisplay-Regular.ttf"),
    ("Libre Caslon Text","libre-caslon-text","serif","libre caslontext","LibreCaslonText-Regular.ttf"),
    ("Alegreya","alegreya","serif","alegreya","Alegreya-Regular.ttf"),
    ("Alegreya SC","alegreya-sc","serif","alegreyasc","AlegreyaSC-Regular.ttf"),
    ("Vollkorn","vollkorn","serif","vollkorn","Vollkorn-Regular.ttf"),
    ("Gentium Book Plus","gentium-book-plus","serif","gentiumbookplus","GentiumBookPlus-Regular.ttf"),
    ("Gentium Plus","gentium-plus","serif","gentiumplus","GentiumPlus-Regular.ttf"),
    ("Sorts Mill Goudy","sorts-mill-goudy","serif","sortsmillgoudy","SortsMillGoudy-Regular.ttf"),
    ("IM Fell English","im-fell-english","serif","imfellenglish","IMFellEnglish-Regular.ttf"),
    ("IM Fell English SC","im-fell-english-sc","serif","imfellenglishsc","IMFellEnglishSC-Regular.ttf"),
    ("IM Fell DW Pica","im-fell-dw-pica","serif","imfelldwpica","IMFellDWPica-Regular.ttf"),
    ("IM Fell DW Pica SC","im-fell-dw-pica-sc","serif","imfelldwpicasc","IMFellDWPicaSC-Regular.ttf"),
    ("IM Fell Great Primer","im-fell-great-primer","serif","imfellgreatprimer","IMFellGreatPrimer-Regular.ttf"),
    ("IM Fell Great Primer SC","im-fell-great-primer-sc","serif","imfellgreatprimersc","IMFellGreatPrimerSC-Regular.ttf"),
    ("IM Fell French Canon","im-fell-french-canon","serif","imfellfrenchcanon","IMFellFrenchCanon-Regular.ttf"),
    ("IM Fell French Canon SC","im-fell-french-canon-sc","serif","imfellfrenchcanonsc","IMFellFrenchCanonSC-Regular.ttf"),
    ("IM Fell Double Pica","im-fell-double-pica","serif","imfelldoublepica","IMFellDoublePica-Regular.ttf"),
    ("IM Fell Double Pica SC","im-fell-double-pica-sc","serif","imfelldoublepicasc","IMFellDoublePicaSC-Regular.ttf"),
    ("Old Standard TT","old-standard-tt","serif","oldstandardtt","OldStandardTT-Regular.ttf"),
    ("Petrona","petrona","serif","petrona","Petrona-Regular.ttf"),
    ("Rosarivo","rosarivo","serif","rosarivo","Rosarivo-Regular.ttf"),
    ("Sahitya","sahitya","serif","sahitya","Sahitya-Regular.ttf"),
    ("Tienne","tienne","serif","tienne","Tienne-Regular.ttf"),
    ("Trykker","trykker","serif","trykker","Trykker-Regular.ttf"),
    ("Yrsa","yrsa","serif","yrsa","Yrsa-Regular.ttf"),
    ("Marcellus","marcellus","serif","marcellus","Marcellus-Regular.ttf"),
    ("Marcellus SC","marcellus-sc","serif","marcellussc","MarcellusSC-Regular.ttf"),
    ("Mate","mate","serif","mate","Mate-Regular.ttf"),
    ("Mate SC","mate-sc","serif","matesc","MateSC-Regular.ttf"),
    ("Neuton","neuton","serif","neuton","Neuton-Regular.ttf"),
    ("Baskervville","baskervville","serif","baskervville","Baskervville-Regular.ttf"),
    ("Bitter","bitter","serif","bitter","Bitter-Regular.ttf"),
    ("Bona Nova","bona-nova","serif","bonanova","BonaNova-Regular.ttf"),
    ("Bree Serif","bree-serif","serif","breeserif","BreeSerif-Regular.ttf"),
    ("Caesar Dressing","caesar-dressing","display","caesardressing","CaesarDressing-Regular.ttf"),
    ("Caudex","caudex","serif","caudex","Caudex-Regular.ttf"),
    ("Cinzel","cinzel","serif","cinzel","Cinzel-Regular.ttf"),
    ("Cinzel Decorative","cinzel-decorative","display","cinzeldecorative","CinzelDecorative-Regular.ttf"),
    ("Copse","copse","serif","copse","Copse-Regular.ttf"),
    ("Domine","domine","serif","domine","Domine-Regular.ttf"),
    ("Donegal One","donegal-one","serif","donegalone","DonegalOne-Regular.ttf"),
    ("Eczar","eczar","serif","eczar","Eczar-Regular.ttf"),
    ("Enriqueta","enriqueta","serif","enriqueta","Enriqueta-Regular.ttf"),
    ("Esteban","esteban","serif","esteban","Esteban-Regular.ttf"),
    ("Faustina","faustina","serif","faustina","Faustina-Regular.ttf"),
    ("Fenix","fenix","serif","fenix","Fenix-Regular.ttf"),
    ("Gelasio","gelasio","serif","gelasio","Gelasio-Regular.ttf"),
    ("Gilda Display","gilda-display","serif","gildadisplay","GildaDisplay-Regular.ttf"),
    ("Glegoo","glegoo","serif","glegoo","Glegoo-Regular.ttf"),
    ("Gloock","gloock","serif","gloock","Gloock-Regular.ttf"),
    ("Halant","halant","serif","halant","Halant-Regular.ttf"),
    ("Headland One","headland-one","serif","headlandone","HeadlandOne-Regular.ttf"),
    ("Holtwood One SC","holtwood-one-sc","display","holtwoodonesc","HoltwoodOneSC-Regular.ttf"),
    ("Imbue","imbue","serif","imbue","Imbue-Regular.ttf"),
    ("Inria Serif","inria-serif","serif","inriaserif","InriaSerif-Regular.ttf"),
    ("Italiana","italiana","serif","italiana","Italiana-Regular.ttf"),
    ("Jacques Francois","jacques-francois","serif","jacquesfrancois","JacquesFrancois-Regular.ttf"),
    ("Judson","judson","serif","judson","Judson-Regular.ttf"),
    ("Kameron","kameron","serif","kameron","Kameron-Regular.ttf"),
    ("Kotta One","kotta-one","serif","kottaone","KottaOne-Regular.ttf"),
    ("Linden Hill","linden-hill","serif","lindenhill","LindenHill-Regular.ttf"),
    ("Literata","literata","serif","literata","Literata-Regular.ttf"),
    ("Lora","lora","serif","lora","Lora-Regular.ttf"),
    ("Lusitana","lusitana","serif","lusitana","Lusitana-Regular.ttf"),
    ("Lustria","lustria","serif","lustria","Lustria-Regular.ttf"),
    ("Maitree","maitree","thai","maitree","Maitree-Regular.ttf"),
    ("Marcellus 2","marcellus-2","serif","marcellus","Marcellus-Regular.ttf"),
    ("Marko One","marko-one","display","markoone","MarkoOne-Regular.ttf"),
    ("Martel","martel","serif","martel","Martel-Regular.ttf"),
    ("Medula One","medula-one","display","medulaone","MedulaOne-Regular.ttf"),
    ("Merriweather 2","merriweather-2","serif","merriweather","Merriweather-Regular.ttf"),
    ("Mirza","mirza","arabic","mirza","Mirza-Regular.ttf"),
    ("Mogra","mogra","hindi","mogra","Mogra-Regular.ttf"),
    ("Nobile","nobile","sans-serif","nobile","Nobile-Regular.ttf"),
    ("Noto Serif 2","noto-serif-2","serif","notoserif","NotoSerif-Regular.ttf"),
    ("Ovo","ovo","serif","ovo","Ovo-Regular.ttf"),
    ("Palanquin","palanquin","hindi","palanquin","Palanquin-Regular.ttf"),
    ("Patua One","patua-one","display","patuaone","PatuaOne-Regular.ttf"),
    ("Peddana","peddana","telugu","peddana","Peddana-Regular.ttf"),
    ("Philosopher","philosopher","sans-serif","philosopher","Philosopher-Regular.ttf"),
    ("Pirata One","pirata-one","display","pirataone","PirataOne-Regular.ttf"),
    ("Playfair Display SC","playfair-display-sc","serif","playfairdisplaysc","PlayfairDisplaySC-Regular.ttf"),
    ("Podkova","podkova","cyrillic","podkova","Podkova-Regular.ttf"),
    ("Poly","poly","serif","poly","Poly-Regular.ttf"),
    ("Ponnala","ponnala","telugu","ponnala","Ponnala-Regular.ttf"),
    ("Pragati Narrow","pragati-narrow","hindi","pragatinarrow","PragatiNarrow-Regular.ttf"),
    ("Prata","prata","serif","prata","Prata-Regular.ttf"),
    ("Prociono","prociono","serif","prociono","Prociono-Regular.ttf"),
    ("Proza Libre","proza-libre","sans-serif","prozalibre","ProzaLibre-Regular.ttf"),
    ("Puritan","puritan","sans-serif","puritan","Puritan-Regular.ttf"),
    ("Rajdhani","rajdhani","hindi","rajdhani","Rajdhani-Regular.ttf"),
    ("Ramabhadra","ramabhadra","telugu","ramabhadra","Ramabhadra-Regular.ttf"),
    ("Ramaraja","ramaraja","telugu","ramaraja","Ramaraja-Regular.ttf"),
    ("Rasa","rasa","gujarati","rasa","Rasa-Regular.ttf"),
    ("Ravi Prakash","ravi-prakash","telugu","raviprakash","RaviPrakash-Regular.ttf"),
    ("Rhodium Libre","rhodium-libre","serif","rhodiumlibre","RhodiumLibre-Regular.ttf"),
    ("Risque","risque","display","risque","Risque-Regular.ttf"),
    ("Romanesco","romanesco","wedding","romanesco","Romanesco-Regular.ttf"),
    ("Ropa Sans","ropa-sans","sans-serif","ropasans","RopaSans-Regular.ttf"),
    ("Rosario","rosario","sans-serif","rosario","Rosario-Regular.ttf"),
    ("Rozha One","rozha-one","hindi","rozhaone","RozhaOne-Regular.ttf"),
    ("Rufina","rufina","serif","rufina","Rufina-Regular.ttf"),
    ("Rum Raisin","rum-raisin","display","rumraisin","RumRaisin-Regular.ttf"),
    ("Ruslan Display","ruslan-display","cyrillic","ruslandisplay","RuslanDisplay-Regular.ttf"),
    ("Ruthie","ruthie","wedding","ruthie","Ruthie-Regular.ttf"),
    ("Sail 2","sail-2","wedding","sail","Sail-Regular.ttf"),
    ("Salsa","salsa","display","salsa","Salsa-Regular.ttf"),
    ("Sancreek","sancreek","display","sancreek","Sancreek-Regular.ttf"),
    ("Sansita","sansita","display","sansita","Sansita-Regular.ttf"),
    ("Sarabun","sarabun","thai","sarabun","Sarabun-Regular.ttf"),
    ("Sarala","sarala","hindi","sarala","Sarala-Regular.ttf"),
    ("Sarpanch","sarpanch","hindi","sarpanch","Sarpanch-Regular.ttf"),
    ("Satisfy 2","satisfy-2","wedding","satisfy","Satisfy-Regular.ttf"),
    ("Scada","scada","cyrillic","scada","Scada-Regular.ttf"),
    ("Scheherazade New","scheherazade-new","arabic","scheherazadenew","ScheherazadeNew-Regular.ttf"),
    ("Seaweed Script","seaweed-script","wedding","seaweedscript","SeaweedScript-Regular.ttf"),
    ("Secular One","secular-one","hebrew","secularone","SecularOne-Regular.ttf"),
    ("Sevillana","sevillana","wedding","sevillana","Sevillana-Regular.ttf"),
    ("Shanti","shanti","sans-serif","shanti","Shanti-Regular.ttf"),
    ("Siemreap","siemreap","khmer","siemreap","Siemreap-Regular.ttf"),
    ("Sigmar One","sigmar-one","display","sigmarone","SigmarOne-Regular.ttf"),
    ("Sirin Stencil","sirin-stencil","display","sirinstencil","SirinStencil-Regular.ttf"),
    ("Six Caps","six-caps","display","sixcaps","SixCaps-Regular.ttf"),
    ("Slabo 13px","slabo-13px","serif","slabo13px","Slabo13px-Regular.ttf"),
    ("Slabo 27px","slabo-27px","serif","slabo27px","Slabo27px-Regular.ttf"),
    ("Smythe","smythe","display","smythe","Smythe-Regular.ttf"),
    ("Sniglet","sniglet","display","sniglet","Sniglet-Regular.ttf"),
    ("Snippet","snippet","sans-serif","snippet","Snippet-Regular.ttf"),
    ("Sonsie One","sonsie-one","display","sonsieone","SonsieOne-Regular.ttf"),
    ("Sorts Mill Goudy 2","sorts-mill-goudy-2","serif","sortsmillgoudy","SortsMillGoudy-Regular.ttf"),
    ("Spectral SC","spectral-sc","serif","spectralsc","SpectralSC-Regular.ttf"),
    ("Spicy Rice","spicy-rice","display","spicyrice","SpicyRice-Regular.ttf"),
    ("Spinnaker","spinnaker","sans-serif","spinnaker","Spinnaker-Regular.ttf"),
    ("Spirax","spirax","wedding","spirax","Spirax-Regular.ttf"),
    ("Squada One","squada-one","display","squadaone","SquadaOne-Regular.ttf"),
    ("Sree Krushnadevaraya","sree-krushnadevaraya","telugu","sreekrushnadevaraya","SreeKrushnadevaraya-Regular.ttf"),
    ("Stardos Stencil","stardos-stencil","display","stardosstencil","StardosStencil-Regular.ttf"),
    ("Stint Ultra Condensed","stint-ultra-condensed","display","stintultracondensed","StintUltraCondensed-Regular.ttf"),
    ("Stint Ultra Expanded","stint-ultra-expanded","display","stintultraexpanded","StintUltraExpanded-Regular.ttf"),
    ("Suranna","suranna","telugu","suranna","Suranna-Regular.ttf"),
    ("Suravaram","suravaram","telugu","suravaram","Suravaram-Regular.ttf"),
    ("Suwannaphum","suwannaphum","khmer","suwannaphum","Suwannaphum-Regular.ttf"),
    ("Swanky and Moo Moo","swanky-and-moo-moo","wedding","swankyandmoomoo","SwankyandMooMoo-Regular.ttf"),
    ("Syncopate","syncopate","display","syncopate","Syncopate-Regular.ttf"),
    ("Tangerine 2","tangerine-2","wedding","tangerine","Tangerine-Regular.ttf"),
    ("Taprom","taprom","khmer","taprom","Taprom-Regular.ttf"),
    ("Tenali Ramakrishna","tenali-ramakrishna","telugu","tenaliramakrishna","TenaliRamakrishna-Regular.ttf"),
    ("Tenor Sans","tenor-sans","sans-serif","tenorsans","TenorSans-Regular.ttf"),
    ("The Nautigal","the-nautigal","wedding","thenautigal","TheNautigal-Regular.ttf"),
    ("Tienne 2","tienne-2","serif","tienne","Tienne-Regular.ttf"),
    ("Tillana","tillana","hindi","tillana","Tillana-Regular.ttf"),
    ("Timmana","timmana","telugu","timmana","Timmana-Regular.ttf"),
    ("Tiro Devanagari Hindi","tiro-devanagari-hindi","hindi","tirodevanagarihindi","TiroDevanagariHindi-Regular.ttf"),
    ("Tiro Devanagari Marathi","tiro-devanagari-marathi","hindi","tirodevanagarimarathi","TiroDevanagariMarathi-Regular.ttf"),
    ("Tiro Devanagari Sanskrit","tiro-devanagari-sanskrit","hindi","tirodevanagarisanskrit","TiroDevanagariSanskrit-Regular.ttf"),
    ("Tiro Gurmukhi","tiro-gurmukhi","punjabi","tirogurmukhi","TiroGurmukhi-Regular.ttf"),
    ("Tiro Gujarati","tiro-gujarati","gujarati","tirogujarati","TiroGujarati-Regular.ttf"),
    ("Tiro Kannada","tiro-kannada","kannada","tirokannada","TiroKannada-Regular.ttf"),
    ("Tiro Tamil","tiro-tamil","tamil","tirotamil","TiroTamil-Regular.ttf"),
    ("Tiro Telugu","tiro-telugu","telugu","tirotelugu","TiroTelugu-Regular.ttf"),
    ("Tiro Bangla","tiro-bangla","bengali","tirobangla","TiroBangla-Regular.ttf"),
    ("Tiro Malayalam","tiro-malayalam","malayalam","tiromalayalam","TiroMalayalam-Regular.ttf"),
    ("Tiro Odia","tiro-odia","odia","tiroodia","TiroOdia-Regular.ttf"),
    ("Titan One","titan-one","display","titanone","TitanOne-Regular.ttf"),
    ("Trade Winds","trade-winds","display","tradewinds","TradeWinds-Regular.ttf"),
    ("Train One","train-one","japanese","trainone","TrainOne-Regular.ttf"),
    ("Trirong","trirong","thai","trirong","Trirong-Regular.ttf"),
    ("Trocchi 2","trocchi-2","wedding","trocchi","Trocchi-Regular.ttf"),
    ("Trochut","trochut","display","trochut","Trochut-Regular.ttf"),
    ("Trykker 2","trykker-2","serif","trykker","Trykker-Regular.ttf"),
    ("Tulpen One","tulpen-one","display","tulpenone","TulpenOne-Regular.ttf"),
    ("Ubuntu Condensed","ubuntu-condensed","sans-serif","ubuntucondensed","UbuntuCondensed-Regular.ttf"),
    ("Ultra","ultra","serif","ultra","Ultra-Regular.ttf"),
    ("Uncial Antiqua","uncial-antiqua","display","uncialantiqua","UncialAntiqua-Regular.ttf"),
    ("Underdog","underdog","cyrillic","underdog","Underdog-Regular.ttf"),
    ("Unica One","unica-one","display","unicaone","UnicaOne-Regular.ttf"),
    ("UnifrakturMaguntia","unifrakturmaguntia2","display","unifrakturmaguntia","UnifrakturMaguntia-Regular.ttf"),
    ("UnifrakturCook","unifrakturcook2","display","unifrakturcook","UnifrakturCook-Bold.ttf"),
    ("Unlock","unlock","display","unlock","Unlock-Regular.ttf"),
    ("Unna","unna","serif","unna","Unna-Regular.ttf"),
    ("Updock","updock","wedding","updock","Updock-Regular.ttf"),
    ("Vampiro One","vampiro-one","display","vampiroone","VampiroOne-Regular.ttf"),
    ("Vast Shadow","vast-shadow","display","vastshadow","VastShadow-Regular.ttf"),
    ("Vesper Libre","vesper-libre","serif","vesperlibre","VesperLibre-Regular.ttf"),
    ("Vibes","vibes","arabic","vibes","Vibes-Regular.ttf"),
    ("Vidaloka","vidaloka","serif","vidaloka","Vidaloka-Regular.ttf"),
    ("Viga","viga","sans-serif","viga","Viga-Regular.ttf"),
    ("Voces","voces","latin","voces","Voces-Regular.ttf"),
    ("Volkhov","volkhov","serif","volkhov","Volkhov-Regular.ttf"),
    ("Vollkorn SC","vollkorn-sc","serif","vollkornsc","VollkornSC-Regular.ttf"),
    ("Voltaire","voltaire","sans-serif","voltaire","Voltaire-Regular.ttf"),
    ("Waiting for the Sunrise 2","waiting-for-the-sunrise-2","wedding","waitingforthesunrise","WaitingfortheSunrise-Regular.ttf"),
    ("Wallpoet","wallpoet","display","wallpoet","Wallpoet-Regular.ttf"),
    ("Warnes","warnes","display","warnes","Warnes-Regular.ttf"),
    ("Wellfleet","wellfleet","display","wellfleet","Wellfleet-Regular.ttf"),
    ("Wendy One","wendy-one","display","wendyone","WendyOne-Regular.ttf"),
    ("Wire One","wire-one","display","wireone","WireOne-Regular.ttf"),
    ("Xanh Mono","xanh-mono","monospace","xanhmono","XanhMono-Regular.ttf"),
    ("Yaldevi","yaldevi","sinhala","yaldevi","Yaldevi-Regular.ttf"),
    ("Yanone Kaffeesatz","yanone-kaffeesatz","display","yanonekaffeesatz","YanoneKaffeesatz-Regular.ttf"),
    ("Yantramanav 2","yantramanav-2","hindi","yantramanav","Yantramanav-Regular.ttf"),
    ("Yatra One","yatra-one","hindi","yatraone","YatraOne-Regular.ttf"),
    ("Yellowtail","yellowtail","wedding","yellowtail","Yellowtail-Regular.ttf"),
    ("Yeseva One","yeseva-one","display","yesevaone","YesevaOne-Regular.ttf"),
    ("Yesteryear 2","yesteryear-2","wedding","yesteryear","Yesteryear-Regular.ttf"),
    ("ZCOOL KuaiLe","zcool-kuaile","chinese","zcoolkuaile","ZCOOLKuaiLe-Regular.ttf"),
    ("ZCOOL QingKe HuangYou","zcool-qingke-huangyou","chinese","zcoolqingkehuangyou","ZCOOLQingKeHuangYou-Regular.ttf"),
    ("ZCOOL XiaoWei","zcool-xiaowei","chinese","zcoolxiaowei","ZCOOLXiaoWei-Regular.ttf"),
    ("Zen Antique","zen-antique","japanese","zenantique","ZenAntique-Regular.ttf"),
    ("Zen Antique Soft","zen-antique-soft","japanese","zenantiquesoft","ZenAntiqueSoft-Regular.ttf"),
    ("Zen Dots","zen-dots","display","zendots","ZenDots-Regular.ttf"),
    ("Zen Kaku Gothic Antique","zen-kaku-gothic-antique","japanese","zenkakugothicantique","ZenKakuGothicAntique-Regular.ttf"),
    ("Zen Kaku Gothic New","zen-kaku-gothic-new","japanese","zenkakugothicnew","ZenKakuGothicNew-Regular.ttf"),
    ("Zen Kurenaido","zen-kurenaido","japanese","zenkurenaido","ZenKurenaido-Regular.ttf"),
    ("Zen Loop","zen-loop","japanese","zenloop","ZenLoop-Regular.ttf"),
    ("Zen Maru Gothic","zen-maru-gothic","japanese","zenmarugothic","ZenMaruGothic-Regular.ttf"),
    ("Zen Old Mincho","zen-old-mincho","japanese","zenoldmincho","ZenOldMincho-Regular.ttf"),
    ("Zen Tokyo Zoo","zen-tokyo-zoo","display","zentokyozoo","ZenTokyoZoo-Regular.ttf"),
    ("Zeyada","zeyada","wedding","zeyada","Zeyada-Regular.ttf"),
    ("Zhi Mang Xing","zhi-mang-xing","chinese","zhimangxing","ZhiMangXing-Regular.ttf"),
    ("Zilla Slab","zilla-slab","serif","zillaslab","ZillaSlab-Regular.ttf"),
    ("Zilla Slab Highlight","zilla-slab-highlight","display","zillaslabhighlight","ZillaSlabHighlight-Regular.ttf"),
]

# Deduplicate
to_download = [(n, fid, cat, folder, fname) for n, fid, cat, folder, fname in new_fonts if fid not in existing_ids]
print(f"Candidates: {len(new_fonts)}, unique new: {len(to_download)}")

def download_font(item):
    name, fid, cat, folder, filename = item
    out_path = f"fonts/{fid.replace('-','_')}.ttf"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        return (name, fid, cat, os.path.getsize(out_path), 'exists')
    for prefix in ['ofl','apache','ufl']:
        url = f"https://cdn.jsdelivr.net/gh/google/fonts@main/{prefix}/{folder}/{filename}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
            if len(data) > 5000:
                with open(out_path, 'wb') as f:
                    f.write(data)
                return (name, fid, cat, len(data), 'downloaded')
        except Exception:
            pass
    # WOFF2 fallback
    try:
        api_url = f"https://fonts.googleapis.com/css2?family={name.replace(' ','+')}:wght@400&display=swap"
        req = urllib.request.Request(api_url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            css = resp.read().decode('utf-8', errors='ignore')
        urls = re.findall(r'url\((https://[^)]+\.woff2)\)', css)
        if urls:
            req2 = urllib.request.Request(urls[0], headers={'User-Agent': UA})
            with urllib.request.urlopen(req2, timeout=25) as resp2:
                wdata = resp2.read()
            out_w = f"fonts/{fid.replace('-','_')}.woff2"
            with open(out_w, 'wb') as f:
                f.write(wdata)
            return (name, fid, cat, len(wdata), 'woff2')
    except Exception:
        pass
    return (name, fid, cat, 0, 'failed')

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as ex:
    for r in ex.map(download_font, to_download):
        results.append(r)

ok = [r for r in results if r[4] in ('downloaded','woff2','exists')]
fail = [r for r in results if r[4] == 'failed']
print(f"\nOK: {len(ok)}, Failed: {len(fail)}")

added = 0
for name, fid, cat, size, status in ok:
    if fid in existing_ids:
        continue
    ext = 'woff2' if status == 'woff2' else 'ttf'
    fpath = f"fonts/{fid.replace('-','_')}.{ext}"
    if not os.path.exists(fpath):
        fpath = f"fonts/{fid.replace('-','_')}.ttf"
    if not os.path.exists(fpath):
        continue
    data['fonts'].append({
        'name': name, 'id': fid, 'file': fpath,
        'size': os.path.getsize(fpath),
        'category': cat, 'format': ext
    })
    existing_ids.add(fid)
    added += 1

data['total'] = len(data['fonts'])
with open('fonts_manifest.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

fonts_js = []
for f in data['fonts']:
    entry = {"n": f["name"], "id": f["id"], "f": f["file"],
             "c": f["category"], "fmt": f.get("format","ttf"), "s": f["size"]}
    if f.get("cdn"): entry["cdn"] = f["cdn"]
    if f.get("subsets"): entry["sub"] = f["subsets"]
    fonts_js.append(entry)
with open('fonts-data.js', 'w') as f:
    f.write("window.FONTS_DATA = ")
    json.dump(fonts_js, f, ensure_ascii=False, separators=(',',':'))
    f.write(";")

print(f"Added {added} new fonts. Total: {len(data['fonts'])}")
cats = {}
for f in data['fonts']:
    cats[f['category']] = cats.get(f['category'], 0) + 1
for c in sorted(cats.keys(), key=lambda x: -cats[x]):
    print(f"  {c:20s}: {cats[c]:4d}")
