#!/usr/bin/env python3
# Generator: builds our storage pages in the wolves-removals THEME (their
# compiled site.min.css + Alpine + their exact component markup), with our
# own storage wording. Only uses class strings confirmed present in their CSS.
import json, os, html
SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.sussexstoragecompany.co.uk/"
CSSV = "/css/site.min.css"
LOGO = "/images/wolves-storage-logo@480.webp"
CONTACT_MAIN = open(os.path.join(SITE,"partials","contact-main.html"),encoding="utf-8").read()
CALC_HTML = open(os.path.join(SITE,"partials","storage-calculator.html"),encoding="utf-8").read()

PHONE1, PHONE2 = "01903 893731", "07789 390421"
EMAIL = "info@sussexstoragecompany.co.uk"
CHK = '<span class="text-green mt-1 shrink-0"><svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.4 4.5L19.5 7"/></svg></span>'
SVG_PHONE = '<svg viewBox="0 0 512 512" class="w-4 text-beige" fill="currentColor" aria-hidden="true"><path d="M493 384l-91-91c-12-12-31-12-43 0l-45 45c-58-30-104-77-134-134l45-45c12-12 12-31 0-43l-91-91c-12-12-31-12-43 0L46 30C32 44 25 64 28 84c19 122 76 232 163 319s197 144 319 163c20 3 40-4 54-18l39-39c12-12 12-31 0-43z"/></svg>'
SVG_MAIL = '<svg viewBox="0 0 512 512" class="w-4 text-beige" fill="currentColor" aria-hidden="true"><path d="M48 96c-18 0-32 14-32 32v10l240 156 240-156v-10c0-18-14-32-32-32H48zm448 79L262 332c-2 2-6 3-10 3s-8-1-10-3L16 175v209c0 18 14 32 32 32h416c18 0 32-14 32-32V175z"/></svg>'

NAV = [("index.html","Home"),("about.html","About"),("storage-solutions.html","Storage"),
       ("how-it-works.html","How It Works"),("pricing.html","Pricing"),
       ("https://wolves-removals.co.uk/services/house-removals/","Removals"),("contact.html","Contact")]

def btn(label, href="contact.html", extra="lg:px-10 xl:px-14"):
    return (f'<a class="button-orange btn-white btn-sweep pulse shrink-0 whitespace-nowrap {extra}" href="{href}">'
            f'<span class="relative z-10">{label}</span><span class="btn-sweep-shine" aria-hidden="true"></span></a>')

STORAGE_SUB = [("storage-solutions.html","Storage Solutions"),("long-term-storage.html","Long-Term Storage"),
               ("short-term-storage.html","Short-Term Storage"),("business-storage.html","Business Storage"),
               ("furniture-storage.html","Furniture Storage"),("storage-size-guide.html","Storage Size Guide"),
               ("areas-we-cover.html","Areas We Cover")]

def storage_dropdown():
    subs = "".join('<li><a href="%s" class="block py-1 lg:py-2 lg:px-5 text-black hover:text-orange font-normal normal-case">%s</a></li>' % (h,l) for h,l in STORAGE_SUB)
    return ('<li class="lg:relative lg:h-full w-full lg:w-auto flex items-center shrink-0 lg:pr-4 xl:pr-5 2xl:pr-7 border-b border-black/10 lg:border-b-0 flex-col lg:flex-row lg:py-10" x-data="{o:false,t:0}" @mouseenter="if(window.innerWidth>=1024){clearTimeout(t);o=true}" @mouseleave="if(window.innerWidth>=1024){t=setTimeout(()=>o=false,250)}">'
            '<div class="flex items-center w-full lg:w-auto justify-between px-4 lg:p-0 py-3 lg:py-0">'
            '<a href="storage-solutions.html" class="nav-top shrink-0 text-black font-semibold uppercase lg:hover:text-orange text-base lg:text-sm">Storage</a>'
            '<button type="button" aria-label="Open Storage menu" @click="o=!o" class="nav-top lg:ml-1 p-1 bg-transparent transition-transform duration-200" :class="o?\'rotate-180\':\'\'"><svg viewBox="0 0 20 20" class="h-5 w-5 fill-current" fill="currentColor" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg></button></div>'
            '<ul x-cloak class="bg-white w-full px-4 py-2 lg:absolute lg:top-full lg:left-0 lg:w-72 lg:z-30 lg:shadow-lg lg:border-t-4 lg:border-lightgrey list-none my-0 lg:p-2" :class="o ? \'block\' : \'hidden\'">'+subs+'</ul></li>')

def nav_lis(mobile=False):
    out=""
    for href,label in NAV:
        if label=="Storage":
            out+=storage_dropdown(); continue
        ext=' target="_blank" rel="noopener"' if href.startswith("http") else ""
        out+=('<li class="lg:h-full w-full lg:w-auto flex items-center shrink-0 lg:pr-4 xl:pr-5 2xl:pr-7 border-b border-black/10 lg:border-b-0 px-4 py-3 lg:p-0 lg:py-10">'
              f'<a href="{href}"{ext} class="nav-top shrink-0 text-black font-semibold uppercase lg:hover:text-orange text-base lg:text-sm">{label}</a></li>')
    return out

HEADER = (
'<header id="header" class="bg-[#dad6c2] z-50 w-full sticky top-0 shadow-custom-header">\n'
'<div class="contact-bar bg-darkgrey py-4 md:py-5"><div class="container"><div class="flex items-center justify-end gap-3 sm:gap-6 font-medium text-white text-sm">'
f'<a class="flex items-center gap-2 hover:text-orange" href="tel:+441903893731">{SVG_PHONE}{PHONE1}</a>'
f'<a class="hidden md:flex items-center gap-2 hover:text-orange" href="tel:+447789390421">{SVG_PHONE}{PHONE2}</a>'
f'<a class="hidden md:flex items-center gap-2 hover:text-orange" href="mailto:{EMAIL}">{SVG_MAIL}{EMAIL}</a>'
'</div></div></div>\n'
'<div class="container mx-auto h-full"><div id="top-header" class="flex flex-wrap sm:flex-nowrap items-stretch h-full justify-between lg:gap-4 xl:gap-8">\n'
'<div id="logo" class="order-1 relative shrink-0 w-[112px] sm:w-[140px] lg:w-[180px] xl:w-[200px] z-50">'
f'<a id="site-logo" class="absolute left-0 top-1/2 -translate-y-1/2 flex z-50" href="index.html" title="Wolves Storage Sussex">'
f'<img class="h-[64px] sm:h-[88px] lg:h-[164px] xl:h-[180px] w-auto drop-shadow-lg" src="{LOGO}" width="200" height="197" alt="Wolves Storage Sussex logo"></a></div>\n'
'<div class="order-2 hidden lg:flex lg:flex-1 items-center justify-end gap-4 xl:gap-6">'
'<nav id="site-navigation" aria-label="Primary" class="font-medium"><ul class="flex lg:flex-row lg:items-center lg:justify-end p-0 mb-0 list-none">'+nav_lis()+'</ul></nav>'
+btn("Get a Free Quote")+'</div>\n'
'<div class="order-3 w-fit flex lg:hidden items-center justify-end gap-4">'
+btn("Free Quote","contact.html","rounded-xl text-xs px-4 sm:text-sm sm:px-6")+
'<button type="button" aria-label="Open menu" @click="menuOpen=!menuOpen" class="text-black bg-transparent p-2"><svg viewBox="0 0 24 24" class="w-7 h-7" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div>\n'
'</div></div>\n'
'<div x-cloak class="lg:hidden absolute top-full left-0 w-full bg-[#dad6c2] max-h-[80vh] overflow-y-auto shadow-custom-header" :class="menuOpen ? \'block\' : \'hidden\'">'
'<nav aria-label="Mobile" class="font-medium"><ul class="flex flex-col p-0 mb-0 list-none">'+nav_lis(True)+'</ul></nav></div>\n'
'</header>')

FOOTER = open(os.path.join(SITE,"partials","footer.html"),encoding="utf-8").read()

# ---------------- section helpers (verbatim theme classes) ----------------
def checklist(items, center=False):
    lis="".join(f'<li class="flex items-start gap-2">{CHK}<span>{x}</span></li>' for x in items)
    if center:
        return '<div class="mt-6 flex justify-center"><ul class="space-y-2 list-none p-0 text-base xl:text-lg inline-block text-left">'+lis+'</ul></div>'
    return '<div class="mt-6"><ul class="space-y-2 list-none p-0 text-base xl:text-lg">'+lis+'</ul></div>'

def hero(img, alt, h1, sub, checks, big=True):
    h1cls = "text-4xl lg:text-6xl" if big else "text-3xl lg:text-5xl"
    return ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
            f'<div class="absolute inset-0"><img src="{img}" alt="{alt}" width="1600" height="1067" loading="eager" fetchpriority="high" decoding="async" class="w-full h-full object-cover"></div>'
            '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
            f'<h1 class="{h1cls} font-bold leading-tight">{h1}</h1><p class="mt-4 text-lg xl:text-xl max-w-xl">{sub}</p>'
            +checklist(checks)+
            f'<div class="mt-7 flex flex-col lg:flex-row gap-3">{btn("Get a Free Quote","contact.html","px-8 lg:px-10")}'
            f'<a class="button-orange btn-white btn-sweep shrink-0 whitespace-nowrap px-8 lg:px-10" href="tel:+441903893731"><span class="relative z-10">Call {PHONE1}</span><span class="btn-sweep-shine" aria-hidden="true"></span></a></div>'
            '</div></div></div></section>')

def split(bg, h2, paras, img, alt, reverse=False):
    body = "".join(f'<p>{p}</p>' for p in paras)
    txt = (f'<div class="col-span-12 lg:col-span-6 {"lg:col-start-7" if reverse else "lg:col-start-2"}">'
           f'<h2 class="relative leading-tight text-black">{h2}</h2>{body}</div>')
    pic = (f'<div class="col-span-12 lg:col-span-4 {"lg:col-start-2" if reverse else "lg:col-start-8"}">'
           f'<div class="relative h-56 sm:h-72 lg:h-full overflow-hidden rounded-xl shadow-custom">'
           f'<img src="{img}" alt="{alt}" width="1600" height="1200" loading="lazy" decoding="async" class="absolute inset-0 w-full h-full object-cover"></div></div>')
    inner = (pic+txt) if reverse else (txt+pic)
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
            f'<div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-stretch">{inner}</div></div></section>')

def centered(bg, h2, lead, inner=""):
    leadp = f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{lead}</p>' if lead else ""
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'
            f'<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">{h2}</h2>{leadp}</div>{inner}</div></section>')

PROC_STEPS = [
 ("Free Quote &amp; Survey","On site, online or by phone","wolves-removals-process-home-survey-clipboard-icon.webp"),
 ("Your Quote","Clear price, no obligation","wolves-removals-process-quotation-price-clipboard-icon.webp"),
 ("Book It In","Confirm a date that suits","wolves-removals-process-quotation-acceptance-handshake-icon.webp"),
 ("We Pack &amp; Wrap","Materials brought, items protected","wolves-removals-process-packing-day-24-hours-clock-icon.webp"),
 ("Collection Day","We load and transport","wolves-removals-process-move-day-van-calendar-icon.webp"),
 ("Secure Storage","Sealed, alarmed, 24/7 CCTV","wolves-removals-process-unloading-at-new-address-box-icon.webp"),
 ("Access Anytime","Just 24 hours&rsquo; notice","wolves-removals-process-placing-furniture-flatpack-hand-icon.webp"),
 ("We Redeliver","Back to your door","wolves-removals-process-happy-customers-new-home-family-icon.webp"),
]
def process():
    cards=""
    for i,(t,s,icon) in enumerate(PROC_STEPS):
        cards+=(f'<div class="proc-step group transition-colors duration-100 hover:bg-darkgrey shrink-0 w-[85%] sm:w-[60%] md:w-auto snap-center relative flex items-center gap-3 bg-lightgrey pl-7 pr-12 py-7 min-h-full">'
                f'<span class="absolute top-3 left-6 font-bold text-darkgrey group-hover:text-white text-lg">{i+1}.</span>'
                f'<div class="flex-1 min-w-0">'
                f'<div class="uppercase font-bold text-black group-hover:text-white leading-snug text-sm xl:text-base">{t}</div>'
                f'<div class="uppercase text-darkgrey group-hover:text-beige leading-snug text-xs xl:text-sm">{s}</div></div>'
                f'<div class="ico-badge shrink-0 w-[5.25rem] h-[5.25rem] xl:w-24 xl:h-24 shadow-[0_8px_18px_-6px_rgba(0,0,0,0.16)]"><img src="/images/process/{icon}" alt="{t} &ndash; storage step icon" width="103" height="103" loading="lazy" decoding="async" class="w-14 h-14 xl:w-16 xl:h-16 object-contain"></div></div>')
    dots="".join(f'<button type="button" class="proc-dot{" is-active" if i==0 else ""}" data-i="{i}" aria-label="Go to step {i+1}"></button>' for i in range(len(PROC_STEPS)))
    procnav_css=('<style>'
      '.proc-nav{display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:1.25rem}'
      '@media(min-width:768px){.proc-nav{display:none}}'
      '.proc-nav .proc-dots{margin-top:0}'
      '.proc-arrow{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;flex:none;border-radius:9999px;background:#fff;border:2px solid #262626;color:#262626;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:background .2s ease,color .2s ease,border-color .2s ease,opacity .2s ease}'
      '.proc-arrow:hover{background:#FC9700;border-color:#FC9700;color:#fff}'
      '.proc-arrow:disabled{opacity:.3;cursor:default}'
      '.proc-arrow svg{width:20px;height:20px}'
      '</style>')
    ARRL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
    ARRR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    inner=(procnav_css+'<div data-proc>'
      '<div class="flex md:grid md:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6 auto-rows-fr overflow-x-auto md:overflow-visible snap-x snap-mandatory proc-scroll -mx-4 px-4 md:mx-0 md:px-0 pb-2 md:pb-0">'+cards+'</div>'
      '<div class="proc-nav">'
      '<button type="button" class="proc-arrow proc-prev" aria-label="Previous step">'+ARRL+'</button>'
      '<div class="proc-dots" role="tablist" aria-label="Storage step navigation">'+dots+'</div>'
      '<button type="button" class="proc-arrow proc-next" aria-label="Next step">'+ARRR+'</button>'
      '</div></div>')
    return centered("bg-beige","Our Step-by-Step Storage Process","We handle the heavy lifting, literally &mdash; here&rsquo;s how storing with us works.",inner)

def faq(items):
    cards=""
    for q,a in items:
        cards+=('<div class="faq-card" x-data="{open:false}" :class="open && \'is-open\'">'
                '<button type="button" class="faq-head" @click="open=!open" :aria-expanded="open">'
                '<span class="faq-ico"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="w-6 h-6"><path d="M3 3h8v8H3zm10 5h8v13h-8zM3 13h8v8H3z"/></svg></span>'
                f'<span class="faq-q">{q}</span>'
                '<span class="faq-toggle" :class="open && \'is-open\'"><svg viewBox="0 0 20 20" class="w-5 h-5 fill-current" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg></span></button>'
                f'<div class="faq-body" x-show="open" x-cloak x-transition.duration.200ms><p>{a}</p></div></div>')
    inner=f'<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2"><div class="faq-list">{cards}</div></div></div>'
    return (f'<section class="relative bg-beige w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'
            f'<div class="text-center mb-6 lg:mb-8"><h2 class="relative leading-tight text-black">Storage &mdash; Your Questions Answered</h2></div>{inner}</div></section>')

def gallery(imgs):
    cells="".join(f'<div class="col-span-12 sm:col-span-6 md:col-span-4"><div class="relative h-56 sm:h-72 overflow-hidden rounded-xl shadow-custom"><img src="{s}" alt="{a}" width="1200" height="900" loading="lazy" decoding="async" class="absolute inset-0 w-full h-full object-cover"></div></div>' for s,a in imgs)
    return centered("bg-white","See Our Sussex Storage in Action","Real photos of our own facility, containers, team and fleet.",
                    f'<div class="grid grid-cols-12 gap-4 lg:gap-6">{cells}</div>')

def cta_band(title, img):
    return ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem]">'
            f'<div class="absolute inset-0"><img src="{img}" alt="Secure storage facility in West Sussex" width="1600" height="900" loading="lazy" decoding="async" class="w-full h-full object-cover"></div>'
            '<div class="container relative z-10 w-full py-[3.6rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2 hero-panel text-center">'
            f'<h2 class="text-3xl lg:text-5xl font-bold leading-tight">{title}</h2>'
            '<p class="mt-3 text-lg xl:text-xl max-w-2xl mx-auto">From just &pound;15 a week with no deposit and no hidden fees. Free, no-obligation quote within 24 hours.</p>'
            f'<div class="mt-6 flex flex-col lg:flex-row flex-wrap gap-3 justify-center">{btn("Get a Free Quote","contact.html","px-8 lg:px-10")}'
            f'<a class="button-orange btn-white btn-sweep shrink-0 px-8 lg:px-10" href="tel:+441903893731"><span class="relative z-10">Call {PHONE1}</span><span class="btn-sweep-shine" aria-hidden="true"></span></a></div>'
            '</div></div></div></section>')

FORM = ('<form id="quote-form" class="enquiry-form mt-5" novalidate><div data-form-fields class="grid grid-cols-12 gap-4">'
 '<div class="col-span-12 md:col-span-6"><label class="block font-semibold mb-1" for="f-first">First name <span class="text-darkgrey">*</span></label><input class="w-full" type="text" id="f-first" name="first_name" required></div>'
 '<div class="col-span-12 md:col-span-6"><label class="block font-semibold mb-1" for="f-last">Last name <span class="text-darkgrey">*</span></label><input class="w-full" type="text" id="f-last" name="last_name" required></div>'
 '<div class="col-span-12 md:col-span-6"><label class="block font-semibold mb-1" for="f-email">Email <span class="text-darkgrey">*</span></label><input class="w-full" type="email" id="f-email" name="email" required></div>'
 '<div class="col-span-12 md:col-span-6"><label class="block font-semibold mb-1" for="f-phone">Phone</label><input class="w-full" type="tel" id="f-phone" name="phone"></div>'
 '<div class="col-span-12"><span class="block font-semibold mb-2">What do you need to store?</span><div class="flex flex-wrap gap-2">'
 +"".join(f'<label class="enq-chip"><input type="checkbox" name="enquiry" value="{v}"><span>{v}</span></label>' for v in ["Household","Long-term","Short-term","Business","Not sure"])+'</div></div>'
 '<div class="col-span-12"><label class="block font-semibold mb-1" for="f-msg">Message</label><textarea class="w-full" id="f-msg" name="message" rows="4"></textarea></div>'
 f'<div class="col-span-12">{btn("Request My Free Quote","javascript:void(0)","px-8 lg:px-10")}</div></div>'
 '<div data-form-success hidden class="mt-5 p-6 bg-lightgrey rounded-xl text-center"><p class="text-xl font-bold text-black">Thank you &mdash; your request is in!</p><p class="mt-2">A member of our family team will be in touch within 24 hours with your free quote.</p></div></form>')
FORM_JS = ('<script>document.addEventListener("submit",async function(e){'
 'var f=e.target.closest(".enquiry-form");if(!f)return;e.preventDefault();'
 'var ok=true;f.querySelectorAll("[required]").forEach(function(x){var bad=x.type==="checkbox"?!x.checked:!x.value.trim();x.style.borderColor=bad?"#c00":"";if(bad)ok=false;});if(!ok)return;'
 'var btn=f.querySelector("button[type=submit]")||f.querySelector("button");var orig=btn?btn.innerHTML:"";'
 'var data={};new FormData(f).forEach(function(v,k){if(k in data){if(!Array.isArray(data[k]))data[k]=[data[k]];data[k].push(v);}else{data[k]=v;}});'
 'data.page=document.title;data.page_url=location.href;'
 'var prev=f.querySelector("[data-form-error]");if(prev)prev.hidden=true;'
 'if(btn){btn.disabled=true;btn.innerHTML="Sending\\u2026";}'
 'try{var res=await fetch("/api/contact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});'
 'var j={};try{j=await res.json();}catch(_){}'
 'if(res.ok&&j&&j.ok){var fl=f.querySelector("[data-form-fields]");if(fl)fl.style.display="none";var s=f.querySelector("[data-form-success]");if(s)s.hidden=false;if(s&&s.scrollIntoView)s.scrollIntoView({behavior:"smooth",block:"center"});}'
 'else{throw new Error((j&&j.error)||"send failed");}'
 '}catch(_){if(btn){btn.disabled=false;btn.innerHTML=orig;}'
 'var box=f.querySelector("[data-form-error]");if(!box){box=document.createElement("div");box.setAttribute("data-form-error","");box.style.cssText="margin-top:1rem;padding:1rem 1.25rem;border-radius:.75rem;background:#fdecec;color:#a11616;font-weight:600;font-size:.95rem";var anchor=f.querySelector("[data-form-fields]")||f;anchor.appendChild(box);}'
 'box.hidden=false;box.textContent="Sorry \\u2014 your message couldn\\u2019t be sent just now. Please call 01903 893731 or email info@sussexstoragecompany.co.uk.";}'
 '});</script>')

# ---------------- head / page assembly ----------------
AREA_SERVED = ["West Sussex","Ashington","Washington","Storrington","Pulborough","Steyning","Billingshurst",
  "Horsham","Henfield","Worthing","Arundel","Petworth","Littlehampton","Shoreham-by-Sea","Findon",
  "Burgess Hill","Haywards Heath","Chichester","Midhurst","Cowfold","Partridge Green"]
SOCIALS_URLS = ["https://www.instagram.com/wolvesremovals/","https://www.facebook.com/wolvesremovals/",
  "https://www.linkedin.com/company/wolves-removals","https://www.pinterest.co.uk/wolvesremovals/",
  "https://x.com/WolvesRemovals","https://www.tumblr.com/wolvesremovalsltd","https://www.youtube.com/@wolvesremovals"]
ORG = json.dumps({"@context":"https://schema.org","@type":["SelfStorage","MovingCompany","LocalBusiness"],
  "@id":BASE+"#business",
  "name":"Wolves Storage Sussex","url":BASE,"telephone":"+441903893731","email":EMAIL,"priceRange":"From £15 per week",
  "currenciesAccepted":"GBP","paymentAccepted":"Cash, Credit Card, Debit Card, Bank Transfer","foundingDate":"2016",
  "image":BASE+"images/wolves-storage-logo@480.webp","logo":BASE+"images/wolves-storage-logo@480.webp",
  "hasMap":"https://www.google.com/maps?q=Doryln+House,+London+Road,+Ashington,+Pulborough,+West+Sussex+RH20+3JT",
  "address":{"@type":"PostalAddress","streetAddress":"Doryln House, London Road, Ashington","addressLocality":"Pulborough","addressRegion":"West Sussex","postalCode":"RH20 3JT","addressCountry":"GB"},
  "geo":{"@type":"GeoCoordinates","latitude":"50.9270","longitude":"-0.4470"},
  "areaServed":[{"@type":"City","name":a} for a in AREA_SERVED],
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:30","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday"],"opens":"09:00","closes":"16:00"}],
  "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"478","bestRating":"5"},
  "sameAs":SOCIALS_URLS},ensure_ascii=False)

def head(d):
    faqjson=""
    if d.get("faqs"):
        faqjson='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faqs"]]},ensure_ascii=False)+'</script>'
    if d["file"]=="index.html":
        crumb=""
    else:
        items=[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"index.html"}]
        if d.get("crumb_parent"):
            pf,pn=d["crumb_parent"]
            items.append({"@type":"ListItem","position":2,"name":pn,"item":BASE+pf})
            items.append({"@type":"ListItem","position":3,"name":d["nav"],"item":BASE+d["file"]})
        else:
            items.append({"@type":"ListItem","position":2,"name":d["nav"],"item":BASE+d["file"]})
        crumb='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items},ensure_ascii=False)+'</script>'
    return ('<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{d["title"]}</title>\n<meta name="description" content="{d["meta"]}">\n<meta name="robots" content="index, follow">\n'
        f'<link rel="canonical" href="{BASE}{d["file"]}">\n<meta name="theme-color" content="#697783">\n'
        '<meta name="geo.region" content="GB-WSX"><meta name="geo.placename" content="Ashington, Pulborough, West Sussex"><meta name="geo.position" content="50.9270;-0.4470"><meta name="ICBM" content="50.9270, -0.4470">\n'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Wolves Storage Sussex"><meta property="og:title" content="{d["title"]}"><meta property="og:description" content="{d["meta"]}"><meta property="og:url" content="{BASE}{d["file"]}"><meta property="og:image" content="{BASE}{d["hero"].lstrip("/")}"><meta property="og:locale" content="en_GB">\n'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{d["title"]}"><meta name="twitter:description" content="{d["meta"]}"><meta name="twitter:image" content="{BASE}{d["hero"].lstrip("/")}">\n'
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="manifest" href="/site.webmanifest">\n'
        '<link rel="preload" href="/fonts/Barlow-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/Barlow-Semibold.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/Barlow-Bold.woff2" as="font" type="font/woff2" crossorigin>\n'
        f'<link rel="stylesheet" href="{CSSV}">\n<script type="application/ld+json">{ORG}</script>\n{crumb}\n{faqjson}\n{d.get("extra_schema","")}\n</head>')

SCRIPTS = '<script defer src="/js/alpine.min.js"></script><script defer src="/js/process-carousel.js"></script>'+FORM_JS

TRUSTED_BY = '<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="text-center mb-10"><h2 class="relative leading-tight text-black">We&rsquo;re Trusted By</h2></div><div class="flex justify-center mb-10 lg:mb-12"><a href="https://lapada.org/dealers/wolves-removals/" target="_blank" rel="noopener" aria-label="Wolves Storage Sussex is LAPADA accredited" class="inline-block hover:opacity-80 transition-opacity"><img src="/images/photos/lapada-approved-service-provider.webp" alt="LAPADA Approved Service Provider, Association of Art &amp; Antiques Dealers" width="520" height="493" loading="lazy" decoding="async" class="h-32 sm:h-40 lg:h-44 w-auto"></a></div><div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 items-center gap-2"><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/fine-and-country-recommend-wolves.png" alt="Fine &amp; Country estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/justin-lloyd-estate-agents-recommend.webp" alt="Justin Lloyd estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/mansell-mctaggart-estate-agents-partner.webp" alt="Mansell McTaggart estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/leaders-estate-agents-recommend.webp" alt="Leaders estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/alex-harvey-estate-agents-recommend.webp" alt="Alex Harvey estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/at-home-estate-lettings-recommend.webp" alt="At Home estate agents recommend Wolves Storage Sussex" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div></div></div></section>'

def page(d):
    body_open=f'<body class="font-body bg-white text-black overflow-x-clip text-base xl:text-lg page-{d["slug"]}"><div id="page" class="relative min-h-screen block" x-data="{{menuOpen:false}}">'
    return head(d)+"\n"+body_open+"\n"+HEADER+"\n<main id=\"main\">\n"+"\n".join(d["sections"])+("" if d["slug"] in ("404","legal") else "\n"+TRUSTED_BY)+"\n</main>\n"+FOOTER+"\n"+SCRIPTS+"\n</div></body></html>"

IMG=lambda n:"/images/"+n
# ---------------- pages ----------------
TRUSTINDEX_SECTION = ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
  '<div class="container"><div class="flex justify-center mb-8 lg:mb-10"><div style="zoom:.8"><div class="ti-reviews-widget max-w-full"><script defer async src="https://cdn.trustindex.io/loader.js?cd741d573fcc673344062ffdcd3"></script></div></div></div></div>'
  '<div style="max-width:1720px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem;"><div style="zoom:.8"><div class="ti-reviews-widget w-full"><script defer async src="https://cdn.trustindex.io/loader.js?c457a627393e67277d368b8df3b"></script></div></div></div>'
  '</section>')

CALC_SECTION = ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container">'
  '<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">Storage Cost Calculator</h2>'
  '<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">Add what you need to store or set the number of pods, and we&rsquo;ll estimate the space and weekly price you need &mdash; then get a free quote to confirm.</p></div>'
  +CALC_HTML+'</div></section>'
  '<script defer src="/js/storage-calculator.js"></script>')

CONTAINER_HTML = {'index.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Beats a Self-Storage Unit</h2><p>More and more West Sussex families choose managed container storage over a drive-up self-storage unit, and it comes down to two things: how clean it stays and how secure it is. Your belongings are wrapped and sealed into your own wooden container inside our dry, ventilated facility in Ashington, rather than left in an unheated metal room you open every week.</p><p>Security is layered, not left to a single padlock. The building is alarmed and monitored, access is staff-controlled, and your container stays sealed for its whole stay. As a family-run, LAPADA-accredited and Checkatrade-verified business, we&rsquo;re fully insured and trusted by local estate agents &mdash; so your things are genuinely looked after.</p><ul class="tick-list"><li>Sealed, private containers &mdash; not shared, open-plan rooms</li><li>Dry, ventilated storage that protects against damp and dust</li><li>Alarmed, 24/7 CCTV and staff-controlled access</li><li>Fully insured, family-run and LAPADA accredited</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'storage-solutions.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Is Cleaner &amp; More Secure Than Self-Storage</h2><p>Cleanliness and security are the two reasons customers most often switch to us from a self-storage unit. Our West Sussex warehouse is dry, ventilated and managed, so your goods aren&rsquo;t exposed to the damp that creeps into unheated metal rooms over winter. Because each container is sealed once it&rsquo;s loaded, dust, pests and moisture have far fewer ways in than in a unit you open weekly.</p><p>We treat the warehouse as a working facility, not a self-service car park. The building is alarmed and monitored, access is staff-controlled rather than open to the public, and your individual container stays sealed throughout its stay. As a LAPADA-member and Checkatrade-verified company we are fully insured, and we&rsquo;re recommended by respected local agents including Fine &amp; Country, Justin Lloyd and Mansell McTaggart.</p><ul class="tick-list"><li>Individually sealed containers &mdash; no shared, open-plan rooms</li><li>Dry, ventilated warehouse that protects against damp</li><li>Alarmed, monitored and staff-controlled access</li><li>Fully insured with LAPADA and Checkatrade backing</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'long-term-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Containers Protect Your Belongings for the Long Term</h2><p>When your things are stored for months or even years, the difference between a sealed container and an open self-storage unit really shows. Our warehouse is dry, ventilated and stable, so furniture, fabrics and electronics don&rsquo;t sit through damp Sussex winters in an unheated metal box. Sealed once and left undisturbed, your container keeps dust, pests and moisture out far better than a unit you keep reopening.</p><p>Long-term storage also needs long-term peace of mind. The facility is alarmed, monitored and staff-controlled, your container stays sealed for its entire stay, and everything is fully insured throughout. You don&rsquo;t need to visit, check or worry &mdash; and when you&rsquo;re finally ready, we simply bring it all back.</p><ul class="tick-list"><li>Dry, ventilated storage &mdash; ideal for months or years</li><li>Sealed once and left undisturbed, keeping damp and dust out</li><li>Alarmed, monitored and fully insured for the long haul</li><li>No need to visit &mdash; we redeliver when you&rsquo;re ready</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'short-term-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Cleaner, Easier &amp; More Secure Than a Self-Storage Unit</h2><p>Even for a few weeks between moves, a sealed container beats hiring a self-storage unit. There&rsquo;s no van to rent, no driving back and forth, and no lugging boxes down a shared corridor &mdash; we pack, collect and seal everything into your own container. It stays clean and dry in our managed Ashington warehouse until the day you need it back.</p><p>It&rsquo;s also more secure than a padlock-and-go unit. The building is alarmed and staff-controlled, your container is sealed throughout, and it&rsquo;s all fully insured &mdash; even for a short stay. When your move date lands, give us 24 hours&rsquo; notice and we redeliver to your door.</p><ul class="tick-list"><li>No van to hire and no boxes to carry yourself</li><li>Sealed, private container kept clean and dry</li><li>Alarmed, staff-controlled and fully insured</li><li>Fast collection and 24-hour redelivery</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'business-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Businesses Choose Containers Over Self-Storage</h2><p>For stock, archives and equipment, a managed container is a safer home than an open self-storage unit. Your items are sealed into a logged container in our dry, ventilated warehouse, protected from the damp and dust that can ruin paperwork, electronics and packaging. Nothing is handled or disturbed until you ask for it back, so your inventory stays in the condition it arrived in.</p><p>Security and accountability matter for business goods. The facility is alarmed, monitored and staff-controlled, every container is logged, and everything is fully insured. We collect from and redeliver to your premises, so freeing up expensive floor space doesn&rsquo;t cost your team time.</p><ul class="tick-list"><li>Sealed, logged containers &mdash; not shared open units</li><li>Dry, ventilated storage that protects stock and archives</li><li>Alarmed, monitored, staff-controlled and fully insured</li><li>Collection and redelivery to your premises</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'pricing.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Is Better Value Than Self-Storage</h2><p>Self-storage can look cheap until you add up the extras &mdash; the van hire, the fuel, the time spent driving back and forth, and paying for floor space you never fully use. With managed container storage you only pay for the space you actually need, from just &pound;15 a week, and collection and redelivery are included &mdash; with no deposit and no hidden fees.</p><p>You also get more for your money. Your belongings are sealed into your own container in our dry, ventilated, alarmed warehouse in Ashington, not left in an unheated metal room you have to visit yourself. As a family-run, LAPADA-accredited and Checkatrade-verified business, everything is fully insured &mdash; so the price you&rsquo;re quoted genuinely covers a clean, secure, fully managed service.</p><ul class="tick-list"><li>Pay only for the container space you use</li><li>Collection &amp; redelivery included &mdash; no van to hire</li><li>No deposit and no hidden fees</li><li>Sealed, dry, alarmed and fully insured</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>'}

# ---------------- "Why store with us" trust card (image + copy + CTA) -------
def _wl(href,text):
    ext=' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a href="{href}"{ext} class="font-bold text-white underline hover:text-orange">{text}</a>'

def whyus(heading,p1,p2,img,alt):
    return ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container">'
            '<div class="bg-darkgrey rounded-2xl shadow-custom p-5 lg:p-10"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-center">'
            '<div class="col-span-12 lg:col-span-5"><div class="relative h-56 sm:h-80 lg:h-full lg:min-h-[22rem] overflow-hidden rounded-xl shadow-custom">'
            f'<img src="{img}" alt="{alt}" width="1600" height="1200" loading="lazy" decoding="async" class="absolute inset-0 w-full h-full object-cover"></div></div>'
            '<div class="col-span-12 lg:col-span-7 text-white">'
            f'<h2 class="relative leading-tight text-white">{heading}</h2>'
            f'<p class="mt-4 text-beige">{p1}</p><p class="mt-4 text-beige">{p2}</p>'
            '<div class="mt-7 flex flex-col lg:flex-row lg:items-center gap-4">'
            +btn("Get a Free Quote","contact.html","px-8 lg:px-10")+
            f'<a class="flex items-center gap-2 text-white font-bold whitespace-nowrap hover:text-orange" href="tel:+441903893731">{SVG_PHONE}{PHONE1}</a>'
            '</div></div></div></div></div></section>')

WHYUS_CONTENT = {
 'index.html':(
   "Why Store With Wolves Storage Sussex?",
   "We&rsquo;re a friendly, family-run Sussex removals and storage company that has kept its promises since 2016. From a single item to the contents of a whole house, every job is fully insured and run by a dedicated coordinator, so you always have one point of contact.",
   "As a "+_wl("about.html","LAPADA member")+" and a Checkatrade-verified team, we handle it all with real care &mdash; expert packing, sealed "+_wl("storage-solutions.html","containerised storage")+" and flexible "+_wl("short-term-storage.html","short-term")+" and "+_wl("long-term-storage.html","long-term")+" options across West Sussex, Surrey, Hampshire and Kent.",
   "/images/hero-forklift.webp","Wolves Storage Sussex team member operating a forklift at our secure West Sussex facility"),
 'storage-solutions.html':(
   "Why Choose Wolves for Managed Storage?",
   "Storing with us isn&rsquo;t self-service. As a family-run Sussex business trusted since 2016, we pack, collect, seal and stack your belongings into their own logged container &mdash; then bring them back when you&rsquo;re ready, all overseen by one dedicated coordinator.",
   "Everything is fully insured, alarmed and covered by 24/7 CCTV, and we&rsquo;re "+_wl("about.html","LAPADA accredited")+" and Checkatrade-verified. See exactly "+_wl("how-it-works.html","how it works")+" or check our honest "+_wl("pricing.html","storage prices")+" from just &pound;15 a week.",
   "/images/hero-team-loading.webp","Wolves Storage Sussex family team carefully loading a sealed storage container"),
 'long-term-storage.html':(
   "Why Trust Us With Long-Term Storage?",
   "When your belongings are stored for months or years, the company matters as much as the container. We&rsquo;ve been a family-run Sussex name since 2016, and every long-term store is sealed once, logged and left undisturbed in our dry, alarmed facility &mdash; fully insured for the whole stay.",
   "You don&rsquo;t need to visit or worry: we&rsquo;re "+_wl("about.html","LAPADA accredited")+", Checkatrade-verified and rated 5.0 by hundreds of customers. Prefer a shorter stay? Our "+_wl("short-term-storage.html","short-term storage")+" flexes by the week, and the "+_wl("how-it-works.html","fully managed service")+" handles every box.",
   "/images/gallery-warehouse-a.webp","Long-term storage containers stacked inside the Wolves Storage Sussex secure warehouse"),
 'short-term-storage.html':(
   "Why We&rsquo;re the Easy Choice for Short-Term Storage",
   "Bridging a move shouldn&rsquo;t mean hiring a van and a self-storage unit. As a family-run Sussex team trusted since 2016, we collect within days, seal everything into your own container and redeliver on 24 hours&rsquo; notice &mdash; with one coordinator looking after the lot.",
   "It&rsquo;s flexible by the week with no deposit, fully insured and "+_wl("about.html","LAPADA accredited")+". Need longer? Switch to "+_wl("long-term-storage.html","long-term storage")+" any time, or see our transparent "+_wl("pricing.html","weekly prices")+" from &pound;15.",
   "/images/hero-packed-container.webp","Short-term storage container neatly packed with wrapped furniture by Wolves Storage Sussex"),
 'business-storage.html':(
   "Why Sussex Businesses Store With Us",
   "Stock, archives and equipment deserve more than an open self-storage unit. We&rsquo;ve helped Sussex businesses free up space since 2016, sealing every item into a logged, fully insured container and collecting from &mdash; and redelivering to &mdash; your premises so your team loses no time.",
   "The facility is alarmed, monitored and "+_wl("about.html","LAPADA accredited")+", and you scale up or down with no long lease. Find out "+_wl("how-it-works.html","how the managed service works")+" or get tailored "+_wl("pricing.html","business pricing")+" within 24 hours.",
   "/images/hero-containers-van.webp","Business storage containers and Wolves Storage Sussex van ready for collection and redelivery"),
 'how-it-works.html':(
   "Why Our Fully Managed Service Works",
   "Fully managed means you never hire a van or lift a box. Since 2016 our family-run Sussex team has quoted, packed, collected, stored and redelivered &mdash; with one dedicated coordinator as your single point of contact from the first call to the day it all comes home.",
   "Every step is fully insured, alarmed and "+_wl("about.html","LAPADA accredited")+". Explore our "+_wl("storage-solutions.html","storage solutions")+", compare "+_wl("short-term-storage.html","short-term")+" and "+_wl("long-term-storage.html","long-term")+" options, or see "+_wl("pricing.html","what&rsquo;s included")+" from &pound;15 a week.",
   "/images/gallery-loading.webp","Wolves Storage Sussex team demonstrating the fully managed packing and loading process"),
 'pricing.html':(
   "Why Our Storage Is Honest Value",
   "No van hire, no fuel, no time wasted driving back and forth &mdash; and no hidden fees. As a family-run Sussex company since 2016, we quote one clear weekly price from &pound;15 that already includes collection, your sealed container and redelivery.",
   "Every penny buys a fully insured, alarmed, "+_wl("about.html","LAPADA-accredited")+" service. Choose "+_wl("short-term-storage.html","short-term")+" or "+_wl("long-term-storage.html","long-term")+" storage, see "+_wl("how-it-works.html","exactly how it works")+", and get your free quote within 24 hours.",
   "/images/gallery-clipboard.webp","Wolves Storage Sussex branded clipboard used for clear, no-obligation storage quotes"),
 'areas-we-cover.html':(
   "Why West Sussex Stores With Wolves",
   "Because we&rsquo;re based in Ashington and have served the county since 2016, we know West Sussex inside out &mdash; and the managed model means we come to you. One family-run team collects, stores and redelivers, wherever you are in the area.",
   "It&rsquo;s a local, fully insured and "+_wl("about.html","LAPADA-accredited")+" service trusted by estate agents across the region. Explore our "+_wl("storage-solutions.html","storage solutions")+" or see "+_wl("pricing.html","prices")+" from just &pound;15 a week.",
   "/images/hero-fleet.webp","Wolves Storage Sussex van fleet that collects and redelivers across West Sussex"),
 'gallery.html':(
   "Why Our Facility Earns Your Trust",
   "Seeing is believing &mdash; and we&rsquo;re proud to show the real facility behind the family name we&rsquo;ve built since 2016. Clean, dry wooden containers, a tidy alarmed warehouse and a friendly team that treats every item as if it were our own.",
   "It&rsquo;s all fully insured, covered by 24/7 CCTV and "+_wl("about.html","LAPADA accredited")+". Like what you see? Explore our "+_wl("storage-solutions.html","storage solutions")+" or check "+_wl("pricing.html","prices")+" from &pound;15 a week.",
   "/images/gallery-forklift-b.webp","Inside the secure, alarmed Wolves Storage Sussex warehouse with containers and forklift"),
 'about.html':(
   "Why Families Trust the Wolves Name",
   "What began as a local removals business in 2016 grew into trusted, fully managed storage &mdash; built on the same family values of care, honesty and genuine local service. Hundreds of West Sussex households and businesses now rely on us, rated 5.0 across Google, Checkatrade and Facebook.",
   "We&rsquo;re LAPADA accredited, Checkatrade-verified and fully insured, with 24/7 CCTV throughout. See "+_wl("how-it-works.html","how our service works")+" or explore "+_wl("storage-solutions.html","storage solutions")+" tailored to you.",
   "/images/hero-facility-van.webp","The Wolves Storage Sussex family-run facility and branded van in West Sussex"),
 'contact.html':(
   "Why Get in Touch With Wolves Storage",
   "One quick call or message is all it takes &mdash; and you&rsquo;ll speak to the family team, not a call centre. Trusted across Sussex since 2016, we&rsquo;ll send a clear, no-obligation quote within 24 hours and give you one dedicated coordinator from start to finish.",
   "Everything is fully insured and "+_wl("about.html","LAPADA accredited")+". Tell us whether you need "+_wl("short-term-storage.html","short-term")+", "+_wl("long-term-storage.html","long-term")+" or "+_wl("business-storage.html","business storage")+" and we&rsquo;ll tailor a price from just &pound;15 a week.",
   "/images/gallery-van.webp","Wolves Storage Sussex van ready to collect and store belongings across West Sussex"),
}
WHYUS = {f: whyus(*v) for f,v in WHYUS_CONTENT.items()}

# ---------------- LOCATION SILO: per-town landing pages ----------------
ADDR_LD = {"@type":"PostalAddress","streetAddress":"Doryln House, London Road, Ashington","addressLocality":"Pulborough","addressRegion":"West Sussex","postalCode":"RH20 3JT","addressCountry":"GB"}

def town_service_schema(t):
    return ('<script type="application/ld+json">'+json.dumps({
        "@context":"https://schema.org","@type":"Service","serviceType":"Managed container storage",
        "name":"Storage in "+t["town"],
        "provider":{"@type":["SelfStorage","MovingCompany"],"name":"Wolves Storage Sussex","telephone":"+441903893731","url":BASE,
            "image":BASE+"images/wolves-storage-logo@480.webp","address":ADDR_LD,
            "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"478","bestRating":"5"}},
        "areaServed":{"@type":"Place","name":t["town"] if "Sussex" in t["town"] else t["town"]+", "+t.get("region","West Sussex"),"geo":{"@type":"GeoCoordinates","latitude":t["lat"],"longitude":t["lng"]}},
        "url":BASE+t["slug"]+".html",
        "offers":{"@type":"Offer","price":"15","priceCurrency":"GBP","priceSpecification":{"@type":"UnitPriceSpecification","price":"15","priceCurrency":"GBP","referenceQuantity":{"@type":"QuantitativeValue","value":"1","unitText":"WEEK"}}}
    },ensure_ascii=False)+'</script>')

def town_map(t):
    q=(t["town"]+", "+t.get("region","West Sussex")).replace(" ","+")
    return ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-12 pb-8 lg:pb-12 border-border"><div class="container">'
            '<div class="grid grid-cols-12 gap-6 lg:gap-10 items-center">'
            '<div class="col-span-12 lg:col-span-5"><h2 class="relative leading-tight text-black">We Cover '+t["town"]+'</h2>'
            '<p class="mt-3">From our alarmed warehouse in Ashington (RH20 3JT) we collect from and redeliver right across '+t["town"]+' and the surrounding area &mdash; just tell us your postcode.</p>'
            +checklist(["Door-to-door collection &amp; redelivery","Sealed, alarmed &amp; fully insured storage","From &pound;15/week, no deposit"])+
            '<div class="mt-6">'+btn("Get a Free Quote","contact.html","px-8 lg:px-10")+'</div></div>'
            '<div class="col-span-12 lg:col-span-7"><iframe title="Map of '+t["town"]+', West Sussex storage area" src="https://www.google.com/maps?q='+q+'&amp;z=12&amp;ie=UTF8&amp;iwloc=&amp;output=embed" class="block w-full rounded-xl shadow-custom" style="border:0;height:320px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
            '</div></div></section>')

TOWN_STATS=('<section class="relative bg-darkgrey text-white w-full py-7 lg:py-9 border-border"><div class="container">'
  '<div class="grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">'
  +"".join(f'<div><div class="text-3xl font-bold">{b}</div><div class="text-beige text-sm mt-1">{s}</div></div>' for b,s in
    [("5.0&#9733;","478 verified reviews"),("Since 2016","Family-run &amp; local"),("&pound;15","per week, no deposit"),("100%","Insured &amp; alarmed")])
  +'</div></div></section>')
TSVC_ICONS={
 "container":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>',
 "calendar":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4.5" width="18" height="17" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/></svg>',
 "clock":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></svg>',
 "briefcase":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="7" width="19" height="13" rx="2"/><path d="M16 7V5.4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2V7M2.5 12.5h19"/></svg>',
 "sofa":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 11V8.5A2.5 2.5 0 0 1 7.5 6h9A2.5 2.5 0 0 1 19 8.5V11"/><path d="M3 13a2 2 0 0 1 4 0v3h10v-3a2 2 0 0 1 4 0v5H3z"/><path d="M6 18v2M18 18v2"/></svg>',
 "van":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1.5 5h13v10h-13z"/><path d="M14.5 8h4l3 3.2V15h-7z"/><circle cx="5.5" cy="17.5" r="1.9"/><circle cx="17.5" cy="17.5" r="1.9"/></svg>',
}
TSVC_ARROW='<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
TSVC_CSS=('<style>'
  '.tsvc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1.25rem;text-align:left}'
  '.tsvc-card{position:relative;display:flex;flex-direction:column;gap:.85rem;background:#fff;border:1px solid #E7E7E7;border-radius:1.15rem;padding:1.7rem 1.6rem 1.5rem;overflow:hidden;text-decoration:none;box-shadow:0 1px 2px rgba(38,38,38,.04);transition:transform .28s cubic-bezier(.2,.7,.3,1),box-shadow .28s ease,border-color .28s ease,background .28s ease}'
  '.tsvc-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:linear-gradient(180deg,#FC9700,#F6BB06);transform:scaleY(0);transform-origin:top;transition:transform .3s ease}'
  '.tsvc-card::after{content:"";position:absolute;right:-32px;top:-32px;width:130px;height:130px;border-radius:50%;background:radial-gradient(circle,rgba(252,151,0,.10),rgba(252,151,0,0) 70%);transition:transform .45s ease}'
  '.tsvc-card:hover{transform:translateY(-6px);box-shadow:0 24px 50px -18px rgba(105,119,131,.55);border-color:#697783;background:#697783}'
  '.tsvc-card:hover::before{transform:scaleY(1)}.tsvc-card:hover::after{transform:scale(1.7)}'
  '.tsvc-card:focus-visible{outline:2px solid #FC9700;outline-offset:3px}'
  '.tsvc-ico{position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:.9rem;background:#E8E6DA;color:#697783;flex:none;transition:background .28s ease,color .28s ease,transform .28s ease}'
  '.tsvc-card:hover .tsvc-ico{background:#FC9700;color:#fff;transform:rotate(-6deg) scale(1.05)}'
  '.tsvc-name{position:relative;z-index:1;font-weight:700;color:#262626;font-size:1.18rem;line-height:1.15;margin:0;transition:color .28s ease}'
  '.tsvc-card:hover .tsvc-name{color:#fff}'
  '.tsvc-desc{position:relative;z-index:1;color:#697783;font-size:.96rem;line-height:1.55;margin:0;flex:1;transition:color .28s ease}'
  '.tsvc-card:hover .tsvc-desc{color:#E8E6DA}'
  '.tsvc-cta{position:relative;z-index:1;display:inline-flex;align-items:center;gap:.45rem;font-weight:700;font-size:.76rem;letter-spacing:.07em;text-transform:uppercase;color:#FC9700;margin-top:.2rem;transition:color .28s ease}'
  '.tsvc-card:hover .tsvc-cta{color:#fff}'
  '.tsvc-cta svg{transition:transform .28s ease}.tsvc-card:hover .tsvc-cta svg{transform:translateX(5px)}'
  '@media (prefers-reduced-motion:reduce){.tsvc-card,.tsvc-ico,.tsvc-cta svg,.tsvc-card::before,.tsvc-card::after{transition:none}}'
  '</style>')
TOWN_SERVICES_DATA=[
 ("storage-solutions.html","container","Containerised Storage","Sealed wooden containers in our dry, alarmed indoor warehouse."),
 ("long-term-storage.html","calendar","Long-Term Storage","Months or years &mdash; and better value the longer you stay."),
 ("short-term-storage.html","clock","Short-Term Storage","Flexible weekly terms for moves, chain delays and renovations."),
 ("business-storage.html","briefcase","Business Storage","Stock, archives &amp; equipment, collected and redelivered."),
 ("furniture-storage.html","sofa","Furniture Storage","Blanket-wrapped, sealed and handled with proper care."),
 ("how-it-works.html","van","Packing &amp; Collection","We bring the materials, pack and collect from your door."),
]
def town_services(tn):
    cells="".join(
        f'<a href="{h}" class="tsvc-card" aria-label="{t} in {tn}">'
        f'<span class="tsvc-ico">{TSVC_ICONS[ic]}</span>'
        f'<h3 class="tsvc-name">{t}</h3><p class="tsvc-desc">{d}</p>'
        f'<span class="tsvc-cta">Learn more {TSVC_ARROW}</span></a>'
        for h,ic,t,d in TOWN_SERVICES_DATA)
    return centered("bg-lightgrey","Storage Services in "+tn,"Whatever you need to store in "+tn+", we tailor a fully managed, fully insured solution &mdash; collected from your door from just &pound;15 a week.",TSVC_CSS+'<div class="tsvc-grid">'+cells+'</div>')
def town_usps(tn):
    usps=[("Fully Insured &amp; Alarmed","Sealed containers in a 24/7 CCTV, alarmed indoor warehouse, fully insured throughout your stay."),
          ("Family-Run Since 2016","A local, LAPADA-accredited family team that treats your belongings like our own."),
          ("From &pound;15/week, No Deposit","Honest weekly pricing with no deposit and no hidden fees &mdash; pay only for the space you use."),
          ("We Come to You","No unit to drive to &mdash; we pack, collect from your "+tn+" door and redeliver on 24 hours&rsquo; notice.")]
    cells="".join(f'<div class="col-span-12 sm:col-span-6 lg:col-span-3"><div class="bg-white rounded-2xl shadow-custom p-6 h-full"><h3 class="font-bold text-black text-lg mb-2">{t}</h3><p class="text-darkgrey mb-0">{d}</p></div></div>' for t,d in usps)
    return centered("bg-lightgrey","Why "+tn+" Chooses Wolves Storage","Local, managed and genuinely cared for &mdash; the reasons "+tn+" stores with us.",'<div class="grid grid-cols-12 gap-4 lg:gap-6">'+cells+'</div>')
def town_nearby(t):
    try: here=(float(t["lat"]),float(t["lng"]))
    except: return ""
    others=[x for x in TOWNS if x.get("slug")!=t.get("slug") and x.get("lat")]
    near=sorted(others,key=lambda x:(float(x["lat"])-here[0])**2+(float(x["lng"])-here[1])**2)[:6]
    chips="".join(f'<a href="{x["slug"]}.html" class="inline-block bg-lightgrey rounded-full px-5 py-2 font-semibold text-black shadow-custom hover:text-orange">Storage in {x["town"]}</a>' for x in near)
    return centered("bg-white","Areas Near "+t["town"]+" We Also Cover","Our managed collection service reaches right across the area &mdash; here are nearby towns we store for too.",'<div class="flex flex-wrap gap-3 justify-center">'+chips+'</div>')

def town(t):
    h1="Storage in "+t["town"]+", "+t.get("region","West Sussex")
    secs=[
        hero(IMG(t["hero"]),t["hero_alt"],h1,t["sub"],t["checks"],big=False),
        TOWN_STATS,
        split("bg-white",t["s1_h2"],t["s1"],IMG(t["img2"]),t["img2_alt"]),
        town_services(t["town"]),
        split("bg-white",t["s2_h2"],t["s2"],IMG(t["img3"]),t["img3_alt"],reverse=True),
        town_usps(t["town"]),
        split("bg-white",t["s3_h2"],t["s3"],IMG(t["img4"]),t["img4_alt"]),
    ]
    if t.get("extra"): secs.append(t["extra"])
    secs+=[process(),town_map(t),town_nearby(t),faq(t["faqs"]),cta_band(t["cta"],IMG("gallery-warehouse-b.webp"))]
    return dict(file=t["slug"]+".html",slug="town",nav="Storage in "+t["town"],
        title=t["title"],meta=t["meta"],hero=IMG(t["hero"]),faqs=t["faqs"],
        crumb_parent=("areas-we-cover.html","Areas We Cover"),extra_schema=town_service_schema(t),
        sections=secs)

TOWNS = [
 dict(slug="storage-ashington",town="Ashington",lat="50.9270",lng="-0.4470",
  title="Storage in Ashington | Wolves Storage Sussex",
  meta="Managed container storage in Ashington, West Sussex from £15/week. We're based in the village — we pack, collect, store and redeliver. Free quote in 24 hours.",
  hero="hero-facility-van.webp",hero_alt="Wolves Storage Sussex facility and van in Ashington, West Sussex",
  sub="We&rsquo;re based right here in Ashington &mdash; clean, dry, fully managed container storage on your doorstep, from just &pound;15 a week with collection and redelivery included.",
  checks=["Our storage facility is in Ashington (RH20 3JT)","We pack, collect, seal &amp; store for you","Alarmed, 24/7 CCTV &amp; fully insured","From &pound;15/week, no deposit"],
  s1_h2="Managed Storage in Ashington &mdash; On Your Doorstep",
  s1=["Our storage facility is right here in Ashington, at Doryln House on London Road (RH20 3JT). That means no driving to an out-of-town unit and no queueing for a lift &mdash; we come to your home, pack and wrap your belongings, seal them into your own wooden container and store them in our alarmed indoor warehouse just minutes away.",
      "Whether you&rsquo;re moving within the village, renovating, decluttering or freeing up a room, you get fully managed storage from just &pound;15 a week with collection and redelivery included. See exactly <a href=\"how-it-works.html\">how it works</a> or check our transparent <a href=\"pricing.html\">storage prices</a>."],
  img2="hero-team-loading.webp",img2_alt="Wolves Storage Sussex team packing a container for an Ashington customer",
  s2_h2="Why Ashington Stores With Wolves",
  s2=["As a family-run business based in the village since 2016, we&rsquo;re your genuine local storer &mdash; not a faceless national chain. Being on the doorstep keeps collection fast, redelivery quick (just 24 hours&rsquo; notice) and our whole service personal.",
      "We&rsquo;re LAPADA accredited, Checkatrade-verified and fully insured, rated 5.0 from 478 reviews and trusted by estate agents along the A24 corridor. Your belongings stay clean, dry and secure with neighbours who genuinely care."],
  img3="hero-containers-van.webp",img3_alt="Sealed storage containers at the Wolves Storage Sussex Ashington warehouse",
  s3_h2="Storage for Every Ashington Need",
  s3=["From a few boxes during a house sale to the entire contents of a home between completion dates, we handle <a href=\"short-term-storage.html\">short-term</a> and <a href=\"long-term-storage.html\">long-term</a> storage, plus <a href=\"business-storage.html\">business storage</a> for local traders and offices and dedicated <a href=\"furniture-storage.html\">furniture storage</a>.",
      "We also cover the surrounding area &mdash; neighbouring <a href=\"storage-washington.html\">Washington</a>, <a href=\"storage-storrington.html\">Storrington</a> and <a href=\"storage-pulborough.html\">Pulborough</a> are all just minutes from base. Not sure how much space you need? Use our <a href=\"storage-size-guide.html\">storage size guide</a>."],
  img4="gallery-warehouse-a.webp",img4_alt="Inside the secure Wolves Storage Sussex warehouse in Ashington",
  cta="Need Storage in Ashington? Get a Free Quote",
  faqs=[("Where is your storage facility in Ashington?","We&rsquo;re at Doryln House, London Road, Ashington, Pulborough RH20 3JT &mdash; managed container storage right in the village."),
        ("Do I need to bring my items to you?","No &mdash; we collect from your Ashington home, pack and wrap everything, and store it for you. You never hire a van or lift a box."),
        ("How much is storage in Ashington?","From just &pound;15 per week per container, with no deposit and no hidden fees. Collection and redelivery are included."),
        ("How quickly can I get my belongings back?","Give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your door anywhere in and around Ashington."),
        ("Is my storage insured and secure?","Yes &mdash; sealed wooden containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured, LAPADA accredited and Checkatrade-verified.")]),
 dict(slug="storage-washington",town="Washington",lat="50.9090",lng="-0.4170",
  title="Storage in Washington | Wolves Storage Sussex",
  meta="Secure managed storage in Washington, West Sussex from £15/week. Minutes from our Ashington base — we collect, store and redeliver. No deposit. Free 24-hour quote.",
  hero="hero-containers-van.webp",hero_alt="Wolves Storage Sussex containers and van serving Washington, West Sussex",
  sub="Just down the A24 from our base, Washington gets the same fast, fully managed container storage &mdash; we collect from your door, store securely and redeliver, from &pound;15 a week.",
  checks=["Minutes from our Ashington (RH20) base","Door-to-door collection &amp; redelivery","Sealed containers, alarmed &amp; insured","From &pound;15/week, no deposit"],
  s1_h2="Local Managed Storage for Washington",
  s1=["Washington sits right beside our Ashington warehouse at the foot of the South Downs, where the A24 meets the A283. Because we&rsquo;re practically next door, collection is quick and redelivery takes just 24 hours&rsquo; notice &mdash; ideal whether you&rsquo;re moving home, renovating a Downland cottage or clearing space.",
      "Our team brings the materials, packs and wraps everything, and seals it into your own container stored in our dry, alarmed indoor facility. It&rsquo;s fully managed from &pound;15 a week &mdash; see <a href=\"how-it-works.html\">how it works</a>."],
  img2="gallery-loading.webp",img2_alt="Wolves Storage Sussex loading a container for a Washington customer",
  s2_h2="Why Washington Chooses Wolves",
  s2=["You won&rsquo;t find a closer, more genuinely local storer. We&rsquo;ve served the villages around Chanctonbury since 2016 as a family-run team, so your belongings stay minutes away rather than in some distant industrial unit.",
      "Fully insured, 24/7 CCTV, LAPADA accredited and Checkatrade-verified, rated 5.0 from 478 reviews. Compare our honest <a href=\"pricing.html\">prices</a> or browse <a href=\"storage-solutions.html\">storage solutions</a>."],
  img3="hero-forklift.webp",img3_alt="Forklift stacking storage containers near Washington, West Sussex",
  s3_h2="Storage to Suit Any Washington Move",
  s3=["Choose <a href=\"short-term-storage.html\">short-term storage</a> to bridge a move, <a href=\"long-term-storage.html\">long-term storage</a> for a renovation or time abroad, or <a href=\"furniture-storage.html\">furniture storage</a> while you redecorate.",
      "We also serve neighbouring <a href=\"storage-ashington.html\">Ashington</a>, <a href=\"storage-storrington.html\">Storrington</a> and <a href=\"storage-steyning.html\">Steyning</a> &mdash; see every <a href=\"areas-we-cover.html\">area we cover</a>."],
  img4="gallery-van.webp",img4_alt="Wolves Storage Sussex van collecting from a Washington home",
  cta="Storing in Washington? Get a Free Quote",
  faqs=[("Do you cover Washington, West Sussex?","Yes &mdash; Washington is minutes from our Ashington base, so we collect, store and redeliver here quickly and easily."),
        ("How does managed storage work?","We bring packing materials, wrap and load your items into a sealed container, and store it in our alarmed warehouse. You never lift a box or hire a van."),
        ("How much does storage cost?","From &pound;15 per week per container with no deposit and no hidden fees, including collection and redelivery."),
        ("Can I access my belongings?","Yes &mdash; give us 24 hours&rsquo; notice and we redeliver to your Washington address."),
        ("Are my items insured?","Absolutely &mdash; everything is fully insured in an alarmed, 24/7 CCTV indoor facility.")]),
 dict(slug="storage-storrington",town="Storrington",lat="50.9170",lng="-0.4520",
  title="Storage in Storrington | Wolves Storage Sussex",
  meta="Managed container storage in Storrington from £15/week. Local family team collect, seal & store your belongings. No deposit. Free 24-hour quote.",
  hero="hero-forklift.webp",hero_alt="Forklift stacking storage containers for Storrington customers",
  sub="Storrington&rsquo;s local storage team &mdash; we pack, collect and seal your belongings into secure containers just minutes from the village, from &pound;15 a week, fully managed.",
  checks=["A few minutes from the village centre","We pack, collect &amp; seal for you","Dry, alarmed &amp; fully insured","From &pound;15/week, no deposit"],
  s1_h2="Fully Managed Storage in Storrington",
  s1=["A short hop along the A283 from our Ashington warehouse, Storrington is firmly on our doorstep. We come to your home at the foot of the Downs, pack and wrap your belongings, and seal them into your own wooden container &mdash; no van hire, no driving to a unit, no heavy lifting.",
      "Everything is stored in our dry, alarmed indoor facility and brought back on 24 hours&rsquo; notice. It&rsquo;s fully managed from just &pound;15 a week &mdash; see <a href=\"how-it-works.html\">how it works</a> or our <a href=\"pricing.html\">prices</a>."],
  img2="hero-team-loading.webp",img2_alt="Wolves Storage Sussex team wrapping furniture for a Storrington home",
  s2_h2="Why Storrington Trusts Wolves",
  s2=["Being a genuinely local, family-run team matters: your belongings stay minutes away, our service is personal, and we know the lanes around Sullington and Thakeham well. We&rsquo;ve served the area since 2016.",
      "LAPADA accredited, Checkatrade-verified, fully insured and rated 5.0 from 478 reviews &mdash; the same care a national chain simply can&rsquo;t match. Explore our <a href=\"storage-solutions.html\">storage solutions</a>."],
  img3="hero-packed-container.webp",img3_alt="A sealed container packed with a Storrington customer's furniture",
  s3_h2="Storage for Homes &amp; Businesses in Storrington",
  s3=["From <a href=\"short-term-storage.html\">short-term</a> space during a move to <a href=\"long-term-storage.html\">long-term</a> storage and <a href=\"business-storage.html\">business storage</a> for village traders, we tailor it to you &mdash; plus dedicated <a href=\"furniture-storage.html\">furniture storage</a>.",
      "We also cover nearby <a href=\"storage-pulborough.html\">Pulborough</a>, <a href=\"storage-washington.html\">Washington</a> and <a href=\"storage-ashington.html\">Ashington</a>. Not sure on space? Try our <a href=\"storage-size-guide.html\">size guide</a>."],
  img4="gallery-warehouse-b.webp",img4_alt="Secure indoor storage warehouse serving Storrington, West Sussex",
  cta="Need Storage in Storrington? Get a Free Quote",
  faqs=[("Do you offer storage in Storrington?","Yes &mdash; Storrington is just a few minutes from our Ashington base, so we collect, store and redeliver here with ease."),
        ("Will you collect from my Storrington home?","Yes &mdash; we bring the materials, pack and wrap your belongings, and load them into a sealed container. You never hire a van."),
        ("How much is storage in Storrington?","From &pound;15 per week per container, no deposit and no hidden fees, with collection and redelivery included."),
        ("How do I get items back?","Just give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your door in Storrington."),
        ("Is my container secure?","Yes &mdash; sealed and stored in an alarmed, 24/7 CCTV indoor warehouse, fully insured.")]),
 dict(slug="storage-pulborough",town="Pulborough",lat="50.9580",lng="-0.5130",
  title="Storage in Pulborough | Wolves Storage Sussex",
  meta="Secure managed storage in Pulborough, West Sussex from £15/week. On your doorstep (RH20) — we pack, collect, store and redeliver. Fully insured. Free 24-hour quote.",
  hero="hero-fleet.webp",hero_alt="Wolves Storage Sussex van fleet serving Pulborough, West Sussex",
  sub="Pulborough shares our RH20 postcode &mdash; managed container storage right on your doorstep, from &pound;15 a week, with packing, collection and redelivery all included.",
  checks=["Same RH20 area as our base","Packing, collection &amp; redelivery included","Sealed, dry, alarmed &amp; insured","From &pound;15/week, no deposit"],
  s1_h2="Managed Storage in Pulborough",
  s1=["Pulborough sits in our own RH20 postcode, a few minutes up the A283 and A29 from our warehouse. We collect from your home near the River Arun or the Brooks, pack and seal your belongings into your own container, and store them securely &mdash; no driving to a unit, ever.",
      "It&rsquo;s fully managed from &pound;15 a week, with redelivery on 24 hours&rsquo; notice. See <a href=\"how-it-works.html\">how it works</a> or check the <a href=\"pricing.html\">prices</a>."],
  img2="gallery-loading.webp",img2_alt="Loading a storage container for a Pulborough customer",
  s2_h2="Your Local Pulborough Storage Team",
  s2=["Because we&rsquo;re practically neighbours, you get a level of local care the national operators can&rsquo;t: fast collection, quick redelivery and a family team that has served the area since 2016.",
      "Fully insured, LAPADA accredited and Checkatrade-verified, rated 5.0 from 478 reviews. Whatever you&rsquo;re storing, browse our <a href=\"storage-solutions.html\">storage solutions</a>."],
  img3="hero-containers-van.webp",img3_alt="Sealed storage containers ready for a Pulborough collection",
  s3_h2="Storage for Every Pulborough Need",
  s3=["Use <a href=\"short-term-storage.html\">short-term storage</a> between completion dates, <a href=\"long-term-storage.html\">long-term storage</a> for an extended stay, <a href=\"business-storage.html\">business storage</a> for stock, or <a href=\"furniture-storage.html\">furniture storage</a> during a renovation.",
      "We also serve nearby <a href=\"storage-storrington.html\">Storrington</a>, <a href=\"storage-billingshurst.html\">Billingshurst</a> and <a href=\"storage-ashington.html\">Ashington</a> &mdash; see all <a href=\"areas-we-cover.html\">areas we cover</a>."],
  img4="gallery-clipboard.webp",img4_alt="Wolves Storage Sussex booking a free storage quote in Pulborough",
  cta="Storing in Pulborough? Get a Free Quote",
  faqs=[("Do you cover Pulborough?","Yes &mdash; Pulborough is in our own RH20 area, so we collect, store and redeliver here quickly."),
        ("Is collection included?","Yes &mdash; collection and redelivery across Pulborough are included in the price. You never hire a van or lift a box."),
        ("How much does storage cost in Pulborough?","From &pound;15 per week per container, with no deposit and no hidden fees."),
        ("How fast can I access my things?","Give us 24 hours&rsquo; notice and we redeliver to your Pulborough address."),
        ("Are my belongings insured?","Yes &mdash; sealed containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured.")]),
 dict(slug="storage-henfield",town="Henfield",lat="50.9290",lng="-0.2760",
  title="Storage in Henfield | Wolves Storage Sussex",
  meta="Managed container storage in Henfield, West Sussex from £15/week. Your local family alternative — we collect, store & redeliver. Free quote.",
  hero="hero-packed-container.webp",hero_alt="A packed storage container collected from a Henfield home",
  sub="Henfield&rsquo;s local, family-run storage alternative &mdash; we collect from your door, seal your belongings into secure containers and redeliver when you&rsquo;re ready, from &pound;15 a week.",
  checks=["Genuinely local, family-run team","We collect, seal &amp; store for you","Alarmed, 24/7 CCTV &amp; fully insured","From &pound;15/week, no deposit"],
  s1_h2="Fully Managed Storage in Henfield",
  s1=["A short drive along the A281 from our Ashington base, Henfield gets our complete managed service. We come to your home near the village high street, Small Dole or Woodmancote, pack and wrap your belongings, and seal them into your own wooden container.",
      "Everything is stored in our dry, alarmed indoor warehouse and brought back on 24 hours&rsquo; notice &mdash; fully managed from &pound;15 a week. See <a href=\"how-it-works.html\">how it works</a>."],
  img2="hero-team-loading.webp",img2_alt="Wolves Storage Sussex team packing belongings for a Henfield customer",
  s2_h2="The Local Choice for Henfield Storage",
  s2=["You don&rsquo;t have to settle for a big self-storage warehouse: as a family-run team since 2016, we offer Henfield a friendlier, fully managed alternative where we do the packing, lifting and driving for you.",
      "LAPADA accredited, Checkatrade-verified, fully insured and rated 5.0 from 478 reviews. Curious how managed storage compares? Browse our <a href=\"storage-solutions.html\">storage solutions</a> and <a href=\"pricing.html\">prices</a>."],
  img3="gallery-warehouse-a.webp",img3_alt="Secure indoor container storage warehouse serving Henfield",
  s3_h2="Storage for Homes &amp; Businesses in Henfield",
  s3=["Whether it&rsquo;s <a href=\"short-term-storage.html\">short-term storage</a> for a move, <a href=\"long-term-storage.html\">long-term storage</a>, <a href=\"furniture-storage.html\">furniture storage</a> during a renovation or <a href=\"business-storage.html\">business storage</a> for a local trader, we tailor it to you.",
      "We also cover neighbouring <a href=\"storage-steyning.html\">Steyning</a> and the villages toward Partridge Green &mdash; see all <a href=\"areas-we-cover.html\">areas we cover</a>."],
  img4="gallery-van.webp",img4_alt="Wolves Storage Sussex van collecting from a Henfield home",
  cta="Need Storage in Henfield? Get a Free Quote",
  faqs=[("Do you provide storage in Henfield?","Yes &mdash; we&rsquo;re a short drive from Henfield and collect, store and redeliver here as your local managed-storage team."),
        ("How is this different from self-storage?","With us you don&rsquo;t drive to a unit or do the lifting &mdash; we pack, collect and store your sealed container, then redeliver on request."),
        ("How much is storage in Henfield?","From &pound;15 per week per container, no deposit and no hidden fees, including collection and redelivery."),
        ("Can I get my items back quickly?","Yes &mdash; just 24 hours&rsquo; notice and we redeliver to your Henfield address."),
        ("Is everything insured and secure?","Yes &mdash; sealed containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured and LAPADA accredited.")]),
 dict(slug="storage-steyning",town="Steyning",lat="50.8900",lng="-0.3290",
  title="Storage in Steyning | Wolves Storage Sussex",
  meta="Secure managed storage in Steyning, West Sussex from £15/week. We collect from your door, seal and store — fully insured, no deposit. Free quote within 24 hours.",
  hero="hero-containers-van.webp",hero_alt="Wolves Storage Sussex containers and van serving Steyning, West Sussex",
  sub="Storage for Steyning, Bramber and Upper Beeding &mdash; we collect from your door, seal your belongings into secure containers and redeliver when you need them, from &pound;15 a week.",
  checks=["Covering Steyning, Bramber &amp; Beeding","Door collection &amp; redelivery included","Sealed, dry, alarmed &amp; insured","From &pound;15/week, no deposit"],
  s1_h2="Managed Storage in Steyning",
  s1=["A few minutes from our base along the A283, the historic market town of Steyning and its neighbours Bramber and Upper Beeding all sit comfortably within our patch. We collect from your home beneath the Downs, pack and wrap everything, and seal it into your own container.",
      "Stored in our alarmed indoor warehouse and redelivered on 24 hours&rsquo; notice, it&rsquo;s fully managed from &pound;15 a week. See <a href=\"how-it-works.html\">how it works</a> and our <a href=\"pricing.html\">prices</a>."],
  img2="gallery-forklift-b.webp",img2_alt="Forklift moving storage containers for a Steyning customer",
  s2_h2="Why Steyning Stores With Wolves",
  s2=["Storing close to home matters in a town like Steyning, and we&rsquo;ve looked after local families and businesses since 2016 as a genuinely local, family-run team &mdash; not a distant chain.",
      "Fully insured, LAPADA accredited, Checkatrade-verified and rated 5.0 from 478 reviews. Explore our <a href=\"storage-solutions.html\">storage solutions</a> to find the right fit."],
  img3="hero-team-loading.webp",img3_alt="Wolves Storage Sussex team loading a container in Steyning",
  s3_h2="Flexible Storage for Steyning",
  s3=["From <a href=\"short-term-storage.html\">short-term storage</a> during a chain delay to <a href=\"long-term-storage.html\">long-term</a> options, <a href=\"furniture-storage.html\">furniture storage</a> and <a href=\"business-storage.html\">business storage</a>, we shape it around you.",
      "We also serve nearby <a href=\"storage-henfield.html\">Henfield</a> and <a href=\"storage-washington.html\">Washington</a>, plus <a href=\"storage-shoreham-by-sea.html\">Shoreham-by-Sea</a> and the coast &mdash; or see all <a href=\"areas-we-cover.html\">areas we cover</a>."],
  img4="gallery-warehouse-b.webp",img4_alt="Indoor secure storage warehouse serving Steyning, West Sussex",
  cta="Storing in Steyning? Get a Free Quote",
  faqs=[("Do you cover Steyning and the nearby villages?","Yes &mdash; we cover Steyning, Bramber and Upper Beeding, collecting, storing and redelivering across the area."),
        ("Do you collect from my home?","Yes &mdash; we bring the materials, pack and wrap everything, and load it into a sealed container. No van hire needed."),
        ("How much does storage cost in Steyning?","From &pound;15 per week per container with no deposit and no hidden fees."),
        ("How quickly can I access my items?","Give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your Steyning address."),
        ("Is my storage insured?","Yes &mdash; sealed containers kept in an alarmed, 24/7 CCTV indoor facility, fully insured.")]),
 dict(slug="storage-billingshurst",town="Billingshurst",lat="51.0220",lng="-0.4530",
  title="Storage in Billingshurst | Wolves Storage",
  meta="Managed container storage in Billingshurst (RH14) from £15/week. We pack, collect, store and redeliver — no deposit, fully insured. Free quote in 24 hours.",
  hero="hero-team-loading.webp",hero_alt="Wolves Storage Sussex team loading a container for Billingshurst",
  sub="Managed storage for Billingshurst and the RH14 villages &mdash; we pack, collect and seal your belongings into secure containers, then redeliver when you&rsquo;re ready, from &pound;15 a week.",
  checks=["Covering Billingshurst &amp; RH14 villages","We pack, collect &amp; seal for you","Dry, alarmed &amp; fully insured","From &pound;15/week, no deposit"],
  s1_h2="Fully Managed Storage in Billingshurst",
  s1=["Just north of our base along the A29, Billingshurst and its surrounding villages are an easy run for our team. We collect from your home near the high street or the station, pack and wrap your belongings, and seal them into your own wooden container.",
      "Stored in our dry, alarmed warehouse and redelivered on 24 hours&rsquo; notice, it&rsquo;s fully managed from &pound;15 a week. See <a href=\"how-it-works.html\">how it works</a> and our <a href=\"pricing.html\">prices</a>."],
  img2="hero-containers-van.webp",img2_alt="Storage containers and van serving Billingshurst, West Sussex",
  s2_h2="Why Billingshurst Chooses Wolves",
  s2=["As a family-run business serving the area since 2016, we keep things personal and local &mdash; your belongings stay nearby and your collection is handled by a team that knows the RH14 lanes.",
      "Fully insured, LAPADA accredited, Checkatrade-verified and rated 5.0 from 478 reviews. Find the right option in our <a href=\"storage-solutions.html\">storage solutions</a>."],
  img3="gallery-loading.webp",img3_alt="Loading belongings into a container for a Billingshurst customer",
  s3_h2="Storage for Homes &amp; Businesses in Billingshurst",
  s3=["Whether you need <a href=\"short-term-storage.html\">short-term storage</a> during a move, <a href=\"long-term-storage.html\">long-term storage</a>, <a href=\"furniture-storage.html\">furniture storage</a> or <a href=\"business-storage.html\">business storage</a> for stock and archives, we tailor it to you.",
      "We also cover nearby <a href=\"storage-pulborough.html\">Pulborough</a> and <a href=\"storage-horsham.html\">Horsham</a> &mdash; see all <a href=\"areas-we-cover.html\">areas we cover</a> or our <a href=\"storage-size-guide.html\">size guide</a>."],
  img4="hero-forklift.webp",img4_alt="Forklift stacking storage containers for Billingshurst customers",
  cta="Need Storage in Billingshurst? Get a Free Quote",
  faqs=[("Do you offer storage in Billingshurst?","Yes &mdash; Billingshurst is a short run north of our base and we collect, store and redeliver across the RH14 area."),
        ("Do you collect from my home?","Yes &mdash; we bring materials, pack and wrap your items, and load them into a sealed container. No van hire or lifting for you."),
        ("How much is storage in Billingshurst?","From &pound;15 per week per container, no deposit and no hidden fees, including collection and redelivery."),
        ("How do I get my belongings back?","Just 24 hours&rsquo; notice and we redeliver to your Billingshurst address."),
        ("Is my container secure and insured?","Yes &mdash; sealed and stored in an alarmed, 24/7 CCTV indoor warehouse, fully insured.")]),
 dict(slug="storage-horsham",town="Horsham",lat="51.0630",lng="-0.3270",
  title="Storage in Horsham | Wolves Storage Sussex",
  meta="Managed storage in Horsham, West Sussex from £15/week. We collect across RH12 and RH13, store securely and redeliver — no deposit, fully insured. Free 24-hour quote.",
  hero="hero-facility-van.webp",hero_alt="Wolves Storage Sussex facility and van serving Horsham, West Sussex",
  sub="Fully managed container storage across Horsham &mdash; we collect from anywhere in RH12 and RH13, store your sealed belongings securely and redeliver on request, from &pound;15 a week.",
  checks=["Collecting across RH12 &amp; RH13","Packing, collection &amp; redelivery included","Sealed, alarmed, 24/7 CCTV &amp; insured","From &pound;15/week, no deposit"],
  s1_h2="Managed Storage Across Horsham",
  s1=["Horsham is the busiest town in our catchment, and our managed model suits it perfectly: instead of renting a unit on an industrial estate and driving your things across town, we come to you. From the Carfax to Roffey, Broadbridge Heath to Southwater, we pack, wrap and seal your belongings into your own container.",
      "Everything is stored in our dry, alarmed indoor warehouse and redelivered on 24 hours&rsquo; notice &mdash; fully managed from &pound;15 a week. See exactly <a href=\"how-it-works.html\">how it works</a> or check the <a href=\"pricing.html\">prices</a>."],
  img2="hero-team-loading.webp",img2_alt="Wolves Storage Sussex team packing a container for a Horsham home",
  s2_h2="Why Horsham Stores With Wolves",
  s2=["With so many storage options around Horsham, the difference is service: we&rsquo;re a family-run team that has looked after Sussex homes since 2016, doing the packing, lifting and driving so you don&rsquo;t have to.",
      "Fully insured, LAPADA accredited, Checkatrade-verified and rated 5.0 from 478 reviews &mdash; and we&rsquo;re trusted by Horsham estate agents. Prefer self-storage? See why our <a href=\"storage-solutions.html\">managed containers</a> are cleaner and more secure."],
  img3="hero-containers-van.webp",img3_alt="Sealed storage containers ready for a Horsham collection",
  s3_h2="Storage for Every Horsham Move",
  s3=["From <a href=\"short-term-storage.html\">short-term storage</a> between houses to <a href=\"long-term-storage.html\">long-term</a> options, <a href=\"furniture-storage.html\">furniture storage</a> during a renovation and <a href=\"business-storage.html\">business storage</a> for the town&rsquo;s many offices and retailers, we tailor everything to you.",
      "We also cover nearby <a href=\"storage-billingshurst.html\">Billingshurst</a> and <a href=\"storage-washington.html\">Washington</a> &mdash; and you can size up your move with our <a href=\"storage-size-guide.html\">storage size guide</a>."],
  img4="gallery-warehouse-a.webp",img4_alt="Inside the secure Wolves Storage Sussex warehouse serving Horsham",
  extra=centered("bg-lightgrey","Who We Help Across Horsham","From busy professionals to growing businesses, our managed storage fits homes and offices right across the RH12 and RH13 postcodes.",
        checklist(["Families moving home or caught in a chain delay","Homeowners renovating or extending","Downsizers and people clearing a property","Landlords and tenants between tenancies","Businesses freeing up office or retail space","Students and people working away from home"],center=True)),
  cta="Need Storage in Horsham? Get a Free Quote",
  faqs=[("Do you cover all of Horsham?","Yes &mdash; we collect, store and redeliver right across the RH12 and RH13 postcodes, including Roffey, Broadbridge Heath and Southwater."),
        ("Is this self-storage or managed storage?","Managed &mdash; you don&rsquo;t drive to a unit. We pack, collect and store your sealed container, then redeliver when you ask."),
        ("How much does storage cost in Horsham?","From &pound;15 per week per container, with no deposit and no hidden fees, including collection and redelivery."),
        ("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote, and we redeliver on 24 hours&rsquo; notice."),
        ("Are my belongings insured in Horsham?","Yes &mdash; sealed containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured and LAPADA accredited.")]),
 dict(slug="storage-worthing",town="Worthing",lat="50.8180",lng="-0.3720",
  title="Storage in Worthing | Wolves Storage Sussex",
  meta="Managed storage in Worthing, West Sussex from £15/week. We collect across BN11–BN14 — ideal for moves, downsizing & students. Free quote.",
  hero="hero-fleet.webp",hero_alt="Wolves Storage Sussex van fleet serving Worthing, West Sussex",
  sub="Fully managed container storage across Worthing &mdash; we collect from anywhere in BN11 to BN14, store your sealed belongings securely and redeliver on request, from &pound;15 a week.",
  checks=["Collecting across BN11&ndash;BN14","Packing, collection &amp; redelivery included","Sealed, alarmed, 24/7 CCTV &amp; insured","From &pound;15/week, no deposit"],
  s1_h2="Managed Storage Across Worthing",
  s1=["Down the A24 on the coast, Worthing is one of the largest towns we serve. Rather than hiring a seafront self-storage unit and ferrying boxes back and forth, you let us come to you &mdash; from the town centre to Goring, Durrington to Findon Valley, we pack, wrap and seal your belongings into your own container.",
      "Stored in our dry, alarmed indoor warehouse and redelivered on 24 hours&rsquo; notice, it&rsquo;s fully managed from &pound;15 a week. See <a href=\"how-it-works.html\">how it works</a> or our <a href=\"pricing.html\">prices</a>."],
  img2="gallery-loading.webp",img2_alt="Wolves Storage Sussex loading a container for a Worthing customer",
  s2_h2="Why Worthing Chooses Wolves",
  s2=["Worthing&rsquo;s mix of downsizers, families and students makes managed storage especially handy &mdash; no van, no driving, no lifting. We&rsquo;ve served the Sussex coast since 2016 as a family-run team.",
      "Fully insured, LAPADA accredited, Checkatrade-verified and rated 5.0 from 478 reviews. Storing furniture? See our dedicated <a href=\"furniture-storage.html\">furniture storage</a>."],
  img3="hero-packed-container.webp",img3_alt="A sealed container packed with a Worthing customer's belongings",
  s3_h2="Storage for Every Worthing Need",
  s3=["Whether it&rsquo;s <a href=\"short-term-storage.html\">short-term storage</a> during a move, <a href=\"long-term-storage.html\">long-term storage</a> while downsizing, <a href=\"business-storage.html\">business storage</a> for seafront traders or student storage over summer, we shape it around you.",
      "We also serve nearby <a href=\"storage-steyning.html\">Steyning</a>, <a href=\"storage-findon.html\">Findon</a> and <a href=\"storage-littlehampton.html\">Littlehampton</a> &mdash; see all <a href=\"areas-we-cover.html\">areas we cover</a>."],
  img4="gallery-van.webp",img4_alt="Wolves Storage Sussex van collecting from a Worthing home",
  extra=centered("bg-lightgrey","Storage That Suits Coastal Worthing","From seafront flats to family homes, our managed containers fit every kind of Worthing move across BN11 to BN14.",
        checklist(["Downsizers and retirees clearing space","Families moving home or between completions","Students storing over the summer holidays","Renovations, redecorations and staging for sale","Seafront and town-centre businesses with stock","Anyone who&rsquo;d rather not hire a van"],center=True)),
  cta="Storing in Worthing? Get a Free Quote",
  faqs=[("Do you cover all of Worthing?","Yes &mdash; we collect, store and redeliver across BN11, BN12, BN13 and BN14, including Goring, Durrington and Findon Valley."),
        ("Do I have to drive to a storage unit?","No &mdash; that&rsquo;s the point of managed storage. We come to your Worthing home, pack and collect, and redeliver when you need it."),
        ("How much is storage in Worthing?","From &pound;15 per week per container, no deposit and no hidden fees, with collection and redelivery included."),
        ("Do you offer student storage in Worthing?","Yes &mdash; we collect at the end of term, store your sealed boxes safely, and redeliver when you return."),
        ("Is my storage insured and secure?","Yes &mdash; sealed containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured and LAPADA accredited.")]),
]
# additional town pages (unique local content generated into a data file)
TOWNS += json.load(open(os.path.join(SITE,"partials","extra-towns.json"),encoding="utf-8"))
TOWNS += json.load(open(os.path.join(SITE,"partials","extra-towns-2.json"),encoding="utf-8"))

# ---------------- P0 content assets: size guide + furniture storage --------
SIZE_CARDS = [
 ("Studio or a few rooms","1 container","A small flat&rsquo;s worth of furniture, boxes and white goods."),
 ("1-bed flat","1 container","Around 250 cu ft &mdash; the typical contents of a one-bedroom home."),
 ("2-bed house","2 containers","Two bedrooms of furniture, sofas, appliances and boxes."),
 ("3-bed house","3&ndash;4 containers","A full family home, including garage and loft items."),
 ("4-bed+ house","4&ndash;5 containers","Larger homes &mdash; we simply add containers as needed."),
 ("Business &amp; stock","Scalable","Pallets, archives and stock &mdash; scale up or down anytime."),
]
SIZE_CSS=('<style>'
  '.sz-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1.25rem;text-align:left;margin-top:2.25rem}'
  '.sz-card{position:relative;display:flex;flex-direction:column;gap:.9rem;background:#fff;border:1px solid #E7E7E7;border-radius:1.15rem;padding:1.6rem;overflow:hidden;box-shadow:0 1px 2px rgba(38,38,38,.04);transition:transform .28s cubic-bezier(.2,.7,.3,1),box-shadow .28s ease,border-color .28s ease}'
  '.sz-card::after{content:"";position:absolute;right:-32px;top:-32px;width:130px;height:130px;border-radius:50%;background:radial-gradient(circle,rgba(252,151,0,.10),rgba(252,151,0,0) 70%);transition:transform .45s ease}'
  '.sz-card:hover{transform:translateY(-6px);box-shadow:0 24px 50px -18px rgba(105,119,131,.55);border-color:#697783;background:#697783}'
  '.sz-card:hover::after{transform:scale(1.6)}'
  '.sz-card:hover .sz-name{color:#fff}.sz-card:hover .sz-desc{color:#E8E6DA}'
  '.sz-top{position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;gap:1rem}'
  '.sz-ico{display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:.85rem;background:#E8E6DA;color:#697783;flex:none;transition:background .28s ease,color .28s ease,transform .28s ease}'
  '.sz-card:hover .sz-ico{background:#FC9700;color:#fff;transform:rotate(-6deg) scale(1.05)}'
  '.sz-badge{display:inline-flex;align-items:center;font-weight:700;font-size:.72rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:linear-gradient(135deg,#FC9700,#F6BB06);border-radius:999px;padding:.42rem .8rem;white-space:nowrap;box-shadow:0 6px 14px -6px rgba(252,151,0,.55)}'
  '.sz-name{position:relative;z-index:1;font-weight:700;color:#262626;font-size:1.22rem;line-height:1.15;margin:0;transition:color .28s ease}'
  '.sz-desc{position:relative;z-index:1;color:#697783;font-size:.96rem;line-height:1.55;margin:0;transition:color .28s ease}'
  '@media (prefers-reduced-motion:reduce){.sz-card,.sz-ico,.sz-card::after{transition:none}}'
  '</style>')
SIZE_BOX='<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>'
def size_cards():
    cells=""
    for name,cont,desc in SIZE_CARDS:
        cells+=(f'<div class="sz-card"><div class="sz-top"><span class="sz-ico">{SIZE_BOX}</span><span class="sz-badge">{cont}</span></div>'
                f'<h3 class="sz-name">{name}</h3><p class="sz-desc">{desc}</p></div>')
    return SIZE_CSS+'<div class="sz-grid">'+cells+'</div>'

def size_guide_page():
    faqs=[("How much storage space do I need?","As a rule of thumb, a one-bedroom home fits in one 250 cu ft container, a two-bed in two, and a three-bed in three to four. If you&rsquo;re unsure, we&rsquo;ll estimate it free during your quote."),
          ("How big is one storage container?","Each wooden container is 5ft &times; 7ft &times; 8.6ft &mdash; about 250 cubic feet, roughly the contents of a one-bedroom flat."),
          ("What if I need more space?","We simply add containers, so you only ever pay for the space you use &mdash; from &pound;15 per week per container."),
          ("Can you tell me how many containers I&rsquo;ll need?","Yes &mdash; tell us your home size or list your main items and we&rsquo;ll estimate the containers and price within 24 hours."),
          ("Do I pay for space I don&rsquo;t use?","No &mdash; managed storage means you pay per container, not for a half-empty room, so it&rsquo;s often better value than self-storage.")]
    inner1=('<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">Not sure how much storage you need? Use this quick guide to estimate how many containers your home or business will fill &mdash; then get an exact figure on your free quote.</p>'+size_cards())
    return dict(file="storage-size-guide.html",slug="guide",nav="Storage Size Guide",
      title="How Much Storage Do I Need? Size Guide | Wolves",
      meta="How much storage do you need? Our West Sussex size guide shows what fits in a 250 cu ft container, by home size. From £15/week. Free quote.",
      hero=IMG("hero-packed-container.webp"),faqs=faqs,
      crumb_parent=("how-it-works.html","How It Works"),
      sections=[
        hero(IMG("hero-packed-container.webp"),"A packed Wolves Storage Sussex container showing how much fits inside","How Much Storage Do I Need?",
          "Work out how much space your move needs in seconds. Our container size guide shows roughly what fits in each 250 cu ft container &mdash; and we&rsquo;ll confirm the exact figure free.",
          ["One container holds about a one-bed home","Pay only for the containers you use","From &pound;15/week, no deposit","Free space estimate within 24 hours"],big=False),
        centered("bg-lightgrey","Storage Size Guide by Home Size",None,inner1),
        split("bg-lightgrey","What Fits in One Container?",
          ["Each wooden container measures 5ft &times; 7ft &times; 8.6ft &mdash; around 250 cubic feet. That&rsquo;s comfortably the contents of a one-bedroom flat: a bed, sofa, a few appliances, a wardrobe and a stack of boxes.",
           "Bigger home? We just use more containers, sealed and stacked in our alarmed indoor warehouse, so you only ever pay for the space you actually fill. See our <a href=\"pricing.html\">prices</a> or <a href=\"storage-solutions.html\">storage solutions</a>."],
          IMG("hero-containers-van.webp"),"Wolves Storage Sussex 250 cubic foot wooden storage containers"),
        split("bg-white","Still Not Sure? We&rsquo;ll Estimate It Free",
          ["Guessing volume is hard, so we do it for you. Tell us your home size or list your main items and our team will estimate the number of containers &mdash; and the price &mdash; within 24 hours, with no obligation.",
           "It&rsquo;s all fully managed: we <a href=\"how-it-works.html\">pack, collect and store</a> for you, then redeliver on 24 hours&rsquo; notice. Storing furniture? See our <a href=\"furniture-storage.html\">furniture storage</a> page."],
          IMG("gallery-clipboard.webp"),"Wolves Storage Sussex estimating storage space for a free quote",reverse=True),
        faq(faqs),
        cta_band("Get a Free Storage Space Estimate",IMG("gallery-warehouse-b.webp")),
      ])

def furniture_page():
    faqs=[("How do you protect furniture in storage?","Every item is blanket-wrapped and padded, then sealed into your own wooden container in a dry, alarmed indoor warehouse &mdash; far better protection than an open self-storage unit."),
          ("Can you collect my furniture?","Yes &mdash; we bring the materials, wrap and load your furniture, and take it away. You never hire a van or lift a thing."),
          ("How much does furniture storage cost?","From &pound;15 per week per container, with no deposit and no hidden fees, including collection and redelivery."),
          ("Is my furniture insured?","Yes &mdash; everything is fully insured while it&rsquo;s with us, in an alarmed, 24/7 CCTV facility. We&rsquo;re LAPADA accredited for handling fine and antique furniture."),
          ("How long can I store furniture for?","As long as you like &mdash; flexible weekly and 4-week rolling terms suit both <a href=\"short-term-storage.html\">short</a> and <a href=\"long-term-storage.html\">long-term</a> furniture storage.")]
    return dict(file="furniture-storage.html",slug="furniture",nav="Furniture Storage",
      title="Furniture Storage West Sussex | Collected & Sealed",
      meta="Furniture storage in West Sussex from £15/week. We blanket-wrap, collect & seal your furniture in secure containers. Fully insured, LAPADA accredited.",
      hero=IMG("hero-team-loading.webp"),faqs=faqs,
      crumb_parent=("storage-solutions.html","Storage Solutions"),
      extra_schema=town_service_schema({"town":"West Sussex","slug":"furniture-storage","lat":"50.9270","lng":"-0.4470"}),
      sections=[
        hero(IMG("hero-team-loading.webp"),"Wolves Storage Sussex team wrapping and loading furniture for storage","Furniture Storage in West Sussex",
          "Storing a sofa, a houseful or a few treasured pieces? We blanket-wrap your furniture, seal it into its own container and keep it clean, dry and secure &mdash; from just &pound;15 a week.",
          ["Blanket-wrapped &amp; padded by our team","Sealed in dry, alarmed containers","Fully insured, LAPADA accredited","From &pound;15/week, no deposit"],big=False),
        split("bg-white","Furniture Storage Done Properly",
          ["Furniture hates damp, dust and being shoved around an open unit. We wrap each piece in blankets and padding, then seal it into your own wooden container kept in our dry, ventilated, alarmed warehouse &mdash; so it comes back exactly as it left.",
           "It&rsquo;s fully managed: we collect from your door, do all the lifting, and redeliver on 24 hours&rsquo; notice. See <a href=\"how-it-works.html\">how it works</a> or our <a href=\"pricing.html\">prices</a>."],
          IMG("hero-packed-container.webp"),"Blanket-wrapped furniture sealed inside a Wolves Storage Sussex container"),
        split("bg-lightgrey","Ideal for Moves, Renovations &amp; Downsizing",
          ["Furniture storage is perfect between house moves, during a renovation, while staging a home for sale, or when downsizing and deciding what to keep. Store a single sofa or an entire home &mdash; you only pay for the containers you use.",
           "As a LAPADA-accredited team we also handle fine and antique furniture with specialist care. Not sure how much space you need? Try our <a href=\"storage-size-guide.html\">size guide</a>."],
          IMG("gallery-warehouse-a.webp"),"Furniture stored in sealed containers at the Wolves Storage Sussex warehouse",reverse=True),
        process(),
        faq(faqs),
        cta_band("Need Furniture Storage in West Sussex?",IMG("gallery-warehouse-b.webp")),
      ])

# ---------------- legal pages (privacy / terms) ----------------
LEGAL_CSS=('<style>'
  '.legal{max-width:48rem;margin:0 auto;color:#262626;font-size:1.02rem;line-height:1.75}'
  '.legal h2{font-size:1.5rem;font-weight:800;color:#262626;text-transform:none;margin:2.2rem 0 .6rem;line-height:1.25}'
  '.legal h2:first-of-type{margin-top:0}'
  '.legal p{margin:.7rem 0}'
  '.legal ul{margin:.7rem 0 .7rem 1.3rem;padding:0;list-style:disc}'
  '.legal li{margin:.35rem 0}'
  '.legal a{color:#FC9700;font-weight:600;text-decoration:underline}'
  '.legal strong{color:#262626}'
  '.legal .updated{color:#697783;font-size:.95rem;margin:0 0 1.4rem}'
  '</style>')
def legal_page(file,nav,title,meta,h1,sub,body):
    header=('<section class="relative w-full bg-darkgrey text-white overflow-hidden"><div class="container py-12 lg:py-16"><div class="max-w-3xl">'
            f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{h1}</h1>'
            f'<p class="mt-3 text-lg xl:text-xl text-beige">{sub}</p></div></div></section>')
    content=('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'
             +LEGAL_CSS+'<div class="legal">'+body+'</div></div></section>')
    return dict(file=file,slug="legal",nav=nav,title=title,meta=meta,hero=IMG("hero-facility-van.webp"),sections=[header,content])

PRIVACY_BODY='''<p class="updated">Last updated: 28 June 2026</p>
<p>This privacy policy explains how <strong>Wolves Storage Sussex</strong> (&ldquo;we&rdquo;, &ldquo;us&rdquo;, &ldquo;our&rdquo;), part of the family-run Wolves Removals business, collects and uses your personal information when you use our website or enquire about our storage services. We are the data controller for the information you provide.</p>
<h2>Who we are</h2>
<p>Wolves Storage Sussex, Doryln House, London Road, Ashington, Pulborough, West Sussex RH20 3JT.<br>Phone: 01903 893731 &middot; Email: <a href="mailto:info@sussexstoragecompany.co.uk">info@sussexstoragecompany.co.uk</a></p>
<h2>What information we collect</h2>
<ul>
<li><strong>Enquiry details</strong> you provide through our contact or quote forms &mdash; your name, email address, phone number and any details you include about what you would like to store.</li>
<li><strong>Communications</strong> &mdash; records of emails, calls and messages between us.</li>
<li><strong>Technical and usage data</strong> &mdash; basic information your browser sends (such as IP address and pages visited), collected by our hosting and any analytics or cookies.</li>
</ul>
<h2>How and why we use your information</h2>
<ul>
<li>To respond to your enquiry and prepare a quote.</li>
<li>To arrange, deliver and manage your storage (and any related removals) service.</li>
<li>To keep records and communicate with you about your booking.</li>
<li>To improve our website and services and keep our site secure.</li>
</ul>
<p>Our lawful bases for processing are your <strong>consent</strong> (when you submit a form), the performance of a <strong>contract</strong> with you, and our <strong>legitimate interests</strong> in running and improving our business.</p>
<h2>Who we share it with</h2>
<p>We do not sell your personal information. We share it only with trusted providers that help us run our business, including:</p>
<ul>
<li><strong>Resend</strong> &mdash; to deliver enquiry and confirmation emails.</li>
<li><strong>Cloudflare</strong> &mdash; website hosting and security.</li>
<li><strong>Google</strong> &mdash; embedded maps, and review display via Trustindex.</li>
</ul>
<p>We may also disclose information where required to do so by law.</p>
<h2>How long we keep it</h2>
<p>We keep enquiry and customer information only for as long as necessary &mdash; to deal with your enquiry, fulfil our service, and meet our legal and accounting obligations &mdash; after which it is securely deleted.</p>
<h2>Your rights</h2>
<p>Under UK data protection law you have the right to access, correct, delete or restrict the use of your personal data, to object to processing, and to data portability. To exercise any of these, contact us at <a href="mailto:info@sussexstoragecompany.co.uk">info@sussexstoragecompany.co.uk</a>. You also have the right to complain to the Information Commissioner&rsquo;s Office (ICO) at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a>.</p>
<h2>Cookies</h2>
<p>Our website uses a small number of cookies and similar technologies that are necessary for the site to work and stay secure, and may use cookies set by embedded content such as Google Maps and the Trustindex reviews widget. You can control cookies through your browser settings.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The latest version will always appear on this page, with the date it was last updated shown above.</p>
<h2>Contact us</h2>
<p>For any questions about this policy or your personal data, contact us at <a href="mailto:info@sussexstoragecompany.co.uk">info@sussexstoragecompany.co.uk</a> or call 01903 893731.</p>'''

TERMS_BODY='''<p class="updated">Last updated: 28 June 2026</p>
<p>These terms govern your use of the Wolves Storage Sussex website and any enquiry you make through it. By using this website you agree to these terms. <strong>Wolves Storage Sussex</strong> is part of the family-run Wolves Removals business, based at Doryln House, London Road, Ashington, Pulborough, West Sussex RH20 3JT.</p>
<h2>Using our website</h2>
<p>You may use this website for lawful purposes only. You must not misuse it, attempt to gain unauthorised access, or use it in any way that could damage the site or impair anyone else&rsquo;s use of it. We aim to keep the site available and accurate but cannot guarantee it will always be uninterrupted or error-free.</p>
<h2>Quotes and enquiries</h2>
<p>Prices shown on this website, including any figure from our storage calculator, are <strong>indicative guides only</strong> and do not form a binding quotation. A formal quote is provided once we understand your requirements, and a contract is only formed when a booking is confirmed in writing. The storage calculator gives an approximate volume and price and is not a guarantee of cost or space.</p>
<h2>Our storage services</h2>
<p>The supply of storage and related services is governed by the specific terms and conditions provided to you at the point of booking, which take precedence over these website terms in respect of the service itself. Service details, inclusions and pricing may change; the terms agreed at booking apply to your contract.</p>
<h2>Intellectual property</h2>
<p>The content, branding, text, images and design of this website are owned by or licensed to Wolves Storage Sussex and are protected by copyright. You may view and print pages for your own personal, non-commercial use only.</p>
<h2>Reviews and third-party content</h2>
<p>Customer reviews shown on this site are displayed via Trustindex from verified sources. The site also links to and embeds third-party content (such as Google Maps and social media). We are not responsible for the content or privacy practices of external sites.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any loss or damage arising from your use of this website or reliance on its content. Nothing in these terms limits our liability for matters that cannot lawfully be limited.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of England and Wales, and any disputes are subject to the exclusive jurisdiction of the courts of England and Wales.</p>
<h2>Changes to these terms</h2>
<p>We may update these terms from time to time. The current version will always be shown on this page.</p>
<h2>Contact us</h2>
<p>Questions about these terms? Email <a href="mailto:info@sussexstoragecompany.co.uk">info@sussexstoragecompany.co.uk</a> or call 01903 893731.</p>'''

# ---------------- reviews page ----------------
REVIEWS = [
 ("Dionne Watson","Wolves provide a very helpful, friendly, efficient and professional service. I would highly recommend them."),
 ("Leiza Bladd-Symms","The team were just amazing and went above and beyond to make the whole move as easy as possible. Huge thanks!"),
 ("Chris Rees","The Wolves team were very courteous and professional. They took care of everything and handled my belongings with real care."),
 ("K H","Jack and his team were incredibly helpful, with great advice for our house move and storage. Always polite and professional."),
 ("Mike Hale","A friendly bunch and very professional in the way they pack and protect all your valuable belongings. Couldn&rsquo;t fault them."),
 ("Lindsay Jordan","We cannot praise this team highly enough. They worked tirelessly and cheerfully throughout &mdash; true professionals from start to finish."),
]
def review_cards():
    STAR='<span style="color:#F6BB06;font-size:1.05rem;letter-spacing:2px" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
    cells=""
    for n,r in REVIEWS:
        cells+=('<div class="col-span-12 md:col-span-6 lg:col-span-4"><div class="bg-white rounded-2xl shadow-custom p-6 h-full">'
                +STAR+'<p class="mt-3 mb-0">&ldquo;'+r+'&rdquo;</p>'
                '<p class="font-bold text-black mt-4 mb-0">'+n+'</p>'
                '<p class="text-sm text-darkgrey mt-0 mb-0">Verified Google review</p></div></div>')
    return '<div class="grid grid-cols-12 gap-4 lg:gap-6">'+cells+'</div>'
def reviews_page():
    rs=('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":["SelfStorage","LocalBusiness"],
        "@id":BASE+"#business","name":"Wolves Storage Sussex","url":BASE+"reviews.html","image":BASE+"images/wolves-storage-logo@480.webp",
        "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"478","bestRating":"5"},
        "review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5","worstRating":"1"},"reviewBody":html.unescape(r)} for n,r in REVIEWS]},ensure_ascii=False)+'</script>')
    return dict(file="reviews.html",slug="reviews",nav="Reviews",
        title="Reviews | 5.0 Stars from 478 | Wolves Storage Sussex",
        meta="Read Wolves Storage Sussex reviews — rated 5.0 from 478 verified reviews on Google, Checkatrade & Facebook. Family-run, LAPADA accredited & fully insured.",
        hero=IMG("hero-fleet.webp"),extra_schema=rs,
        sections=[
          hero(IMG("hero-fleet.webp"),"Wolves Storage Sussex 5-star rated family team and van fleet in West Sussex","Our Customers Rate Us 5.0",
            "Don&rsquo;t just take our word for it &mdash; here&rsquo;s what West Sussex families and businesses say about storing with our family team.",
            ["5.0 stars from 478 reviews","Verified on Google, Checkatrade &amp; Facebook","LAPADA accredited &amp; fully insured","Trusted by West Sussex estate agents"],big=False),
          centered("bg-white","What Our Customers Say","Genuine, verified reviews from the families and businesses we&rsquo;ve helped across West Sussex.",review_cards()),
          cta_band("Join Hundreds of Happy West Sussex Customers",IMG("gallery-warehouse-b.webp")),
        ])

def build():
    P=[]
    # HOME
    P.append(dict(file="index.html",slug="home",nav="Home",
      title="Secure Storage in West Sussex | Wolves Storage Sussex",
      meta="Safe, secure & affordable managed storage in West Sussex from £15/week. We pack, collect, store & redeliver. LAPADA accredited, fully insured, 24/7 CCTV. Free quote.",
      hero=IMG("hero-facility-van.webp"),
      sections=[
        hero(IMG("hero-facility-van.webp"),"Wolves Storage Sussex secure facility and van in West Sussex","Secure Storage in West Sussex",
          "Need somewhere safe to keep your belongings? Our clean, dry, ultra-secure <strong>containerised storage</strong> suits home and business, short or long-term &mdash; fully managed, including packing, collection and delivery.",
          ["Cost-effective long- and short-term storage","Packing, collection &amp; delivery included","Fully secure, alarmed &amp; insured","Family-run, LAPADA accredited"]),
        split("bg-white","Storage That Flexes Around Your Move",
          ["Whether you&rsquo;re between properties, downsizing, renovating or freeing up space, our containerised storage keeps your belongings safe and accessible. Items are professionally packed and sealed into containers, protected from damp and damage.",
           'Choose <a href="short-term-storage.html">short-term</a> for moving delays, <a href="long-term-storage.html">long-term</a> for extended needs, or <a href="business-storage.html">business storage</a> for stock and equipment &mdash; from just &pound;15 a week.'],
          IMG("hero-containers-van.webp"),"Storage containers and van at the Wolves Storage Sussex facility"),
        split("bg-lightgrey","Why Store With Wolves Storage Sussex?",
          ["We don&rsquo;t just store boxes &mdash; we look after your home. Our trained, fully insured family team treats every item as if it were our own, from professional packing to careful stacking in our secure West Sussex facility.",
           "LAPADA accredited and Checkatrade members, with 24/7 CCTV, an alarmed store and full insurance &mdash; trusted by Sussex families and businesses for over 10 years."],
          IMG("hero-forklift.webp"),"Forklift stacking storage containers in our secure West Sussex warehouse",reverse=True),
        process(),
        gallery([(IMG("hero-facility-van.webp"),"Facility and van"),(IMG("gallery-warehouse-a.webp"),"Stacked storage containers"),
                 (IMG("gallery-loading.webp"),"Loading a storage container"),(IMG("hero-forklift.webp"),"Forklift stacking containers"),
                 (IMG("gallery-van.webp"),"Wolves storage van"),(IMG("hero-fleet.webp"),"Our van fleet")]),
        faq([("How much does storage cost in West Sussex?","Managed storage starts from just &pound;15 per week with no deposit and no hidden fees, on flexible weekly and 4-week terms. Your free quote is confirmed within 24 hours."),
             ("How is my furniture stored?","Items are professionally packed and sealed into your own wooden container, kept clean, dry and secure in our alarmed, 24/7 CCTV facility &mdash; not loose on open shelving."),
             ("Do I need to do anything?","No &mdash; our team brings the materials, packs and wraps your belongings, and loads everything into your container. You never lift a box."),
             ("How quickly can I access my items?","Just give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your door anywhere across West Sussex.")]),
        cta_band("Ready to Store With West Sussex&rsquo;s Trusted Family Team?",IMG("gallery-warehouse-b.webp")),
      ]))
    # generic builder for service pages
    def service(file,slug,nav,title,meta,heroimg,heroalt,h1,sub,checks,p1,p2,faqs):
        return dict(file=file,slug=slug,nav=nav,title=title,meta=meta,hero=heroimg,faqs=faqs,sections=[
            hero(heroimg,heroalt,h1,sub,checks,big=False),
            split("bg-white",p1[0],p1[1],IMG("hero-team-loading.webp"),"Wolves team loading a storage container"),
            split("bg-lightgrey",p2[0],p2[1],IMG("hero-containers-van.webp"),"Storage containers at our facility",reverse=True),
            process(),
            gallery([(IMG("hero-facility-van.webp"),"Facility and van"),(IMG("gallery-warehouse-a.webp"),"Storage containers"),
                     (IMG("gallery-loading.webp"),"Loading a container"),(IMG("hero-forklift.webp"),"Forklift stacking"),
                     (IMG("gallery-warehouse-b.webp"),"Warehouse interior"),(IMG("hero-fleet.webp"),"Van fleet")]),
            faq(faqs),
            cta_band("Need "+nav+" in West Sussex?",IMG("gallery-warehouse-b.webp")),
        ])
    P.append(service("storage-solutions.html","storage","Storage Solutions",
      "Managed Storage in West Sussex | Wolves Storage Sussex",
      "Secure, fully managed storage in West Sussex from £15/week. We pack, collect, store & redeliver. No deposit, fully insured, LAPADA accredited.",
      IMG("hero-facility-van.webp"),"Wolves Storage Sussex secure facility and van","Secure, Fully Managed Storage in Sussex",
      "From a few boxes to a whole house, household to business, short stays to long-term &mdash; we tailor secure managed storage to exactly what you need, all from our alarmed Ashington facility.",
      ["Cost-effective long- and short-term storage","Packing, collection &amp; delivery included","Fully secure, alarmed &amp; insured","No deposit, flexible weekly terms"],
      ("How Containerised Storage Works",["Your goods are professionally wrapped and loaded into a private 250 cu ft wooden container (about a one-bedroom flat). Each container is sealed, logged and stacked inside our secure indoor store.","Because everything stays in its own sealed container, your belongings aren&rsquo;t handled again until they come back to you &mdash; cleaner and safer than a drive-up unit."]),
      ("Secure, Insured & Family-Run",["24/7 CCTV, an alarmed facility and full insurance keep your belongings protected, while our family team handles the packing, collection and redelivery.","LAPADA accredited and Checkatrade members, trusted across West Sussex for over a decade."]),
      [("How much does storage cost?","From &pound;15 per week with no deposit and no hidden fees, on flexible weekly and 4-week rolling terms."),
       ("How big is a container?","Each wooden container is 5ft &times; 7ft &times; 8.6ft &mdash; 250 cu ft, roughly the contents of a one-bedroom flat. Need more? We simply use additional containers."),
       ("Is my stuff insured?","Yes &mdash; the facility is fully insured with optional extended cover, monitored by 24/7 CCTV and alarmed."),
       ("How do I get my items back?","Give us 24 hours&rsquo; notice and we redeliver to your door anywhere in West Sussex.")]))
    P.append(service("long-term-storage.html","longterm","Long-Term Storage",
      "Long-Term Storage West Sussex | Wolves Storage Sussex",
      "Affordable long-term storage in West Sussex from £15/week. Fully insured, 24/7 CCTV, no deposit. Ideal for emigrating, renovations & downsizing.",
      IMG("hero-forklift.webp"),"Forklift stacking long-term storage containers","Long-Term Storage in West Sussex",
      "Storing for months or years? Our containerised long-term storage keeps your belongings clean, dry and secure &mdash; with better value the longer you stay.",
      ["Better value the longer you store","Clean, dry, sealed containers","Fully insured &amp; 24/7 CCTV","No deposit, simple rolling terms"],
      ("Who Long-Term Storage Suits",["Perfect for working abroad, major renovations, downsizing or settling an estate. Your belongings stay sealed, clean and insured for as long as you need.","Store with total peace of mind and access whenever you need it &mdash; we redeliver the moment you&rsquo;re ready."]),
      ("Clean, Dry & Secure for the Long Haul",["Everything is wrapped and sealed in its own wooden container inside our dry, alarmed indoor facility, so it stays protected for the long term.","The longer you store, the better the value &mdash; ask about long-term rates on your free quote."]),
      [("How much does long-term storage cost?","From &pound;15 per week with no deposit, and the longer you store the better the value."),
       ("Will my belongings stay in good condition?","Yes &mdash; sealed wooden containers in a dry, alarmed indoor facility keep everything clean and protected."),
       ("Can I access items during storage?","Absolutely &mdash; give us 24 hours&rsquo; notice and we&rsquo;ll redeliver what you need."),
       ("Is there a minimum term?","No long tie-ins &mdash; store for as long as you like on flexible rolling terms.")]))
    P.append(service("short-term-storage.html","shortterm","Short-Term Storage",
      "Short-Term Storage West Sussex | Wolves Storage Sussex",
      "Flexible short-term storage in West Sussex from £15/week. No deposit, weekly terms, fast collection — perfect for moves & chain delays. Free quote.",
      IMG("hero-packed-container.webp"),"A storage container packed with wrapped furniture","Short-Term Storage in West Sussex",
      "Bridging a move, a broken chain or a quick renovation? Flexible weekly short-term storage with no deposit &mdash; we collect, store and bring it all back when you&rsquo;re ready.",
      ["Flexible weekly terms, no deposit","Fast collection &mdash; often within days","We pack, store and redeliver","Fully insured &amp; 24/7 CCTV"],
      ("When Short-Term Storage Helps",["House move delayed? Staging your home for sale? Quick renovation? Short-term storage gives you flexible, secure space for exactly as long as you need.","You pay by the week and stop whenever you like, with collection and redelivery included."]),
      ("Quick, Flexible & Fully Managed",["Tell us your timescale and we&rsquo;ll fit around your move, often collecting within a few days.","Only pay for the time you actually need &mdash; no deposit, no long contracts."]),
      [("How short can I store for?","As little as a week &mdash; billed weekly with no deposit, so you only pay for the time you need."),
       ("How quickly can you collect?","Often within a few days. Tell us your timescale on your free quote."),
       ("What if my move date changes?","No problem &mdash; flexible rolling terms let you extend or end your storage whenever you need."),
       ("Do you deliver it back?","Yes &mdash; give us 24 hours&rsquo; notice and we redeliver to your new address across West Sussex.")]))
    P.append(service("business-storage.html","business","Business Storage",
      "Business Storage West Sussex | Wolves Storage Sussex",
      "Secure business storage in West Sussex from £15/week — stock, archives & equipment. Fully insured, 24/7 CCTV, collection & redelivery. Free quote.",
      IMG("hero-containers-van.webp"),"Stacked storage containers for business stock","Business Storage in West Sussex",
      "Free up your office or premises. We collect, store and redeliver stock, archives and equipment &mdash; fully insured and flexible, so you only pay for the space you need.",
      ["Scale up or down &mdash; no long lease","Stock, archives, equipment &amp; documents","Fully insured &amp; 24/7 CCTV","We collect and redeliver to you"],
      ("Storage That Works for Business",["Running out of space for stock, archives or equipment? Business storage frees up expensive premises while keeping everything secure, insured and easy to retrieve.","Ideal for retailers, ecommerce, tradespeople, offices and businesses relocating."]),
      ("Flexible, Secure & Collected for You",["We collect from and redeliver to your premises, saving your team time, and scale your storage up or down as your business changes.","Fully insured, alarmed and monitored by 24/7 CCTV."]),
      [("What can I store as a business?","Stock, ecommerce inventory, archives and documents, tools and equipment, seasonal items and more."),
       ("Can I scale storage as I grow?","Yes &mdash; we add or remove containers as your needs change, on flexible rolling terms with no long lease."),
       ("Can you collect and redeliver?","Absolutely &mdash; collection and redelivery are included, saving your team the hassle."),
       ("How much does it cost?","From &pound;15 per week per container with no deposit &mdash; tailored to your needs within 24 hours.")]))
    # HOW IT WORKS
    P.append(dict(file="how-it-works.html",slug="how",nav="How It Works",
      title="How Our Managed Storage Works | Wolves Storage Sussex",
      meta="How fully managed storage in West Sussex works: we quote, pack, collect, store in secure containers and redeliver. From £15/week, no deposit. Free quote in 24 hours.",
      hero=IMG("hero-team-loading.webp"),faqs=[("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote."),("How do I access my belongings?","Give us 24 hours&rsquo; notice and we redeliver to your door across West Sussex."),("What&rsquo;s included?","Packing materials, professional packing, collection, secure container storage and redelivery.")],
      sections=[
        hero(IMG("hero-team-loading.webp"),"Wolves team loading a storage container","How Our Managed Storage Works",
          "Fully managed means you never hire a van or lift a box. We quote, pack, collect, store and redeliver &mdash; here&rsquo;s exactly how.",
          ["We bring the materials &amp; pack for you","Collection &amp; redelivery included","Sealed, individually logged containers","From &pound;15/week, no deposit"],big=False),
        process(),
        split("bg-white","What&rsquo;s Included",["Every managed storage job includes professional packing materials, careful wrapping, collection from your door, a sealed private container in our alarmed store, and redelivery when you&rsquo;re ready.","Optional extras include extended insurance cover and help unpacking."],IMG("hero-containers-van.webp"),"Storage containers at our facility"),
        split("bg-lightgrey","The Container Explained",["Each wooden container measures 5ft &times; 7ft &times; 8.6ft &mdash; 250 cu ft, roughly the contents of a one-bedroom flat. Containers are sealed, logged and stacked in our secure indoor facility.","Need more space? We simply use additional containers, so you only pay for what you use."],IMG("hero-packed-container.webp"),"A packed storage container",reverse=True),
        faq([("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote."),("How do I access my belongings?","Give us 24 hours&rsquo; notice and we redeliver to your door across West Sussex."),("What&rsquo;s included?","Packing materials, professional packing, collection, secure container storage and redelivery.")]),
        cta_band("Ready to Get Started?",IMG("gallery-warehouse-b.webp")),
      ]))
    # PRICING
    P.append(dict(file="pricing.html",slug="pricing",nav="Pricing",
      title="Storage Prices West Sussex | Wolves Storage Sussex",
      meta="Transparent storage pricing in West Sussex from £15/week. No deposit, no hidden fees, flexible weekly & 4-week terms. Collection & redelivery included. Free quote.",
      hero=IMG("hero-packed-container.webp"),faqs=[("How much is storage?","From &pound;15 per week per container with no deposit and no hidden fees."),("Are there any extra fees?","No hidden fees. Optional extras are extended insurance cover and help unpacking."),("Is collection included?","Yes &mdash; collection and redelivery across West Sussex are included.")],
      sections=[
        hero(IMG("hero-packed-container.webp"),"A packed storage container","Simple, Transparent Storage Prices",
          "Storage from just &pound;15 per week with no deposit and no hidden fees. You only pay for the container space you use &mdash; collection and redelivery included.",
          ["From &pound;15 per week, no deposit","Flexible weekly &amp; 4-week terms","Collection &amp; redelivery included","Free quote within 24 hours"],big=False),
        centered("bg-white","What&rsquo;s Always Included","Every storage plan includes the essentials &mdash; no surprises.",
          '<div class="grid grid-cols-12 gap-x-6 gap-y-5 mt-8">'+"".join('<div class="col-span-12 sm:col-span-6 lg:col-span-3 flex items-start gap-2 text-base xl:text-lg">'+CHK+'<span>'+x+'</span></div>' for x in ["Collection from your door","Your own sealed wooden container","24/7 CCTV &amp; alarmed store","Full insurance cover","Redelivery on 24 hours notice","Flexible weekly &amp; 4-week terms","No deposit, no hidden fees","Family-run, LAPADA accredited"])+'</div>'),
        split("bg-lightgrey","Optional Extras",["Add professional packing materials, extended insurance cover for higher-value items, or help unpacking when your belongings come home.","Tell us what you need on your free quote and we&rsquo;ll tailor a price."],IMG("hero-team-loading.webp"),"Team packing belongings for storage"),
        faq([("How much is storage?","From &pound;15 per week per container with no deposit and no hidden fees."),("Are there any extra fees?","No hidden fees. Optional extras are extended insurance cover and help unpacking."),("Is collection included?","Yes &mdash; collection and redelivery across West Sussex are included.")]),
        cta_band("Get Your Free, No-Obligation Quote",IMG("gallery-warehouse-b.webp")),
      ]))
    # AREAS — location silo hub
    area_groups=[
      ("On Our Doorstep",[
        ("storage-ashington","Ashington","RH20","Our home village &mdash; storage minutes from your door."),
        ("storage-washington","Washington","RH20","Beside our base at the foot of the South Downs."),
        ("storage-storrington","Storrington","RH20","A few minutes along the A283 from our warehouse."),
        ("storage-pulborough","Pulborough","RH20","Same RH20 area as our base, by the River Arun."),
        ("storage-steyning","Steyning","BN44","Covering Steyning, Bramber and Upper Beeding."),
        ("storage-findon","Findon","BN14","Downland village just north of Worthing on the A24."),
      ]),
      ("North &amp; Around Horsham",[
        ("storage-billingshurst","Billingshurst","RH14","Managed storage across the RH14 villages."),
        ("storage-horsham","Horsham","RH12&ndash;13","Collecting right across RH12 and RH13."),
        ("storage-henfield","Henfield","BN5","Your friendly local managed-storage alternative."),
        ("storage-cowfold","Cowfold","RH13","Village storage between Horsham and Henfield."),
        ("storage-partridge-green","Partridge Green","RH13","Rural storage near Henfield and West Grinstead."),
      ]),
      ("Crawley &amp; the North-East",[
        ("storage-crawley","Crawley","RH10&ndash;11","West Sussex&rsquo;s largest town &mdash; homes, business &amp; Gatwick."),
        ("storage-east-grinstead","East Grinstead","RH19","High Weald town where Sussex meets Surrey &amp; Kent."),
        ("storage-haywards-heath","Haywards Heath","RH16","Commuter-town storage across RH16 and RH17."),
        ("storage-burgess-hill","Burgess Hill","RH15","Managed storage across the RH15 area."),
      ]),
      ("Arun Valley &amp; West Coast",[
        ("storage-arundel","Arundel","BN18","Moves, downsizing and antiques across the Arun Valley."),
        ("storage-littlehampton","Littlehampton","BN17","Coastal storage by the mouth of the River Arun."),
        ("storage-rustington","Rustington","BN16","Leafy seaside village between Littlehampton &amp; Angmering."),
        ("storage-bognor-regis","Bognor Regis","PO21&ndash;22","Sunny coastal storage &mdash; downsizing &amp; holiday lets."),
      ]),
      ("Worthing &amp; the Adur Coast",[
        ("storage-worthing","Worthing","BN11&ndash;14","Across BN11&ndash;BN14 &mdash; moves, downsizing and students."),
        ("storage-lancing","Lancing","BN15","Between Worthing and Shoreham on the BN15 coast."),
        ("storage-shoreham-by-sea","Shoreham-by-Sea","BN43","Between Worthing and Brighton on the River Adur."),
        ("storage-brighton","Brighton &amp; Hove","BN1&ndash;3","City storage for flats, students &amp; downsizers."),
      ]),
      ("West Sussex &amp; the Downs",[
        ("storage-petworth","Petworth","GU28","Antiques capital &mdash; specialist furniture care."),
        ("storage-midhurst","Midhurst","GU29","South Downs market town storage on the A272."),
        ("storage-chichester","Chichester","PO19","Cathedral city storage, west of our patch."),
      ]),
    ]
    LOC_CSS=('<style>'
      '.loc-wrap{--o:#FC9700;--o2:#F6BB06;--dg:#697783;--beige:#E8E6DA;--lg:#F9F8F6;--bd:#E7E7E7;--ink:#262626;text-align:left}'
      '.loc-group{margin-top:2.75rem}.loc-group:first-of-type{margin-top:.25rem}'
      '.loc-ghead{display:flex;align-items:center;gap:.85rem;margin-bottom:1.35rem}'
      '.loc-gpin{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:var(--dg);color:#fff;flex:none}'
      '.loc-glabel{font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--o);font-size:.9rem;white-space:nowrap}'
      '.loc-grule{height:2px;flex:1;border-radius:2px;background:linear-gradient(90deg,var(--bd),rgba(231,231,231,0))}'
      '.loc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1.25rem}'
      '.loc-card{position:relative;display:flex;flex-direction:column;gap:.85rem;background:#fff;border:1px solid var(--bd);border-radius:1.15rem;padding:1.6rem 1.6rem 1.4rem;overflow:hidden;text-decoration:none;box-shadow:0 1px 2px rgba(38,38,38,.04);transition:transform .28s cubic-bezier(.2,.7,.3,1),box-shadow .28s ease,border-color .28s ease}'
      '.loc-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:linear-gradient(180deg,var(--o),var(--o2));transform:scaleY(0);transform-origin:top;transition:transform .3s ease}'
      '.loc-card:hover{transform:translateY(-6px);box-shadow:0 24px 50px -18px rgba(105,119,131,.55);border-color:var(--dg);background:var(--dg)}'
      '.loc-card:hover::before{transform:scaleY(1)}'
      '.loc-card:hover .loc-name{color:#fff}.loc-card:hover .loc-tag{color:var(--beige)}'
      '.loc-card:hover .loc-pc{color:#fff;background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.32)}'
      '.loc-card:hover .loc-cta{color:#fff}'
      '.loc-card:focus-visible{outline:2px solid var(--o);outline-offset:3px}'
      '.loc-top{display:flex;align-items:center;gap:.9rem}'
      '.loc-ico{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:.85rem;background:var(--beige);color:var(--dg);flex:none;transition:background .28s ease,color .28s ease,transform .28s ease}'
      '.loc-card:hover .loc-ico{background:var(--o);color:#fff;transform:rotate(-6deg) scale(1.05)}'
      '.loc-head{display:flex;flex-direction:column;gap:.35rem;min-width:0}'
      '.loc-name{font-weight:700;color:var(--ink);font-size:1.2rem;line-height:1.15;transition:color .28s ease}'
      '.loc-pc{align-self:flex-start;font-size:.68rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--dg);background:var(--lg);border:1px solid var(--bd);border-radius:999px;padding:.12rem .55rem;transition:color .28s ease,background .28s ease,border-color .28s ease}'
      '.loc-tag{color:var(--dg);font-size:.96rem;line-height:1.5;margin:0;flex:1;transition:color .28s ease}'
      '.loc-cta{display:inline-flex;align-items:center;gap:.45rem;font-weight:700;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--o);transition:color .28s ease}'
      '.loc-cta svg{transition:transform .28s ease}.loc-card:hover .loc-cta svg{transform:translateX(5px)}'
      '.loc-more{margin-top:2.75rem;padding-top:1.6rem;border-top:1px solid var(--bd)}'
      '.loc-more-h{font-weight:700;color:var(--ink);margin:0 0 .9rem;font-size:1.02rem}'
      '.loc-pills{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}'
      '.loc-pill{font-size:.85rem;font-weight:600;color:var(--ink);background:var(--lg);border:1px solid var(--bd);border-radius:999px;padding:.4rem .85rem}'
      '.loc-ask{color:var(--dg);margin:0}.loc-ask a{color:var(--o);font-weight:700;text-decoration:underline}'
      '@media (prefers-reduced-motion:reduce){.loc-card,.loc-ico,.loc-cta svg,.loc-card::before{transition:none}}'
      '</style>')
    LOC_PIN='<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>'
    LOC_GPIN='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>'
    LOC_ARR='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg>'
    more_towns=["Amberley","Bramber","Upper Beeding","West Chiltington","Wisborough Green","Lindfield","Hassocks","Hurstpierpoint","Pyecombe","Walberton","Small Dole","Ashurst"]
    def area_cards():
        out=LOC_CSS+'<div class="loc-wrap">'
        for label,items in area_groups:
            out+=f'<div class="loc-group"><div class="loc-ghead"><span class="loc-gpin">{LOC_GPIN}</span><span class="loc-glabel">{label}</span><span class="loc-grule"></span></div><div class="loc-grid">'
            for slug,tn,pc,tag in items:
                out+=(f'<a class="loc-card" href="{slug}.html" aria-label="Storage in {tn} ({pc})">'
                      f'<div class="loc-top"><span class="loc-ico">{LOC_PIN}</span>'
                      f'<span class="loc-head"><span class="loc-name">Storage in {tn}</span><span class="loc-pc">{pc}</span></span></div>'
                      f'<p class="loc-tag">{tag}</p>'
                      f'<span class="loc-cta">View {tn} storage {LOC_ARR}</span></a>')
            out+='</div></div>'
        out+=('<div class="loc-more"><p class="loc-more-h">Also serving across West Sussex</p><div class="loc-pills">'
              +"".join(f'<span class="loc-pill">{t}</span>' for t in more_towns)+'</div>'
              '<p class="loc-ask">Don&rsquo;t see your town? <a href="contact.html">Just ask</a> &mdash; if it&rsquo;s in West Sussex, we almost certainly cover it.</p></div></div>')
        return out
    area_itemlist=('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"ItemList","name":"Storage locations across West Sussex",
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":"Storage in "+tn,"url":BASE+slug+".html"}
          for i,(slug,tn,pc,tag) in enumerate([x for _,items in area_groups for x in items])]},ensure_ascii=False)+'</script>')
    P.append(dict(file="areas-we-cover.html",slug="areas",nav="Areas We Cover",
      title="Storage Across West Sussex | Areas We Cover | Wolves",
      meta="Managed storage across West Sussex — Ashington, Storrington, Pulborough, Horsham, Worthing, Steyning, Henfield & more. We collect & redeliver from £15/week.",
      hero=IMG("hero-fleet.webp"),extra_schema=area_itemlist,
      sections=[
        hero(IMG("hero-fleet.webp"),"Wolves Storage Sussex van fleet serving West Sussex","Storage Across West Sussex",
          "Based in Ashington, we collect from and redeliver across West Sussex &mdash; the managed model means we come to you, wherever you are. Find your town below.",
          ["We collect and redeliver to your door","Dedicated pages for towns across West Sussex","Local, family-run service","From &pound;15/week, no deposit"],big=False),
        centered("bg-lightgrey","Find Storage in Your West Sussex Town","From our Ashington base we serve homes and businesses right across West Sussex. Choose your town for local storage details, or get a free quote.",area_cards()),
        split("bg-white","Local &amp; Family-Run Matters",["Because we&rsquo;re based in the heart of West Sussex, we know the area inside out &mdash; and we treat your belongings like our own.","The managed model means there&rsquo;s no unit to drive to: we come to you, pack and seal everything, and bring it back on 24 hours&rsquo; notice."],IMG("gallery-van.webp"),"Wolves storage van serving towns across West Sussex"),
        cta_band("Storing in West Sussex? Get a Free Quote",IMG("gallery-warehouse-b.webp")),
      ]))
    # GALLERY
    P.append(dict(file="gallery.html",slug="gallery",nav="Gallery",
      title="Storage Gallery | Wolves Storage Sussex",
      meta="Photos of the Wolves Storage Sussex facility, containers, team and fleet. Secure, alarmed, fully insured managed storage in West Sussex from £15/week.",
      hero=IMG("hero-containers-van.webp"),
      sections=[
        hero(IMG("hero-containers-van.webp"),"Storage containers and van at the Wolves Storage Sussex facility","Our West Sussex Storage Facility",
          "A look inside our secure, alarmed facility &mdash; from our containers and forklift to the friendly family team and fleet.",
          ["Secure, alarmed &amp; 24/7 CCTV","Clean, dry wooden containers","Family-run, LAPADA accredited","From &pound;15/week, no deposit"],big=False),
        gallery([(IMG("hero-facility-van.webp"),"Facility and van"),(IMG("hero-containers-van.webp"),"Containers and van"),
                 (IMG("gallery-warehouse-a.webp"),"Stacked containers"),(IMG("gallery-warehouse-b.webp"),"Warehouse interior"),
                 (IMG("hero-forklift.webp"),"Forklift stacking"),(IMG("gallery-forklift-b.webp"),"Forklift and containers"),
                 (IMG("gallery-loading.webp"),"Loading a container"),(IMG("hero-packed-container.webp"),"A packed container"),
                 (IMG("hero-fleet.webp"),"Van fleet"),(IMG("gallery-van.webp"),"Storage van"),
                 (IMG("gallery-clipboard.webp"),"Wolves branded clipboard"),(IMG("hero-team-loading.webp"),"Team loading a container")]),
        cta_band("Like What You See? Get a Free Quote",IMG("gallery-warehouse-b.webp")),
      ]))
    # ABOUT
    P.append(dict(file="about.html",slug="about",nav="About",
      title="About Wolves Storage Sussex | West Sussex Storage",
      meta="Wolves Storage Sussex is a family-run, LAPADA-accredited storage business in Ashington, West Sussex with 10+ years' experience. Fully insured, 24/7 CCTV.",
      hero=IMG("hero-fleet.webp"),faqs=[("Are you insured and accredited?","Yes &mdash; fully insured, LAPADA accredited and Checkatrade members."),("How long have you been going?","Over 10 years serving West Sussex as a family-run business.")],
      sections=[
        hero(IMG("hero-fleet.webp"),"The Wolves family van fleet in West Sussex","A Trusted Family Name in West Sussex",
          "Wolves Storage Sussex is part of the family-run Wolves Removals business, serving West Sussex for over a decade from our base in Ashington.",
          ["Family-run, 10+ years&rsquo; experience","LAPADA accredited &amp; Checkatrade","Fully insured, 24/7 CCTV","Trusted by Sussex families &amp; businesses"],big=False),
        split("bg-white","Our Story",["What began as a local removals business grew into trusted, fully managed storage &mdash; built on the same family values of care, honesty and genuine local service.","Today we look after the belongings of hundreds of West Sussex families and businesses, from a few boxes to entire homes."],IMG("gallery-loading.webp"),"Wolves team loading a storage container"),
        split("bg-lightgrey","Why You Can Trust Us",["LAPADA accreditation means we&rsquo;re trusted to pack, store and handle high-value items. Add full insurance, 24/7 CCTV and an alarmed facility, and your belongings are in safe hands.","We&rsquo;re trusted by local estate agents and rated 5.0 from hundreds of reviews."],IMG("gallery-clipboard.webp"),"Wolves Removals and Storage branded clipboard",reverse=True),
        faq([("Are you insured and accredited?","Yes &mdash; fully insured, LAPADA accredited and Checkatrade members."),("How long have you been going?","Over 10 years serving West Sussex as a family-run business.")]),
        cta_band("Store With a Family You Can Trust",IMG("gallery-warehouse-b.webp")),
      ]))
    # CONTACT
    P.append(dict(file="contact.html",slug="contact",nav="Contact",
      title="Contact Wolves Storage Sussex | Free Storage Quote",
      meta="Contact Wolves Storage Sussex for a free storage quote within 24 hours. Call 01903 893731 / 07789 390421 or email. Ashington, Pulborough, West Sussex RH20 3JT.",
      hero=IMG("hero-facility-van.webp"),
      sections=[
        hero(IMG("hero-facility-van.webp"),"Wolves Storage Sussex facility and van","Get a Free Storage Quote",
          "Tell us what you need to store and we&rsquo;ll send a clear, no-obligation quote within 24 hours &mdash; from just &pound;15 a week.",
          ["Free quote within 24 hours","No deposit, no obligation","From &pound;15/week","Family-run, fully insured"],big=False),
        ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'+CONTACT_MAIN+'</div></section>'),
        (f'<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="grid grid-cols-12 gap-8 lg:gap-12 items-start">'
         '<div class="col-span-12 lg:col-span-5"><h2 class="relative leading-tight text-black">Find Us</h2>'
         '<address class="not-italic leading-relaxed mt-3">Doryln House, London Road, Ashington<br>Pulborough (Horsham District)<br>West Sussex RH20 3JT</address>'
         f'<ul class="list-none p-0 mt-4 space-y-3 text-lg"><li class="flex items-center gap-3">{SVG_PHONE}<a class="hover:text-orange" href="tel:+441903893731">{PHONE1}</a></li>'
         f'<li class="flex items-center gap-3">{SVG_PHONE}<a class="hover:text-orange" href="tel:+447789390421">{PHONE2}</a></li>'
         f'<li class="flex items-center gap-3">{SVG_MAIL}<a class="hover:text-orange" href="mailto:{EMAIL}">{EMAIL}</a></li></ul>'
         '<p class="mt-4 text-sm text-darkgrey">Office hours: Mon&ndash;Fri 8:30am&ndash;6pm &middot; Sat 9am&ndash;4pm</p></div>'
         '<div class="col-span-12 lg:col-span-7"><iframe title="Wolves Storage Sussex location" src="https://www.google.com/maps?q=RH20%203JT&t=&z=13&ie=UTF8&iwloc=&output=embed" class="block w-full rounded-xl shadow-custom" style="border:0;height:380px"></iframe></div></div></div></section>'),
      ]))
    # P0 content assets
    P.append(size_guide_page())
    P.append(furniture_page())
    # LOCATION SILO — per-town pages
    for t in TOWNS:
        P.append(town(t))
    # REVIEWS
    P.append(reviews_page())
    # LEGAL
    P.append(legal_page("privacy-policy.html","Privacy Policy",
      "Privacy Policy | Wolves Storage Sussex",
      "How Wolves Storage Sussex collects, uses and protects your personal data when you enquire about storage. Your rights, cookies and how to contact us.",
      "Privacy Policy","How we handle and protect your personal information.",PRIVACY_BODY))
    P.append(legal_page("terms.html","Terms &amp; Conditions",
      "Terms & Conditions | Wolves Storage Sussex",
      "The terms for using the Wolves Storage Sussex website, our quotes and storage calculator, intellectual property, liability and governing law.",
      "Terms &amp; Conditions","The terms for using our website and services.",TERMS_BODY))
    # 404
    P.append(dict(file="404.html",slug="404",nav="Page not found",
      title="Page Not Found (404) | Wolves Storage Sussex",
      meta="Sorry, we couldn't find that page. Return to Wolves Storage Sussex for secure managed storage in West Sussex from £15/week.",
      hero=IMG("hero-facility-van.webp"),
      sections=[centered("bg-white","Page Not Found","Sorry, we couldn&rsquo;t find that page. Let&rsquo;s get you back to storing safely in West Sussex.",
        f'<div class="flex flex-wrap gap-3 justify-center">{btn("Back to Home","index.html","px-8 lg:px-10")}{btn("Contact Us","contact.html","px-8 lg:px-10")}</div>')]))

    for d in P:
        if d["slug"] not in ("404","legal") and d["file"]!="contact.html":
            d["sections"].insert(1, TRUSTINDEX_SECTION)
        if d["file"] in WHYUS:
            d["sections"].insert(2, WHYUS[d["file"]])
        if d["file"]=="pricing.html":
            d["sections"].insert(1, CALC_SECTION)
        if d["file"] in CONTAINER_HTML:
            d["sections"].insert(len(d["sections"])-1, CONTAINER_HTML[d["file"]])
    for d in P:
        if d["file"]=="404.html":
            # noindex
            pass
        html=page(d)
        if d["file"]=="404.html":
            html=html.replace('<meta name="robots" content="index, follow">','<meta name="robots" content="noindex, follow">')
        open(os.path.join(SITE,d["file"]),"w",encoding="utf-8").write(html)
        print(f"  built {d['file']:26} {len(html)//1024}KB")
    # sitemap.xml (all indexable pages)
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for d in P:
        if d["file"]=="404.html": continue
        if d["file"]=="index.html": pr="1.0"
        elif d["slug"]=="legal": pr="0.3"
        elif d["slug"] in ("town","guide","furniture"): pr="0.8"
        else: pr="0.7"
        sm+=f'  <url><loc>{BASE}{d["file"]}</loc><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n'
    sm+='</urlset>\n'
    open(os.path.join(SITE,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    print(f"  sitemap.xml  {sum(1 for d in P if d['file']!='404.html')} urls")
    # llms.txt (LLM-readable site index — auto-generated from every page, as a rule)
    def llms_cat(d):
        f,s=d["file"],d["slug"]
        if s=="town" or f=="areas-we-cover.html": return "Storage by location (West Sussex)"
        if f in {"storage-solutions.html","long-term-storage.html","short-term-storage.html","business-storage.html","furniture-storage.html"}: return "Storage services"
        if f in {"how-it-works.html","pricing.html","storage-size-guide.html"}: return "How it works, pricing & guides"
        return "Company & contact"
    CATS=["Storage services","Storage by location (West Sussex)","How it works, pricing & guides","Company & contact"]
    home=next(d for d in P if d["file"]=="index.html")
    buckets={c:[] for c in CATS}
    for d in P:
        if d["file"] in ("index.html","404.html"): continue
        buckets[llms_cat(d)].append(d)
    llms=("# Wolves Storage Sussex\n\n> "+home["meta"]+"\n\n"
          "Family-run, fully managed containerised storage across West Sussex, based in Ashington (Doryln House, London Road, Pulborough RH20 3JT). "
          "We pack, collect, seal and store your belongings in an alarmed, fully insured indoor warehouse, then redeliver — no self-storage unit to drive to. "
          "Trading since 2016. LAPADA accredited, Checkatrade-verified, 5.0/5 from 478 reviews. From £15/week, no deposit. Phone 01903 893731.\n\n"
          f"- [Home]({BASE}index.html): {home['meta']}\n\n")
    for c in CATS:
        if not buckets[c]: continue
        llms+=f"## {c}\n"
        for d in buckets[c]:
            llms+=f"- [{d['nav']}]({BASE}{d['file']}): {d['meta']}\n"
        llms+="\n"
    open(os.path.join(SITE,"llms.txt"),"w",encoding="utf-8").write(llms)
    print(f"  llms.txt     {sum(len(v) for v in buckets.values())+1} pages indexed")
    print("Done:",len(P),"pages in the wolves-removals theme.")

build()
