#!/usr/bin/env python3
# Deterministic generator: rebuilds the 4 storage pages to mirror the
# wolves-removals /services/storage/ 21-row layout, with page-specific copy.
# Shares head/header/footer partials from an existing page so brand chrome
# (overlapping logo, Barlow, colour tokens, WebP) stays identical.
import re, json, os

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.wolvesstoragesussex.co.uk/"

# ---------- pull shared partials from an existing brand-matched page ----------
src = open(os.path.join(SITE, "contact.html"), encoding="utf-8").read()
head_full, after_head = src.split("</head>", 1)
blocks = list(re.finditer(r'<script type="application/ld\+json">[\s\S]*?</script>', head_full))
head_base = head_full[:blocks[1].start()].rstrip() if len(blocks) >= 2 else head_full
bstart = after_head.index('<main id="main">')
HEADER = after_head[:bstart]
FOOTER = after_head.split("</main>", 1)[1]

# ---------- tiny inline SVG helpers ----------
CHK = '<svg class="w-5 h-5 text-green-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/></svg>'
CHKW = CHK.replace('text-green-500', 'text-green-400')
def ic(path, cls="w-7 h-7"):
    return f'<svg class="{cls}" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="{path}"/></svg>'
I_SHIELD = ic("M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6l7-3z")
I_LOCK = ic("M16 11V7a4 4 0 00-8 0v4M6 11h12v9H6z")
I_CAM = ic("M3 8h3l2-2h8l2 2h3v11H3zM12 17a3.5 3.5 0 100-7 3.5 3.5 0 000 7z")
I_TRUCK = ic("M3 7h11v8H3zM14 10h4l3 3v2h-7zM7 18a2 2 0 100-4 2 2 0 000 4zM18 18a2 2 0 100-4 2 2 0 000 4z")
I_BOX = ic("M3 7l9-4 9 4-9 4-9-4zM3 7v10l9 4 9-4V7M12 11v10")
I_POUND = ic("M8 20h9M9 20c2-2 2-4 1-6M7 12h6M8 12c-1-2-1-5 2-6s5 1 5 3")
I_CLOCK = ic("M12 7v5l3 2M21 12a9 9 0 11-18 0 9 9 0 0118 0z")
I_KEY = ic("M15 7a4 4 0 11-3.5 6L7 17H4v-3l5.5-5.5A4 4 0 0115 7z")
I_HOME = ic("M3 11l9-7 9 7M5 10v10h14V10")
I_HAND = ic("M5 11l4 4 10-10")
I_SURVEY = ic("M9 12h6M9 16h6M9 8h6M5 4h14v16H5zM9 4v0")

def img(src, alt, cls, eager=False):
    load = "" if eager else ' loading="lazy"'
    fp = ' fetchpriority="high"' if eager else ""
    fb = src if src.startswith("placeholder") else "placeholder-4x3.svg"
    return (f'<img src="images/{src}" alt="{alt}"{load} decoding="async"{fp} '
            f'data-fallback="images/{fb}" class="{cls}">')

ORANGE_BTN = ('inline-flex items-center justify-center gap-2 bg-amber-400 hover:bg-amber-500 '
              'text-white font-bold uppercase tracking-wider px-7 py-3.5 rounded-full shadow-lg transition')
GHOST_DARK = ('inline-flex items-center gap-2 border border-white/30 text-white hover:bg-white/10 '
              'font-semibold px-6 py-3.5 rounded-full transition')
NAVY_BTN = ('inline-flex items-center justify-center gap-2 bg-navy-800 hover:bg-navy-900 text-white '
            'font-bold uppercase tracking-wider px-7 py-3.5 rounded-full shadow-lg transition')

def H2(t, dark=False):
    c = "text-white" if dark else "text-navy-800"
    return f'<h2 class="font-display text-3xl md:text-4xl font-extrabold {c} leading-tight">{t}</h2>'
def EY(t):
    return f'<p class="text-amber-600 font-bold uppercase tracking-wider text-sm mb-3">{t}</p>'
def sec(bg, inner, extra=""):
    return f'<section class="relative {bg} w-full py-12 lg:py-20 border-b border-[#E7E7E7] overflow-hidden {extra}"><div class="max-w-6xl mx-auto px-5">{inner}</div></section>'

# ---------- shared rows ----------
def breadcrumb(d):
    return (f'<nav class="bg-[#F9F8F6] border-b border-[#E7E7E7]" aria-label="Breadcrumb"><div class="max-w-6xl mx-auto px-5 py-3 text-sm text-slate-500">'
            f'<a href="index.html" class="hover:text-navy-800">Home</a> <span class="mx-1.5">/</span> '
            f'<span class="text-navy-800 font-medium">{d["nav"]}</span></div></nav>')

def hero(d):
    checks = "".join(f'<li class="flex items-start gap-3">{CHKW}<span class="text-slate-100">{x}</span></li>' for x in d["checks"])
    return ('<section class="relative overflow-hidden min-h-[30rem] lg:min-h-[36rem] flex items-center bg-navy-800">'
            f'{img(d["hero"], d["heroAlt"], "absolute inset-0 w-full h-full object-cover", eager=True)}'
            '<div class="absolute inset-0 hero-overlay"></div>'
            '<div class="relative w-full max-w-6xl mx-auto px-5 py-20 md:py-24 text-white">'
            f'{EY(d["eyebrow"])}'
            f'<h1 class="font-display text-4xl md:text-6xl font-extrabold leading-tight text-shadow max-w-3xl reveal">{d["h1"]}</h1>'
            f'<p class="mt-5 text-lg md:text-xl text-slate-100 leading-relaxed max-w-2xl reveal" data-delay="1">{d["sub"]}</p>'
            '<div class="mt-6 inline-flex items-center gap-3 bg-white rounded-xl shadow-lg px-5 py-3 reveal" data-delay="1">'
            '<span class="text-star text-lg tracking-tight">★★★★★</span><span class="text-sm font-bold text-navy-800">478 reviews</span>'
            f'<span class="inline-flex items-center gap-1 text-sm text-slate-500">{CHK.replace("w-5 h-5","w-4 h-4").replace("mt-0.5","")}Trustindex</span></div>'
            f'<ul class="mt-7 space-y-3 max-w-xl reveal" data-delay="2">{checks}</ul>'
            f'<div class="mt-8 flex flex-wrap gap-4 reveal" data-delay="3"><button type="button" data-modal-open class="{ORANGE_BTN}">Get A Free Quote</button>'
            f'<a href="how-it-works.html" class="{GHOST_DARK}">How It Works</a></div>'
            '</div></section>')

def quote_band():
    return ('<section class="relative overflow-hidden bg-navy-800"><div class="absolute inset-0 opacity-25" style="background:radial-gradient(620px circle at 18% 20%, #FC9700, transparent 42%)"></div>'
            '<div class="relative max-w-6xl mx-auto px-5 py-12 md:py-14 flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">'
            '<div><h2 class="font-display text-2xl md:text-3xl font-extrabold text-white">Need Storage? Get a Free Quote</h2>'
            '<p class="mt-2 text-slate-300 max-w-xl">Tell us roughly what you need to store and we’ll send a clear, no-obligation quote within 24 hours — from just £15 a week.</p></div>'
            f'<div class="flex flex-wrap gap-3 justify-center shrink-0"><button type="button" data-modal-open class="{ORANGE_BTN}">Get A Free Quote</button>'
            f'<a href="tel:01903893731" class="{GHOST_DARK}">{ic("M2 5l4-1 2 5-2 1a12 12 0 006 6l1-2 5 2-1 4a16 16 0 01-15-15z","w-5 h-5")} 01903 893731</a></div></div></section>')

def split(bg, eyebrow, h2, paras, image, alt, reverse=False, bullets=None):
    order = "lg:order-2" if reverse else ""
    bl = ""
    if bullets:
        bl = '<ul class="mt-5 space-y-3">' + "".join(f'<li class="flex items-start gap-3">{CHK}<span class="text-slate-700">{b}</span></li>' for b in bullets) + "</ul>"
    text = f'<div class="reveal">{EY(eyebrow)}{H2(h2)}' + "".join(f'<p class="mt-4 text-lg text-slate-600 leading-relaxed">{p}</p>' for p in paras) + bl + "</div>"
    pic = f'<div class="reveal {order}">{img(image, alt, "w-full h-72 lg:h-96 object-cover rounded-2xl ring-1 ring-[#E7E7E7] shadow-sm")}</div>'
    return sec(bg, f'<div class="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">{text if not reverse else pic}{pic if not reverse else text}</div>')

def trust_strip():
    items = [("10+","Years’ experience"),("£15","Per week, no deposit"),("24/7","CCTV & alarmed"),("478","5★ reviews")]
    cells = "".join(f'<div class="reveal"><div class="counter font-display text-4xl font-extrabold text-navy-800" data-counter="{v.replace("+","").replace("£","")}" data-prefix="{"£" if "£" in v else ""}" data-suffix="{"+" if "+" in v else ""}">0</div><div class="mt-1 text-sm text-slate-500 font-medium">{l}</div></div>' for v,l in items)
    badges = " ".join(f'<span class="text-xs font-bold rounded-full bg-white ring-1 ring-[#E7E7E7] px-4 py-2 text-navy-800">{b}</span>' for b in ["LAPADA Accredited","Checkatrade","Fully Insured","Family-Run"])
    return sec("bg-[#F9F8F6]", f'<div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">{cells}</div><div class="mt-10 flex flex-wrap gap-3 justify-center">{badges}</div>')

def secure_intro(d):
    return sec("bg-white", f'<div class="max-w-3xl reveal">{EY("Managed storage, not self-storage")}{H2("Secure Storage with Wolves Storage Sussex")}'
        '<p class="mt-4 text-lg text-slate-600 leading-relaxed">Most storage means hiring a van, lifting heavy boxes and driving back and forth to a unit. We do it differently. Our family team packs your belongings, collects them from your door, stores them in secure wooden containers inside our alarmed West Sussex facility, and redelivers whenever you’re ready — you never need a vehicle or to lift a thing.</p>'
        f'<p class="mt-4 text-lg text-slate-600 leading-relaxed">{d["intro"]}</p>')

def how_works():
    return split("bg-[#e8e6da]","The process","How Containerised Storage Actually Works",
        ["Your goods are professionally wrapped and loaded into a private 250 cu ft wooden container (5ft × 7ft × 8.6ft — about the contents of a one-bedroom flat). Each container is sealed, logged and stacked inside our secure indoor store.",
         "Because everything stays in its own sealed container, your belongings aren’t handled again until they come back to you — cleaner, safer and more space-efficient than a drive-up unit."],
        "hero-team-loading.webp","Wolves team loading wrapped belongings into a storage container", reverse=True,
        bullets=["We bring the materials and pack for you","Collection included — no van to hire","Sealed, individually logged containers"])

def vs_self():
    rows = [("Drive to a unit & lift everything yourself","We collect, pack and redeliver to your door"),
            ("Open shelving, dust & shared aisles","Sealed private containers in a clean indoor store"),
            ("Pay for air you don’t use","Pay only for the container space you need"),
            ("DIY security","24/7 CCTV, alarmed facility, fully insured")]
    table = "".join(f'<div class="grid grid-cols-2 gap-4 py-4 border-b border-[#E7E7E7]"><div class="flex items-start gap-2 text-slate-500"><span class="text-slate-300 mt-1">✕</span><span>{a}</span></div><div class="flex items-start gap-2 text-navy-800 font-medium">{CHK}<span>{b}</span></div></div>' for a,b in rows)
    return sec("bg-white", f'<div class="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center"><div class="reveal">{img("placeholder-4x3.svg","Container storage size guide","w-full h-72 lg:h-96 object-cover rounded-2xl ring-1 ring-[#E7E7E7]")}</div>'
        f'<div class="reveal">{EY("Container vs self-storage")}{H2("Why Container Storage Is Cleaner & More Secure Than Self-Storage")}<div class="mt-5"><div class="grid grid-cols-2 gap-4 pb-2 text-xs font-bold uppercase tracking-wider text-slate-400"><div>Traditional self-storage</div><div>Wolves managed storage</div></div>{table}</div></div></div>')

def access():
    return split("bg-[#e8e6da]","Access when you need it","Accessing Your Goods While They’re In Store",
        ["Need something back? Just give us 24 hours’ notice and we’ll redeliver to your door anywhere across West Sussex. Storing long-term but need occasional access? We’ll arrange it — simply, and without you lifting a box.",
         "Because every container is logged, we know exactly where your belongings are at all times."],
        "gallery-loading.webp","Accessing wrapped belongings from a Wolves storage container")

def what_store():
    can = ["Furniture, sofas & beds","Boxes, books & kitchenware","White goods & appliances","Business stock & archives","Antiques & artwork (LAPADA-trusted)","Garden & seasonal items"]
    cant = ["Food or perishables","Plants or livestock","Hazardous / flammable goods","Illegal items","Cash or jewellery"]
    canl = "".join(f'<li class="flex items-start gap-3">{CHK}<span class="text-slate-700">{x}</span></li>' for x in can)
    cantl = "".join(f'<li class="flex items-start gap-3"><span class="text-red-400 mt-1 shrink-0">✕</span><span class="text-slate-600">{x}</span></li>' for x in cant)
    return sec("bg-white", f'{EY("Good to know")}{H2("What You Can — And Can’t — Put Into Storage")}'
        f'<div class="mt-6 grid lg:grid-cols-2 gap-8"><div class="bg-[#F9F8F6] rounded-2xl p-7 ring-1 ring-[#E7E7E7] reveal"><h3 class="font-display text-xl font-bold text-navy-800 mb-4">Perfect for storage</h3><ul class="space-y-3">{canl}</ul></div>'
        f'<div class="bg-[#F9F8F6] rounded-2xl p-7 ring-1 ring-[#E7E7E7] reveal" data-delay="1"><h3 class="font-display text-xl font-bold text-navy-800 mb-4">Please don’t store</h3><ul class="space-y-3">{cantl}</ul></div></div>')

CALC_JS = """
<script>
(function(){
 var sel=document.getElementById('calc-rooms');var out=document.getElementById('calc-out');
 if(!sel)return;
 var map={studio:1,one:1,two:2,three:3,four:4};
 function upd(){var n=map[sel.value]||1;out.innerHTML='<span class="font-display text-4xl font-extrabold text-navy-800">'+n+'</span> <span class="text-slate-600">container'+(n>1?'s':'')+' — approx. '+(n*250)+' cu ft</span>';}
 sel.addEventListener('change',upd);upd();
})();
</script>"""

def calculator():
    inner = (f'{EY("Plan ahead")}{H2("Sizing Your Storage — Quick Estimator")}'
        '<p class="mt-4 text-lg text-slate-600 max-w-2xl">Each container holds roughly a one-bedroom flat (250 cu ft). Get a rough idea of how many you’ll need — we’ll confirm exactly on your free quote.</p>'
        '<div class="mt-6 grid lg:grid-cols-2 gap-8 items-center">'
        '<div class="bg-white rounded-2xl p-7 ring-1 ring-[#E7E7E7] shadow-sm reveal"><label for="calc-rooms" class="block text-sm font-bold text-navy-800 mb-2">Roughly how much are you storing?</label>'
        '<select id="calc-rooms" class="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm"><option value="studio">A few rooms / studio</option><option value="one">1-bed home</option><option value="two">2-bed home</option><option value="three">3-bed home</option><option value="four">4-bed+ home</option></select>'
        '<div id="calc-out" class="mt-5"></div>'
        f'<button type="button" data-modal-open class="{ORANGE_BTN} mt-5 w-full">Get My Exact Quote</button></div>'
        f'<div class="reveal">{img("placeholder-4x3.svg","Wolves Storage Sussex container size guide","w-full h-72 lg:h-96 object-cover rounded-2xl ring-1 ring-[#E7E7E7]")}</div></div>')
    return sec("bg-[#F9F8F6]", inner) + CALC_JS

def term_options(d):
    cards = [
        ("long-term-storage.html","Long-Term Storage","Best value the longer you stay — ideal for emigrating, renovations and downsizing.","long-term"),
        ("short-term-storage.html","Short-Term Storage","Flexible weekly terms for moves, chain delays and quick projects.","short-term"),
        ("business-storage.html","Business Storage","Stock, archives and equipment — scale up or down as you need.","business"),
        ("how-it-works.html","Combined With a Move","Moving with us? We’ll store in between and redeliver to your new home.","flexible"),
    ]
    cc = ""
    for href,t,desc,term in cards:
        active = ' ring-2 ring-amber-400' if term==d["term"] else ' ring-1 ring-[#E7E7E7]'
        cc += f'<a href="{href}" class="block bg-white rounded-2xl p-7{active} card-hover reveal"><h3 class="font-display text-xl font-bold text-navy-800">{t}</h3><p class="mt-2 text-slate-600">{desc}</p><span class="mt-3 inline-flex items-center gap-1 text-amber-600 font-semibold text-sm">Learn more →</span></a>'
    return sec("bg-white", f'<div class="text-center max-w-2xl mx-auto mb-10">{EY("Flexible options")}{H2("Short-Term, Long-Term, Business & Move Storage")}<p class="mt-3 text-lg text-slate-600">Whatever you’re storing and for however long, there’s a flexible option to suit.</p></div><div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">{cc}</div>')

def trusted():
    return split("bg-[#e8e6da]","Trusted in Sussex","A Trusted Family Name for Over 10 Years",
        ["Wolves Storage Sussex is part of the family-run Wolves Removals business, serving West Sussex for over a decade from our base in Ashington. We’re LAPADA accredited, Checkatrade members and fully insured — trusted by local estate agents and hundreds of families and businesses.",
         "That experience means your belongings are handled with genuine care, from the first quote to the moment they’re back in your home."],
        "hero-fleet.webp","The Wolves Removals and Storage family van fleet in West Sussex", reverse=True)

def gallery_row(title, eyebrow, imgs, note=""):
    cells = "".join(f'<figure class="overflow-hidden rounded-2xl ring-1 ring-[#E7E7E7] aspect-[4/3] reveal bg-[#F9F8F6]">{img(s, a, "h-full w-full object-cover transition duration-500 hover:scale-105")}</figure>' for s,a in imgs)
    n = f'<p class="mt-5 text-sm text-slate-500">{note}</p>' if note else ""
    return sec("bg-white", f'<div class="text-center max-w-2xl mx-auto mb-10">{EY(eyebrow)}{H2(title)}</div><div data-gallery class="grid grid-cols-2 md:grid-cols-3 gap-4">{cells}</div>{n}')

def process():
    steps = [("1","Free quote & survey",I_SURVEY,"Tell us what you’re storing — we send a clear, no-obligation quote within 24 hours."),
             ("2","We pack & collect",I_BOX,"Our team arrives, professionally wraps and packs your items, and loads them into your container."),
             ("3","Secure storage",I_SHIELD,"Your sealed container is stored in our alarmed, 24/7 CCTV facility — fully insured."),
             ("4","We redeliver",I_TRUCK,"Give us 24 hours’ notice and we bring everything back to your door, anywhere in West Sussex.")]
    cc = "".join(f'<div class="relative bg-white rounded-2xl p-7 ring-1 ring-[#E7E7E7] card-hover reveal"><div class="flex items-center gap-3 mb-3"><span class="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-amber-50 text-amber-600">{i}</span><span class="font-display text-3xl font-extrabold text-[#E7E7E7]">{n}</span></div><h3 class="font-display text-lg font-bold text-navy-800">{t}</h3><p class="mt-2 text-slate-600 text-sm leading-relaxed">{p}</p></div>' for n,t,i,p in steps)
    return sec("bg-[#e8e6da]", f'<div class="text-center max-w-2xl mx-auto mb-10">{EY("Simple & managed")}{H2("Our Step-by-Step Storage Process")}<p class="mt-3 text-lg text-slate-600">Four easy steps — we handle the heavy lifting, literally.</p></div><div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">{cc}</div>')

def dark_cta(d):
    return ('<section class="relative overflow-hidden bg-navy-800 text-white">'
            f'{img("gallery-warehouse-b.webp","Secure container storage warehouse interior in West Sussex","absolute inset-0 w-full h-full object-cover opacity-25")}'
            '<div class="relative max-w-4xl mx-auto px-5 py-16 lg:py-24 text-center">'
            f'{H2(d["ctaTitle"], dark=True)}'
            '<p class="mt-4 text-lg text-slate-200 max-w-2xl mx-auto">From just £15 a week with no deposit and no hidden fees. Free, no-obligation quote within 24 hours.</p>'
            f'<div class="mt-7 flex flex-wrap gap-3 justify-center"><button type="button" data-modal-open class="{ORANGE_BTN}">Get A Free Quote</button>'
            f'<a href="tel:01903893731" class="{GHOST_DARK}">Call 01903 893731</a></div></div></section>')

def why_choose():
    feats = [(I_SHIELD,"Fully insured","Your belongings are covered while in our care, with optional extended cover."),
             (I_CAM,"24/7 CCTV & alarmed","A monitored, alarmed indoor facility — security you can count on."),
             (I_POUND,"From £15 / week","Transparent pricing, no deposit and no hidden fees."),
             (I_TRUCK,"We collect & redeliver","No van to hire, no heavy lifting — we come to you."),
             (I_HOME,"Family-run, local","Over 10 years serving West Sussex, with genuine care."),
             (I_KEY,"LAPADA accredited","Trusted to pack, store and handle high-value items.")]
    cc = "".join(f'<div class="bg-white rounded-2xl p-7 ring-1 ring-[#E7E7E7] card-hover reveal"><span class="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-amber-50 text-amber-600">{i}</span><h3 class="font-display text-lg font-bold text-navy-800 mt-4">{t}</h3><p class="mt-2 text-slate-600 text-sm leading-relaxed">{p}</p></div>' for i,t,p in feats)
    return sec("bg-white", f'<div class="text-center max-w-2xl mx-auto mb-10">{EY("Why us")}{H2("Why Choose Wolves Storage Sussex?")}</div><div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{cc}</div>')

def related(d):
    links = [("how-it-works.html","How It Works"),("pricing.html","Pricing & Offers"),("areas-we-cover.html","Areas We Cover"),("gallery.html","Gallery"),("about.html","About Us"),("contact.html","Contact Us")]
    ll = "".join(f'<a href="{h}" class="bg-white rounded-xl px-5 py-4 ring-1 ring-[#E7E7E7] hover:ring-amber-400 font-semibold text-navy-800 reveal flex items-center justify-between gap-2">{t}<span class="text-amber-600">→</span></a>' for h,t in links)
    return sec("bg-[#e8e6da]", f'<div class="text-center max-w-2xl mx-auto mb-8">{EY("Explore")}{H2("More From Wolves Storage Sussex")}</div><div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">{ll}</div>')

INP = 'w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-navy-900 placeholder-slate-400 focus:border-amber-400 focus:ring-2 focus:ring-amber-200 outline-none transition'
def quote_form():
    return sec("bg-white", f'<div class="grid lg:grid-cols-2 gap-10 items-start"><div class="reveal">{EY("Free quote")}{H2("Get a Free Storage Quote")}'
        '<p class="mt-4 text-lg text-slate-600">No deposit, no obligation — we’ll reply within 24 hours. Prefer to talk? Call <a href="tel:01903893731" class="text-amber-600 font-semibold">01903 893731</a> or <a href="tel:07789390421" class="text-amber-600 font-semibold">07789 390421</a>.</p>'
        f'<div class="mt-6 rounded-2xl overflow-hidden ring-1 ring-[#E7E7E7]">{img("gallery-loading.webp","Wolves team loading a storage container in West Sussex","w-full h-64 object-cover")}</div></div>'
        '<form data-fake-form novalidate class="bg-[#F9F8F6] rounded-2xl p-6 sm:p-8 ring-1 ring-[#E7E7E7] reveal"><div data-form-fields class="space-y-4">'
        f'<div><label class="block text-sm font-medium text-navy-800 mb-1.5" for="qf-name">Full name</label><input id="qf-name" name="name" required class="{INP}" placeholder="Jane Smith"></div>'
        f'<div class="grid sm:grid-cols-2 gap-4"><div><label class="block text-sm font-medium text-navy-800 mb-1.5" for="qf-phone">Phone</label><input id="qf-phone" name="phone" required class="{INP}" placeholder="07789 390421"></div>'
        f'<div><label class="block text-sm font-medium text-navy-800 mb-1.5" for="qf-email">Email</label><input id="qf-email" name="email" type="email" required class="{INP}" placeholder="you@email.com"></div></div>'
        f'<div><label class="block text-sm font-medium text-navy-800 mb-1.5" for="qf-msg">What do you need to store?</label><textarea id="qf-msg" name="message" rows="3" class="{INP}" placeholder="Roughly how much, and when you’d like to start..."></textarea></div>'
        f'<button type="submit" class="{ORANGE_BTN} w-full">Request My Free Quote</button><p class="text-xs text-slate-400 text-center">\U0001f512 Your details are safe with us and never shared.</p></div>'
        '<div data-form-success hidden class="text-center py-8"><div class="mx-auto mb-4 h-16 w-16 rounded-full bg-green-100 text-green-600 flex items-center justify-center"><svg class="w-9 h-9" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/></svg></div><h3 class="font-display text-xl font-extrabold text-navy-800">Thank you — your request is in!</h3><p class="text-slate-500 mt-2 text-sm">A member of our family team will be in touch within 24 hours with your free quote.</p></div></form></div>')

def faq(d):
    items = "".join(
        f'<div class="accordion__item bg-white rounded-xl ring-1 ring-[#E7E7E7]"><button type="button" class="accordion__btn w-full flex items-center justify-between gap-4 text-left p-5 font-semibold text-navy-800" aria-expanded="false">{q}<span class="accordion__icon text-amber-500 text-2xl leading-none">+</span></button><div class="accordion__panel px-5"><div class="pb-5 text-slate-600">{a}</div></div></div>'
        for q,a in d["faqs"])
    return sec("bg-[#e8e6da]", f'<div class="text-center max-w-2xl mx-auto mb-10">{EY("FAQs")}{H2(d["nav"]+" — Your Questions Answered")}</div><div data-accordion class="space-y-3 max-w-3xl mx-auto">{items}</div>')

def build_main(d):
    return "\n".join([
        hero(d), quote_band(),
        split("bg-white","Flexible storage","Storage That Flexes Around Your Move",
            ["Whether you’re between homes, renovating or simply decluttering, our managed storage flexes around you. Store for a week or for years, scale up or down, and only pay for the container space you actually use.",
             d["sub2"]],
            "gallery-van.webp","Wolves Removals and Storage van outside the West Sussex storage facility",
            bullets=["No deposit, flexible weekly & 4-week terms","Collection and redelivery included","Free quote within 24 hours"]),
        split("bg-[#e8e6da]","Why Wolves","Why Choose Wolves Storage for Your Move?",
            ["Because we don’t just store boxes — we look after your home. Our trained, fully insured family team treats every item as if it were our own, from professional packing to careful stacking in our secure facility."],
            "hero-forklift.webp","Forklift operator stacking wooden storage containers in our secure West Sussex warehouse", reverse=True,
            bullets=["LAPADA accredited & Checkatrade members","24/7 CCTV, alarmed & fully insured","Trusted by Sussex estate agents"]),
        trust_strip(), secure_intro(d), how_works(), vs_self(), access(), what_store(), calculator(),
        term_options(d), trusted(),
        gallery_row("See Our Sussex Storage in Action","Gallery",
            [("hero-facility-van.webp","Wolves Storage Sussex facility and van"),("hero-containers-van.webp","Wooden storage containers and van at our facility"),
             ("gallery-warehouse-a.webp","Stacked wooden storage containers in our warehouse"),("gallery-forklift-b.webp","Forklift moving storage containers"),
             ("gallery-loading.webp","Team loading a storage container"),("gallery-van.webp","Wolves storage van at the facility")],
            note="Real photos of our own West Sussex facility, containers, team and fleet."),
        process(), dark_cta(d), why_choose(), related(d), quote_form(), faq(d),
        gallery_row("More From Our Sussex Store","Behind the scenes",
            [("hero-fleet.webp","The Wolves family van fleet in West Sussex"),("gallery-warehouse-b.webp","Container storage warehouse interior"),
             ("gallery-clipboard.webp","Wolves Removals and Storage branded clipboard in the warehouse"),("hero-packed-container.webp","A storage container packed with wrapped furniture")]),
    ])

def page_jsonld(d):
    service = {"@context":"https://schema.org","@type":"Service","serviceType":d["nav"],"name":"Wolves Storage Sussex — "+d["nav"],
        "description":d["meta"],"areaServed":["West Sussex","Ashington","Pulborough","Storrington","Horsham","Worthing","Steyning","Billingshurst","Henfield"],
        "provider":{"@type":"LocalBusiness","name":"Wolves Storage Sussex","telephone":"+441903893731",
            "address":{"@type":"PostalAddress","streetAddress":"Doryln House, London Road, Ashington","addressLocality":"Pulborough","addressRegion":"West Sussex","postalCode":"RH20 3JT","addressCountry":"GB"}},
        "offers":{"@type":"Offer","price":"15","priceCurrency":"GBP","description":"Storage from £15 per week. No deposit. No hidden fees."}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"index.html"},
        {"@type":"ListItem","position":2,"name":d["nav"],"item":BASE+d["file"]}]}
    faqp = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in d["faqs"]]}
    return ('<script type="application/ld+json">'+json.dumps(service,ensure_ascii=False)+'</script>\n'
            '<script type="application/ld+json">'+json.dumps(crumb,ensure_ascii=False)+'</script>\n'
            '<script type="application/ld+json">'+json.dumps(faqp,ensure_ascii=False)+'</script>')

def assemble(d):
    head = head_base
    head = re.sub(r"<title>.*?</title>", "<title>"+d["title"]+"</title>", head, 1)
    head = re.sub(r'(<meta name="description" content=")(?:.*?)(">)', lambda m:m.group(1)+d["meta"]+m.group(2), head, 1)
    head = re.sub(r'(<meta name="keywords" content=")(?:.*?)(">)', lambda m:m.group(1)+d["keywords"]+m.group(2), head, 1)
    head = re.sub(r'(<link rel="canonical" href="https://www\.wolvesstoragesussex\.co\.uk/)[^"]*(">)', lambda m:m.group(1)+d["file"]+m.group(2), head, 1)
    head = re.sub(r'(<meta property="og:url" content="https://www\.wolvesstoragesussex\.co\.uk/)[^"]*(">)', lambda m:m.group(1)+d["file"]+m.group(2), head, 1)
    head = re.sub(r'(<meta property="og:title" content=")(?:.*?)(">)', lambda m:m.group(1)+d["title"]+m.group(2), head, 1)
    head = re.sub(r'(<meta property="og:description" content=")(?:.*?)(">)', lambda m:m.group(1)+d["meta"]+m.group(2), head, 1)
    head = re.sub(r'(<meta property="og:image" content="https://www\.wolvesstoragesussex\.co\.uk/)[^"]*(">)', lambda m:m.group(1)+"images/"+d["hero"]+m.group(2), head, 1)
    head = re.sub(r'(<meta name="twitter:title" content=")(?:.*?)(">)', lambda m:m.group(1)+d["title"]+m.group(2), head, 1)
    head = re.sub(r'(<meta name="twitter:description" content=")(?:.*?)(">)', lambda m:m.group(1)+d["meta"]+m.group(2), head, 1)
    full = head + "\n" + page_jsonld(d) + "\n</head>" + HEADER + '<main id="main">\n' + build_main(d) + "\n</main>" + FOOTER
    return full

PAGES = [
 dict(file="storage-solutions.html", nav="Storage Solutions", term="flexible",
   title="Secure Managed Storage in West Sussex | Wolves Storage Sussex",
   meta="Secure, fully managed storage in West Sussex from £15/week. We pack, collect, store & redeliver — no deposit, fully insured, LAPADA accredited. Free quote in 24 hours.",
   keywords="storage West Sussex, managed storage, containerised storage, secure storage Ashington, furniture storage Sussex, household storage",
   eyebrow="Family-run · Over 10 years’ experience · West Sussex",
   h1="Secure, Fully Managed Storage in West Sussex",
   hero="hero-facility-van.webp", heroAlt="Wolves Storage Sussex secure facility and removals van in West Sussex",
   sub="Need space during a move, renovation or downsize? We pack, collect, store and redeliver your belongings from just £15 a week — collection and delivery included.",
   sub2="It’s the simplest way to store: no van to hire, no heavy lifting, and no long contracts — just secure, insured space that flexes around your life.",
   ctaTitle="Need Secure Storage in West Sussex?",
   intro="From a few boxes to a whole house, household to business, short stays to long-term — we tailor secure managed storage to exactly what you need, all from our alarmed Ashington facility.",
   checks=["Cost-effective long- and short-term storage","Packing, collection and delivery included","Fully secure, alarmed and insured","Family-run, LAPADA accredited","No deposit · flexible weekly terms"],
   faqs=[("How much does storage cost in West Sussex?","Managed storage starts from just £15 per week with no deposit and no hidden fees. We offer flexible weekly and 4-week rolling terms, and your free quote is confirmed within 24 hours."),
         ("Do I need to prepare anything?","No — our team brings the materials and professionally packs and wraps your belongings for you, then loads everything into your sealed container."),
         ("Is my stuff insured in storage?","Yes. Our facility is fully insured and you can add optional extended cover. Everything is stored in your own sealed, logged container in an alarmed, 24/7 CCTV building."),
         ("How quickly can I access my belongings?","Just give us 24 hours’ notice and we’ll redeliver to your door anywhere across West Sussex."),
         ("How big is a storage container?","Each wooden container is 5ft × 7ft × 8.6ft — 250 cu ft, roughly the contents of a one-bedroom flat. Need more? We simply use additional containers.")]),
 dict(file="long-term-storage.html", nav="Long-Term Storage", term="long-term",
   title="Long-Term Storage in West Sussex from £15/week | Wolves Storage Sussex",
   meta="Affordable long-term storage in West Sussex from £15/week. Fully insured, 24/7 CCTV, no deposit. Ideal for emigrating, renovations & downsizing. Free quote in 24 hours.",
   keywords="long-term storage West Sussex, long term furniture storage, secure storage Ashington, household storage Sussex",
   eyebrow="Best value the longer you stay · West Sussex",
   h1="Long-Term Storage in West Sussex",
   hero="hero-forklift.webp", heroAlt="Forklift stacking long-term storage containers in our secure West Sussex warehouse",
   sub="Storing for months or years? Our containerised long-term storage keeps your belongings clean, dry and secure — with better value the longer you stay.",
   sub2="Perfect for working abroad, major renovations, downsizing or settling an estate — store with total peace of mind and access whenever you need it.",
   ctaTitle="Need Long-Term Storage in West Sussex?",
   intro="Going abroad, renovating or downsizing? Long-term managed storage means your belongings stay sealed, clean and insured for as long as you need — and we redeliver the moment you’re ready.",
   checks=["Better value the longer you store","Clean, dry, sealed wooden containers","Fully insured & 24/7 CCTV","No deposit · simple rolling terms","We collect now and redeliver later"],
   faqs=[("How much does long-term storage cost?","From £15 per week with no deposit, and the longer you store the better the value — ask about long-term rates on your free quote."),
         ("Will my belongings stay in good condition?","Yes. Everything is wrapped and sealed in its own wooden container inside our dry, alarmed indoor facility, so it stays clean and protected for the long term."),
         ("Can I access items during long-term storage?","Absolutely — give us 24 hours’ notice and we’ll redeliver what you need, or arrange access to your container."),
         ("Is there a minimum or maximum term?","No long tie-ins — store for as long as you like on flexible rolling terms, and stop whenever you’re ready."),
         ("Is long-term storage insured?","Yes, the facility is fully insured with optional extended cover available for higher-value items.")]),
 dict(file="short-term-storage.html", nav="Short-Term Storage", term="short-term",
   title="Short-Term Storage in West Sussex from £15/week | Wolves Storage Sussex",
   meta="Flexible short-term storage in West Sussex from £15/week. No deposit, weekly terms, fast collection. Perfect for moves, chain delays & renovations. Free quote in 24 hours.",
   keywords="short-term storage West Sussex, temporary storage Sussex, storage between moves, weekly storage Ashington",
   eyebrow="Flexible weekly terms · West Sussex",
   h1="Short-Term Storage in West Sussex",
   hero="hero-packed-container.webp", heroAlt="A storage container packed with wrapped furniture ready for short-term storage",
   sub="Bridging a move, a broken chain or a quick renovation? Flexible weekly short-term storage with no deposit — we collect, store and bring it all back when you’re ready.",
   sub2="Only need it for a few weeks? That’s no problem — you pay by the week and stop whenever you like, with collection and redelivery included.",
   ctaTitle="Need Short-Term Storage in West Sussex?",
   intro="House move delayed? Staging your home for sale? Quick renovation? Short-term managed storage gives you flexible, secure space for exactly as long as you need — not a day more.",
   checks=["Flexible weekly terms, no deposit","Fast collection — often within days","We pack, store and redeliver","Fully insured & 24/7 CCTV","Only pay for what you need"],
   faqs=[("How short can I store for?","As little as a week — our short-term storage is billed weekly with no deposit, so you only pay for the time you actually need."),
         ("How quickly can you collect?","Often within a few days. Tell us your timescale on your free quote and we’ll fit around your move."),
         ("What if my move date changes?","No problem — flexible rolling terms mean you can extend or end your storage whenever you need, just give us a little notice."),
         ("Do you deliver it back to my new home?","Yes — give us 24 hours’ notice and we redeliver to your new address anywhere in West Sussex."),
         ("Is short-term storage insured?","Yes, fully insured, with optional extended cover, and stored in sealed containers in our alarmed facility.")]),
 dict(file="business-storage.html", nav="Business Storage", term="business",
   title="Business Storage in West Sussex from £15/week | Wolves Storage Sussex",
   meta="Secure business storage in West Sussex from £15/week. Stock, archives & equipment — fully insured, 24/7 CCTV, flexible terms, collection & redelivery. Free quote in 24 hours.",
   keywords="business storage West Sussex, stock storage Sussex, archive storage Ashington, commercial storage, document storage",
   eyebrow="Flexible commercial storage · West Sussex",
   h1="Business Storage in West Sussex",
   hero="hero-containers-van.webp", heroAlt="Stacked storage containers for business stock and archives at our Sussex facility",
   sub="Free up your office or premises. We collect, store and redeliver stock, archives and equipment — fully insured and flexible, so you only pay for the space you need.",
   sub2="Scale your storage up or down as your business changes, with no long lease — ideal for stock, ecommerce, archives, equipment and relocations.",
   ctaTitle="Need Business Storage in West Sussex?",
   intro="Running out of space for stock, archives or equipment? Business storage frees up expensive premises while keeping everything secure, insured and easy to retrieve — we collect and redeliver to save your team time.",
   checks=["Scale up or down — no long lease","Stock, archives, equipment & documents","Fully insured & 24/7 CCTV","We collect and redeliver to you","Free up costly office space"],
   faqs=[("What can I store as a business?","Stock, ecommerce inventory, archives and documents, tools and equipment, seasonal items and more — anything except perishable, hazardous or illegal goods."),
         ("Can I scale storage as my business grows?","Yes — we simply add or remove containers as your needs change, on flexible rolling terms with no long lease."),
         ("Can you collect from and deliver to our premises?","Absolutely — collection and redelivery are included, saving your team the time and hassle."),
         ("Is business storage insured?","Yes, the facility is fully insured with optional extended cover, monitored by 24/7 CCTV and alarmed."),
         ("How much does business storage cost?","From £15 per week per container with no deposit — we’ll tailor a quote to your exact requirements within 24 hours.")]),
]

for d in PAGES:
    out = assemble(d)
    open(os.path.join(SITE, d["file"]), "w", encoding="utf-8").write(out)
    print(f"  built {d['file']:24} {len(out)//1024}KB")
print("Done: 4 storage pages rebuilt.")
