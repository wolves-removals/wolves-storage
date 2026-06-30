import os, re, json, glob, html
from collections import defaultdict

SITE = "/Users/jackwolfe/Desktop/My WebSites/wolves-storage-sussex"
DOMAIN = "sussexstoragecompany.co.uk"
files = sorted(glob.glob(os.path.join(SITE, "*.html")))
F = {os.path.basename(f): open(f, encoding="utf-8").read() for f in files}
existing = set(os.listdir(SITE))

def txt(tag_html):
    return re.sub(r"<[^>]+>", "", tag_html)

# ---- tier classification for word floors (R12) ----
def tier(name):
    if name in ("contact.html","privacy-policy.html","terms.html","gallery.html","404.html"):
        return ("exempt", 0)
    if re.match(r"storage-[a-z-]+\.html$", name) and name not in (
        "storage-solutions.html","storage-size-guide.html"):
        return ("location", 1500)
    if name in ("about.html","pricing.html","index.html"):
        return ("pillar", 1200)
    if name in ("storage-solutions.html","long-term-storage.html","short-term-storage.html",
                "business-storage.html","furniture-storage.html","how-it-works.html",
                "storage-size-guide.html"):
        return ("service", 1000)
    if name in ("areas-we-cover.html","reviews.html"):
        return ("nav-hub", 700)
    return ("other", 0)

def main_text_wordcount(s):
    m = re.search(r"<main\b[^>]*>(.*?)</main>", s, re.S)
    body = m.group(1) if m else s
    body = re.sub(r"<script\b.*?</script>", " ", body, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<svg\b.*?</svg>", " ", body, flags=re.S)
    # strip the calculator UI (inflates counts) if present
    body = re.sub(r'<section[^>]*>(?:(?!</section>).)*?data-scalc.*?</section>', " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    words = re.findall(r"[A-Za-z0-9£&'-]+", body)
    return len(words)

GENERIC_ANCHORS = {"click here","read more","learn more","here","more","find out more",
                   "this page","link","click","details","info"}

# accumulators
issues = defaultdict(list)   # rule -> list of (page, detail)
warns  = defaultdict(list)
titles, metas, h1s = {}, {}, {}

for name, s in F.items():
    is404 = name == "404.html"
    legacy = False
    # R1
    if "charset" not in s.lower(): issues["R1 head"].append((name,"missing charset"))
    if "viewport" not in s.lower(): issues["R1 head"].append((name,"missing viewport"))
    if not re.search(r"<html[^>]*\blang=", s): issues["R1 head"].append((name,"missing html lang"))
    # R2 title
    tm = re.search(r"<title>(.*?)</title>", s, re.S)
    t = html.unescape(tm.group(1)).strip() if tm else ""
    titles[name]=t
    if not t: issues["R2 title"].append((name,"missing title"))
    else:
        if len(t) > 65: issues["R2 title"].append((name,f"len {len(t)} >65: {t}"))
        elif len(t) > 60: warns["R2 title >60"].append((name,f"len {len(t)}: {t}"))
    # R3 meta
    mm = re.search(r'<meta\s+name="description"\s+content="(.*?)">', s, re.S)
    md = html.unescape(mm.group(1)).strip() if mm else ""
    metas[name]=md
    if not md: issues["R3 meta"].append((name,"missing meta description"))
    elif not is404:
        if len(md) > 160: issues["R3 meta"].append((name,f"len {len(md)} >160"))
        elif len(md) > 145: warns["R3 meta 146-160"].append((name,f"len {len(md)}"))
        elif len(md) < 140: warns["R3 meta <140"].append((name,f"len {len(md)}"))
    # R4 h1
    hh = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    h1s[name]=[txt(x).strip() for x in hh]
    if len(hh)!=1: issues["R4 h1"].append((name,f"{len(hh)} H1s"))
    # R5 canonical
    cm = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', s)
    can = cm.group(1) if cm else ""
    if not can: issues["R5 canonical"].append((name,"missing canonical"))
    else:
        exp = f"https://www.{DOMAIN}/" + ("" if name=="index.html" else name)
        if can != exp: warns["R5 canonical mismatch"].append((name,f"{can} (exp {exp})"))
    # R6 OG/twitter
    for need in ['og:title','og:url','og:image','twitter:card']:
        if f'"{need}"' not in s and f"'{need}'" not in s and f'property="{need}"' not in s and f'name="{need}"' not in s:
            issues["R6 OG/twitter"].append((name,f"missing {need}"))
    ogi = re.search(r'(?:property|name)="og:image"\s+content="(.*?)"', s)
    if ogi:
        u=ogi.group(1)
        if not u.startswith("http"): issues["R6 OG/twitter"].append((name,"og:image not absolute"))
        elif DOMAIN not in u: warns["R6 og:image off-domain"].append((name,u))
    # R7 JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    types=set()
    for b in blocks:
        try:
            data=json.loads(b)
        except Exception as e:
            issues["R7 JSON-LD invalid"].append((name,str(e)[:60])); continue
        for obj in (data if isinstance(data,list) else [data]):
            tt=obj.get("@type") if isinstance(obj,dict) else None
            if isinstance(tt,list): types.update(tt)
            elif tt: types.add(tt)
    if not ({"LocalBusiness","SelfStorage","MovingCompany"} & types):
        warns["R7 no LocalBusiness/SelfStorage"].append((name,sorted(types)))
    # R8 images alt/width/height + R10 exists + R16 size + R19 filename + R11 http
    for img in re.findall(r"<img\b[^>]*>", s):
        src = (re.search(r'src="(.*?)"', img) or [None,""])[1]
        if not re.search(r'\balt="', img): issues["R8 img alt"].append((name,src or img[:50]))
        elif re.search(r'\balt=""', img): warns["R8 empty alt"].append((name,src))
        if not re.search(r'\bwidth="', img) or not re.search(r'\bheight="', img):
            issues["R8 img w/h"].append((name,src))
        if src.startswith("http://"): issues["R11 mixed-content"].append((name,src))
        # local file checks
        if src.startswith("/"):
            fp = os.path.join(SITE, src.lstrip("/"))
            if not os.path.exists(fp):
                # may have data-fallback; still flag missing primary
                issues["R10 missing image"].append((name,src))
            else:
                kb = os.path.getsize(fp)/1024
                if kb > 200: warns["R16 image >200KB"].append((name,f"{src} {kb:.0f}KB"))
                base=os.path.basename(src)
                if re.match(r"(IMG[_-]|DSC|\d+\.)", base) or re.match(r"^\d+", base):
                    warns["R19 img filename"].append((name,base))
    # R10 internal links + R11 index.html + R15 anchor text
    for a in re.findall(r"<a\b[^>]*>.*?</a>", s, re.S):
        href=(re.search(r'href="(.*?)"', a) or [None,""])[1]
        atext=txt(a).strip().lower()
        if href.startswith("http://") and DOMAIN in href:
            issues["R11 mixed-content"].append((name,href))
        if re.search(r'(^|/)index\.html', href):
            issues["R11 link to index.html"].append((name,href))
        if href.endswith(".html") and not href.startswith("http"):
            tgt=href.split("#")[0].lstrip("/")
            if tgt and tgt not in existing:
                issues["R10 broken link"].append((name,href))
        if atext in GENERIC_ANCHORS:
            issues["R15 generic anchor"].append((name,f'"{atext}" -> {href}'))
        if href and not atext and not re.search(r"aria-label", a):
            warns["R15 empty link text"].append((name,href))
    # R9 duplicate content image on same page
    srcs=[m for m in re.findall(r'<img\b[^>]*\bsrc="(/images/[^"]+)"', s)]
    seen=defaultdict(int)
    for sc in srcs:
        if any(k in sc for k in ("logo","placeholder","icon","process/")): continue
        seen[sc]+=1
    for sc,c in seen.items():
        if c>1: warns["R9 dup photo on page"].append((name,f"{sc} x{c}"))
    # R13 FAQ schema on location pages + FAQ==visible everywhere
    vis=[html.unescape(x).strip() for x in re.findall(r'faq-q">(.*?)</span>', s)]
    sch=[html.unescape(x).strip() for x in re.findall(r'"@type":\s*"Question",\s*"name":\s*"(.*?)"', s)]
    tier_name=tier(name)[0]
    if tier_name=="location" and not sch:
        issues["R13 FAQPage on location"].append((name,"no FAQPage schema"))
    if vis and set(vis)!=set(sch):
        issues["R13 FAQ visible!=schema"].append((name,f"{len(vis)} vis / {len(sch)} sch"))
    # R14 tel links
    if re.search(r"01903\s?893731", txt(s)) and "tel:" not in s:
        warns["R14 tel link"].append((name,"phone shown but no tel: link"))
    # R17 noindex
    ni = "noindex" in s
    allowed = is404 or name in ("home.html","quote.html")
    if ni and not allowed: issues["R17 noindex"].append((name,"noindex on indexable page"))
    if (not ni) and is404: issues["R17 noindex"].append((name,"404 NOT noindex"))
    # R12 word floor
    tn, floor = tier(name)
    if floor:
        wc = main_text_wordcount(s)
        infl = " (calc-inflated)" if name in ("pricing.html","storage-size-guide.html") else ""
        if wc < floor:
            issues["R12 word floor"].append((name,f"{tn}: {wc} < {floor}{infl}"))
        elif wc < floor*1.1:
            warns["R12 word near-floor"].append((name,f"{tn}: {wc} (floor {floor})"))

# uniqueness (R2/R3/R4)
def dups(d):
    rev=defaultdict(list)
    for k,v in d.items():
        if v: rev[v].append(k)
    return {v:ks for v,ks in rev.items() if len(ks)>1}
for v,ks in dups(titles).items(): issues["R2 title NOT unique"].append((",".join(ks),v[:50]))
for v,ks in dups(metas).items(): issues["R3 meta NOT unique"].append((",".join(ks),v[:50]))
flat_h1={n:(h[0] if h else "") for n,h in h1s.items()}
for v,ks in dups(flat_h1).items(): issues["R4 h1 NOT unique"].append((",".join(ks),v[:50]))

# sitemap / llms coverage
sm=open(os.path.join(SITE,"sitemap.xml")).read() if os.path.exists(os.path.join(SITE,"sitemap.xml")) else ""
indexable=[n for n in F if n!="404.html"]
missing_sm=[n for n in indexable if n not in sm and not (n=="index.html" and f"www.{DOMAIN}/</loc" in sm or f'www.{DOMAIN}/<' in sm)]
# ---- report ----
print("="*70); print(f"SEO SCAN — {len(F)} pages"); print("="*70)
total_iss=sum(len(v) for v in issues.values())
total_warn=sum(len(v) for v in warns.values())
print(f"\nHARD ISSUES: {total_iss}   |   WARNINGS: {total_warn}\n")
print("----- HARD ISSUES (R-rule failures) -----")
if not issues: print("  NONE")
for rule in sorted(issues):
    print(f"\n[{rule}]  ({len(issues[rule])})")
    for pg,det in issues[rule][:30]:
        print(f"   - {pg}: {det}")
print("\n----- WARNINGS -----")
for rule in sorted(warns):
    print(f"\n[{rule}]  ({len(warns[rule])})")
    for pg,det in warns[rule][:30]:
        print(f"   - {pg}: {det}")
print("\n----- COVERAGE -----")
print(f"sitemap.xml present: {bool(sm)} | pages possibly missing from sitemap: {missing_sm}")
