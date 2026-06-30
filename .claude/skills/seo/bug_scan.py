import os, re, json, glob, html
from collections import defaultdict

SITE = "/Users/jackwolfe/Desktop/My WebSites/wolves-storage-sussex"
files = sorted(glob.glob(os.path.join(SITE, "*.html")))
existing = set(os.listdir(SITE))
bugs = defaultdict(list)      # severity-tagged
def bug(sev, page, msg): bugs[sev].append((page, msg))

PAIR_TAGS = ["div","section","a","p","h1","h2","h3","ul","ol","li","button","form","main","nav","span","script","style"]

for f in files:
    name = os.path.basename(f)
    s = open(f, encoding="utf-8").read()

    # 1) tag balance for paired tags
    for tag in PAIR_TAGS:
        opens = len(re.findall(r"<"+tag+r"(?:\s|>|/)", s))
        closes = len(re.findall(r"</"+tag+r">", s))
        if opens != closes:
            bug("STRUCT", name, f"<{tag}> open={opens} close={closes} (Δ{opens-closes})")

    # 2) internal .html links resolve
    for hrefm in re.findall(r'href="([^"]+)"', s):
        h = hrefm.split("#")[0]
        if h.endswith(".html") and not h.startswith("http"):
            tgt = h.lstrip("/")
            if tgt and tgt not in existing:
                bug("LINK", name, f"broken link -> {hrefm}")
        if h == "":
            bug("LINK", name, "empty href=''")

    # 3) images referenced exist + valid
    for srcm in re.findall(r'<img\b[^>]*\bsrc="(/[^"]+)"', s):
        fp = os.path.join(SITE, srcm.lstrip("/"))
        if not os.path.exists(fp):
            bug("IMG", name, f"missing image {srcm}")

    # 4) mixed content
    for m in re.findall(r'(?:src|href)="(http://[^"]+)"', s):
        bug("MIXED", name, m)

    # 5) leaked Python/template artifacts in rendered HTML
    for pat in [r"'\),", r"'\s*\+\s*IMG\(", r"\bNone\b", r"\{t\[", r"&rsquo;s\b\s*'", r"</section>'", r"'<p>", r"\]\)\)", r"\bdict\(", r"x-data=\"\""]:
        for mm in re.findall(pat, s):
            # 'None' can legitimately... no. flag occurrences
            bug("ARTIFACT", name, f"suspicious pattern {pat!r}: ...{mm}...")
            break

    # 6) JSON-LD valid
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(blk)
        except Exception as e: bug("SCHEMA", name, f"invalid JSON-LD: {str(e)[:50]}")

    # 7) FAQ schema == visible
    vis = [html.unescape(x).strip() for x in re.findall(r'faq-q">(.*?)</span>', s)]
    sch = [html.unescape(x).strip() for x in re.findall(r'"@type":\s*"Question",\s*"name":\s*"(.*?)"', s)]
    if vis and set(vis) != set(sch):
        bug("SCHEMA", name, f"FAQ visible({len(vis)})!=schema({len(sch)})")

    # 8) headings
    h1 = re.findall(r"<h1\b", s)
    if len(h1) != 1: bug("HEAD", name, f"{len(h1)} H1")
    # heading order: first heading should be h1; no h3 before any h2 in body
    order = re.findall(r"<h([1-3])\b", s)
    seen2 = False
    for lvl in order:
        if lvl == "2": seen2 = True
        if lvl == "3" and not seen2:
            bug("HEAD", name, "H3 appears before any H2"); break

    # 9) duplicate element IDs (breaks JS/anchors)
    ids = re.findall(r'\bid="([^"]+)"', s)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup: bug("DOMID", name, f"duplicate id(s): {sorted(dup)[:6]}")

    # 10) content imgs missing alt (exclude alpine :alt dynamic)
    for img in re.findall(r"<img\b[^>]*>", s):
        if " :src=" in img or ":alt=" in img:  # dynamic lightbox template
            continue
        if not re.search(r'\balt="', img):
            bug("A11Y", name, f"img missing alt: {img[:60]}")

    # 11) unescaped ampersand (not part of entity)
    body = re.sub(r"<script\b.*?</script>", "", s, flags=re.S)
    for m in re.finditer(r"&(?!#?\w{1,8};)", body):
        seg = body[m.start():m.start()+15]
        bug("ENTITY", name, f"raw '&': ...{seg}...")
        break  # one per page is enough to flag

# home link sanity (R11 change)
idx = open(os.path.join(SITE,"index.html"),encoding="utf-8").read()
if 'href="index.html"' in "".join(open(f,encoding="utf-8").read() for f in files):
    bug("LINK","(site)","href=\"index.html\" still present somewhere")

# recompressed images valid
try:
    from PIL import Image
    for n in ["hero-facility-van.webp","hero-containers-van.webp","hero-fleet.webp","aerial-storage-collection-west-sussex-hero.webp","storage-warehouse-van-west-sussex-hero.webp","hero-packed-container.webp","hero-forklift.webp"]:
        p=os.path.join(SITE,"images",n)
        Image.open(p).verify()
        if os.path.getsize(p) > 200*1024: bug("IMG","(images)",f"{n} still >200KB")
except Exception as e:
    bug("IMG","(images)",f"image verify failed: {e}")

# report
order = ["STRUCT","LINK","IMG","MIXED","ARTIFACT","SCHEMA","HEAD","DOMID","A11Y","ENTITY"]
total = sum(len(v) for v in bugs.values())
print(f"=== STATIC BUG SCAN — {len(files)} pages — {total} findings ===\n")
if not total: print("  NO STATIC BUGS FOUND")
for sev in order:
    if bugs.get(sev):
        print(f"[{sev}] ({len(bugs[sev])})")
        for pg,msg in bugs[sev][:25]: print(f"   - {pg}: {msg}")
        print()
