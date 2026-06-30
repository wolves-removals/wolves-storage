#!/usr/bin/env python3
# Generator: builds our storage pages in the wolves-removals THEME (their
# compiled site.min.css + Alpine + their exact component markup), with our
# own storage wording. Only uses class strings confirmed present in their CSS.
import json, os, html, datetime, re
SITE = os.path.dirname(os.path.abspath(__file__))
LASTMOD = datetime.date.today().isoformat()
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
            '<button type="button" aria-label="Open Storage menu" :aria-expanded="o ? \'true\' : \'false\'" @click="o=!o" class="nav-top lg:ml-1 p-1 bg-transparent transition-transform duration-200" :class="o?\'rotate-180\':\'\'"><svg viewBox="0 0 20 20" class="h-5 w-5 fill-current" fill="currentColor" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg></button></div>'
            '<ul x-cloak class="bg-white w-full px-4 py-2 lg:absolute lg:top-full lg:left-0 lg:w-72 lg:z-30 lg:shadow-lg lg:border-t-4 lg:border-lightgrey list-none my-0 lg:p-2" :class="o ? \'block\' : \'hidden\'">'+subs+'</ul></li>')

def nav_lis(mobile=False):
    out=""
    for href,label in NAV:
        if label=="Storage":
            out+=storage_dropdown(); continue
        ext=' target="_blank" rel="noopener"' if href.startswith("http") else ""
        out+=('<li class="lg:h-full w-full lg:w-auto flex items-center shrink-0 lg:pr-4 xl:pr-5 2xl:pr-7 border-b border-black/10 lg:border-b-0 px-4 py-3 lg:p-0 lg:py-10">'
              f'<a href="{"/" if href=="index.html" else href}"{ext} class="nav-top shrink-0 text-black font-semibold uppercase lg:hover:text-orange text-base lg:text-sm">{label}</a></li>')
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
f'<a id="site-logo" class="absolute left-0 top-1/2 -translate-y-1/2 flex z-50" href="/" title="Wolves Storage Sussex" aria-label="Wolves Storage Sussex &ndash; home">'
f'<img class="h-[64px] sm:h-[88px] lg:h-[164px] xl:h-[180px] w-auto drop-shadow-lg" src="{LOGO}" width="200" height="197" alt="Wolves Storage Sussex logo"></a></div>\n'
'<div class="order-2 hidden lg:flex lg:flex-1 items-center justify-end gap-4 xl:gap-6">'
'<nav id="site-navigation" aria-label="Primary" class="font-medium"><ul class="flex lg:flex-row lg:items-center lg:justify-end p-0 mb-0 list-none">'+nav_lis()+'</ul></nav>'
+btn("Get a Free Quote")+'</div>\n'
'<div class="order-3 w-fit flex lg:hidden items-center justify-end gap-4">'
+btn("Free Quote","contact.html","rounded-xl text-xs px-4 sm:text-sm sm:px-6")+
'<button type="button" :aria-label="menuOpen ? \'Close menu\' : \'Open menu\'" :aria-expanded="menuOpen ? \'true\' : \'false\'" aria-controls="mobile-nav" @click="menuOpen=!menuOpen" class="text-black bg-transparent p-2">'
'<svg x-show="!menuOpen" viewBox="0 0 24 24" class="w-7 h-7" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'
'<svg x-show="menuOpen" x-cloak viewBox="0 0 24 24" class="w-7 h-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>\n'
'</div></div>\n'
'<div id="mobile-nav" x-cloak class="lg:hidden absolute top-full left-0 w-full bg-[#dad6c2] max-h-[80vh] overflow-y-auto shadow-custom-header" :class="menuOpen ? \'block\' : \'hidden\'">'
'<nav aria-label="Mobile" class="font-medium"><ul class="flex flex-col p-0 mb-0 list-none">'+nav_lis(True)+'</ul></nav></div>\n'
'</header>')

FOOTER = open(os.path.join(SITE,"partials","footer.html"),encoding="utf-8").read()

# ---------------- section helpers (verbatim theme classes) ----------------
def checklist(items, center=False):
    lis="".join(f'<li class="flex items-start gap-2">{CHK}<span>{x}</span></li>' for x in items)
    if center:
        return '<div class="mt-6 flex justify-center"><ul class="space-y-2 list-none p-0 text-base xl:text-lg inline-block text-left">'+lis+'</ul></div>'
    return '<div class="mt-6"><ul class="space-y-2 list-none p-0 text-base xl:text-lg">'+lis+'</ul></div>'
AUD_ICONS={
 "home":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.2 12 4l9 7.2"/><path d="M5 9.8V20h14V9.8"/><path d="M10 20v-5h4v5"/></svg>',
 "wrench":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15.6 6.4a3.5 3.5 0 0 0-4.7 4.7l-6 6a1.5 1.5 0 0 0 2.1 2.1l6-6a3.5 3.5 0 0 0 4.7-4.7l-2.3 2.3-1.9-1.9 2-2.5z"/></svg>',
 "box":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>',
 "key":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="8" r="4.2"/><path d="M11 11l8.5 8.5"/><path d="M16.5 16.5l2-2"/></svg>',
 "briefcase":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8 7.5V5.8a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.7"/><path d="M3 12.5h18"/></svg>',
 "cap":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4 2.5 8.5 12 13l9.5-4.5L12 4z"/><path d="M6.5 10.7v4.3c0 1.2 2.5 2.5 5.5 2.5s5.5-1.3 5.5-2.5v-4.3"/><path d="M21.5 8.5v5"/></svg>',
}
CKG_CK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.4 4.5L19.5 7"/></svg>'
CKG_CSS=('<style>'
  '.ckg-panel{position:relative;overflow:hidden;max-width:64rem;margin:1.6rem auto 0;border-radius:1.5rem;padding:1.9rem 1.3rem;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%);border:1px solid rgba(255,255,255,.1);box-shadow:0 30px 70px -34px rgba(38,38,38,.55);list-style:none;display:grid;grid-template-columns:1fr;gap:.85rem}'
  '@media(min-width:640px){.ckg-panel{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.ckg-panel{grid-template-columns:repeat(3,1fr);padding:2.2rem 1.9rem;gap:1rem}}'
  '.ckg-panel::before{content:"";position:absolute;inset:0;background:radial-gradient(120% 120% at 85% -10%,rgba(252,151,0,.16),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.ckg-panel::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.ckg-item{position:relative;overflow:hidden;display:flex;align-items:center;gap:.95rem;background:#fff;border:1px solid #E7E7E7;border-radius:.95rem;padding:1rem 1.1rem;box-shadow:0 2px 6px rgba(38,38,38,.05);transition:transform .3s cubic-bezier(.2,.7,.3,1),box-shadow .3s ease,border-color .3s ease}'
  '.ckg-item::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,#FC9700,#F6BB06);transform:scaleY(0);transform-origin:top;transition:transform .3s ease}'
  '.ckg-item:hover{transform:translateY(-4px);box-shadow:0 18px 36px -18px rgba(105,119,131,.5);border-color:#d9dde1}'
  '.ckg-item:hover::before{transform:scaleY(1)}'
  '.ckg-ico{position:relative;flex:none;display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:.78rem;background:#E8E6DA;color:#697783;transition:background .3s ease,color .3s ease,transform .3s ease}'
  '.ckg-item:hover .ckg-ico{background:#FC9700;color:#fff;transform:rotate(-6deg) scale(1.05)}'
  '.ckg-ico svg{width:24px;height:24px}'
  '.ckg-mark{position:absolute;bottom:-5px;right:-5px;display:inline-flex;align-items:center;justify-content:center;width:21px;height:21px;border-radius:999px;background:#1b7f3b;color:#fff;border:2px solid #fff}'
  '.ckg-mark svg{width:11px;height:11px}'
  '.ckg-text{flex:1;min-width:0;color:#262626;font-weight:600;font-size:.96rem;line-height:1.32;text-align:left}'
  '@media (prefers-reduced-motion:reduce){.ckg-item,.ckg-ico,.ckg-item::before{transition:none}.ckg-item:hover{transform:none}}'
  '</style>')
def checklist_grid(items, cols=None):
    cells=""
    for it in items:
        ic,txt = (it[0],it[1]) if isinstance(it,(list,tuple)) else ("home",it)
        cells+=('<li class="ckg-item"><span class="ckg-ico">'+AUD_ICONS.get(ic,AUD_ICONS["home"])
                +'<span class="ckg-mark">'+CKG_CK+'</span></span><span class="ckg-text">'+txt+'</span></li>')
    return CKG_CSS+'<ul class="ckg-panel">'+cells+'</ul>'

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

SPLIT_CSS=('<style>'
  '.sp-figure{position:relative;height:100%}'
  '.sp-img{position:relative;height:100%;overflow:hidden;border-radius:1.15rem;border:1px solid #E7E7E7;box-shadow:0 20px 46px -24px rgba(38,38,38,.5);transition:transform .4s cubic-bezier(.2,.7,.3,1),box-shadow .4s ease}'
  '.sp-img::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;z-index:2;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.sp-img img{transition:transform .6s cubic-bezier(.2,.7,.3,1)}'
  '.sp-figure:hover .sp-img{transform:translateY(-5px);box-shadow:0 30px 60px -26px rgba(38,38,38,.55)}'
  '.sp-figure:hover .sp-img img{transform:scale(1.045)}'
  '.sp-rule{display:block;width:54px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FC9700,#F6BB06);margin:.85rem 0 1.05rem}'
  '@media (prefers-reduced-motion:reduce){.sp-img,.sp-img img{transition:none}.sp-figure:hover .sp-img{transform:none}.sp-figure:hover .sp-img img{transform:none}}'
  '</style>')
# Accessibility contrast tweaks (WCAG 1.4.11 / 1.4.3) layered over the compiled theme.
A11Y_CSS=('<style>'
  '.top-0{top:0}'                                                # sticky-header offset (class absent from compiled site.min.css)
  '@media(min-width:1024px){.lg\\:pt-12{padding-top:3rem}.lg\\:pb-12{padding-bottom:3rem}}'  # cov-sec desktop padding (classes absent from site.min.css)
  '@media(min-width:1280px){.xl\\:text-sm{font-size:.875rem;line-height:1.25rem}}'           # process subtext size at xl (class absent from site.min.css)
  '.text-green{color:#1b7f3b}'                                   # darker green ticks meet 3:1 graphical contrast
  '.enquiry-form input,.enquiry-form select,.enquiry-form textarea{border:1px solid #6b7280}'  # 3:1 input borders
  '.enquiry-form input::placeholder,.enquiry-form textarea::placeholder{color:#5b626b}'         # readable placeholder
  '</style>')
def split(bg, h2, paras, img, alt, reverse=False):
    body = "".join(f'<p>{p}</p>' for p in paras)
    txt = (f'<div class="col-span-12 lg:col-span-6 {"lg:col-start-6" if reverse else "lg:col-start-2"}">'
           f'<h2 class="relative leading-tight text-black">{h2}</h2><span class="sp-rule" aria-hidden="true"></span>{body}</div>')
    pic = (f'<div class="col-span-12 lg:col-span-4 {"lg:col-start-2" if reverse else "lg:col-start-8"}">'
           f'<div class="sp-figure"><div class="sp-img relative h-56 sm:h-72 lg:h-full">'
           f'<img src="{img}" alt="{alt}" width="1600" height="1200" loading="lazy" decoding="async" class="absolute inset-0 w-full h-full object-cover"></div></div></div>')
    inner = (pic+txt) if reverse else (txt+pic)
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
            f'<div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-stretch">{inner}</div></div></section>')

def centered(bg, h2, lead, inner=""):
    leadp = f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{lead}</p>' if lead else ""
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'
            f'<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">{h2}</h2>{leadp}</div>{inner}</div></section>')

CG_ICONS={
 'container':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8.5l-9-5-9 5v7l9 5 9-5z"/><path d="M3 8.5l9 5 9-5"/><path d="M12 13.5V21"/></svg>',
 'shield':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7.5 3.2v5c0 4.6-3.2 7.8-7.5 9.3-4.3-1.5-7.5-4.7-7.5-9.3v-5z"/><path d="M9 12l2.2 2.2L15.5 9.5"/></svg>',
 'badge':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9" r="5.2"/><path d="M9.2 13.3L7.5 21l4.5-2.6L16.5 21l-1.7-7.7"/><path d="M9.7 9l1.6 1.6L14.4 7.4"/></svg>',
 'boxes':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="10" width="8" height="8" rx="1.2"/><rect x="13" y="10" width="8" height="8" rx="1.2"/><rect x="8" y="3" width="8" height="6" rx="1.2"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>',
 'spark':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.5 3l1.7 4.6L18 9.3l-4.8 1.7L11.5 16l-1.7-5L5 9.3l4.8-1.7z"/><path d="M18 14l.8 2.3 2.2.8-2.2.8L18 20l-.8-2.1-2.2-.8 2.2-.8z"/></svg>',
 'tag':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0l-7-7A2 2 0 0 1 3 12.2V5a2 2 0 0 1 2-2h7.2a2 2 0 0 1 1.4.6l7 7a2 2 0 0 1 0 2.8z"/><circle cx="7.8" cy="7.8" r="1.3"/></svg>',
 'package':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8.5h18V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><rect x="2" y="5" width="20" height="3.5" rx="1"/><path d="M12 5v16"/><path d="M12 5S10.5 2 8.3 3 9.5 5 12 5z"/><path d="M12 5s1.5-3 3.7-2S14.5 5 12 5z"/></svg>',
 'truck':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h11v9H3z"/><path d="M14 9h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></svg>',
 'family':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3 20a5 5 0 0 1 10 0"/><path d="M14.5 20a4 4 0 0 1 6.5-3.1"/></svg>',
 'home':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.2 12 4l9 7.2"/><path d="M5 9.8V20h14V9.8"/><path d="M10 20v-5h4v5"/></svg>',
}
CG_CSS=('<style>'
  '.cg-sec{position:relative;overflow:hidden;background:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.5px) 0 0/24px 24px,linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%)}'
  '.cg-sec::before{content:"";position:absolute;inset:0;background:radial-gradient(130% 135% at 6% -18%,rgba(252,151,0,.24),rgba(252,151,0,0) 52%);pointer-events:none}'
  '.cg-sec::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.cg-blob{position:absolute;right:-150px;bottom:-150px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(246,187,6,.13),rgba(246,187,6,0) 68%);pointer-events:none;z-index:0}'
  '.cg-wrap{position:relative;z-index:1;max-width:74rem;margin:0 auto}'
  '.cg-head{text-align:center;max-width:54rem;margin:0 auto}'
  '.cg-ey{display:inline-flex;align-items:center;gap:.5rem;color:#F6BB06;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.82rem;margin-bottom:.7rem}'
  '.cg-ey::before,.cg-ey::after{content:"";width:18px;height:1px;background:rgba(246,187,6,.55)}'
  '.cg-h2{color:#fff;font-weight:800;font-size:1.85rem;line-height:1.12;margin:0}'
  '@media(min-width:1024px){.cg-h2{font-size:2.3rem}}'
  '.cg-rule{width:62px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FC9700,#F6BB06);margin:1.15rem auto 0}'
  '.cg-lead{font-size:1.1rem;line-height:1.7;color:#ece9df;max-width:50rem;margin:1.15rem auto 0;text-align:center}'
  '.cg-grid{display:grid;grid-template-columns:1fr;gap:1.2rem;margin-top:2.5rem;align-items:stretch}'
  '@media(min-width:760px){.cg-grid{grid-template-columns:1fr 1fr;gap:1.4rem;margin-top:3rem}}'
  '.cg-card{position:relative;overflow:hidden;background:#fff;border-radius:1.35rem;padding:1.9rem 1.7rem;box-shadow:0 26px 50px -28px rgba(20,28,36,.62);transition:transform .32s cubic-bezier(.2,.7,.3,1),box-shadow .32s ease}'
  '.cg-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,#FC9700,#F6BB06);transform:scaleY(0);transform-origin:top;transition:transform .35s ease}'
  '.cg-card:hover{transform:translateY(-7px);box-shadow:0 36px 64px -26px rgba(20,28,36,.68)}'
  '.cg-card:hover::before{transform:scaleY(1)}'
  '.cg-num{position:absolute;top:.7rem;right:1.2rem;font-weight:800;font-size:3.1rem;line-height:1;color:#f1f3f5;letter-spacing:-.03em;z-index:0}'
  '.cg-ico{position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:1rem;background:#E8E6DA;color:#697783;margin-bottom:1.05rem;transition:background .3s ease,color .3s ease,transform .3s ease}'
  '.cg-card:hover .cg-ico{background:linear-gradient(135deg,#FC9700,#F6BB06);color:#fff;transform:rotate(-6deg) scale(1.07)}'
  '.cg-ico svg{width:27px;height:27px}'
  '.cg-h{position:relative;z-index:1;font-weight:800;color:#26303a;font-size:1.16rem;line-height:1.25;margin:0 0 .55rem;padding-right:2.4rem}'
  '.cg-p{position:relative;z-index:1;color:#56606b;font-size:.97rem;line-height:1.62;margin:0}'
  '.cg-p a{color:#c97400;font-weight:700;text-decoration:underline;text-underline-offset:2px}'
  '.cg-p a:hover{color:#697783}'
  '.cg-statband{grid-column:1/-1;position:relative;overflow:hidden;border-radius:1.35rem;background:linear-gradient(120deg,rgba(255,255,255,.10),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.16);padding:1.5rem 1rem;display:grid;grid-template-columns:1fr 1fr;gap:1.1rem 0}'
  '.cg-statband::after{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '@media(min-width:680px){.cg-statband{grid-template-columns:repeat(4,1fr);padding:1.7rem 1.4rem}}'
  '.cg-stat{position:relative;text-align:center}'
  '.cg-stat-n{display:block;font-weight:800;font-size:2rem;line-height:1;color:#F6BB06}'
  '.cg-stat-l{display:block;margin-top:.45rem;font-size:.8rem;line-height:1.3;color:#e7e4d8;text-transform:uppercase;letter-spacing:.04em}'
  '@media(min-width:680px){.cg-stat+.cg-stat::before{content:"";position:absolute;left:0;top:12%;bottom:12%;width:1px;background:rgba(255,255,255,.18)}}'
  '.cg-feat{position:relative;overflow:hidden;background:#fff;border-radius:1.6rem;box-shadow:0 34px 66px -30px rgba(15,22,30,.74);display:grid;grid-template-columns:1fr;margin-bottom:1.3rem}'
  '@media(min-width:820px){.cg-feat{grid-template-columns:43% 1fr}}'
  '.cg-feat-img{position:relative;min-height:250px}'
  '.cg-feat-img>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
  '.cg-feat-img::after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(34,44,54,.34),rgba(34,44,54,0) 56%)}'
  '.cg-feat-tag{position:absolute;top:1.05rem;left:1.05rem;z-index:1;background:linear-gradient(135deg,#FC9700,#F6BB06);color:#fff;font-weight:700;text-transform:uppercase;letter-spacing:.07em;font-size:.68rem;padding:.42rem .8rem;border-radius:999px;box-shadow:0 8px 18px -6px rgba(252,151,0,.6)}'
  '.cg-feat-body{position:relative;padding:2.1rem 1.9rem}'
  '@media(min-width:820px){.cg-feat-body{padding:2.9rem 2.7rem;display:flex;flex-direction:column;justify-content:center}}'
  '.cg-feat-k{font-weight:800;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:#c97400}'
  '.cg-feat-h{font-weight:800;color:#222c36;font-size:1.5rem;line-height:1.16;margin:.6rem 0 .75rem}'
  '@media(min-width:1024px){.cg-feat-h{font-size:1.78rem}}'
  '.cg-feat-p{color:#56606b;font-size:1.02rem;line-height:1.62;margin:0}'
  '.cg-photo{position:relative;overflow:hidden;border-radius:1.35rem;min-height:230px;box-shadow:0 26px 50px -28px rgba(15,22,30,.64)}'
  '.cg-photo>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .5s ease}'
  '.cg-photo:hover>img{transform:scale(1.05)}'
  '.cg-photo::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(16,23,31,.84),rgba(16,23,31,.05) 60%)}'
  '.cg-photo-cap{position:absolute;left:1.2rem;right:1.2rem;bottom:1.1rem;z-index:1;color:#fff;font-weight:700;font-size:.97rem;line-height:1.3;display:flex;align-items:center;gap:.6rem}'
  '.cg-photo-cap::before{content:"";flex:none;width:26px;height:3px;border-radius:2px;background:linear-gradient(90deg,#FC9700,#F6BB06)}'
  '@media(prefers-reduced-motion:reduce){.cg-card,.cg-ico,.cg-card::before,.cg-photo>img{transition:none}}'
  '</style>')
def content_grid(eyebrow, h2, lead, items, feature=None, photos=None, stats=None, kicker="The managed difference"):
    feat=""
    if feature:
        fic,fh,fp,fimg,falt,fw,fh_px=feature
        feat=(f'<div class="cg-feat"><div class="cg-feat-img"><span class="cg-feat-tag">{kicker}</span>'
              f'<img src="{IMG(fimg)}" alt="{falt}" width="{fw}" height="{fh_px}" loading="lazy" decoding="async"></div>'
              f'<div class="cg-feat-body"><span class="cg-feat-k">01 &mdash; how we work</span>'
              f'<h3 class="cg-feat-h">{fh}</h3><p class="cg-feat-p">{fp}</p></div></div>')
    def photo_tile(spec):
        pim,palt,pcap,pw,ph=spec
        return (f'<div class="cg-photo"><img src="{IMG(pim)}" alt="{palt}" width="{pw}" height="{ph}" loading="lazy" decoding="async">'
                f'<span class="cg-photo-cap">{pcap}</span></div>')
    ph_list=photos or []
    band=""
    if stats:
        band='<div class="cg-statband">'+"".join(
          f'<div class="cg-stat"><span class="cg-stat-n">{n}</span><span class="cg-stat-l">{l}</span></div>' for n,l in stats)+'</div>'
    out=""
    for i,(ic,h,p) in enumerate(items):
        c=(f'<div class="cg-card"><span class="cg-num">{i+2:02d}</span>'
           f'<span class="cg-ico">{CG_ICONS.get(ic,CG_ICONS["container"])}</span>'
           f'<h3 class="cg-h">{h}</h3><p class="cg-p">{p}</p></div>')
        pc=photo_tile(ph_list[i]) if i<len(ph_list) else ""
        out+=(c+pc) if i%2==0 else (pc+c)     # zigzag: alternate card/photo side each row
        if band and i==2: out+=band            # full-width stat band after 3 rows
    return (CG_CSS+'<section id="cg" class="cg-sec relative w-full pt-10 lg:pt-20 pb-10 lg:pb-20 border-border"><span class="cg-blob"></span><div class="container"><div class="cg-wrap">'
      '<div class="cg-head">'
      f'<span class="cg-ey">{eyebrow}</span>'
      f'<h2 class="cg-h2">{h2}</h2><div class="cg-rule"></div></div>'
      f'<p class="cg-lead">{lead}</p>'
      f'{feat}<div class="cg-grid">{out}</div></div></div></section>')

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
    dots="".join(f'<button type="button" class="proc-dot{" is-active" if i==0 else ""}" data-i="{i}" aria-current="{"true" if i==0 else "false"}" aria-label="Go to step {i+1}"></button>' for i in range(len(PROC_STEPS)))
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
      '<div class="proc-dots" role="group" aria-label="Storage step navigation">'+dots+'</div>'
      '<button type="button" class="proc-arrow proc-next" aria-label="Next step">'+ARRR+'</button>'
      '</div></div>')
    return centered("bg-beige","Our Step-by-Step Storage Process","We handle the heavy lifting, literally &mdash; here&rsquo;s how storing with us works.",inner)

def faq(items):
    cards=""
    for q,a in items:
        cards+=('<div class="faq-card" x-data="{open:false}" :class="open && \'is-open\'">'
                '<button type="button" class="faq-head" @click="open=!open" :aria-expanded="open ? \'true\' : \'false\'">'
                '<span class="faq-ico"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="w-6 h-6"><path d="M3 3h8v8H3zm10 5h8v13h-8zM3 13h8v8H3z"/></svg></span>'
                f'<span class="faq-q">{q}</span>'
                '<span class="faq-toggle" :class="open && \'is-open\'"><svg viewBox="0 0 20 20" class="w-5 h-5 fill-current" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg></span></button>'
                f'<div class="faq-body" x-show="open" x-cloak x-transition.duration.200ms><p>{a}</p></div></div>')
    inner=f'<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2"><div class="faq-list">{cards}</div></div></div>'
    return (f'<section class="relative bg-beige w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container">'
            f'<div class="text-center mb-6 lg:mb-8"><h2 class="relative leading-tight text-black">Storage &mdash; Your Questions Answered</h2></div>{inner}</div></section>')

GAL_ZOOM='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/></svg>'
GAL_ARR_L='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
GAL_ARR_R='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
GAL_CSS=('<style>'
  '.gal-grid{display:grid;grid-template-columns:1fr;gap:1rem}'
  '@media (min-width:640px){.gal-grid{grid-template-columns:repeat(2,1fr)}}'
  '@media (min-width:1024px){.gal-grid{grid-template-columns:repeat(3,1fr);gap:1.25rem}}'
  '.gal-tile{position:relative;display:block;width:100%;padding:0;border:0;cursor:pointer;overflow:hidden;border-radius:1.15rem;background:#262626;aspect-ratio:4/3;box-shadow:0 14px 34px -18px rgba(38,38,38,.5);transition:transform .35s cubic-bezier(.2,.7,.3,1),box-shadow .35s ease}'
  '.gal-tile:hover{transform:translateY(-6px);box-shadow:0 30px 60px -22px rgba(38,38,38,.6)}'
  '.gal-tile:focus-visible{outline:2px solid #FC9700;outline-offset:3px}'
  '.gal-tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.7,.3,1)}'
  '.gal-tile:hover img{transform:scale(1.07)}'
  '.gal-scrim{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(to top,rgba(38,38,38,.86),rgba(38,38,38,.18) 44%,rgba(38,38,38,0) 70%)}'
  '.gal-cap{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:.95rem 1.05rem;color:#fff;font-weight:700;font-size:.95rem;line-height:1.3;text-align:left;display:flex;align-items:center;gap:.55rem}'
  '.gal-cap::before{content:"";width:14px;height:3px;border-radius:3px;flex:none;background:linear-gradient(90deg,#FC9700,#F6BB06);transition:width .35s ease}'
  '.gal-tile:hover .gal-cap::before,.gal-tile:focus-visible .gal-cap::before{width:28px}'
  '.gal-badge{position:absolute;top:.7rem;right:.7rem;z-index:2;width:40px;height:40px;border-radius:.72rem;display:flex;align-items:center;justify-content:center;background:#E8E6DA;color:#697783;box-shadow:0 6px 16px -6px rgba(0,0,0,.5);opacity:0;transform:translateY(-4px) scale(.9);transition:opacity .3s ease,transform .3s ease,background .3s ease,color .3s ease}'
  '.gal-tile:hover .gal-badge,.gal-tile:focus-visible .gal-badge{opacity:1;transform:none}.gal-tile:hover .gal-badge{background:#FC9700;color:#fff}'
  '.gal-eyebrow{display:inline-block;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:.55rem}'
  '.gal-lb[x-cloak]{display:none}'
  '.gal-lb{position:fixed;inset:0;z-index:90;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.5rem;background:rgba(20,22,24,.94);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}'
  '.gal-lb-stage{position:relative;display:flex;align-items:center;justify-content:center;max-width:min(1100px,94vw)}'
  '.gal-lb-stage img{max-width:100%;max-height:80vh;border-radius:.9rem;box-shadow:0 30px 80px -20px rgba(0,0,0,.8)}'
  '.gal-lb-cap{margin-top:1.1rem;color:#E8E6DA;font-weight:600;font-size:.98rem;text-align:center;max-width:42rem}'
  '.gal-lb-count{margin-top:.4rem;color:rgba(255,255,255,.55);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase}'
  '.gal-lb-nav{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border-radius:999px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff;cursor:pointer;transition:background .25s ease,border-color .25s ease}'
  '.gal-lb-nav:hover{background:#FC9700;border-color:#FC9700}.gal-lb-nav svg{width:22px;height:22px}'
  '.gal-lb-prev{left:6px}.gal-lb-next{right:6px}'
  '@media(min-width:768px){.gal-lb-prev{left:-66px}.gal-lb-next{right:-66px}}'
  '.gal-lb-close{position:absolute;top:1.1rem;right:1.3rem;width:44px;height:44px;border-radius:999px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.7rem;line-height:1;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);cursor:pointer;transition:background .25s ease,border-color .25s ease}'
  '.gal-lb-close:hover{background:#FC9700;border-color:#FC9700}'
  '@media (prefers-reduced-motion:reduce){.gal-tile,.gal-tile img,.gal-badge{transition:none}.gal-tile:hover,.gal-tile:hover img{transform:none}}'
  '</style>')
def gallery(imgs, heading="See Our Sussex Storage in Action", lead="Real photos of our own facility, containers, team and fleet.", eyebrow="Inside Wolves Storage Sussex"):
    tiles=""
    for ix,it in enumerate(imgs):
        s,a=it[0],it[1]; cap=it[2] if len(it)>2 else a
        tiles+=(f'<button type="button" class="gal-tile" @click="i={ix}" aria-label="View larger: {a}">'
                f'<img src="{s}" alt="{a}" width="1200" height="900" loading="lazy" decoding="async">'
                f'<span class="gal-scrim" aria-hidden="true"></span><span class="gal-badge" aria-hidden="true">{GAL_ZOOM}</span>'
                f'<span class="gal-cap">{cap}</span></button>')
    n=len(imgs)
    data=[{"s":it[0],"a":html.unescape(it[1]),"c":html.unescape(it[2] if len(it)>2 else it[1])} for it in imgs]
    gjson=html.escape(json.dumps(data,ensure_ascii=False))
    leadp=f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{lead}</p>' if lead else ""
    eb=f'<span class="gal-eyebrow">{eyebrow}</span>' if eyebrow else ""
    return ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border" x-data="{g:'+gjson+',i:-1}">'
            +GAL_CSS+
            f'<div class="container"><div class="text-center mb-8 lg:mb-10">{eb}<h2 class="relative leading-tight text-black">{heading}</h2>{leadp}</div>'
            f'<div class="gal-grid">{tiles}</div></div>'
            '<div x-show="i>=0" x-cloak class="gal-lb" @keydown.escape.window="i=-1" @keydown.arrow-left.window="if(i>=0)i=(i-1+g.length)%g.length" @keydown.arrow-right.window="if(i>=0)i=(i+1)%g.length" @click.self="i=-1">'
            '<button type="button" class="gal-lb-close" @click="i=-1" aria-label="Close gallery">&times;</button>'
            '<div class="gal-lb-stage">'
            f'<button type="button" class="gal-lb-nav gal-lb-prev" @click="i=(i-1+g.length)%g.length" aria-label="Previous image">{GAL_ARR_L}</button>'
            '<img :src="g[i]?.s||\'\'" :alt="g[i]?.a||\'\'" alt="Enlarged Wolves Storage Sussex gallery photo" width="1200" height="900">'
            f'<button type="button" class="gal-lb-nav gal-lb-next" @click="i=(i+1)%g.length" aria-label="Next image">{GAL_ARR_R}</button>'
            '</div>'
            '<p class="gal-lb-cap" x-text="i>=0?g[i].c:\'\'"></p>'
            f'<p class="gal-lb-count"><span x-text="i+1"></span> / {n}</p>'
            '</section>')

VIDEO_POSTER="storage-container-promo-poster.webp"   # exact title-card frame baked from the clip
def video_promo():
    # Baked 16:9 poster (the clip's title-card frame) guarantees the same landscape
    # still on every device before play; width/height reserve the box (no CLS).
    inner=('<div class="mx-auto" style="max-width:56rem">'
           '<div class="relative rounded-2xl overflow-hidden shadow-custom" style="border:1px solid #E7E7E7;background:#000">'
           f'<video class="block w-full" controls preload="metadata" playsinline width="1280" height="720" poster="{IMG(VIDEO_POSTER)}" '
           'style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;background:#000;display:block" '
           'aria-label="Wolves Storage Sussex managed container storage video">'
           '<source src="/videos/storage-container-promo-b.mp4" type="video/mp4">'
           'Your browser does not support embedded video. </video></div>'
           '<p class="text-darkgrey mt-4 text-center">Our team loading and storing mobile storage containers securely at our Sussex depot.</p>'
           '</div>')
    return centered("bg-lightgrey","Secure Storage with Wolves Removals","",inner)
VIDEO_SCHEMA='<script type="application/ld+json">'+json.dumps({
  "@context":"https://schema.org","@type":"VideoObject",
  "name":"Managed Container Storage in West Sussex — Wolves Storage Sussex",
  "description":"See how Wolves Storage Sussex packs, wraps, collects and securely stores your belongings in sealed wooden containers at our alarmed Ashington facility.",
  "thumbnailUrl":[BASE+"images/"+VIDEO_POSTER],"uploadDate":"2026-06-01",
  "contentUrl":BASE+"videos/storage-container-promo-b.mp4",
  "publisher":{"@type":"Organization","name":"Wolves Storage Sussex","logo":{"@type":"ImageObject","url":BASE+"images/wolves-storage-logo@480.webp"}}
},ensure_ascii=False)+'</script>'

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
 'function showErr(msg){var box=f.querySelector("[data-form-error]");if(!box){box=document.createElement("div");box.setAttribute("data-form-error","");box.setAttribute("role","alert");box.setAttribute("aria-live","assertive");box.style.cssText="margin-top:1rem;padding:1rem 1.25rem;border-radius:.75rem;background:#fdecec;color:#a11616;font-weight:600;font-size:.95rem";var anchor=f.querySelector("[data-form-fields]")||f;anchor.appendChild(box);}box.hidden=false;box.textContent=msg;}'
 'var prev=f.querySelector("[data-form-error]");if(prev)prev.hidden=true;'
 'var ok=true,first=null;f.querySelectorAll("[required]").forEach(function(x){var bad=x.type==="checkbox"?!x.checked:!x.value.trim();x.style.borderColor=bad?"#c00":"";x.setAttribute("aria-invalid",bad?"true":"false");if(bad){ok=false;if(!first)first=x;}});'
 'var em=f.querySelector("input[type=email]"),bademail=false;if(em&&em.value.trim()&&!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em.value.trim())){ok=false;bademail=true;em.style.borderColor="#c00";em.setAttribute("aria-invalid","true");if(!first)first=em;}'
 'if(!ok){showErr((bademail&&first===em)?"Please enter a valid email address.":"Please complete the highlighted required fields before sending.");if(first){try{first.focus();}catch(_){}if(first.scrollIntoView)first.scrollIntoView({behavior:"smooth",block:"center"});}return;}'
 'var btn=f.querySelector("button[type=submit]")||f.querySelector("button");var orig=btn?btn.innerHTML:"";'
 'var data={};new FormData(f).forEach(function(v,k){if(k in data){if(!Array.isArray(data[k]))data[k]=[data[k]];data[k].push(v);}else{data[k]=v;}});'
 'data.page=document.title;data.page_url=location.href;'
 'if(btn){btn.disabled=true;btn.innerHTML="Sending\\u2026";}'
 'try{var res=await fetch("/api/contact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});'
 'var j={};try{j=await res.json();}catch(_){}'
 'if(res.ok&&j&&j.ok){var fl=f.querySelector("[data-form-fields]");if(fl)fl.style.display="none";var s=f.querySelector("[data-form-success]");if(s){s.hidden=false;s.setAttribute("role","status");s.setAttribute("tabindex","-1");try{s.focus();}catch(_){}if(s.scrollIntoView)s.scrollIntoView({behavior:"smooth",block:"center"});}}'
 'else{var se=new Error((j&&j.error)||"send failed");se.fromServer=true;throw se;}'
 '}catch(err){if(btn){btn.disabled=false;btn.innerHTML=orig;}'
 'showErr((err&&err.fromServer&&err.message&&err.message!=="send failed")?err.message:"Sorry \\u2014 your message couldn\\u2019t be sent just now. Please call 01903 893731 or email info@sussexstoragecompany.co.uk.");}'
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
        items=[{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
        if d.get("crumb_parent"):
            pf,pn=d["crumb_parent"]
            items.append({"@type":"ListItem","position":2,"name":pn,"item":BASE+pf})
            items.append({"@type":"ListItem","position":3,"name":d["nav"],"item":BASE+d["file"]})
        else:
            items.append({"@type":"ListItem","position":2,"name":d["nav"],"item":BASE+d["file"]})
        crumb='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items},ensure_ascii=False)+'</script>'
    canon = BASE if d["file"]=="index.html" else BASE+d["file"]
    gpos = d.get("geo_pos","50.9270;-0.4470"); gplace = d.get("geo_place","Ashington, Pulborough, West Sussex"); gicbm = gpos.replace(";",", ")
    return ('<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{d["title"]}</title>\n<meta name="description" content="{d["meta"]}">\n<meta name="robots" content="index, follow">\n'
        f'<link rel="canonical" href="{canon}">\n<meta name="theme-color" content="#697783">\n'+SPLIT_CSS+'\n'
        f'<meta name="geo.region" content="GB-WSX"><meta name="geo.placename" content="{gplace}"><meta name="geo.position" content="{gpos}"><meta name="ICBM" content="{gicbm}">\n'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Wolves Storage Sussex"><meta property="og:title" content="{d["title"]}"><meta property="og:description" content="{d["meta"]}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}{d["hero"].lstrip("/")}"><meta property="og:locale" content="en_GB">\n'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{d["title"]}"><meta name="twitter:description" content="{d["meta"]}"><meta name="twitter:image" content="{BASE}{d["hero"].lstrip("/")}">\n'
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="manifest" href="/site.webmanifest">\n'
        '<link rel="preload" href="/fonts/Barlow-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/Barlow-Semibold.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/Barlow-Bold.woff2" as="font" type="font/woff2" crossorigin>\n'
        f'<link rel="stylesheet" href="{CSSV}">'+A11Y_CSS+f'\n<script type="application/ld+json">{ORG}</script>\n{crumb}\n{faqjson}\n{d.get("extra_schema","")}\n</head>')

SCRIPTS = '<script defer src="/js/alpine.min.js"></script><script defer src="/js/process-carousel.js?v=3"></script>'+FORM_JS

TRUSTED_BY = '<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="text-center mb-10"><h2 class="relative leading-tight text-black">We&rsquo;re Trusted By</h2></div><div class="flex justify-center mb-10 lg:mb-12"><a href="https://lapada.org/dealers/wolves-removals/" target="_blank" rel="noopener" aria-label="Wolves Storage Sussex is LAPADA accredited" class="inline-block hover:opacity-80 transition-opacity"><img src="/images/photos/lapada-approved-service-provider.webp" alt="LAPADA Approved Service Provider, Association of Art &amp; Antiques Dealers" width="520" height="493" loading="lazy" decoding="async" class="h-32 sm:h-40 lg:h-44 w-auto"></a></div><div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 items-center gap-2"><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/fine-and-country-recommend-wolves.webp" alt="Fine &amp; Country estate agents recommend Wolves Storage Sussex" width="500" height="250" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/justin-lloyd-estate-agents-recommend.webp" alt="Justin Lloyd estate agents recommend Wolves Storage Sussex" width="210" height="80" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/mansell-mctaggart-estate-agents-partner.webp" alt="Mansell McTaggart estate agents recommend Wolves Storage Sussex" width="179" height="81" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/leaders-estate-agents-recommend.webp" alt="Leaders estate agents recommend Wolves Storage Sussex" width="251" height="81" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/alex-harvey-estate-agents-recommend.webp" alt="Alex Harvey estate agents recommend Wolves Storage Sussex" width="400" height="200" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div><div class="flex items-center justify-center py-3 px-3"><img src="/images/photos/at-home-estate-lettings-recommend.webp" alt="At Home estate agents recommend Wolves Storage Sussex" width="389" height="108" loading="lazy" decoding="async" class="h-10 sm:h-12 lg:h-14 w-auto max-w-full"></div></div></div></section>'

def fix_amps(html):
    # Escape raw & -> &amp; in HTML text/attributes for valid markup, while leaving
    # <script>/<style> blocks untouched (protects JSON-LD + JS), skipping && (Alpine/JS
    # logical-and) and existing entities (&amp;, &rsquo;, &#39;, ...).
    parts = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)', html, flags=re.S|re.I)
    for i in range(0, len(parts), 2):   # even indices = non-script/style segments
        parts[i] = re.sub(r'(?<!&)&(?!&)(?!#?[A-Za-z0-9]+;)', '&amp;', parts[i])
    return "".join(parts)

def page(d):
    skip='<a href="#main" style="position:absolute;left:-999px;top:0;z-index:100;background:#262626;color:#fff;padding:.65rem 1.1rem;font-weight:600;border-radius:0 0 .5rem 0" onfocus="this.style.left=\'0\'" onblur="this.style.left=\'-999px\'">Skip to content</a>'
    body_open=f'<body class="font-body bg-white text-black overflow-x-clip text-base xl:text-lg page-{d["slug"]}">{skip}<div id="page" class="relative min-h-screen block" x-data="{{menuOpen:false}}" x-effect="document.documentElement.classList.toggle(\'overflow-hidden\', menuOpen)" @keydown.escape.window="menuOpen=false">'
    return head(d)+"\n"+body_open+"\n"+HEADER+"\n<main id=\"main\">\n"+"\n".join(d["sections"])+("" if d["slug"] in ("404","legal") else "\n"+TRUSTED_BY)+"\n</main>\n"+FOOTER+"\n"+SCRIPTS+"\n</div></body></html>"

IMG=lambda n:"/images/"+n

# ── Hero images ── the ONLY images used as page heroes (per brief). (img, alt)
HERO_VAN_COLLECT=("wolves-storage-team-collection-luton-van-hero.webp","Wolves Storage Sussex team member walking to the Luton van on a managed collection in West Sussex")
HERO_FURNITURE  =("furniture-packing-wrapping-storage-hero.webp","Wolves Storage Sussex packer wrapping furniture in Furni-guard padding before secure storage")
HERO_PACKING    =("professional-packing-labelling-boxes-hero.webp","Wolves Storage Sussex packer labelling a carefully packed box during a professional home pack")
HERO_ANTIQUE    =("antique-fine-art-storage-hero.webp","An elegant West Sussex room of antiques and fine art prepared for specialist Wolves storage")
HERO_LOADING    =("loading-boxes-removal-van-storage-hero.webp","Wolves Storage Sussex movers loading packed boxes up the ramp into the van")
HERO_AERIAL     =("aerial-storage-collection-west-sussex-hero.webp","Aerial view of Wolves Storage Sussex vans collecting from a West Sussex property")
HERO_WAREHOUSE  =("storage-warehouse-van-west-sussex-hero.webp","The Wolves Storage Sussex van outside our secure container storage warehouse in West Sussex")
TOWN_HEROES=[HERO_WAREHOUSE,HERO_VAN_COLLECT,HERO_AERIAL,HERO_LOADING,HERO_PACKING,HERO_FURNITURE,HERO_ANTIQUE]
def town_hero(t):
    h=TOWN_HEROES[sum(ord(c) for c in t["slug"])%len(TOWN_HEROES)]
    return IMG(h[0]), f'{h[1]} &mdash; storage in {t["town"]}, {t.get("region","West Sussex")}'
# ---------------- pages ----------------
TRUSTINDEX_SECTION = ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
  '<div class="container"><div class="flex justify-center mb-8 lg:mb-10"><div style="zoom:.8"><div class="ti-reviews-widget max-w-full"><script defer async src="https://cdn.trustindex.io/loader.js?cd741d573fcc673344062ffdcd3"></script></div></div></div></div>'
  '<div style="max-width:1720px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem;"><div style="zoom:.8"><div class="ti-reviews-widget w-full"><script defer async src="https://cdn.trustindex.io/loader.js?c457a627393e67277d368b8df3b"></script></div></div></div>'
  '</section>')

CALC_SECTION = ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container">'
  '<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">Storage Cost Calculator</h2>'
  '<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">Add what you need to store or set the number of pods, and we&rsquo;ll estimate the space and weekly price you need &mdash; then get a free quote to confirm.</p></div>'
  +CALC_HTML+'</div></section>'
  '<script defer src="/js/storage-calculator.js?v=2"></script>')

CX_BOX='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>'
CX_CK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.4 4.5L19.5 7"/></svg>'
CX_CSS=('<style>'
  '.cx-sec{position:relative;overflow:hidden;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%)}'
  '.cx-sec::before{content:"";position:absolute;inset:0;background:radial-gradient(110% 120% at 12% -10%,rgba(252,151,0,.18),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.cx-sec::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.cx-sec .container{position:relative;z-index:1}'
  '.cx-eyebrow{display:inline-block;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:.55rem}'
  '.cx-sec h2{color:#fff}'
  '.cx-rule{display:block;width:54px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FC9700,#F6BB06);margin:.85rem 0 1.15rem}'
  '.cx-sec p{color:rgba(255,255,255,.85)}'
  '.cx-list{list-style:none;margin:1.5rem 0 0;padding:0;display:flex;flex-direction:column;gap:.8rem}'
  '.cx-list li{display:flex;align-items:flex-start;gap:.7rem;color:#fff;font-weight:600;font-size:1rem;line-height:1.4}'
  '.cx-tick{flex:none;display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:999px;background:rgba(70,217,138,.18);color:#5ee0a0;margin-top:.02rem}'
  '.cx-tick svg{width:14px;height:14px}'
  '.cx-figure{position:relative;text-align:center}'
  '.cx-img{position:relative;overflow:hidden;border-radius:1.15rem;background:#fff;padding:12px;box-shadow:0 28px 64px -26px rgba(0,0,0,.62);transition:transform .4s cubic-bezier(.2,.7,.3,1),box-shadow .4s ease}'
  '.cx-img::after{content:"";position:absolute;left:0;right:0;top:0;height:4px;z-index:2;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.cx-img img{display:block;width:100%;height:auto;border-radius:.6rem}'
  '.cx-figure:hover .cx-img{transform:translateY(-5px);box-shadow:0 38px 78px -28px rgba(0,0,0,.68)}'
  '.cx-spec{display:inline-flex;align-items:center;gap:.45rem;margin-top:1.1rem;padding:.5rem .95rem;border-radius:.6rem;background:#262626;color:#fff;font-size:.78rem;font-weight:700;box-shadow:0 10px 22px -10px rgba(0,0,0,.55)}'
  '.cx-spec svg{width:15px;height:15px;color:#FC9700;flex:none}'
  '@media (prefers-reduced-motion:reduce){.cx-img{transition:none}.cx-figure:hover .cx-img{transform:none}}'
  '</style>')
def container_explainer(heading,paras,ticks,eyebrow="The container advantage"):
    body="".join('<p>'+p+'</p>' for p in paras)
    lis="".join('<li><span class="cx-tick">'+CX_CK+'</span><span>'+t+'</span></li>' for t in ticks)
    return ('<section class="cx-sec relative w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'+CX_CSS+
            '<div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-12 items-center">'
            '<div class="col-span-12 lg:col-span-6 lg:col-start-2">'
            '<span class="cx-eyebrow">'+eyebrow+'</span>'
            '<h2 class="relative leading-tight">'+heading+'</h2><span class="cx-rule" aria-hidden="true"></span>'
            +body+'<ul class="cx-list">'+lis+'</ul></div>'
            '<div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="cx-figure"><div class="cx-img">'
            '<img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async">'
            '</div><span class="cx-spec">'+CX_BOX+'250 cu ft &middot; 5&times;7&times;8.6ft</span>'
            '</div></div></div></div></section>')
CONTAINER_DATA={
 'index.html':("Why Container Storage Beats a Self-Storage Unit",
   ["More and more West Sussex families choose managed container storage over a drive-up self-storage unit, and it comes down to two things: how clean it stays and how secure it is. Your belongings are wrapped and sealed into your own wooden container inside our dry, ventilated facility in Ashington, rather than left in an unheated metal room you open every week.",
    "Security is layered, not left to a single padlock. The building is alarmed and monitored, access is staff-controlled, and your container stays sealed for its whole stay. As a family-run, LAPADA-accredited and Checkatrade-verified business, we&rsquo;re fully insured and trusted by local estate agents &mdash; so your things are genuinely looked after."],
   ["Sealed, private containers &mdash; not shared, open-plan rooms","Dry, ventilated storage that protects against damp and dust","Alarmed, 24/7 CCTV and staff-controlled access","Fully insured, family-run and LAPADA accredited"]),
 'storage-solutions.html':("Why Container Storage Is Cleaner &amp; More Secure Than Self-Storage",
   ["Cleanliness and security are the two reasons customers most often switch to us from a self-storage unit. Our West Sussex warehouse is dry, ventilated and managed, so your goods aren&rsquo;t exposed to the damp that creeps into unheated metal rooms over winter. Because each container is sealed once it&rsquo;s loaded, dust, pests and moisture have far fewer ways in than in a unit you open weekly.",
    "We treat the warehouse as a working facility, not a self-service car park. The building is alarmed and monitored, access is staff-controlled rather than open to the public, and your individual container stays sealed throughout its stay. As a LAPADA-member and Checkatrade-verified company we are fully insured, and we&rsquo;re recommended by respected local agents including Fine &amp; Country, Justin Lloyd and Mansell McTaggart."],
   ["Individually sealed containers &mdash; no shared, open-plan rooms","Dry, ventilated warehouse that protects against damp","Alarmed, monitored and staff-controlled access","Fully insured with LAPADA and Checkatrade backing"]),
 'long-term-storage.html':("Why Containers Protect Your Belongings for the Long Term",
   ["When your things are stored for months or even years, the difference between a sealed container and an open self-storage unit really shows. Our warehouse is dry, ventilated and stable, so furniture, fabrics and electronics don&rsquo;t sit through damp Sussex winters in an unheated metal box. Sealed once and left undisturbed, your container keeps dust, pests and moisture out far better than a unit you keep reopening.",
    "Long-term storage also needs long-term peace of mind. The facility is alarmed, monitored and staff-controlled, your container stays sealed for its entire stay, and everything is fully insured throughout. You don&rsquo;t need to visit, check or worry &mdash; and when you&rsquo;re finally ready, we simply bring it all back."],
   ["Dry, ventilated storage &mdash; ideal for months or years","Sealed once and left undisturbed, keeping damp and dust out","Alarmed, monitored and fully insured for the long haul","No need to visit &mdash; we redeliver when you&rsquo;re ready"]),
 'short-term-storage.html':("Cleaner, Easier &amp; More Secure Than a Self-Storage Unit",
   ["Even for a few weeks between moves, a sealed container beats hiring a self-storage unit. There&rsquo;s no van to rent, no driving back and forth, and no lugging boxes down a shared corridor &mdash; we pack, collect and seal everything into your own container. It stays clean and dry in our managed Ashington warehouse until the day you need it back.",
    "It&rsquo;s also more secure than a padlock-and-go unit. The building is alarmed and staff-controlled, your container is sealed throughout, and it&rsquo;s all fully insured &mdash; even for a short stay. When your move date lands, give us 24 hours&rsquo; notice and we redeliver to your door."],
   ["No van to hire and no boxes to carry yourself","Sealed, private container kept clean and dry","Alarmed, staff-controlled and fully insured","Fast collection and 24-hour redelivery"]),
 'business-storage.html':("Why Businesses Choose Containers Over Self-Storage",
   ["For stock, archives and equipment, a managed container is a safer home than an open self-storage unit. Your items are sealed into a logged container in our dry, ventilated warehouse, protected from the damp and dust that can ruin paperwork, electronics and packaging. Nothing is handled or disturbed until you ask for it back, so your inventory stays in the condition it arrived in.",
    "Security and accountability matter for business goods. The facility is alarmed, monitored and staff-controlled, every container is logged, and everything is fully insured. We collect from and redeliver to your premises, so freeing up expensive floor space doesn&rsquo;t cost your team time."],
   ["Sealed, logged containers &mdash; not shared open units","Dry, ventilated storage that protects stock and archives","Alarmed, monitored, staff-controlled and fully insured","Collection and redelivery to your premises"]),
 'pricing.html':("Why Container Storage Is Better Value Than Self-Storage",
   ["Self-storage can look cheap until you add up the extras &mdash; the van hire, the fuel, the time spent driving back and forth, and paying for floor space you never fully use. With managed container storage you only pay for the space you actually need, from just &pound;15 a week, and collection and redelivery are included &mdash; with no deposit and no hidden fees.",
    "You also get more for your money. Your belongings are sealed into your own container in our dry, ventilated, alarmed warehouse in Ashington, not left in an unheated metal room you have to visit yourself. As a family-run, LAPADA-accredited and Checkatrade-verified business, everything is fully insured &mdash; so the price you&rsquo;re quoted genuinely covers a clean, secure, fully managed service."],
   ["Pay only for the container space you use","Collection &amp; redelivery included &mdash; no van to hire","No deposit and no hidden fees","Sealed, dry, alarmed and fully insured"]),
 'furniture-storage.html':("Why Container Storage Protects Furniture Best",
   ["Furniture is exactly what suffers in an open self-storage unit &mdash; damp, dust and being shifted around all take their toll. We blanket-wrap and pad every piece, then seal it into your own wooden container inside our dry, ventilated, alarmed warehouse, so sofas, tables and wardrobes come back in the condition they left.",
    "Because the container is sealed once and left undisturbed, your furniture isn&rsquo;t handled again until it comes home. As a LAPADA-accredited, Checkatrade-verified family business we&rsquo;re fully insured and experienced with fine and antique pieces &mdash; so even treasured furniture is genuinely looked after."],
   ["Blanket-wrapped &amp; padded before sealing","Dry, ventilated storage that protects against damp","Sealed once and left undisturbed &mdash; no scuffs","LAPADA-accredited care for antique &amp; fine furniture"]),
}
CONTAINER_HTML={f:container_explainer(*v) for f,v in CONTAINER_DATA.items()}
_OLD_CONTAINER_HTML = {'index.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Beats a Self-Storage Unit</h2><p>More and more West Sussex families choose managed container storage over a drive-up self-storage unit, and it comes down to two things: how clean it stays and how secure it is. Your belongings are wrapped and sealed into your own wooden container inside our dry, ventilated facility in Ashington, rather than left in an unheated metal room you open every week.</p><p>Security is layered, not left to a single padlock. The building is alarmed and monitored, access is staff-controlled, and your container stays sealed for its whole stay. As a family-run, LAPADA-accredited and Checkatrade-verified business, we&rsquo;re fully insured and trusted by local estate agents &mdash; so your things are genuinely looked after.</p><ul class="tick-list"><li>Sealed, private containers &mdash; not shared, open-plan rooms</li><li>Dry, ventilated storage that protects against damp and dust</li><li>Alarmed, 24/7 CCTV and staff-controlled access</li><li>Fully insured, family-run and LAPADA accredited</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'storage-solutions.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Is Cleaner &amp; More Secure Than Self-Storage</h2><p>Cleanliness and security are the two reasons customers most often switch to us from a self-storage unit. Our West Sussex warehouse is dry, ventilated and managed, so your goods aren&rsquo;t exposed to the damp that creeps into unheated metal rooms over winter. Because each container is sealed once it&rsquo;s loaded, dust, pests and moisture have far fewer ways in than in a unit you open weekly.</p><p>We treat the warehouse as a working facility, not a self-service car park. The building is alarmed and monitored, access is staff-controlled rather than open to the public, and your individual container stays sealed throughout its stay. As a LAPADA-member and Checkatrade-verified company we are fully insured, and we&rsquo;re recommended by respected local agents including Fine &amp; Country, Justin Lloyd and Mansell McTaggart.</p><ul class="tick-list"><li>Individually sealed containers &mdash; no shared, open-plan rooms</li><li>Dry, ventilated warehouse that protects against damp</li><li>Alarmed, monitored and staff-controlled access</li><li>Fully insured with LAPADA and Checkatrade backing</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'long-term-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Containers Protect Your Belongings for the Long Term</h2><p>When your things are stored for months or even years, the difference between a sealed container and an open self-storage unit really shows. Our warehouse is dry, ventilated and stable, so furniture, fabrics and electronics don&rsquo;t sit through damp Sussex winters in an unheated metal box. Sealed once and left undisturbed, your container keeps dust, pests and moisture out far better than a unit you keep reopening.</p><p>Long-term storage also needs long-term peace of mind. The facility is alarmed, monitored and staff-controlled, your container stays sealed for its entire stay, and everything is fully insured throughout. You don&rsquo;t need to visit, check or worry &mdash; and when you&rsquo;re finally ready, we simply bring it all back.</p><ul class="tick-list"><li>Dry, ventilated storage &mdash; ideal for months or years</li><li>Sealed once and left undisturbed, keeping damp and dust out</li><li>Alarmed, monitored and fully insured for the long haul</li><li>No need to visit &mdash; we redeliver when you&rsquo;re ready</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'short-term-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Cleaner, Easier &amp; More Secure Than a Self-Storage Unit</h2><p>Even for a few weeks between moves, a sealed container beats hiring a self-storage unit. There&rsquo;s no van to rent, no driving back and forth, and no lugging boxes down a shared corridor &mdash; we pack, collect and seal everything into your own container. It stays clean and dry in our managed Ashington warehouse until the day you need it back.</p><p>It&rsquo;s also more secure than a padlock-and-go unit. The building is alarmed and staff-controlled, your container is sealed throughout, and it&rsquo;s all fully insured &mdash; even for a short stay. When your move date lands, give us 24 hours&rsquo; notice and we redeliver to your door.</p><ul class="tick-list"><li>No van to hire and no boxes to carry yourself</li><li>Sealed, private container kept clean and dry</li><li>Alarmed, staff-controlled and fully insured</li><li>Fast collection and 24-hour redelivery</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'business-storage.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Businesses Choose Containers Over Self-Storage</h2><p>For stock, archives and equipment, a managed container is a safer home than an open self-storage unit. Your items are sealed into a logged container in our dry, ventilated warehouse, protected from the damp and dust that can ruin paperwork, electronics and packaging. Nothing is handled or disturbed until you ask for it back, so your inventory stays in the condition it arrived in.</p><p>Security and accountability matter for business goods. The facility is alarmed, monitored and staff-controlled, every container is logged, and everything is fully insured. We collect from and redeliver to your premises, so freeing up expensive floor space doesn&rsquo;t cost your team time.</p><ul class="tick-list"><li>Sealed, logged containers &mdash; not shared open units</li><li>Dry, ventilated storage that protects stock and archives</li><li>Alarmed, monitored, staff-controlled and fully insured</li><li>Collection and redelivery to your premises</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>', 'pricing.html': '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden"><div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-start lg:items-center"><div class="col-span-12 lg:col-span-6 lg:col-start-2"><h2 class="relative leading-tight text-black">Why Container Storage Is Better Value Than Self-Storage</h2><p>Self-storage can look cheap until you add up the extras &mdash; the van hire, the fuel, the time spent driving back and forth, and paying for floor space you never fully use. With managed container storage you only pay for the space you actually need, from just &pound;15 a week, and collection and redelivery are included &mdash; with no deposit and no hidden fees.</p><p>You also get more for your money. Your belongings are sealed into your own container in our dry, ventilated, alarmed warehouse in Ashington, not left in an unheated metal room you have to visit yourself. As a family-run, LAPADA-accredited and Checkatrade-verified business, everything is fully insured &mdash; so the price you&rsquo;re quoted genuinely covers a clean, secure, fully managed service.</p><ul class="tick-list"><li>Pay only for the container space you use</li><li>Collection &amp; redelivery included &mdash; no van to hire</li><li>No deposit and no hidden fees</li><li>Sealed, dry, alarmed and fully insured</li></ul></div><div class="col-span-12 lg:col-span-4 lg:col-start-8"><div class="bg-white rounded-xl shadow-custom p-6"><img src="/images/photos/storage-pod-size-guide.webp" alt="Wolves Storage Sussex 5ft x 7ft x 8.6ft storage container size guide, 250 cubic feet (about a one-bedroom flat)" width="900" height="760" loading="lazy" decoding="async" class="w-full h-auto"></div></div></div></div></section>'}

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
   "/images/wolves-forklift-operator-loading-container.webp","Wolves Storage Sussex operator loading a sealed wooden storage container with a forklift at our secure West Sussex facility"),
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
 'furniture-storage.html':(
   "Why Trust Us With Your Furniture",
   "Furniture deserves more than being shoved around an open self-storage unit. As a family-run Sussex team since 2016, we blanket-wrap every piece, seal it into its own logged container and keep it in our dry, alarmed warehouse &mdash; fully insured, and handled by one dedicated coordinator from collection to redelivery.",
   "We&rsquo;re "+_wl("about.html","LAPADA accredited")+" for fine and antique furniture, Checkatrade-verified and rated 5.0 by hundreds of customers. See exactly "+_wl("how-it-works.html","how it works")+" or check our honest "+_wl("pricing.html","prices")+" from just &pound;15 a week.",
   "/images/carrying-furniture-past-storage-van.webp","Wolves Storage Sussex movers carrying furniture past the branded van during a collection in West Sussex"),
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

COV_PIN='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.4 7-11a7 7 0 0 0-14 0c0 4.6 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>'
COV_PHONE='<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.5.6 3.8.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.6.6 3.8.1.4 0 .8-.2 1z"/></svg>'
COV_NAV='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l18-8-8 18-2-7-8-3z"/></svg>'
COV_TRUCK='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1.5 5h13v10h-13z"/><path d="M14.5 8h4l3 3.2V15h-7z"/><circle cx="5.5" cy="17.5" r="1.9"/><circle cx="17.5" cy="17.5" r="1.9"/></svg>'
COV_CSS=('<style>'
  '.cov-eyebrow{display:inline-flex;align-items:center;gap:.55rem;font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#FC9700}'
  '.cov-eyebrow::before{content:"";width:26px;height:2px;border-radius:2px;background:linear-gradient(90deg,#FC9700,#F6BB06)}'
  '.cov-ctarow{margin-top:1.5rem;display:flex;flex-wrap:wrap;align-items:center;gap:.9rem 1.4rem}'
  '.cov-call{display:inline-flex;align-items:center;gap:.5rem;font-weight:700;color:#262626;text-decoration:none;transition:color .25s ease}'
  '.cov-call:hover{color:#FC9700}.cov-call:focus-visible{outline:2px solid #FC9700;outline-offset:3px;border-radius:6px}.cov-call svg{color:#FC9700;flex:none}'
  '.cov-console{position:relative;border-radius:1.25rem;background:#fff;border:1px solid #E7E7E7;box-shadow:0 18px 50px -22px rgba(38,38,38,.45);overflow:hidden;transition:transform .35s cubic-bezier(.2,.7,.3,1),box-shadow .35s ease}'
  '.cov-console:hover{transform:translateY(-5px);box-shadow:0 30px 72px -26px rgba(38,38,38,.55)}'
  '.cov-console::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;z-index:3;pointer-events:none;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.cov-bar{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.85rem 1rem;color:#fff;background:linear-gradient(120deg,#6f7d89,#697783 55%,#5d6a75)}'
  '.cov-pin{display:inline-flex;align-items:center;gap:.55rem;min-width:0;font-weight:700;font-size:.92rem}'
  '.cov-pinico{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;flex:none;border-radius:9px;color:#FC9700;background:rgba(252,151,0,.18)}'
  '.cov-pintxt{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
  '.cov-live{display:inline-flex;align-items:center;gap:.45rem;flex:none;padding:.32rem .7rem;border-radius:999px;font-size:.7rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8E6DA;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16)}'
  '.cov-dot{width:9px;height:9px;border-radius:50%;background:#36d07f;animation:cov-pulse 2s ease-out infinite}'
  '@keyframes cov-pulse{0%{box-shadow:0 0 0 0 rgba(54,208,127,.55)}70%{box-shadow:0 0 0 7px rgba(54,208,127,0)}100%{box-shadow:0 0 0 0 rgba(54,208,127,0)}}'
  '.cov-map{position:relative;line-height:0;background:#E8E6DA}'
  '.cov-map iframe{display:block;width:100%;height:340px;border:0;filter:saturate(1.02)}'
  '@media (min-width:1024px){.cov-map iframe{height:380px}}'
  '.cov-float{position:absolute;right:1rem;top:1rem;z-index:2;display:flex;align-items:center;gap:.7rem;max-width:calc(100% - 2rem);padding:.7rem .9rem;border-radius:.85rem;background:rgba(255,255,255,.92);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border:1px solid rgba(231,231,231,.9);box-shadow:0 12px 30px -14px rgba(38,38,38,.5);pointer-events:none}'
  '.cov-floatico{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;flex:none;border-radius:10px;color:#fff;background:#FC9700}'
  '.cov-floatnum{display:block;font-weight:800;font-size:1.02rem;line-height:1.1;color:#262626;letter-spacing:-.01em}'
  '.cov-floatsub{display:block;margin-top:.12rem;font-size:.74rem;line-height:1.25;color:#697783}'
  '.cov-foot{display:flex;align-items:center;flex-wrap:wrap;gap:.55rem;padding:.7rem 1rem;font-size:.8rem;color:#697783;background:#F9F8F6;border-top:1px solid #E7E7E7}'
  '.cov-foot svg{color:#FC9700;flex:none}.cov-foot strong{color:#262626;font-weight:700}'
  '.cov-foot-lab{font-weight:700;color:#697783;letter-spacing:.03em}'
  '.cov-chip{display:inline-flex;align-items:center;font-size:.76rem;font-weight:600;color:#262626;background:#fff;border:1px solid #E7E7E7;border-radius:999px;padding:.3rem .7rem}'
  '@media (prefers-reduced-motion:reduce){.cov-console,.cov-call{transition:none}.cov-console:hover{transform:none}.cov-dot{animation:none}}'
  '</style>')
def cov_miles(t):
    from math import radians, sin, cos, asin, sqrt
    try:
        lat=float(t["lat"]); lng=float(t["lng"])
    except (KeyError, TypeError, ValueError):
        return 0
    hlat, hlng = 50.9266, -0.4632
    dlat=radians(lat-hlat); dlng=radians(lng-hlng)
    a=sin(dlat/2)**2 + cos(radians(hlat))*cos(radians(lat))*sin(dlng/2)**2
    return max(1, int(round(3958.8*2*asin(sqrt(a)))))
def town_map(t):
    town=t["town"]; reg=t.get("region","West Sussex")
    q=(town+", "+reg).replace(" ","+")
    m=cov_miles(t)
    if m<=1:
        fnum="Ashington HQ"; fsub="You&rsquo;re right on our doorstep"
    else:
        fnum="~"+str(m)+" miles"; fsub="from our Ashington HQ &middot; same-day redelivery"
    return ('<section class="cov-sec relative bg-lightgrey w-full pt-8 lg:pt-12 pb-8 lg:pb-12 border-border" aria-label="Storage coverage area for '+town+'">'
            +COV_CSS+
            '<div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-center">'
            '<div class="col-span-12 lg:col-span-5">'
            '<span class="cov-eyebrow">Local Coverage</span>'
            '<h2 class="relative leading-tight text-black mt-3">We Cover '+town+'</h2>'
            '<p class="mt-3">From our alarmed warehouse in Ashington (RH20 3JT) we collect from and redeliver right across '+town+' and the surrounding area &mdash; just tell us your postcode.</p>'
            +checklist(["Door-to-door collection &amp; redelivery","Sealed, alarmed &amp; fully insured storage","From &pound;15/week, no deposit"])+
            '<div class="cov-ctarow">'+btn("Get a Free Quote","contact.html","px-8 lg:px-10")+
            '<a class="cov-call" href="tel:+441903893731" aria-label="Call us on '+PHONE1+'">'+COV_PHONE+'<span>Call '+PHONE1+'</span></a>'
            '</div></div>'
            '<div class="col-span-12 lg:col-span-7"><div class="cov-console">'
            '<div class="cov-bar"><span class="cov-pin"><span class="cov-pinico" aria-hidden="true">'+COV_PIN+'</span>'
            '<span class="cov-pintxt">'+town+' &amp; surrounding postcodes</span></span>'
            '<span class="cov-live"><span class="cov-dot" aria-hidden="true"></span>Service area</span></div>'
            '<div class="cov-map"><iframe title="Map of '+town+', '+reg+' storage area" src="https://www.google.com/maps?q='+q+'&amp;z=12&amp;ie=UTF8&amp;iwloc=&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            '<div class="cov-float" aria-hidden="true"><span class="cov-floatico">'+COV_NAV+'</span>'
            '<span><span class="cov-floatnum">'+fnum+'</span><span class="cov-floatsub">'+fsub+'</span></span></div></div>'
            '<div class="cov-foot">'+COV_TRUCK+'<span class="cov-foot-lab">Also serving:</span>'
            '<span class="cov-chip">Door-to-door across '+reg+'</span>'
            '<span class="cov-chip">Free quote on your postcode</span></div>'
            '</div></div>'
            '</div></div></section>')

TSTAT_ICONS={
 "star":'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.6 1.1 6.45L12 17.9l-5.8 3.05 1.1-6.45L2.6 9.45 9.1 8.5z"/></svg>',
 "home":'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.2 12 4l9 7.2"/><path d="M5 9.8V20h14V9.8"/><path d="M10 20v-5h4v5"/></svg>',
 "tag":'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 12 4.8H4.5v7.5l8.6 8.6a1.6 1.6 0 0 0 2.3 0l5.2-5.2a1.6 1.6 0 0 0 0-2.3z"/><circle cx="8" cy="8" r="1.4"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 5.7V11c0 4.6 3 7.8 7 9.3 4-1.5 7-4.7 7-9.3V5.7z"/><path d="M9 11.8l2 2 4-4"/></svg>',
}
TSTAT_DATA=[("star","5.0","478 verified reviews"),("home","Since 2016","Family-run &amp; local"),
            ("tag","&pound;15","per week, no deposit"),("shield","100%","Insured &amp; alarmed")]
TSTAT_CSS=('<style>'
  '.tstats{position:relative;overflow:hidden;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%)}'
  '.tstats::before{content:"";position:absolute;inset:0;background:radial-gradient(120% 140% at 85% -20%,rgba(252,151,0,.16),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.tstats::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700);opacity:.9}'
  '.tstat-grid{position:relative;z-index:1;display:grid;grid-template-columns:repeat(2,1fr)}'
  '.tstat{display:flex;flex-direction:column;align-items:center;text-align:center;padding:1.5rem 1rem;border-left:1px solid rgba(255,255,255,.12);transition:transform .3s cubic-bezier(.2,.7,.3,1)}'
  '.tstat:hover{transform:translateY(-4px)}'
  '.tstat:nth-child(2n+1){border-left:0}'
  '.tstat:nth-child(n+3){border-top:1px solid rgba(255,255,255,.12)}'
  '@media (min-width:1024px){.tstat-grid{grid-template-columns:repeat(4,1fr)}'
  '.tstat{border-left:1px solid rgba(255,255,255,.12);border-top:0;padding:2rem 1rem}'
  '.tstat:nth-child(4n+1){border-left:0}.tstat:nth-child(n+3){border-top:0}}'
  '.tstat-ico{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:999px;background:rgba(252,151,0,.16);color:#FC9700;margin-bottom:.7rem;transition:background .3s ease,color .3s ease,transform .3s ease}'
  '.tstat:hover .tstat-ico{background:#FC9700;color:#fff;transform:scale(1.06)}'
  '.tstat-num{font-weight:800;font-size:1.9rem;line-height:1;color:#fff;letter-spacing:-.01em}'
  '.tstat-lab{margin-top:.45rem;font-size:.82rem;color:#E8E6DA;letter-spacing:.02em}'
  '@media (min-width:1024px){.tstat-num{font-size:2.15rem}}'
  '@media (prefers-reduced-motion:reduce){.tstat,.tstat-ico{transition:none}}'
  '</style>')
def town_stats(tn):
    cells="".join(f'<div class="tstat"><span class="tstat-ico">{TSTAT_ICONS[ic]}</span>'
                  f'<span class="tstat-num">{b}</span><span class="tstat-lab">{s}</span></div>' for ic,b,s in TSTAT_DATA)
    return (f'<section class="tstats relative w-full border-border" aria-label="Why {tn} trusts Wolves Storage at a glance">'
            f'{TSTAT_CSS}<div class="container"><div class="tstat-grid">{cells}</div></div></section>')
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
# True, data-driven per-town detail (distance from base + nearest towns) so the
# shared template sections read uniquely per town — real facts only (E-E-A-T).
def near_towns(t,n=3):
    try: here=(float(t["lat"]),float(t["lng"]))
    except (KeyError,TypeError,ValueError): return []
    others=[x for x in TOWNS if x.get("slug")!=t.get("slug") and x.get("lat")]
    near=sorted(others,key=lambda x:(float(x["lat"])-here[0])**2+(float(x["lng"])-here[1])**2)[:n]
    return [x["town"] for x in near]
def dist_phrase(t):
    m=cov_miles(t)
    return "based right here in "+t["town"] if m<=1 else f"just about {m} miles from {t['town']}"
SVCX_CSS=('<style>'
  '.svcx{position:relative;overflow:hidden;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%)}'
  '.svcx::before{content:"";position:absolute;inset:0;background:radial-gradient(110% 120% at 15% -10%,rgba(252,151,0,.18),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.svcx::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.svcx-head{position:relative;z-index:1;text-align:center;margin-bottom:2.4rem}'
  '.svcx-eyebrow{display:inline-block;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.7rem}'
  '.svcx-head h2{color:#fff;margin:0}'
  '.svcx-lead{color:rgba(255,255,255,.82);font-size:1.05rem;font-weight:500;max-width:50rem;margin:.7rem auto 0}'
  '.svcx-grid{position:relative;z-index:1;display:grid;grid-template-columns:1fr;gap:1.1rem}'
  '@media(min-width:640px){.svcx-grid{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.svcx-grid{grid-template-columns:repeat(3,1fr);gap:1.3rem}}'
  '.svcx-card{position:relative;overflow:hidden;display:flex;flex-direction:column;gap:.7rem;border-radius:1.25rem;padding:1.7rem 1.5rem 1.5rem;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:0 18px 40px -24px rgba(0,0,0,.5);text-decoration:none;transition:transform .35s cubic-bezier(.2,.7,.3,1),background .35s ease,border-color .35s ease,box-shadow .35s ease}'
  '.svcx-card:hover{transform:translateY(-7px);background:rgba(255,255,255,.11);border-color:rgba(252,151,0,.5);box-shadow:0 32px 62px -26px rgba(0,0,0,.6)}'
  '.svcx-card:focus-visible{outline:2px solid #FC9700;outline-offset:3px}'
  '.svcx-ico{display:inline-flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:.95rem;color:#697783;background:#E8E6DA;box-shadow:0 10px 22px -10px rgba(0,0,0,.45);transition:transform .35s ease,color .3s ease}'
  '.svcx-card:hover .svcx-ico{transform:rotate(-6deg) scale(1.06);color:#FC9700}'
  '.svcx-ico svg{width:26px;height:26px}'
  '.svcx-name{color:#fff;font-weight:800;font-size:1.12rem;line-height:1.18;margin:0}'
  '.svcx-desc{color:rgba(255,255,255,.8);font-size:.96rem;line-height:1.55;margin:0;flex:1}'
  '.svcx-cta{display:inline-flex;align-items:center;gap:.45rem;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.07em;text-transform:uppercase;margin-top:.2rem}'
  '.svcx-cta svg{transition:transform .3s ease}.svcx-card:hover .svcx-cta svg{transform:translateX(5px)}'
  '@media (prefers-reduced-motion:reduce){.svcx-card,.svcx-ico,.svcx-cta svg{transition:none}.svcx-card:hover{transform:none}}'
  '</style>')
def town_services(t):
    tn=t["town"]
    cards="".join(
        '<a class="svcx-card" href="'+h+'" aria-label="'+st+' in '+tn+'">'
        '<span class="svcx-ico">'+TSVC_ICONS[ic]+'</span>'
        '<h3 class="svcx-name">'+st+'</h3><p class="svcx-desc">'+sd+'</p>'
        '<span class="svcx-cta">Learn more '+TSVC_ARROW+'</span></a>'
        for h,ic,st,sd in TOWN_SERVICES_DATA)
    near=near_towns(t,2)
    nearbit=(" We collect right across "+tn+", over to "+" and ".join(near)+" too.") if len(near)>=2 else ""
    lead=("Whatever you need to store in "+tn+", we tailor a fully managed, fully insured solution &mdash; "
          "collected from your door from just &pound;15 a week and sealed into your own wooden container at our alarmed Ashington warehouse."+nearbit)
    return ('<section class="svcx relative w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border">'+SVCX_CSS+
            '<div class="container"><div class="svcx-head">'
            '<span class="svcx-eyebrow">Fully managed storage</span>'
            '<h2 class="relative leading-tight">Storage Services in '+tn+'</h2>'
            '<p class="svcx-lead">'+lead+'</p>'
            '</div><div class="svcx-grid">'+cards+'</div></div></section>')
USP_CSS=('<style>'
  '.uspx{position:relative;overflow:hidden;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%)}'
  '.uspx::before{content:"";position:absolute;inset:0;background:radial-gradient(110% 120% at 85% -10%,rgba(252,151,0,.20),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.uspx::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.uspx-head{position:relative;z-index:1;text-align:center;margin-bottom:2.4rem}'
  '.uspx-eyebrow{display:inline-block;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.7rem}'
  '.uspx-head h2{color:#fff;margin:0}'
  '.uspx-lead{color:rgba(255,255,255,.82);font-size:1.05rem;font-weight:500;max-width:46rem;margin:.7rem auto 0}'
  '.uspx-grid{position:relative;z-index:1;display:grid;grid-template-columns:1fr;gap:1.1rem}'
  '@media(min-width:640px){.uspx-grid{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.uspx-grid{grid-template-columns:repeat(4,1fr);gap:1.4rem}}'
  '.uspx-card{position:relative;overflow:hidden;border-radius:1.25rem;padding:2rem 1.5rem 1.7rem;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:0 18px 40px -24px rgba(0,0,0,.5);transition:transform .35s cubic-bezier(.2,.7,.3,1),background .35s ease,border-color .35s ease,box-shadow .35s ease}'
  '.uspx-card:hover{transform:translateY(-7px);background:rgba(255,255,255,.11);border-color:rgba(252,151,0,.5);box-shadow:0 32px 62px -26px rgba(0,0,0,.6)}'
  '.uspx-num{position:absolute;top:.7rem;right:1rem;font-weight:800;font-size:2.6rem;line-height:1;color:rgba(255,255,255,.09);letter-spacing:-.02em}'
  '.uspx-ico{position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;width:58px;height:58px;border-radius:1rem;color:#697783;background:#E8E6DA;box-shadow:0 10px 22px -10px rgba(0,0,0,.45);margin-bottom:1.2rem;transition:transform .35s ease,color .3s ease}'
  '.uspx-card:hover .uspx-ico{transform:rotate(-6deg) scale(1.07);color:#FC9700}'
  '.uspx-ico svg{width:28px;height:28px}'
  '.uspx-card h3{position:relative;z-index:1;color:#fff;font-weight:800;font-size:1.08rem;line-height:1.22;margin:0 0 .55rem}'
  '.uspx-card p{position:relative;z-index:1;color:rgba(255,255,255,.8);font-size:.95rem;line-height:1.55;margin:0}'
  '@media (prefers-reduced-motion:reduce){.uspx-card,.uspx-ico{transition:none}.uspx-card:hover{transform:none}}'
  '</style>')
USP_ICONS={
 "shield":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 5.7V11c0 4.6 3 7.8 7 9.3 4-1.5 7-4.7 7-9.3V5.7z"/><path d="M9 11.8l2 2 4-4"/></svg>',
 "family":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.1"/><path d="M3.6 19.5a5.4 5.4 0 0 1 10.8 0"/><path d="M16 5.3a3.1 3.1 0 0 1 0 5.9"/><path d="M17.4 14.2a5.4 5.4 0 0 1 3 4.9"/></svg>',
 "tag":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 12 4.8H4.5v7.5l8.6 8.6a1.6 1.6 0 0 0 2.3 0l5.2-5.2a1.6 1.6 0 0 0 0-2.3z"/><circle cx="8" cy="8" r="1.4"/></svg>',
 "truck":'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1.5 5.5h12v9h-12z"/><path d="M13.5 8.5h4l3 3.2v2.8h-7z"/><circle cx="5.5" cy="17.5" r="1.9"/><circle cx="17.5" cy="17.5" r="1.9"/></svg>',
}
def town_usps(t):
    tn=t["town"]; reg=t.get("region","West Sussex")
    usps=[("shield","Fully Insured &amp; Alarmed","Your belongings are sealed into their own wooden container in our 24/7 CCTV, alarmed indoor warehouse and stay fully insured throughout &mdash; whether it&rsquo;s a few boxes or an entire "+reg+" home."),
          ("family","Local, Family-Run Since 2016","A LAPADA-accredited family team that knows "+tn+" and the surrounding area &mdash; so your collection and redelivery stay quick, careful and personal."),
          ("tag","From &pound;15/week, No Deposit","Honest weekly pricing with no deposit and no hidden fees &mdash; you pay only for the container space your "+tn+" move actually needs."),
          ("truck","We Come to You","No unit to drive to: we&rsquo;re "+dist_phrase(t)+", so we pack, collect from your "+tn+" door and redeliver on 24 hours&rsquo; notice.")]
    cards="".join('<article class="uspx-card"><span class="uspx-num" aria-hidden="true">'+f'{i+1:02d}'+'</span><span class="uspx-ico">'+USP_ICONS[ic]+'</span><h3>'+ti+'</h3><p>'+de+'</p></article>' for i,(ic,ti,de) in enumerate(usps))
    return ('<section class="uspx relative w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border">'+USP_CSS+
            '<div class="container"><div class="uspx-head">'
            '<span class="uspx-eyebrow">Why '+tn+' chooses us</span>'
            '<h2 class="relative leading-tight">The Wolves Storage Difference in '+tn+'</h2>'
            '<p class="uspx-lead">Local, managed and genuinely cared for &mdash; why '+tn+' homes and businesses choose us.</p>'
            '</div><div class="uspx-grid">'+cards+'</div></div></section>')
def town_nearby(t):
    try: here=(float(t["lat"]),float(t["lng"]))
    except: return ""
    others=[x for x in TOWNS if x.get("slug")!=t.get("slug") and x.get("lat")]
    near=sorted(others,key=lambda x:(float(x["lat"])-here[0])**2+(float(x["lng"])-here[1])**2)[:6]
    chips="".join(f'<a href="{x["slug"]}.html" class="inline-block bg-lightgrey rounded-full px-5 py-2 font-semibold text-black shadow-custom hover:text-orange">Storage in {x["town"]}</a>' for x in near)
    leads=["Our managed collection reaches well beyond "+t["town"]+" &mdash; here are nearby towns we store for too.",
           "We don&rsquo;t just cover "+t["town"]+"; these neighbouring towns rely on the same door-to-door managed storage.",
           "Storing near "+t["town"]+"? We collect across these nearby towns on the same simple weekly terms."]
    lead=leads[sum(ord(c) for c in t["slug"])%len(leads)]
    return centered("bg-white","Areas Near "+t["town"]+" We Also Cover",lead,'<div class="flex flex-wrap gap-3 justify-center">'+chips+'</div>')

# ---- Deeper town-page content (gated; add slugs to EXPAND_TOWNS to roll out) ----
TOWN_INFO = {}                          # slug -> {pc, tag, group}; populated in build() from area_groups
EXPAND_TOWNS = "ALL"                    # ROLLED OUT: every town gets the full advanced treatment
EXPAND_SERVICES = {"long-term-storage.html","storage-solutions.html","short-term-storage.html","business-storage.html"}  # ROLLED OUT to all service() pages
AREA_CSS=('<style>'
  '.acov-panel{position:relative;overflow:hidden;max-width:66rem;margin:0 auto;border-radius:1.5rem;padding:2rem 1.4rem 2.2rem;background:linear-gradient(155deg,#edece4 0%,#e3e0d2 100%);border:1px solid #dcd8c8;box-shadow:0 26px 64px -34px rgba(38,38,38,.4)}'
  '@media(min-width:768px){.acov-panel{padding:2.4rem 2.2rem 2.6rem}}'
  '.acov-panel::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.acov-eyebrow{display:flex;align-items:center;justify-content:center;gap:.65rem;color:#FC9700;font-weight:700;font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;margin:0 0 1.5rem}'
  '.acov-eyebrow::before,.acov-eyebrow::after{content:"";width:26px;height:2px;border-radius:2px;background:#FC9700;opacity:.55}'
  '.acov-grid{display:grid;grid-template-columns:1fr;gap:.85rem}'
  '@media(min-width:640px){.acov-grid{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.acov-grid{grid-template-columns:repeat(3,1fr);gap:1rem}}'
  '.acov-card{position:relative;overflow:hidden;display:flex;align-items:center;gap:.9rem;background:#fff;border:1px solid #E7E7E7;border-radius:1rem;padding:.95rem 1.1rem;text-decoration:none;box-shadow:0 2px 8px rgba(38,38,38,.06);transition:transform .32s cubic-bezier(.2,.7,.3,1),box-shadow .32s ease,background .32s ease,border-color .32s ease}'
  '.acov-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,#FC9700,#F6BB06);transform:scaleY(0);transform-origin:top;transition:transform .32s ease}'
  '.acov-card:hover{transform:translateY(-5px);background:linear-gradient(150deg,#74828d 0%,#697783 60%,#5d6a75 100%);border-color:transparent;box-shadow:0 24px 46px -20px rgba(105,119,131,.62)}'
  '.acov-card:hover::before{transform:scaleY(1)}'
  '.acov-card:focus-visible{outline:2px solid #FC9700;outline-offset:3px}'
  '.acov-pin{flex:none;display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:.72rem;background:#E8E6DA;color:#697783;transition:background .32s ease,color .32s ease,transform .32s ease}'
  '.acov-card:hover .acov-pin{background:#FC9700;color:#fff;transform:rotate(-6deg) scale(1.05)}'
  '.acov-body{flex:1;min-width:0;text-align:left}'
  '.acov-name{display:block;font-weight:700;color:#262626;line-height:1.15;transition:color .32s ease}'
  '.acov-card:hover .acov-name{color:#fff}'
  '.acov-pc{display:inline-block;margin-top:.3rem;font-size:.66rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#697783;background:#F9F8F6;border:1px solid #E7E7E7;border-radius:999px;padding:.14rem .55rem;transition:color .32s ease,background .32s ease,border-color .32s ease}'
  '.acov-card:hover .acov-pc{color:#fff;background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.32)}'
  '.acov-arr{flex:none;color:#FC9700;transition:color .32s ease,transform .32s ease}'
  '.acov-card:hover .acov-arr{color:#fff;transform:translateX(3px)}'
  '@media (prefers-reduced-motion:reduce){.acov-card,.acov-pin,.acov-arr,.acov-card::before{transition:none}.acov-card:hover{transform:none}}'
  '</style>')
AREA_PIN='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>'
AREA_ARR='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg>'
def town_areas(t):
    tn=t["town"]; reg=t.get("region","West Sussex"); pc=TOWN_INFO.get(t["slug"],{}).get("pc","")
    try: here=(float(t["lat"]),float(t["lng"]))
    except (KeyError,TypeError,ValueError): here=None
    cards=""
    if here:
        others=[x for x in TOWNS if x.get("slug")!=t.get("slug") and x.get("lat")]
        near=sorted(others,key=lambda x:(float(x["lat"])-here[0])**2+(float(x["lng"])-here[1])**2)[:6]
        for x in near:
            xpc=TOWN_INFO.get(x["slug"],{}).get("pc","")
            pcb='<span class="acov-pc">'+xpc+'</span>' if xpc else ''
            cards+=('<a class="acov-card" href="'+x["slug"]+'.html" aria-label="Storage in '+x["town"]+'">'
                    '<span class="acov-pin">'+AREA_PIN+'</span>'
                    '<span class="acov-body"><span class="acov-name">Storage in '+x["town"]+'</span>'+pcb+'</span>'
                    '<span class="acov-arr">'+AREA_ARR+'</span></a>')
    covbit=("right across the "+pc+" postcode area, "+tn+" itself and the surrounding villages" if pc
            else "right across "+tn+" and the surrounding villages")
    lead=("We collect "+covbit+" &mdash; there&rsquo;s no self-storage unit to drive to. Just tell us your postcode and our family team packs, seals and stores your belongings, then redelivers across "+reg+" on 24 hours&rsquo; notice.")
    inner=AREA_CSS+'<div class="acov-panel"><p class="acov-eyebrow">Nearby towns we also cover</p><div class="acov-grid">'+cards+'</div></div>'
    return centered("bg-white","Areas &amp; Postcodes We Cover Around "+tn,lead,inner)
TPRICE_CSS=('<style>'
  '.tp-wrap{position:relative;display:grid;grid-template-columns:1fr;background:#fff;border:1px solid #E7E7E7;border-radius:1.5rem;box-shadow:0 28px 64px -32px rgba(38,38,38,.4);overflow:hidden;text-align:left}'
  '@media(min-width:1024px){.tp-wrap{grid-template-columns:minmax(0,400px) 1fr}}'
  '.tp-price{position:relative;padding:2.6rem 2rem;color:#fff;background:linear-gradient(150deg,#76838e 0%,#697783 52%,#586571 100%);overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}'
  '.tp-price::before{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 80% -10%,rgba(252,151,0,.22),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.tp-price::after{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.tp-eyebrow{position:relative;z-index:1;text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;color:#E8E6DA}'
  '.tp-amount{position:relative;z-index:1;display:flex;align-items:flex-start;justify-content:center;gap:.12rem;margin:.45rem 0 .15rem;line-height:1}'
  '.tp-pound{font-size:1.8rem;font-weight:700;margin-top:.5rem}'
  '.tp-num{font-size:4.4rem;font-weight:800;letter-spacing:-.02em}'
  '.tp-per{align-self:flex-end;margin-bottom:.75rem;font-size:1.05rem;font-weight:600;color:#E8E6DA}'
  '.tp-sub{position:relative;z-index:1;margin:.1rem 0 1.5rem;color:#E8E6DA;font-size:.95rem}'
  '.tp-trust{position:relative;z-index:1;display:flex;flex-wrap:wrap;justify-content:center;gap:.5rem;margin-top:1.5rem}'
  '.tp-chip{display:inline-flex;align-items:center;gap:.35rem;padding:.34rem .72rem;border-radius:999px;font-size:.74rem;font-weight:600;color:#fff;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22)}'
  '.tp-chip .st{color:#F6BB06}'
  '.tp-detail{padding:2.3rem 2rem;display:grid;grid-template-columns:1fr;gap:1.8rem 2.5rem}'
  '@media(min-width:640px){.tp-detail{grid-template-columns:1fr 1fr}}'
  '.tp-h{position:relative;font-weight:800;color:#262626;font-size:1.02rem;text-transform:uppercase;letter-spacing:.04em;padding-bottom:.6rem;margin:0 0 1.05rem}'
  '.tp-h::after{content:"";position:absolute;left:0;bottom:0;width:38px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FC9700,#F6BB06)}'
  '.tp-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.72rem}'
  '.tp-list li{display:flex;align-items:flex-start;gap:.6rem;color:#262626;font-size:1rem;line-height:1.4}'
  '.tp-tick{flex:none;display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:999px;background:rgba(27,127,59,.12);color:#1b7f3b;margin-top:.04rem}'
  '.tp-tick svg{width:13px;height:13px}'
  '.tp-spec{display:inline-flex;align-items:center;gap:.45rem;margin:-.35rem 0 1.05rem;padding:.36rem .72rem;border-radius:.6rem;background:#F9F8F6;border:1px solid #E7E7E7;font-size:.76rem;font-weight:700;letter-spacing:.01em;color:#697783}'
  '.tp-spec svg{width:15px;height:15px;color:#FC9700;flex:none}'
  '@media (prefers-reduced-motion:no-preference){.tp-wrap{transition:box-shadow .35s ease,transform .35s ease}.tp-wrap:hover{transform:translateY(-4px);box-shadow:0 40px 84px -34px rgba(38,38,38,.45)}}'
  '</style>')
TP_CK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.4 4.5L19.5 7"/></svg>'
TP_BOX='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>'
def town_pricing(t, heading=None, lead=None, eyebrow=None, quote=None, fits=None):
    tn=t["town"]
    eyebrow=eyebrow or ("Storage in "+tn+" from"); quote=quote or ("Get Your "+tn+" Quote")
    inc=["Door-to-door collection &amp; redelivery","Your own private sealed container","24/7 CCTV &amp; alarmed indoor store","Full insurance cover throughout","No deposit and no hidden fees","Flexible weekly &amp; 4-week terms"]
    fits=fits or ["A typical one-bedroom flat","Around 30&ndash;40 standard boxes","A sofa, bed, drawers &amp; boxes","The contents of a single garage"]
    def lis(items): return "".join('<li><span class="tp-tick">'+TP_CK+'</span><span>'+x+'</span></li>' for x in items)
    price=('<div class="tp-price">'
           '<span class="tp-eyebrow">'+eyebrow+'</span>'
           '<span class="tp-amount"><span class="tp-pound">&pound;</span><span class="tp-num">15</span><span class="tp-per">/week</span></span>'
           '<p class="tp-sub">No deposit &middot; collection &amp; redelivery included</p>'
           +btn(quote,"contact.html","px-8")+
           '<div class="tp-trust"><span class="tp-chip"><span class="st">&#9733;</span> 5.0 from 478 reviews</span>'
           '<span class="tp-chip">Fully insured</span></div></div>')
    detail=('<div class="tp-detail">'
            '<div><h3 class="tp-h">What&rsquo;s included</h3><ul class="tp-list">'+lis(inc)+'</ul></div>'
            '<div><h3 class="tp-h">What fits in a container</h3>'
            '<span class="tp-spec">'+TP_BOX+'250 cu ft &middot; 5ft &times; 7ft &times; 8.6ft</span>'
            '<ul class="tp-list">'+lis(fits)+'</ul></div></div>')
    inner=TPRICE_CSS+'<div class="tp-wrap">'+price+detail+'</div>'
    heading=heading or ("Storage Prices in "+tn)
    lead=lead or ("Honest, simple pricing for "+tn+" &mdash; from just &pound;15 a week with everything included and no deposit. Need more room? We simply add another container, so you only pay for the space you use.")
    return centered("bg-beige",heading,lead,inner)
SIT_CSS=('<style>'
  '.sit-panel{position:relative;overflow:hidden;max-width:74rem;margin:1.6rem auto 0;border-radius:1.5rem;padding:1.9rem 1.3rem;background:linear-gradient(120deg,#6f7d89 0%,#697783 45%,#5d6a75 100%);border:1px solid rgba(255,255,255,.1);box-shadow:0 30px 70px -34px rgba(38,38,38,.55);display:grid;grid-template-columns:1fr;gap:.95rem}'
  '@media(min-width:640px){.sit-panel{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.sit-panel{grid-template-columns:repeat(4,1fr);padding:2.1rem 1.7rem;gap:1rem}}'
  '.sit-panel::before{content:"";position:absolute;inset:0;background:radial-gradient(120% 120% at 15% -10%,rgba(252,151,0,.16),rgba(252,151,0,0) 55%);pointer-events:none}'
  '.sit-panel::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.sit-card{position:relative;z-index:1;display:flex;flex-direction:column;gap:.65rem;background:#fff;border:1px solid #E7E7E7;border-radius:1rem;padding:1.5rem 1.25rem;box-shadow:0 6px 16px rgba(0,0,0,.2);transition:transform .3s cubic-bezier(.2,.7,.3,1),box-shadow .3s ease}'
  '.sit-card:hover{transform:translateY(-5px);box-shadow:0 24px 46px -18px rgba(0,0,0,.32)}'
  '.sit-ico{display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:.78rem;background:#E8E6DA;color:#697783;margin-bottom:.2rem;transition:background .3s ease,color .3s ease,transform .3s ease}'
  '.sit-card:hover .sit-ico{background:#FC9700;color:#fff;transform:rotate(-6deg) scale(1.05)}'
  '.sit-ico svg{width:24px;height:24px}'
  '.sit-name{font-weight:800;color:#262626;font-size:1.05rem;line-height:1.18;margin:0}'
  '.sit-desc{color:#697783;font-size:.92rem;line-height:1.5;margin:0}'
  '@media (prefers-reduced-motion:reduce){.sit-card,.sit-ico{transition:none}.sit-card:hover{transform:none}}'
  '</style>')
def town_situations(t):
    tn=t["town"]; tag=TOWN_INFO.get(t["slug"],{}).get("tag","").lower()
    POOL=[(("business","gatwick","commerc","largest"),"briefcase","Business &amp; stock","Stock, archives, tools and seasonal equipment &mdash; collected from your "+tn+" premises and redelivered when you need them."),
          (("antique","furniture","downs"),"sofa","Antiques &amp; furniture","Blanket-wrapped, sealed and given proper LAPADA-accredited care &mdash; ideal for fragile, high-value pieces."),
          (("student","commuter","city","flats"),"cap","Students &amp; renters","Somewhere secure between tenancies or over the summer, collected from the door and brought back for the new term."),
          (("coast","seaside","holiday","sunny","river","arun","adur"),"box","Holiday lets &amp; downsizing","Seasonal furniture or the contents of a downsized home, kept clean, dry and close to "+tn+".")]
    GEN=[("home","House moves &amp; chain delays","Bridge the gap between completion dates, or store the overflow while you settle into your new "+tn+" home."),
         ("box","Downsizing &amp; decluttering","Free up space without parting with what matters &mdash; sealed, insured and close by until you need it."),
         ("wrench","Renovations &amp; extensions","Protect furniture and boxes from dust and damage while the work&rsquo;s underway, then have it all brought back."),
         ("key","Probate &amp; house clearance","A calm, fully insured place to keep a loved one&rsquo;s belongings for as long as you need, with no pressure on timing.")]
    picked=[(ic,ti,de) for keys,ic,ti,de in POOL if any(k in tag for k in keys)]
    for g in GEN:
        if len(picked)>=4: break
        picked.append(g)
    picked=picked[:4]
    icons=dict(AUD_ICONS); icons["sofa"]=TSVC_ICONS.get("sofa") or AUD_ICONS["box"]
    cards="".join('<div class="sit-card"><span class="sit-ico">'+icons.get(ic,AUD_ICONS["home"])+'</span><h3 class="sit-name">'+ti+'</h3><p class="sit-desc">'+de+'</p></div>' for ic,ti,de in picked)
    return centered("bg-lightgrey","What "+tn+" Stores With Us","Whatever&rsquo;s behind your move, we&rsquo;ve got "+tn+" covered &mdash; fully managed, fully insured, from just &pound;15 a week.",SIT_CSS+'<div class="sit-panel">'+cards+'</div>')
def svc_situations(heading, lead, items):
    icons=dict(AUD_ICONS); icons["sofa"]=TSVC_ICONS.get("sofa") or AUD_ICONS["box"]
    cards="".join('<div class="sit-card"><span class="sit-ico">'+icons.get(ic,AUD_ICONS["home"])+'</span><h3 class="sit-name">'+ti+'</h3><p class="sit-desc">'+de+'</p></div>' for ic,ti,de in items)
    return centered("bg-white",heading,lead,SIT_CSS+'<div class="sit-panel">'+cards+'</div>')
def svc_whychoose(nav, points=None):
    usps=points or [("shield","Fully Insured &amp; Alarmed","Your belongings are sealed into their own wooden container in our 24/7 CCTV, alarmed indoor warehouse and stay fully insured throughout your stay."),
          ("family","Family-Run Since 2016","A LAPADA-accredited West Sussex family team that treats your belongings like our own &mdash; careful, personal and genuinely local."),
          ("tag","From &pound;15/week, No Deposit","Honest weekly pricing with no deposit and no hidden fees &mdash; you only pay for the container space you actually use."),
          ("truck","We Come to You","No unit to drive to: we bring the materials, pack, collect from your door and redeliver on 24 hours&rsquo; notice.")]
    cards="".join('<article class="uspx-card"><span class="uspx-num" aria-hidden="true">'+f'{i+1:02d}'+'</span><span class="uspx-ico">'+USP_ICONS[ic]+'</span><h3>'+ti+'</h3><p>'+de+'</p></article>' for i,(ic,ti,de) in enumerate(usps))
    return ('<section class="uspx relative w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border">'+USP_CSS+
            '<div class="container"><div class="uspx-head">'
            '<span class="uspx-eyebrow">Why choose Wolves</span>'
            '<h2 class="relative leading-tight">Why West Sussex Chooses Wolves for '+nav+'</h2>'
            '<p class="uspx-lead">Local, managed and genuinely cared for &mdash; the Wolves Storage Sussex difference.</p>'
            '</div><div class="uspx-grid">'+cards+'</div></div></section>')
def service_schema(file,nav):
    return ('<script type="application/ld+json">'+json.dumps({
        "@context":"https://schema.org","@type":"Service","serviceType":nav,
        "name":nav+" in West Sussex",
        "description":"Fully managed "+nav.lower()+" across West Sussex from Wolves Storage Sussex &mdash; collected from your door, sealed into your own wooden container, securely stored and redelivered.",
        "provider":{"@type":["SelfStorage","MovingCompany"],"name":"Wolves Storage Sussex","telephone":"+441903893731","url":BASE,
            "image":BASE+"images/wolves-storage-logo@480.webp","address":ADDR_LD,
            "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"478","bestRating":"5"}},
        "areaServed":{"@type":"AdministrativeArea","name":"West Sussex"},
        "url":BASE+file,
        "offers":{"@type":"Offer","price":"15","priceCurrency":"GBP","priceSpecification":{"@type":"UnitPriceSpecification","price":"15","priceCurrency":"GBP","referenceQuantity":{"@type":"QuantitativeValue","value":"1","unitText":"WEEK"}}}
    },ensure_ascii=False)+'</script>')
def _faq_key(q,tn):
    return ''.join(c for c in q.lower().replace(tn.lower(),'') if c.isalpha())
def _faq_dup(k,keys):
    for e in keys:
        if k==e: return True
        if len(k)>14 and len(e)>14 and (k.startswith(e) or e.startswith(k)): return True  # "...cost?" vs "...cost in town?"
    return False
def merged_faqs(t):
    tn=t["town"]; out=list(t.get("faqs",[])); have=[_faq_key(q,tn) for q,_ in out]
    std=[("How much does storage cost in "+tn+"?","From just &pound;15 per week per container, with no deposit and no hidden fees &mdash; collection and redelivery across "+tn+" are included, and your free quote is confirmed within 24 hours."),
         ("Do you have self-storage units in "+tn+"?","We&rsquo;re a smarter alternative to a self-storage unit in "+tn+" &mdash; there&rsquo;s no unit to drive to and no lifting to do. We bring the materials, pack and wrap your belongings, seal them into your own wooden container and store them in our alarmed Ashington warehouse, then redeliver to your "+tn+" door whenever you ask. It&rsquo;s usually more secure and better value than a self-access unit once van hire, fuel and your own time are counted."),
         ("How big is a storage container?","Each private wooden container is 250 cu ft (5ft &times; 7ft &times; 8.6ft) &mdash; about the contents of a one-bedroom flat. Need more space? We simply use additional containers, so you only pay for what you use."),
         ("How quickly can you collect in "+tn+"?","Often within a few days &mdash; tell us your timescale on your free quote, and we redeliver on just 24 hours&rsquo; notice."),
         ("Are my belongings insured?","Yes &mdash; everything is kept in a sealed container in our alarmed, 24/7 CCTV indoor warehouse and is fully insured throughout, with optional extended cover for higher-value items.")]
    for q,a in std:
        if len(out)>=8: break
        k=_faq_key(q,tn)
        if not _faq_dup(k,have): out.append((q,a)); have.append(k)
    return out

# Rotating photo pool for the three split sections on every area (town) page.
# Mixes the new 2026 inventory shots with strong existing warehouse/container
# images so each town shows a varied, fresh, on-brand set. alt is generated with
# the town name for natural local-SEO relevance.
AREA_POOL=[
 ("wolves-operator-forklift-storage-containers.webp","An operator moving sealed wooden storage containers by forklift inside our secure West Sussex warehouse"),
 ("wolves-van-loading-at-storage-facility.webp","A Wolves Storage Sussex Luton van loading at our secure storage facility"),
 ("furniture-loaded-sussex-removal-service.webp","Wolves Storage vans collecting furniture from a Sussex home for fully managed storage"),
 ("protecting-customer-belongings-house-move.webp","The Wolves team carefully carrying a wrapped box out to the van for storage"),
 ("careful-packing-sussex-home-removal.webp","The Wolves Storage Sussex van fleet ready to collect and store across West Sussex"),
 ("packing-books-into-moving-boxes.webp","A Wolves team member labelling a carefully packed box of books"),
 ("packing-small-item-into-box.webp","Wrapping a small item in protective paper before it goes into storage"),
 ("taping-furni-soft-around-furniture.webp","Wrapping furniture in Furni-soft padding before sealing it into a storage container"),
 ("wolves-luton-storage-packing-van.webp","A branded Wolves Storage Sussex Luton van used for door-to-door collection and storage"),
 ("wolves-removals-team-fleet-vans.webp","The family-run Wolves Storage Sussex team in front of the van fleet"),
 ("wolves-team-loading-luton-van-collection.webp","A Wolves Storage Sussex team member loading the Luton van during a door-to-door collection"),
 ("team-carrying-wrapped-armchair-to-van.webp","Two Wolves Storage Sussex movers carrying a blanket-wrapped armchair to the van"),
 ("team-positioning-wooden-storage-container.webp","Wolves Storage Sussex movers positioning a sealed wooden storage container"),
 ("carrying-wooden-storage-container-outdoors.webp","Two Wolves Storage Sussex movers carrying a wooden storage container to the van"),
 ("loading-packed-boxes-into-removal-van.webp","A Wolves Storage Sussex team member loading packed boxes into the van for storage"),
 ("loading-box-up-ramp-into-van.webp","Wolves Storage Sussex movers loading a packed box up the ramp into the van"),
 ("carrying-furniture-past-storage-van.webp","A Wolves Storage Sussex mover carrying furniture past the branded van at a customer&rsquo;s home"),
 ("wrapping-fragile-item-protective-paper.webp","A Wolves Storage Sussex packer wrapping a fragile item in protective paper"),
 ("furniture-wrapped-furni-soft-dining-set.webp","A dining table and chairs protected in Furni-soft wrapping ready for storage"),
 ("wrapping-chair-protective-blanket-container.webp","A Wolves Storage Sussex mover wrapping a chair in a protective blanket inside a storage container"),
 ("wrapping-marble-table-furni-guard.webp","A Wolves Storage Sussex packer protecting a marble-topped table with Furni-guard"),
 ("wrapping-framed-picture-furni-soft.webp","A Wolves Storage Sussex packer wrapping a framed picture in Furni-soft padding"),
 ("taping-furni-guard-around-furniture-lounge.webp","A Wolves Storage Sussex packer taping Furni-guard protection around furniture"),
 ("white-glove-antique-painting-handling.webp","Wolves Storage Sussex team handling an antique painting with white gloves &mdash; LAPADA-accredited care"),
 ("hero-containers-van.webp","Sealed wooden storage containers loaded ready for our secure warehouse"),
 ("hero-forklift.webp","A forklift stacking sealed storage containers in the Wolves Storage Sussex warehouse"),
 ("gallery-warehouse-a.webp","Long-term storage containers stacked inside the secure Wolves Storage Sussex warehouse"),
 ("gallery-warehouse-b.webp","Inside the dry, alarmed Wolves Storage Sussex container warehouse"),
 ("hero-packed-container.webp","A storage container neatly packed with blanket-wrapped furniture"),
 ("gallery-loading.webp","Loading wrapped belongings into a sealed wooden storage container"),
]
def area_imgs(t):
    base=sum(ord(c) for c in t["slug"]); n=len(AREA_POOL); tn=t["town"]
    return [(IMG(fn), f"{alt} &mdash; Wolves Storage Sussex serving {tn}")
            for fn,alt in (AREA_POOL[(base+k)%n] for k in range(3))]

def town_local(t, data):
    h2, body = data
    return ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="max-w-4xl mx-auto">'
            '<span class="block text-orange font-bold uppercase tracking-wider text-sm mb-2">Storage in '+t["town"]+'</span>'
            '<h2 class="leading-tight text-black">'+h2+'</h2>'
            '<div class="mt-5 text-darkgrey text-lg">'+body+'</div></div></div></section>')

def town(t):
    h1="Storage in "+t["town"]+", "+t.get("region","West Sussex")
    ai=area_imgs(t); th=town_hero(t)
    expand = (EXPAND_TOWNS == "ALL") or (t["slug"] in EXPAND_TOWNS)
    fq = merged_faqs(t) if expand else t["faqs"]
    secs=[
        hero(th[0],th[1],h1,t["sub"],t["checks"],big=False),
        town_stats(t["town"]),
        split("bg-white",t["s1_h2"],t["s1"],ai[0][0],ai[0][1]),
        town_services(t),
        split("bg-white",t["s2_h2"],t["s2"],ai[1][0],ai[1][1],reverse=True),
    ]
    if expand: secs.append(town_pricing(t))
    secs.append(town_usps(t))
    secs.append(split("bg-white",t["s3_h2"],t["s3"],ai[2][0],ai[2][1]))
    if t["slug"] in TOWN_LOCAL: secs.append(town_local(t, TOWN_LOCAL[t["slug"]]))
    if t.get("extra"): secs.append(t["extra"])
    elif expand: secs.append(town_situations(t))
    areas = town_areas(t) if expand else town_nearby(t)
    secs+=[process(),town_map(t),areas,faq(fq),cta_band(t["cta"],IMG("gallery-warehouse-b.webp"))]
    pc1=re.split(r'&ndash;|&amp;|,|–',TOWN_INFO.get(t["slug"],{}).get("pc",""))[0].strip()
    ttitle=f'Storage in {t["town"]}'+(f' ({pc1})' if pc1 else '')+' | From &pound;15/wk, We Collect'
    gd={}
    if t.get("lat") and t.get("lng"):
        gd=dict(geo_pos=f'{t["lat"]};{t["lng"]}', geo_place=f'{t["town"]}, {t.get("region","West Sussex")}')
    return dict(file=t["slug"]+".html",slug="town",nav="Storage in "+t["town"],
        title=ttitle,meta=t["meta"],hero=th[0],faqs=fq,
        crumb_parent=("areas-we-cover.html","Areas We Cover"),extra_schema=town_service_schema(t),
        sections=secs,**gd)

TOWN_LOCAL = {
 "storage-ashington": ("What Ashington Households &amp; Businesses Store With Us",
  '<p>Living a few minutes from our warehouse has real advantages for Ashington residents. Period cottages along the old London Road and the newer closes off the A24 all face the same squeeze for space, and being on the doorstep means we can usually collect within the same week and have your belongings back the very next day. We store for families renovating older village homes, downsizers clearing a lifetime of belongings, and tradespeople along the A24 corridor who need a secure home for tools and stock between jobs.</p>'
  '<p>Because everything is sealed into your own wooden container and logged in our alarmed warehouse, it makes no difference whether you&rsquo;re putting away a few boxes of garden furniture for winter or the entire contents of a house between completion dates. Add <a href="short-term-storage.html">short-term</a> flexibility, <a href="business-storage.html">business storage</a> for local traders, and full insurance throughout, and you have storage that genuinely fits village life &mdash; all from just &pound;15 a week with no deposit.</p>'),
 "storage-billingshurst": ("Local Storage for Billingshurst &amp; the Stane Street Villages",
  '<p>Billingshurst grew up along Stane Street, the old Roman road that&rsquo;s now the A29, and that easy north&ndash;south link is exactly why our team can reach you so quickly. From the village centre and the railway station to the surrounding RH14 hamlets, we collect from your door and bring everything back on 24 hours&rsquo; notice &mdash; no battling the A29 to an out-of-town unit with a hired van.</p>'
  '<p>The mix of growing new-build estates and established family homes around Billingshurst means storage needs vary widely. We help families freeing up a room for a new arrival or a home office, sellers de-cluttering to show a property at its best, and commuters downsizing before a move. Landlords across the RH14 villages use us to turn rentals around quickly, while local businesses store stock and archives to free up working space.</p>'
  '<p>Whatever the reason, you get the same fully managed service: we pack, wrap and seal your belongings into their own container, store them in our dry, alarmed warehouse, and redeliver whenever you&rsquo;re ready &mdash; from just &pound;15 a week with no deposit. Not sure how much room you&rsquo;ll need? Our <a href="storage-size-guide.html">storage size guide</a> makes it easy to estimate.</p>'),
 "storage-bognor-regis": ("Seaside Storage for Bognor Regis Homes &amp; Holiday Lets",
  '<p>Bognor&rsquo;s mix of seafront flats, family homes and holiday lets gives storage a distinctly coastal rhythm. We help owners clearing out between guests and seasons, retirees downsizing from larger PO21 and PO22 properties, and families making room while they renovate close to the front. With salt air and space at a premium near the coast, keeping belongings in our dry, alarmed inland warehouse often makes far more sense than a damp garage or an over-stuffed spare room.</p>'
  '<p>As ever, it&rsquo;s fully managed: we collect from your Bognor address, seal everything into your own container, and redeliver on 24 hours&rsquo; notice, from &pound;15 a week with no deposit. Heading away for the season or letting your place out? <a href="long-term-storage.html">Long-term storage</a> keeps it all safe and fully insured until you&rsquo;re ready for it back.</p>'),
 "storage-brighton": ("City Storage for Brighton &amp; Hove Flats &amp; Students",
  '<p>Storage in Brighton and Hove comes with its own challenges: narrow streets around the Lanes and the Kemptown terraces, tight parking, and small city flats with nowhere to put anything spare. Our managed model is built for exactly that &mdash; we bring the van and the team, pack and load at your door, and take everything away to our secure warehouse, so you don&rsquo;t have to find storage space the city simply doesn&rsquo;t have.</p>'
  '<p>We&rsquo;re a popular choice with students moving between term-time lets across BN1 to BN3, professionals downsizing or moving in together, and anyone caught between flats. Store for a few summer weeks or the whole year on flexible, fully insured terms, from just &pound;15 a week &mdash; <a href="short-term-storage.html">short-term storage</a> is ideal for the student holidays, with collection and redelivery included.</p>'),
 "storage-east-grinstead": ("Storage Where Sussex Meets Surrey &amp; Kent",
  '<p>Perched in the High Weald where three counties meet, East Grinstead has one of the longest medieval high streets in England and a real mix of period timber-framed homes and newer RH19 estates. Older properties often mean awkward access and little storage space, which is where a fully managed service earns its keep &mdash; we handle the packing, the lifting and the logistics, and your belongings end up sealed and safe in our alarmed warehouse rather than crammed into a loft.</p>'
  '<p>Commuters moving for the London line, families renovating period homes, and businesses freeing up space all store with us here. Collection and redelivery are included, terms are flexible, and it all starts from just &pound;15 a week with no deposit &mdash; see exactly <a href="how-it-works.html">how it works</a> before you decide.</p>'),
 "storage-henfield": ("Village Storage for Henfield, Small Dole &amp; Woodmancote",
  '<p>Henfield has the feel of a proper Sussex village &mdash; a busy high street, a strong community, and homes that range from characterful cottages to newer family houses around the edges. What it doesn&rsquo;t always have is spare space, and that&rsquo;s where we come in. A short run down the A281 from our base, Henfield and its neighbours Small Dole and Woodmancote get our complete managed service, with collection from your door and redelivery on just 24 hours&rsquo; notice.</p>'
  '<p>We store for villagers moving within the area or further afield, families clearing rooms for renovation or a new arrival, and downsizers keeping the pieces that matter while they decide. Local businesses and tradespeople use us to keep stock, tools and seasonal equipment secure without paying for a permanent unit. Antiques and inherited furniture are handled with the same care &mdash; as a LAPADA-accredited team, that&rsquo;s exactly the sort of thing we&rsquo;re trusted with.</p>'
  '<p>Everything is sealed into your own wooden container and kept in our dry, alarmed, 24/7 CCTV warehouse, fully insured, from just &pound;15 a week with no deposit. Browse our full range of <a href="storage-solutions.html">storage solutions</a> to find the right fit for your move.</p>'),
 "storage-horsham": ("Storage Across Horsham, from the Carfax to Southwater",
  '<p>Horsham is the busiest town in our catchment, and our managed model suits it especially well. The town centre around the Carfax and the streets near Horsham Park are full of period and terraced homes with little storage to spare, while the growing communities at Broadbridge Heath, Southwater and Roffey bring a steady stream of families moving, extending and downsizing. Rather than hiring a van and driving your belongings to an industrial-estate unit, you let us come to you &mdash; we pack, wrap and seal everything into your own container at your door.</p>'
  '<p>That convenience matters in a town where parking and access can be tight and time is short. We collect from right across the RH12 and RH13 postcodes, store your container in our dry, alarmed warehouse, and redeliver on 24 hours&rsquo; notice whenever you&rsquo;re ready. It works for families bridging a delayed completion, sellers de-cluttering to show a home at its best, and anyone renovating one of Horsham&rsquo;s older properties.</p>'
  '<p>Horsham&rsquo;s thriving business community uses us too. With offices and trades spread between the town centre and the surrounding business parks, our <a href="business-storage.html">business storage</a> frees up expensive floor space for stock, archives and equipment, collected and redelivered to your premises so it never costs your team time. Households choosing between <a href="short-term-storage.html">short-term</a> and <a href="long-term-storage.html">long-term</a> storage get the same flexible, fully insured service throughout.</p>'
  '<p>It all starts from just &pound;15 a week with no deposit and no hidden fees. As a family-run, LAPADA-accredited and Checkatrade-verified team trusted by Horsham estate agents, we treat every collection as if it were our own &mdash; compare our honest <a href="pricing.html">storage prices</a> or get a free quote confirmed within 24 hours.</p>'),
 "storage-lancing": ("Coastal Storage Between Worthing &amp; Shoreham",
  '<p>Lancing sits on the coast between Worthing and Shoreham, with the landmark chapel of Lancing College watching over the Adur valley above the village. Homes here run from seafront and beach-green properties to the busy streets around North Lancing, and storage space is often in short supply close to the water. Keeping belongings in our dry, alarmed inland warehouse beats a damp garage or a cramped spare room, especially through a salty coastal winter.</p>'
  '<p>We collect from across the BN15 area, seal everything into your own container, and redeliver on 24 hours&rsquo; notice &mdash; ideal for families moving along the coast, downsizers, and anyone caught between homes. Store short or long term, fully insured, from just &pound;15 a week with no deposit. See what fits inside a container with our handy <a href="storage-size-guide.html">size guide</a>.</p>'),
 "storage-pulborough": ("Managed Storage for Pulborough &amp; the Arun Valley",
  '<p>Pulborough shares our own RH20 postcode, sitting just up the A283 and A29 where the River Arun winds through the Brooks. That makes it one of the quickest collections we do &mdash; we&rsquo;re practically neighbours, so a Pulborough pick-up often happens within days and your belongings can be back the very next day after a call. Its position on the main rail line also makes it popular with commuters, who frequently store with us when relocating for work.</p>'
  '<p>The town and its surrounding villages have a real mix of riverside cottages, period homes and newer houses, and storage needs vary just as widely. We help families moving along the Arun Valley, downsizers clearing larger homes, and people heading abroad or working away who need somewhere secure for months or years. The low-lying ground near the river makes a dry, alarmed warehouse particularly appealing &mdash; far better than risking damp in a garage or outbuilding.</p>'
  '<p>As always, it&rsquo;s fully managed: we bring the materials, pack and wrap your belongings, seal them into your own wooden container, and store them securely with 24/7 CCTV and full insurance, from just &pound;15 a week with no deposit. Choose <a href="long-term-storage.html">long-term storage</a> while you&rsquo;re away or <a href="short-term-storage.html">short-term</a> for a move, and we&rsquo;ll fit around your timescale. See every <a href="areas-we-cover.html">area we cover</a> nearby, or simply call and tell us what you need to store &mdash; we&rsquo;ll talk you through the options with no pressure and no obligation.</p>'),
 "storage-rustington": ("Seaside Village Storage for Rustington",
  '<p>Rustington is one of the leafier spots on the coast, a seaside village tucked between Littlehampton and Angmering with a strong community and a good number of retired residents. Downsizing is a common reason people store with us here &mdash; moving from a long-held family home into something smaller often means keeping treasured furniture and belongings safe while decisions are made, and that&rsquo;s exactly what managed storage is for.</p>'
  '<p>We collect from across the BN16 area, pack and seal everything into your own container, and keep it in our dry, alarmed warehouse with 24/7 CCTV and full insurance. Whether it&rsquo;s a few weeks during a move or longer-term storage for inherited or antique pieces &mdash; handled with LAPADA-accredited care &mdash; you only pay for the space you use, from just &pound;15 a week. We redeliver to your Rustington door on 24 hours&rsquo; notice, so your belongings are never more than a phone call away. Read more <a href="about.html">about our family business</a>.</p>'),
 "storage-steyning": ("Storage for Steyning, Bramber &amp; Upper Beeding",
  '<p>The historic market town of Steyning, with its timber-framed high street and its neighbours Bramber and Upper Beeding, sits in a beautiful but tightly-built corner beneath the South Downs. Many of the homes here are old, characterful and short on storage, and the narrow streets aren&rsquo;t always easy to manoeuvre a hired van around &mdash; which is precisely why a fully managed service makes sense. We bring everything to your door, do the packing and lifting, and take it all away to our secure warehouse a few minutes up the A283.</p>'
  '<p>We store for families renovating period properties, downsizers, people moving in or out of the area, and businesses along the high street needing room for stock or records. Antique and inherited furniture &mdash; common in Steyning&rsquo;s older homes &mdash; is wrapped and handled with the specialist care our LAPADA accreditation demands, so even the most delicate pieces are in safe hands.</p>'
  '<p>Everything is sealed into your own wooden container, logged, and stored in our dry, alarmed, 24/7 CCTV warehouse, fully insured, from just &pound;15 a week with no deposit. We redeliver on 24 hours&rsquo; notice across Steyning, Bramber and Upper Beeding &mdash; see exactly <a href="how-it-works.html">how it works</a>, then get a free, no-obligation quote confirmed within 24 hours.</p>'),
 "storage-storrington": ("Doorstep Storage for Storrington &amp; the Downs Villages",
  '<p>A short hop along the A283 from our Ashington warehouse, Storrington is firmly on our doorstep &mdash; and that closeness shows in how quickly we can help. This bustling village at the foot of the Downs, with Sullington and the surrounding hamlets, gets our fastest collections and next-day redeliveries, so storage never feels like a chore.</p>'
  '<p>Storrington&rsquo;s mix of period cottages, bungalows and family homes brings the full range of storage needs. We help downsizers and retirees freeing up space, families between moves or mid-renovation, and people clearing a relative&rsquo;s home after a bereavement &mdash; a job we handle with patience and no pressure on timing. Local businesses and tradespeople store stock, tools and seasonal equipment without committing to a permanent unit.</p>'
  '<p>Whatever the reason, the service is the same: we pack, wrap and seal your belongings into their own container, store them in our dry, alarmed warehouse, and bring them back on 24 hours&rsquo; notice, from just &pound;15 a week. Compare our honest <a href="pricing.html">storage prices</a> or get a free quote today.</p>'),
 "storage-washington": ("Storage Minutes From Your Door in Washington",
  '<p>Washington sits right beside our Ashington base at the foot of the South Downs, where the A24 meets the A283 and Chanctonbury Ring rises on the skyline. Being practically next door means we&rsquo;re about as local as storage gets &mdash; collections are quick, redeliveries take just 24 hours&rsquo; notice, and there&rsquo;s never any need to drive your belongings to an out-of-town unit.</p>'
  '<p>The village and its scattered Downland homes bring a steady mix of storage needs: families renovating older cottages, walkers and commuters downsizing, and people moving in or out of this sought-after corner of the Downs. We also help those clearing space for building work or holding furniture between homes, with antiques and valuables wrapped and handled with LAPADA-accredited care.</p>'
  '<p>Everything is packed at your door, sealed into your own wooden container, and stored in our dry, alarmed, 24/7 CCTV warehouse, fully insured and from just &pound;15 a week with no deposit. Whether you need <a href="short-term-storage.html">short-term storage</a> for a move or <a href="long-term-storage.html">long-term storage</a> while you&rsquo;re away, we&rsquo;ll fit neatly around your plans &mdash; just tell us your timescale and we&rsquo;ll handle the rest, from the first box we pack to the final redelivery.</p>'),
 "storage-worthing": ("Storage Across Worthing, from the Seafront to Durrington",
  '<p>Worthing is one of the largest towns we serve, and its sweep of streets from the seafront and pier back through the town centre to Broadwater, Tarring and Durrington brings a constant flow of storage needs. The town&rsquo;s many Victorian and Edwardian houses &mdash; often converted into flats &mdash; tend to be long on character and short on storage, while a strong retired community means downsizing is a regular reason people call us.</p>'
  '<p>Our managed model is ideal for a busy coastal town: we bring the van and the team, pack and load at your door anywhere across the BN11 to BN14 postcodes, and take everything away to our secure inland warehouse, well away from the salt air. That suits seafront flat-owners short on space, families moving or renovating, students between term-time lets, and landlords turning over rentals along the coast.</p>'
  '<p>Every job is fully managed and fully insured: belongings are wrapped, sealed into your own wooden container, and kept in our dry, alarmed, 24/7 CCTV facility, from just &pound;15 a week with no deposit. Store for a few weeks or several years on flexible terms, with collection and redelivery included &mdash; explore our full range of <a href="storage-solutions.html">storage solutions</a> or get a free quote confirmed within 24 hours. Wherever you are in Worthing, a member of our family team is ready to help you store with confidence.</p>'),
}

TOWNS = [
 dict(slug="storage-ashington",town="Ashington",lat="50.9270",lng="-0.4470",
  title="Storage in Ashington | Wolves Storage Sussex",
  meta="Managed container storage in Ashington, West Sussex from £15/week. We're based in the village — we pack, collect, store and redeliver.",
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
  meta="Secure managed storage in Washington, West Sussex from £15/week. Minutes from our Ashington base — we collect, store and redeliver.",
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
  meta="Secure managed storage in Pulborough, West Sussex from £15/week. On your doorstep (RH20) — we pack, collect, store and redeliver. Fully insured.",
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
  meta="Secure managed storage in Steyning, West Sussex from £15/week. We collect from your door, seal and store securely — fully insured, no deposit.",
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
  title="Storage in Billingshurst | Wolves Storage Sussex",
  meta="Managed container storage in Billingshurst (RH14) from £15/week. We pack, collect, store and redeliver — no deposit, fully insured.",
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
  meta="Managed storage in Horsham, West Sussex from £15/week. We collect across RH12 and RH13, store securely and redeliver — no deposit, fully insured.",
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
        checklist_grid([("home","Families moving home or caught in a chain delay"),("wrench","Homeowners renovating or extending"),("box","Downsizers and people clearing a property"),("key","Landlords and tenants between tenancies"),("briefcase","Businesses freeing up office or retail space"),("cap","Students and people working away from home")])),
  cta="Need Storage in Horsham? Get a Free Quote",
  faqs=[("Do you cover all of Horsham?","Yes &mdash; we collect, store and redeliver right across the RH12 and RH13 postcodes, including Roffey, Broadbridge Heath and Southwater."),
        ("Is this self-storage or managed storage?","Managed &mdash; you don&rsquo;t drive to a unit. We pack, collect and store your sealed container, then redeliver when you ask."),
        ("How much does storage cost in Horsham?","From &pound;15 per week per container, with no deposit and no hidden fees, including collection and redelivery."),
        ("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote, and we redeliver on 24 hours&rsquo; notice."),
        ("Are my belongings insured in Horsham?","Yes &mdash; sealed containers in an alarmed, 24/7 CCTV indoor warehouse, fully insured and LAPADA accredited.")]),
 dict(slug="storage-worthing",town="Worthing",lat="50.8180",lng="-0.3720",
  title="Storage in Worthing | Wolves Storage Sussex",
  meta="Managed storage in Worthing, West Sussex from £15/week. We collect across BN11–BN14 — ideal for moves, downsizing & students. No deposit.",
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
      title="How Much Storage Do I Need? | Wolves Storage Sussex",
      meta="How much storage do you need? Our West Sussex size guide shows what fits in a 250 cu ft container, room by room. From £15/week, no deposit.",
      hero=IMG(HERO_WAREHOUSE[0]),faqs=faqs,
      crumb_parent=("how-it-works.html","How It Works"),
      sections=[
        hero(IMG(HERO_WAREHOUSE[0]),HERO_WAREHOUSE[1],"How Much Storage Do I Need?",
          "Work out how much space your move needs in seconds. Our container size guide shows roughly what fits in each 250 cu ft container &mdash; and we&rsquo;ll confirm the exact figure free.",
          ["One container holds about a one-bed home","Pay only for the containers you use","From &pound;15/week, no deposit","Free space estimate within 24 hours"],big=False),
        centered("bg-lightgrey","Storage Size Guide by Home Size",None,inner1),
        split("bg-lightgrey","What Fits in One Container?",
          ["Each wooden container measures 5ft &times; 7ft &times; 8.6ft &mdash; around 250 cubic feet. That&rsquo;s comfortably the contents of a one-bedroom flat: a bed, sofa, a few appliances, a wardrobe and a stack of boxes.",
           "Bigger home? We just use more containers, sealed and stacked in our alarmed indoor warehouse, so you only ever pay for the space you actually fill. See our <a href=\"pricing.html\">prices</a> or <a href=\"storage-solutions.html\">storage solutions</a>."],
          IMG("hero-containers-van.webp"),"Wolves Storage Sussex 250 cubic foot wooden storage containers"),
        ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="max-w-4xl mx-auto">'
         '<span class="block text-orange font-bold uppercase tracking-wider text-sm mb-2">Room by room</span>'
         '<h2 class="leading-tight text-black">Estimating Your Storage, Room by Room</h2>'
         '<div class="mt-5 text-darkgrey text-lg">'
         '<p>The easiest way to picture how much storage you need is to think room by room. As a rule of thumb, one 250 cubic-foot container comfortably holds the contents of a single furnished room or a one-bedroom flat &mdash; so the more rooms you&rsquo;re clearing, the more containers you&rsquo;ll use. Below is a practical guide to help you estimate before we confirm the exact figure for free.</p>'
         '<h3 class="text-black font-bold text-xl mt-7 mb-2">Bedrooms and living spaces</h3>'
         '<p>A typical double bedroom &mdash; bed and mattress, wardrobe, chest of drawers, bedside tables and a few boxes of clothes &mdash; fills roughly half to two-thirds of a container. A living room with a three-seater sofa, an armchair, a TV unit, a coffee table and bookshelves usually takes up a similar amount, so a one-bedroom flat as a whole tends to settle neatly into a single container. A two-bedroom home generally needs two containers, and a three- or four-bedroom house two to three, depending on how much furniture and how many boxes are involved.</p>'
         '<h3 class="text-black font-bold text-xl mt-7 mb-2">Kitchens, appliances and white goods</h3>'
         '<p>Kitchens are mostly boxes &mdash; crockery, pans, small appliances and cupboard contents &mdash; which pack down efficiently, but large white goods take more room. A fridge-freezer, washing machine, tumble dryer or dishwasher each occupy a meaningful slice of a container, so if you&rsquo;re storing several appliances it&rsquo;s worth mentioning them when you ask for a quote. We wrap and protect appliances properly and stand them upright so nothing is damaged in storage.</p>'
         '<h3 class="text-black font-bold text-xl mt-7 mb-2">Gardens, garages and bulky items</h3>'
         '<p>Garages and sheds are where volume hides. Lawnmowers, bikes, tools, garden furniture, BBQs and DIY equipment add up quickly, and bulky one-off items &mdash; a piano, a wardrobe that won&rsquo;t dismantle, a large mirror or a set of golf clubs &mdash; are worth flagging early so we bring the right protection. Antiques, artwork and high-value pieces are handled with specialist care by our LAPADA-accredited team.</p>'
         '<h3 class="text-black font-bold text-xl mt-7 mb-2">Businesses, archives and stock</h3>'
         '<p>For businesses, storage usually comes down to pallets, archive boxes and stock. A standard archive box is small, so a single container holds a great many of them; bulkier stock, display units or office furniture will use more. Whether you&rsquo;re freeing up office space, holding seasonal stock or archiving paperwork, we&rsquo;ll help you work out the most cost-effective number of containers for your <a href="business-storage.html">business storage</a>.</p>'
         '<h3 class="text-black font-bold text-xl mt-7 mb-2">Let us do the maths</h3>'
         '<p>If all of that still feels like guesswork, don&rsquo;t worry &mdash; estimating volume is genuinely hard, and getting it wrong means paying for space you don&rsquo;t need. Use the calculator on this page for an instant guide, or simply tell us your home size or list your main items and we&rsquo;ll give you an accurate container count and a fixed <a href="pricing.html">price</a> within 24 hours. There&rsquo;s no obligation, and because it&rsquo;s all <a href="how-it-works.html">fully managed</a> we&rsquo;ll pack, collect and store everything for you, then redeliver across <a href="areas-we-cover.html">West Sussex</a> whenever you&rsquo;re ready.</p>'
         '</div></div></div></section>'),
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
          ("How long can I store furniture for?","As long as you like &mdash; flexible weekly and 4-week rolling terms suit both <a href=\"short-term-storage.html\">short</a> and <a href=\"long-term-storage.html\">long-term</a> furniture storage."),
          ("How big is a storage container?","Each wooden container is 250 cu ft (5ft &times; 7ft &times; 8.6ft) &mdash; about a one-bedroom flat&rsquo;s worth of furniture. Larger homes simply use additional containers."),
          ("Do you handle antiques and fragile pieces?","Yes &mdash; as a LAPADA-accredited team we give antique, fragile and high-value furniture specialist wrapping and white-glove handling."),
          ("Is this self-storage or managed storage?","Managed &mdash; there&rsquo;s no unit to drive to. We wrap, collect and seal your furniture into your own container, then redeliver when you&rsquo;re ready.")]
    return dict(file="furniture-storage.html",slug="furniture",nav="Furniture Storage",
      title="Furniture Storage West Sussex | Wolves Storage Sussex",
      meta="Furniture storage in West Sussex from £15/week. We blanket-wrap, collect & seal furniture in secure containers. Fully insured. Get a free quote.",
      hero=IMG(HERO_FURNITURE[0]),faqs=faqs,
      crumb_parent=("storage-solutions.html","Storage Solutions"),
      extra_schema=service_schema("furniture-storage.html","Furniture Storage"),
      sections=[
        hero(IMG(HERO_FURNITURE[0]),HERO_FURNITURE[1],"Furniture Storage in West Sussex",
          "Storing a sofa, a houseful or a few treasured pieces? We blanket-wrap your furniture, seal it into its own container and keep it clean, dry and secure &mdash; from just &pound;15 a week.",
          ["Blanket-wrapped &amp; padded by our team","Sealed in dry, alarmed containers","Fully insured, LAPADA accredited","From &pound;15/week, no deposit"],big=False),
        split("bg-white","Furniture Storage Done Properly",
          ["Furniture hates damp, dust and being shoved around an open unit. We wrap each piece in blankets and padding, then seal it into your own wooden container kept in our dry, ventilated, alarmed warehouse &mdash; so it comes back exactly as it left.",
           "It&rsquo;s fully managed: we collect from your door, do all the lifting, and redeliver on 24 hours&rsquo; notice. See <a href=\"how-it-works.html\">how it works</a> or our <a href=\"pricing.html\">prices</a>."],
          IMG("furniture-wrapped-furni-soft-dining-set.webp"),"A dining table and chairs blanket-wrapped in Furni-soft by Wolves Storage Sussex before storage"),
        town_pricing({"town":"West Sussex","slug":"furniture"},heading="Furniture Storage Prices in West Sussex",eyebrow="Furniture Storage from",quote="Get Your Furniture Quote",lead="Furniture storage in West Sussex from just &pound;15 a week &mdash; blanket-wrapped, sealed and fully insured, with no deposit. Store a single sofa or a whole home.",fits=["A sofa, armchairs &amp; a coffee table","A double bedroom suite &amp; mattress","A dining table &amp; six chairs","The furniture from a one-bed flat"]),
        split("bg-lightgrey","Ideal for Moves, Renovations &amp; Downsizing",
          ["Furniture storage is perfect between house moves, during a renovation, while staging a home for sale, or when downsizing and deciding what to keep. Store a single sofa or an entire home &mdash; you only pay for the containers you use.",
           "As a LAPADA-accredited team we also handle fine and antique furniture with specialist care. Not sure how much space you need? Try our <a href=\"storage-size-guide.html\">size guide</a>."],
          IMG("wrapping-framed-picture-furni-soft.webp"),"A Wolves Storage Sussex packer wrapping a framed picture in Furni-soft padding before storage",reverse=True),
        svc_situations("When Furniture Storage Helps","Whatever&rsquo;s behind your move, our fully managed furniture storage is built for it &mdash; wrapped, sealed and fully insured, from just &pound;15 a week.",[("home","Between homes","Store a sofa or a whole houseful between moves &mdash; blanket-wrapped, sealed and brought back when you&rsquo;re in."),("wrench","Renovating &amp; redecorating","Protect furniture from dust and damage while the work&rsquo;s done, then have it all returned."),("box","Downsizing","Keep the pieces you&rsquo;re not ready to part with, safely stored until you decide."),("sofa","Antiques &amp; fine pieces","LAPADA-accredited care for antique, fragile and high-value furniture &mdash; wrapped and handled properly.")]),
        svc_whychoose("Furniture Storage",[("shield","Blanket-Wrapped &amp; Sealed","Every piece is wrapped and padded, then sealed into your own container in a dry, alarmed warehouse &mdash; no scuffs, no damp."),("family","LAPADA-Accredited Care","Trusted to handle fine, antique and fragile furniture &mdash; a family team rated 5.0 from 478 reviews."),("truck","We Collect &amp; Redeliver","We bring the materials, do all the lifting and wrapping, and redeliver on 24 hours&rsquo; notice."),("tag","From &pound;15/week, No Deposit","Store a single sofa or a whole home &mdash; pay only for the container space you use, with no hidden fees.")]),
        process(),
        gallery([(IMG("wrapping-chair-protective-blanket-container.webp"),"A Wolves Storage Sussex packer wrapping a chair in a protective blanket for container storage","Wrapped ready for storage"),
                 (IMG("taping-furni-guard-around-furniture-lounge.webp"),"A Wolves Storage Sussex packer taping Furni-guard protection around furniture","Padded &amp; protected"),
                 (IMG("wrapping-marble-table-furni-guard.webp"),"A Wolves Storage Sussex packer protecting a marble-topped table with Furni-guard","Fragile pieces, handled properly"),
                 (IMG("team-carrying-wrapped-armchair-to-van.webp"),"Two Wolves Storage Sussex movers carrying a blanket-wrapped armchair to the van","Collected from your door"),
                 (IMG("wrapping-fragile-item-protective-paper.webp"),"A Wolves Storage Sussex packer wrapping a fragile item in protective paper before storage","Fragile items protected"),
                 (IMG("white-glove-antique-painting-handling.webp"),"Wolves Storage Sussex team handling an antique painting with white gloves","Specialist antique handling")],
                heading="Furniture Storage in Action",lead="Real photos of our team wrapping, protecting and storing furniture across West Sussex."),
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
    return dict(file=file,slug="legal",nav=nav,title=title,meta=meta,hero=IMG(HERO_WAREHOUSE[0]),sections=[header,content])

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
    # Attach the review array to the single site-wide #business entity (declared in ORG)
    # via an @id reference only — no duplicate @type/url/aggregateRating (rule 18).
    rs=('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org",
        "@id":BASE+"#business",
        "review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5","worstRating":"1"},"reviewBody":html.unescape(r)} for n,r in REVIEWS]},ensure_ascii=False)+'</script>')
    return dict(file="reviews.html",slug="reviews",nav="Reviews",
        title="Reviews | 5.0 Stars from 478 | Wolves Storage Sussex",
        meta="Read Wolves Storage Sussex reviews — rated 5.0 from 478 verified reviews on Google, Checkatrade & Facebook. Family-run & fully insured.",
        hero=IMG(HERO_ANTIQUE[0]),extra_schema=rs,
        sections=[
          hero(IMG(HERO_ANTIQUE[0]),HERO_ANTIQUE[1],"Our Storage Customers Rate Us 5.0",
            "Don&rsquo;t just take our word for it &mdash; here&rsquo;s what West Sussex families and businesses say about storing with our family team.",
            ["5.0 stars from 478 reviews","Verified on Google, Checkatrade &amp; Facebook","LAPADA accredited &amp; fully insured","Trusted by West Sussex estate agents"],big=False),
          centered("bg-white","What Our Customers Say","Genuine, verified reviews from the families and businesses we&rsquo;ve helped across West Sussex.",review_cards()),
          ('<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="max-w-4xl mx-auto">'
           '<span class="block text-orange font-bold uppercase tracking-wider text-sm mb-2">5.0 from 478 reviews</span>'
           '<h2 class="leading-tight text-black">A Reputation Built on Word of Mouth</h2>'
           '<div class="mt-5 text-darkgrey text-lg">'
           '<p>Storage is a business built entirely on trust &mdash; you&rsquo;re handing over the things that matter most and trusting someone to look after them properly. That&rsquo;s why we&rsquo;re proud that so much of our work comes from personal recommendations and repeat customers, and why we&rsquo;ve earned a 5.0-star rating across hundreds of verified reviews on Google, Checkatrade and Facebook. Every one of those reviews comes from a real West Sussex household or business we&rsquo;ve actually helped store, move or downsize.</p>'
           '<h3 class="text-black font-bold text-xl mt-7 mb-2">What customers tell us matters most</h3>'
           '<p>Read through our feedback and the same themes come up again and again: belongings returned in exactly the condition they left in, a friendly team that turns up when they say they will, clear and honest pricing with no surprises, and the reassurance of dealing with the same people from the first quote to the final redelivery. Because we&rsquo;re a small, family-run team rather than a faceless national chain, those details don&rsquo;t slip through the cracks.</p>'
           '<h3 class="text-black font-bold text-xl mt-7 mb-2">Independently verified, not cherry-picked</h3>'
           '<p>Our reviews are collected and verified through Trustindex, which gathers genuine, spam-checked feedback from multiple platforms in one place &mdash; so what you see is the real picture, not a hand-picked selection. We&rsquo;re also LAPADA-accredited, Checkatrade-verified and fully insured, and we&rsquo;re recommended by respected estate agents across the region.</p>'
           '<h3 class="text-black font-bold text-xl mt-7 mb-2">Trusted right across West Sussex</h3>'
           '<p>From <a href="storage-horsham.html">Horsham</a> and <a href="storage-crawley.html">Crawley</a> to the <a href="storage-worthing.html">Worthing</a> and <a href="storage-chichester.html">Chichester</a> coast, families and businesses across the county have chosen us for storage they don&rsquo;t have to worry about. Wherever you are, you can expect the same standard of care that earned those five-star reviews &mdash; see every <a href="areas-we-cover.html">area we cover</a>.</p>'
           '<h3 class="text-black font-bold text-xl mt-7 mb-2">See for yourself, then store with confidence</h3>'
           '<p>The best way to judge a storage company is by what its customers say once the job is done. Browse the reviews on this page, take a look inside our facility in the <a href="gallery.html">gallery</a>, or read more <a href="about.html">about our family business</a> and exactly <a href="how-it-works.html">how managed storage works</a>. When you&rsquo;re ready, <a href="contact.html">get a free quote</a> &mdash; and we&rsquo;ll do everything we can to earn a five-star review of our own.</p>'
           '<h3 class="text-black font-bold text-xl mt-7 mb-2">New to storage? You&rsquo;re in good hands</h3>'
           '<p>If you&rsquo;ve never used storage before, the reviews are the best place to start &mdash; they&rsquo;re written by people who were once in exactly your position, unsure how much space they&rsquo;d need or how the whole process worked. Time and again they mention how easy we made it: a clear quote up front, a team that did the heavy lifting, and belongings that came back exactly as they left. Many of those customers found us through a friend&rsquo;s or estate agent&rsquo;s recommendation, and a good number have stored with us more than once. We&rsquo;d love the chance to add you to them.</p>'
           '</div></div></div></section>'),
          cta_band("Join Hundreds of Happy West Sussex Customers",IMG("gallery-warehouse-b.webp")),
        ])

# Location silo: link the homepage and every service/money page down to ALL town pages.
SILO_PAGES={"index.html","storage-solutions.html","long-term-storage.html","short-term-storage.html",
            "business-storage.html","furniture-storage.html","how-it-works.html","pricing.html","storage-size-guide.html"}
LTS_CSS=('<style>'
  '.lts-panel{position:relative;overflow:hidden;max-width:74rem;margin:0 auto;border-radius:1.5rem;padding:1.6rem 1.4rem;background:linear-gradient(155deg,#edece4 0%,#e3e0d2 100%);border:1px solid #dcd8c8;box-shadow:0 26px 64px -34px rgba(38,38,38,.4)}'
  '@media(min-width:768px){.lts-panel{padding:2rem 2rem}}'
  '.lts-panel::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#F6BB06,#FC9700)}'
  '.lts-grid{display:grid;grid-template-columns:1fr;gap:1rem;text-align:left}'
  '@media(min-width:640px){.lts-grid{grid-template-columns:1fr 1fr}}'
  '@media(min-width:1024px){.lts-grid{grid-template-columns:repeat(3,1fr);gap:1.25rem}}'
  '.lts-group{background:#fff;border:1px solid #E7E7E7;border-radius:1.1rem;padding:1.35rem 1.3rem 1.05rem;box-shadow:0 3px 10px rgba(38,38,38,.05);transition:transform .3s cubic-bezier(.2,.7,.3,1),box-shadow .3s ease}'
  '.lts-group:hover{transform:translateY(-3px);box-shadow:0 18px 36px -18px rgba(105,119,131,.45)}'
  '.lts-ghead{display:flex;align-items:center;gap:.6rem;margin:0 0 .85rem;padding-bottom:.8rem;border-bottom:1px solid #EDEBE3}'
  '.lts-gtile{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:.6rem;background:#E8E6DA;color:#697783;flex:none}'
  '.lts-gtile svg{width:16px;height:16px}'
  '.lts-glabel{color:#FC9700;font-weight:700;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;line-height:1.2}'
  '.lts-links{list-style:none;margin:0;padding:0}'
  '.lts-link{display:flex;align-items:center;gap:.55rem;color:#262626;font-weight:600;font-size:.95rem;text-decoration:none;padding:.4rem .5rem;border-radius:.5rem;transition:background .2s ease,color .2s ease}'
  '.lts-link:hover{background:#F9F8F6;color:#FC9700}'
  '.lts-link:focus-visible{outline:2px solid #FC9700;outline-offset:2px}'
  '.lts-dot{width:6px;height:6px;border-radius:999px;background:#FC9700;opacity:.45;flex:none;transition:opacity .2s ease}'
  '.lts-link:hover .lts-dot{opacity:1}'
  '.lts-ar{margin-left:auto;color:#FC9700;opacity:0;transform:translateX(-4px);transition:opacity .2s ease,transform .2s ease}'
  '.lts-link:hover .lts-ar{opacity:1;transform:none}.lts-ar svg{width:14px;height:14px;display:block}'
  '@media (prefers-reduced-motion:reduce){.lts-group,.lts-link,.lts-dot,.lts-ar{transition:none}.lts-group:hover{transform:none}}'
  '</style>')
def all_towns_strip():
    pin='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.6"/></svg>'
    ar='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    groups={}
    for t in TOWNS:
        g=TOWN_INFO.get(t["slug"],{}).get("group","Across West Sussex")
        groups.setdefault(g,[]).append(t)
    cols=""
    for label,ts in groups.items():
        links="".join('<li><a class="lts-link" href="'+x["slug"]+'.html"><span class="lts-dot" aria-hidden="true"></span>Storage in '+x["town"]+'<span class="lts-ar" aria-hidden="true">'+ar+'</span></a></li>' for x in ts)
        cols+='<div class="lts-group"><div class="lts-ghead"><span class="lts-gtile">'+pin+'</span><span class="lts-glabel">'+label+'</span></div><ul class="lts-links">'+links+'</ul></div>'
    return centered("bg-white","Local Storage Across Sussex",
        "Dedicated local pages for the towns and villages we cover right across West Sussex and just over the border &mdash; find yours.",
        LTS_CSS+'<div class="lts-panel"><div class="lts-grid">'+cols+'</div></div>')

def build():
    P=[]
    HOME_FAQS=[("How much does storage cost in West Sussex?","Managed storage starts from just &pound;15 per week with no deposit and no hidden fees, on flexible weekly and 4-week terms. Your free quote is confirmed within 24 hours."),
               ("How is my furniture stored?","Items are professionally packed and sealed into your own wooden container, kept clean, dry and secure in our alarmed, 24/7 CCTV facility &mdash; not loose on open shelving."),
               ("Do I need to do anything?","No &mdash; our team brings the materials, packs and wraps your belongings, and loads everything into your container. You never lift a box."),
               ("How quickly can I access my items?","Just give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your door anywhere across West Sussex.")]
    # HOME
    P.append(dict(file="index.html",slug="home",nav="Home",
      title="Secure Storage in West Sussex | Wolves Storage Sussex",
      meta="Secure managed storage in West Sussex from £15/week. We pack, collect, store & redeliver. LAPADA accredited, fully insured, 24/7 CCTV.",
      hero=IMG(HERO_WAREHOUSE[0]),extra_schema=VIDEO_SCHEMA,faqs=HOME_FAQS,
      sections=[
        hero(IMG(HERO_WAREHOUSE[0]),HERO_WAREHOUSE[1],"Secure Storage in West Sussex",
          "Need somewhere safe to keep your belongings? Our clean, dry, ultra-secure <strong>containerised storage</strong> suits home and business, short or long-term &mdash; fully managed, including packing, collection and delivery.",
          ["Cost-effective long- and short-term storage","Packing, collection &amp; delivery included","Fully secure, alarmed &amp; insured","Family-run, LAPADA accredited"]),
        split("bg-white","Storage That Flexes Around Your Move",
          ["Whether you&rsquo;re between properties, downsizing, renovating or freeing up space, our containerised storage keeps your belongings safe and accessible. Items are professionally packed and sealed into containers, protected from damp and damage.",
           'Choose <a href="short-term-storage.html">short-term</a> for moving delays, <a href="long-term-storage.html">long-term</a> for extended needs, or <a href="business-storage.html">business storage</a> for stock and equipment &mdash; from just &pound;15 a week.'],
          IMG("hero-containers-van.webp"),"Storage containers and van at the Wolves Storage Sussex facility"),
        split("bg-lightgrey","More Than Storage &mdash; We Look After Your Home",
          ["We don&rsquo;t just store boxes &mdash; we look after your home. Our trained, fully insured family team treats every item as if it were our own, from professional packing to careful stacking in our secure West Sussex facility.",
           "LAPADA accredited and Checkatrade members, with 24/7 CCTV, an alarmed store and full insurance &mdash; trusted by Sussex families and businesses for over 10 years."],
          IMG("forklift-loading-storage-container-sussex.webp"),"Wolves Storage Sussex operator loading a sealed wooden storage container with a CAT forklift at our secure West Sussex facility",reverse=True),
        ('<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border"><div class="container"><div class="max-w-4xl mx-auto">'
         '<span class="block text-orange font-bold uppercase tracking-wider text-sm mb-2">Secure storage in West Sussex</span>'
         '<h2 class="leading-tight text-black">Storage in West Sussex, Without the Hassle</h2>'
         '<div class="mt-5 text-darkgrey text-lg">'
         '<p>When you need extra space in West Sussex you really have two choices: rent an empty self-storage unit and do all the lifting yourself, or let a managed team handle the lot. We&rsquo;re firmly in the second camp. From our base in <a href="storage-ashington.html">Ashington</a> we bring the boxes and materials to your door, pack and wrap your belongings, seal them into your own wooden container and store them in our dry, alarmed, 24/7 CCTV warehouse &mdash; then bring everything back whenever you&rsquo;re ready. There&rsquo;s no van to hire, no mileage and no heavy lifting.</p>'
         '<p class="mt-4">It&rsquo;s a flexible, fully insured service that suits almost any situation &mdash; <a href="short-term-storage.html">short-term storage</a> for a delayed move or renovation, <a href="long-term-storage.html">long-term storage</a> while you&rsquo;re working away, <a href="business-storage.html">business storage</a> for stock and archives, or specialist <a href="furniture-storage.html">furniture storage</a> for the pieces that matter most. You only pay for the container space you use, from just &pound;15 a week with no deposit, and you can store for a single week or several years on simple rolling terms.</p>'
         '<p class="mt-4">Being local and family-run is the whole point: we&rsquo;ve looked after West Sussex households and businesses for over ten years, we&rsquo;re LAPADA-accredited and Checkatrade-verified, and we&rsquo;re trusted by estate agents right across the county. Not sure how much space you&rsquo;ll need? Try our <a href="storage-size-guide.html">size guide</a>, compare our honest <a href="pricing.html">prices</a>, or <a href="contact.html">get a free quote</a> confirmed within 24 hours &mdash; with no deposit and no obligation, whatever you decide. Wherever you are in the county, from the coast to the Downs, we collect from and redeliver to your door across <a href="areas-we-cover.html">every town we cover in West Sussex</a>.</p>'
         '</div></div></div></section>'),
        process(),
        video_promo(),
        gallery([(IMG("wolves-operator-forklift-storage-containers.webp"),"Operator moving sealed storage containers by forklift"),(IMG("gallery-warehouse-a.webp"),"Stacked storage containers"),
                 (IMG("wolves-van-loading-at-storage-facility.webp"),"Van loading at our storage facility"),(IMG("furniture-loaded-sussex-removal-service.webp"),"Collecting furniture from a Sussex home for storage"),
                 (IMG("careful-packing-sussex-home-removal.webp"),"The Wolves Storage Sussex van fleet"),(IMG("wolves-removals-team-fleet-vans.webp"),"The family-run Wolves Storage Sussex team")]),
        faq(HOME_FAQS),
        cta_band("Ready to Store With West Sussex&rsquo;s Trusted Family Team?",IMG("gallery-warehouse-b.webp")),
      ]))
    # generic builder for service pages
    def service(file,slug,nav,title,meta,heroimg,heroalt,h1,sub,checks,p1,p2,faqs,uses=None,why=None,uses_lead=None,fits=None):
        exp = file in EXPAND_SERVICES
        secs=[hero(heroimg,heroalt,h1,sub,checks,big=False),
              split("bg-white",p1[0],p1[1],IMG("hero-team-loading.webp"),"Wolves team loading a storage container")]
        if exp: secs.append(town_pricing({"town":"West Sussex","slug":slug},heading=nav+" Prices in West Sussex",eyebrow=nav+" from",quote="Get Your "+nav+" Quote",lead=nav+" in West Sussex from just &pound;15 a week &mdash; everything included, no deposit, and you only pay for the container space you use. Need more room? We simply add another container.",fits=fits))
        secs.append(split("bg-lightgrey",p2[0],p2[1],IMG("hero-containers-van.webp"),"Storage containers at our facility",reverse=True))
        if exp and uses: secs.append(svc_situations("When "+nav+" Helps",uses_lead or ("The situations our fully managed "+nav.lower()+" is built for &mdash; fully insured, from just &pound;15 a week."),uses))
        if exp: secs.append(svc_whychoose(nav,why))
        secs += [process(),
            gallery([(IMG("hero-facility-van.webp"),"Facility and van"),(IMG("gallery-warehouse-a.webp"),"Storage containers"),
                     (IMG("gallery-loading.webp"),"Loading a container"),(IMG("hero-forklift.webp"),"Forklift stacking"),
                     (IMG("gallery-warehouse-b.webp"),"Warehouse interior"),(IMG("hero-fleet.webp"),"Van fleet")]),
            faq(faqs),
            cta_band("Need "+nav+" in West Sussex?",IMG("gallery-warehouse-b.webp"))]
        d=dict(file=file,slug=slug,nav=nav,title=title,meta=meta,hero=heroimg,faqs=faqs,sections=secs)
        if exp: d["extra_schema"]=service_schema(file,nav)
        return d
    P.append(service("storage-solutions.html","storage","Storage Solutions",
      "Managed Storage in West Sussex | Wolves Storage Sussex",
      "Secure, fully managed storage in West Sussex from £15/week. We pack, collect, store & redeliver. No deposit, fully insured. Get a free quote.",
      IMG(HERO_VAN_COLLECT[0]),HERO_VAN_COLLECT[1],"Secure, Fully Managed Storage in Sussex",
      "From a few boxes to a whole house, household to business, short stays to long-term &mdash; we tailor secure managed storage to exactly what you need, all from our alarmed Ashington facility.",
      ["Cost-effective long- and short-term storage","Packing, collection &amp; delivery included","Fully secure, alarmed &amp; insured","No deposit, flexible weekly terms"],
      ("How Containerised Storage Works",["Your goods are professionally wrapped and loaded into a private 250 cu ft wooden container (about a one-bedroom flat). Each container is sealed, logged and stacked inside our secure indoor store.","Because everything stays in its own sealed container, your belongings aren&rsquo;t handled again until they come back to you &mdash; cleaner and safer than a drive-up unit."]),
      ("Secure, Insured & Family-Run",["24/7 CCTV, an alarmed facility and full insurance keep your belongings protected, while our family team handles the packing, collection and redelivery.","LAPADA accredited and Checkatrade members, trusted across West Sussex for over a decade."]),
      [("How much does storage cost?","From &pound;15 per week with no deposit and no hidden fees, on flexible weekly and 4-week rolling terms."),
       ("How big is a container?","Each wooden container is 5ft &times; 7ft &times; 8.6ft &mdash; 250 cu ft, roughly the contents of a one-bedroom flat. Need more? We simply use additional containers."),
       ("Is my stuff insured?","Yes &mdash; the facility is fully insured with optional extended cover, monitored by 24/7 CCTV and alarmed."),
       ("How do I get my items back?","Give us 24 hours&rsquo; notice and we redeliver to your door anywhere in West Sussex."),
       ("Is this self-storage or managed storage?","Managed &mdash; there&rsquo;s no unit to drive to. We bring the materials, pack and seal your belongings into your own container and store it at our alarmed Ashington warehouse."),
       ("Do you pack and collect for me?","Yes &mdash; collection, professional packing and redelivery are all included. You never hire a van or lift a box."),
       ("How quickly can you collect?","Often within a few days &mdash; just tell us your timescale on your free quote."),
       ("What can I store?","Household contents, furniture, business stock, archives and more &mdash; anything that fits safely in a sealed container.")],
      uses_lead="From a few boxes to a whole home, household to business &mdash; these are the moves our fully managed storage is built for.",
      uses=[("home","Household storage","A whole home or a few rooms while you move, renovate or free up space &mdash; packed, sealed and stored, then brought back."),
            ("briefcase","Business storage","Stock, archives and equipment collected from your premises and redelivered the moment you need them."),
            ("sofa","Furniture &amp; antiques","Blanket-wrapped and sealed with LAPADA-accredited care &mdash; ideal for fine, fragile and high-value pieces."),
            ("cap","Students &amp; renters","Secure storage between tenancies or over the summer, collected from the door and brought back for term.")],
      why=[("shield","Sealed, Not Shelved","Your own private wooden container, sealed and logged in our alarmed, 24/7 CCTV warehouse &mdash; never loose on open shelving."),
           ("truck","Fully Managed, Door to Door","We bring the materials, pack, collect and redeliver &mdash; you never hire a van or lift a box."),
           ("tag","From &pound;15/week, No Deposit","Pay only for the container space you use, on flexible weekly and 4-week terms with no hidden fees."),
           ("family","Family-Run &amp; LAPADA Accredited","A local West Sussex family team, Checkatrade-verified and rated 5.0 from 478 reviews.")]))
    P.append(service("long-term-storage.html","longterm","Long-Term Storage",
      "Long-Term Storage West Sussex | Wolves Storage Sussex",
      "Affordable long-term storage in West Sussex from £15/week. Fully insured, 24/7 CCTV, no deposit — ideal for emigrating, renovations & downsizing.",
      IMG(HERO_AERIAL[0]),HERO_AERIAL[1],"Long-Term Storage in West Sussex",
      "Storing for months or years? Our containerised long-term storage keeps your belongings clean, dry and secure &mdash; with better value the longer you stay.",
      ["Better value the longer you store","Clean, dry, sealed containers","Fully insured &amp; 24/7 CCTV","No deposit, simple rolling terms"],
      ("Who Long-Term Storage Suits",["Perfect for working abroad, major renovations, downsizing or settling an estate. Your belongings stay sealed, clean and insured for as long as you need.","Store with total peace of mind and access whenever you need it &mdash; we redeliver the moment you&rsquo;re ready.","Because each container is sealed and logged on collection, your belongings aren&rsquo;t handled again until they come home &mdash; cleaner and far safer over months or years than a drive-up unit you keep visiting yourself."]),
      ("Clean, Dry & Secure for the Long Haul",["Everything is wrapped and sealed in its own wooden container inside our dry, alarmed indoor facility, so it stays protected for the long term.","The longer you store, the better the value &mdash; ask about long-term rates on your free quote.","We&rsquo;re LAPADA accredited and Checkatrade-verified, rated 5.0 from 478 reviews, with full insurance and 24/7 CCTV throughout &mdash; so your belongings are in genuinely trusted hands for the long haul. See exactly <a href=\"how-it-works.html\">how it works</a>."]),
      [("How much does long-term storage cost?","From &pound;15 per week with no deposit, and the longer you store the better the value &mdash; ask about long-term rates on your free quote."),
       ("Will my belongings stay in good condition?","Yes &mdash; sealed wooden containers in a dry, alarmed indoor facility keep everything clean and protected for years."),
       ("Can I access items during storage?","Absolutely &mdash; give us 24 hours&rsquo; notice and we&rsquo;ll redeliver what you need, then store the rest."),
       ("Is there a minimum term?","No long tie-ins &mdash; store for as long as you like on flexible weekly and 4-week rolling terms."),
       ("How big is a storage container?","Each private wooden container is 250 cu ft (5ft &times; 7ft &times; 8.6ft) &mdash; about the contents of a one-bedroom flat. Need more space? We simply use additional containers."),
       ("Do you collect and redeliver?","Yes &mdash; collection and redelivery across West Sussex are included. We bring the materials, pack, load and store; you never hire a van or lift a box."),
       ("Do I have to pack everything myself?","No &mdash; our team brings the materials and does the packing, wrapping and loading, so long-term items are sealed properly and stay protected."),
       ("Are my belongings insured the whole time?","Yes &mdash; everything is fully insured throughout your stay in an alarmed, 24/7 CCTV indoor warehouse, with optional extended cover for higher-value items.")],
      uses=[("briefcase","Working or living abroad","Store a whole home securely while you&rsquo;re overseas &mdash; sealed, insured and waiting, with redelivery the day you&rsquo;re back."),
            ("wrench","Major renovations","Clear the house for building work and keep furniture and boxes protected from dust and damage until the job&rsquo;s done."),
            ("box","Downsizing","Keep the pieces that matter while you decide, without cramming a smaller home &mdash; you only pay for the space you use."),
            ("key","Estate &amp; probate","A calm, fully insured place to hold a loved one&rsquo;s belongings for as long as you need, with no pressure on timing.")],
      uses_lead="Storing for months or years? These are the situations our fully managed long-term storage is built for &mdash; fully insured, from just &pound;15 a week.",
      why=[("tag","Better Value the Longer You Stay","Long stays cost less per week &mdash; ask about our long-term rates. Always no deposit and no hidden fees, however many months or years you store."),
           ("shield","Sealed &amp; Protected for Years","Your own wooden container is sealed and logged, then kept in a dry, alarmed, 24/7 CCTV warehouse &mdash; built to protect furniture and boxes for the long haul."),
           ("truck","Access Without the Hassle","Need something back mid-storage? Give us 24 hours&rsquo; notice and we redeliver it to your door, then keep the rest safe and sealed."),
           ("family","LAPADA-Accredited Family Team","Trusted to store whole homes, furniture and antiques long-term &mdash; family-run since 2016 and rated 5.0 from 478 reviews.")]))
    P.append(service("short-term-storage.html","shortterm","Short-Term Storage",
      "Short-Term Storage West Sussex | Wolves Storage Sussex",
      "Flexible short-term storage in West Sussex from £15/week. No deposit, weekly terms, fast collection — perfect for moves & chain delays.",
      IMG(HERO_LOADING[0]),HERO_LOADING[1],"Short-Term Storage in West Sussex",
      "Bridging a move, a broken chain or a quick renovation? Flexible weekly short-term storage with no deposit &mdash; we collect, store and bring it all back when you&rsquo;re ready.",
      ["Flexible weekly terms, no deposit","Fast collection &mdash; often within days","We pack, store and redeliver","Fully insured &amp; 24/7 CCTV"],
      ("Flexible Storage for Exactly As Long As You Need",["House move delayed? Staging your home for sale? Quick renovation? Short-term storage gives you flexible, secure space for exactly as long as you need.","You pay by the week and stop whenever you like, with collection and redelivery included."]),
      ("Quick, Flexible & Fully Managed",["Tell us your timescale and we&rsquo;ll fit around your move, often collecting within a few days.","Only pay for the time you actually need &mdash; no deposit, no long contracts."]),
      [("How short can I store for?","As little as a week &mdash; billed weekly with no deposit, so you only pay for the time you need."),
       ("How quickly can you collect?","Often within a few days. Tell us your timescale on your free quote."),
       ("What if my move date changes?","No problem &mdash; flexible rolling terms let you extend or end your storage whenever you need."),
       ("Do you deliver it back?","Yes &mdash; give us 24 hours&rsquo; notice and we redeliver to your new address across West Sussex."),
       ("How much does short-term storage cost?","From &pound;15 per week per container with no deposit and no hidden fees &mdash; collection and redelivery included."),
       ("Is there a deposit or minimum term?","No deposit and no long tie-in &mdash; store for a single week or a few months on flexible rolling terms."),
       ("How big is a storage container?","Each wooden container is 250 cu ft (5ft &times; 7ft &times; 8.6ft) &mdash; about a one-bedroom flat. Need more? We add containers."),
       ("Is my furniture protected for a short stay?","Yes &mdash; everything is wrapped, sealed and fully insured in our alarmed, 24/7 CCTV warehouse, even for just a few weeks.")],
      uses_lead="Bridging a move, a sale or a quick project? These are the situations our flexible short-term storage is built for.",
      uses=[("home","Chain delays &amp; moves","Bridge the gap when your move date slips &mdash; store everything safely and we redeliver the day you complete."),
            ("box","Selling &amp; staging","Declutter to show your home at its best, then store the overflow until you&rsquo;ve moved on."),
            ("wrench","Quick renovations","Clear a room or the whole house for the works, then have it all brought back when the dust settles."),
            ("key","Between tenancies","Somewhere secure for a few weeks between rentals, collected from your door and returned when you&rsquo;re ready.")],
      why=[("truck","Fast Collection","Often within a few days &mdash; we bring the materials, pack and collect, with no van for you to hire."),
           ("tag","Pay by the Week","Flexible weekly terms with no deposit &mdash; only pay for the time and the space you actually use."),
           ("shield","Sealed &amp; Insured, Even Short-Term","Your container is sealed and fully insured in our alarmed, 24/7 CCTV warehouse, even for a few weeks."),
           ("family","Local, Family-Run","A West Sussex family team that fits around your timescale, rated 5.0 from 478 reviews.")]))
    P.append(service("business-storage.html","business","Business Storage",
      "Business Storage West Sussex | Wolves Storage Sussex",
      "Secure business storage in West Sussex from £15/week — stock, archives & equipment. Fully insured, 24/7 CCTV, collection & redelivery.",
      IMG(HERO_PACKING[0]),HERO_PACKING[1],"Business Storage in West Sussex",
      "Free up your office or premises. We collect, store and redeliver stock, archives and equipment &mdash; fully insured and flexible, so you only pay for the space you need.",
      ["Scale up or down &mdash; no long lease","Stock, archives, equipment &amp; documents","Fully insured &amp; 24/7 CCTV","We collect and redeliver to you"],
      ("Storage That Works for Business",["Running out of space for stock, archives or equipment? Business storage frees up expensive premises while keeping everything secure, insured and easy to retrieve.","Ideal for retailers, ecommerce, tradespeople, offices and businesses relocating."]),
      ("Flexible, Secure & Collected for You",["We collect from and redeliver to your premises, saving your team time, and scale your storage up or down as your business changes.","Fully insured, alarmed and monitored by 24/7 CCTV."]),
      [("What can I store as a business?","Stock, ecommerce inventory, archives and documents, tools and equipment, seasonal items and more."),
       ("Can I scale storage as I grow?","Yes &mdash; we add or remove containers as your needs change, on flexible rolling terms with no long lease."),
       ("Can you collect and redeliver?","Absolutely &mdash; collection and redelivery are included, saving your team the hassle."),
       ("How much does it cost?","From &pound;15 per week per container with no deposit &mdash; tailored to your needs within 24 hours."),
       ("Is my business stock insured?","Yes &mdash; every container is sealed, logged and fully insured in an alarmed, 24/7 CCTV facility, with optional extended cover."),
       ("Can I access my stock during storage?","Yes &mdash; give us 24 hours&rsquo; notice and we redeliver what you need, then keep the rest sealed and secure."),
       ("Do you store documents and archives securely?","Yes &mdash; files and records are sealed into logged containers in our dry, ventilated warehouse, protected from damp and dust."),
       ("Is this self-storage or managed storage?","Managed &mdash; we collect from your premises, store your sealed containers off-site and redeliver when you ask. No unit for your team to drive to.")],
      uses_lead="Stock, archives, equipment or overflow &mdash; these are the situations our managed business storage is built for.",
      uses=[("box","Stock &amp; e-commerce","Store inventory and packaging off-site and scale up or down as orders change &mdash; collected and redelivered to you."),
            ("briefcase","Archives &amp; documents","Free up office space; keep files and records sealed, logged and protected from damp and dust."),
            ("wrench","Tools &amp; equipment","A secure home for trade tools, kit and machinery between jobs &mdash; alarmed and fully insured."),
            ("key","Relocation &amp; overflow","Clearing or relocating premises? Store the overflow securely and redeliver when your new space is ready.")],
      why=[("truck","Collected From Your Premises","We collect from and redeliver to your business, saving your team time and the cost of van hire."),
           ("tag","Scale Up or Down &mdash; From &pound;15/week","Add or remove containers as your business changes; no long lease, no deposit, pay for what you use."),
           ("shield","Logged, Alarmed &amp; Insured","Every container is logged and sealed in an alarmed, 24/7 CCTV warehouse, fully insured throughout."),
           ("family","Family-Run &amp; Trusted","A West Sussex family team trusted by local businesses, Checkatrade-verified and rated 5.0 from 478 reviews.")]))
    # HOW IT WORKS
    P.append(dict(file="how-it-works.html",slug="how",nav="How It Works",
      title="How Our Managed Storage Works | Wolves Storage Sussex",
      meta="How fully managed storage in West Sussex works: we quote, pack, collect, store in secure containers and redeliver. From £15/week, no deposit.",
      hero=IMG(HERO_LOADING[0]),faqs=[("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote."),("How do I access my belongings?","Give us 24 hours&rsquo; notice and we redeliver to your door across West Sussex."),("What&rsquo;s included?","Packing materials, professional packing, collection, secure container storage and redelivery.")],
      sections=[
        hero(IMG(HERO_LOADING[0]),HERO_LOADING[1],"How Our Managed Storage Works",
          "Fully managed means you never hire a van or lift a box. We quote, pack, collect, store and redeliver &mdash; here&rsquo;s exactly how.",
          ["We bring the materials &amp; pack for you","Collection &amp; redelivery included","Sealed, individually logged containers","From &pound;15/week, no deposit"],big=False),
        process(),
        split("bg-white","What&rsquo;s Included",["Every managed storage job includes professional packing materials, careful wrapping, collection from your door, a sealed private container in our alarmed store, and redelivery when you&rsquo;re ready.","Optional extras include extended insurance cover and help unpacking."],IMG("hero-containers-van.webp"),"Storage containers at our facility"),
        split("bg-lightgrey","The Container Explained",["Each wooden container measures 5ft &times; 7ft &times; 8.6ft &mdash; 250 cu ft, roughly the contents of a one-bedroom flat. Containers are sealed, logged and stacked in our secure indoor facility.","Need more space? We simply use additional containers, so you only pay for what you use."],IMG("hero-packed-container.webp"),"A packed storage container",reverse=True),
                '''<style>
.hx-sec{background:#F7F5EF;color:#46505a;padding:5.5rem 1.25rem;}
.hx-wrap{max-width:1180px;margin:0 auto;}
.hx-head{max-width:760px;margin:0 auto 3.25rem;}
.hx-eyebrow{display:inline-flex;align-items:center;gap:.7rem;text-transform:uppercase;letter-spacing:.18em;font-size:.74rem;font-weight:700;color:#FC9700;margin:0 0 1.1rem;}
.hx-eyebrow::before{content:"";width:28px;height:2px;background:#FC9700;display:inline-block;}
.hx-h2{font-size:clamp(2rem,4.4vw,2.95rem);line-height:1.08;font-weight:800;color:#23282d;letter-spacing:-.02em;margin:0 0 1.4rem;}
.hx-h2 em{font-style:normal;color:#FC9700;}
.hx-lead{font-size:1.13rem;line-height:1.75;color:#46505a;margin:0;}
.hx-lead::first-letter{float:left;font-size:3.6rem;line-height:.82;font-weight:800;color:#FC9700;padding:.35rem .6rem 0 0;}

.hx-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;}
.hx-step{position:relative;display:flex;flex-direction:column;background:linear-gradient(180deg,#ffffff 0%,#fbfaf6 100%);border:1px solid rgba(35,40,45,.10);border-radius:18px;padding:1.9rem 1.7rem 1.7rem;box-shadow:0 1px 2px rgba(35,40,45,.04);transition:transform .28s ease,box-shadow .28s ease,border-color .28s ease;overflow:hidden;}
.hx-step::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#FC9700,rgba(252,151,0,.25));}
.hx-step:hover{transform:translateY(-6px);box-shadow:0 18px 38px rgba(35,40,45,.10);border-color:rgba(252,151,0,.45);}

.hx-top{display:flex;align-items:center;gap:.85rem;margin-bottom:1.2rem;}
.hx-num{flex:none;width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.05rem;color:#23282d;background:#F7F5EF;border:1px solid rgba(35,40,45,.12);transition:color .28s ease,border-color .28s ease;}
.hx-step:hover .hx-num{color:#FC9700;border-color:rgba(252,151,0,.4);}
.hx-icon{flex:none;width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(252,151,0,.12);color:#FC9700;}
.hx-icon svg{width:24px;height:24px;}
.hx-flow{margin-left:auto;flex:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#FC9700;color:#fff;font-size:1.15rem;line-height:1;box-shadow:0 4px 12px rgba(252,151,0,.35);transition:transform .28s ease;}
.hx-flow svg{width:18px;height:18px;display:block;transition:transform .28s ease;}
.hx-step:hover .hx-flow--right svg{transform:translateX(4px);}
.hx-step:hover .hx-flow--down svg{transform:translateY(4px);}

.hx-kicker{text-transform:uppercase;letter-spacing:.16em;font-size:.7rem;font-weight:700;color:#FC9700;margin:0 0 .45rem;}
.hx-title{font-size:1.28rem;line-height:1.2;font-weight:800;color:#23282d;letter-spacing:-.01em;margin:0 0 .7rem;}
.hx-summary{font-size:1rem;font-weight:700;color:#23282d;line-height:1.4;margin:0 0 .9rem;}
.hx-body{font-size:.96rem;line-height:1.68;color:#46505a;margin:0 0 1.4rem;}
.hx-body strong{color:#FC9700;font-weight:700;}
.hx-body a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.5);text-underline-offset:2px;transition:color .2s ease;}
.hx-body a:hover{color:#FC9700;}

.hx-chip{margin-top:auto;align-self:flex-start;display:inline-flex;align-items:center;gap:.5rem;background:#F7F5EF;border:1px solid rgba(252,151,0,.35);color:#23282d;font-size:.78rem;font-weight:700;letter-spacing:.02em;padding:.5rem .85rem;border-radius:999px;}
.hx-chip svg{width:14px;height:14px;color:#FC9700;flex:none;}

.hx-cta{position:relative;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;background:linear-gradient(155deg,#23282d 0%,#2f363d 100%);border-radius:18px;padding:2.2rem 1.9rem;color:#fff;overflow:hidden;}
.hx-cta::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#FC9700,rgba(252,151,0,.25));}
.hx-cta__mark{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:#FC9700;color:#fff;margin-bottom:1.1rem;}
.hx-cta__mark svg{width:24px;height:24px;}
.hx-cta__tag{text-transform:uppercase;letter-spacing:.16em;font-size:.68rem;font-weight:700;color:#FC9700;margin:0 0 .5rem;}
.hx-cta__txt{font-size:1.32rem;font-weight:800;line-height:1.25;letter-spacing:-.01em;margin:0 0 1.4rem;color:#fff;}
.hx-cta__txt em{font-style:normal;color:#FC9700;}
.hx-cta__link{display:inline-flex;align-items:center;gap:.55rem;background:#FC9700;color:#23282d;font-weight:800;font-size:.95rem;padding:.75rem 1.3rem;border-radius:999px;text-decoration:none;transition:transform .25s ease,box-shadow .25s ease;}
.hx-cta__link svg{width:16px;height:16px;transition:transform .25s ease;}
.hx-cta__link:hover{transform:translateY(-2px);box-shadow:0 12px 26px rgba(252,151,0,.4);}
.hx-cta__link:hover svg{transform:translateX(4px);}

.hx-note{max-width:820px;margin:3rem auto 0;padding-top:2rem;border-top:1px solid rgba(35,40,45,.13);font-size:1.02rem;line-height:1.75;color:#46505a;}
.hx-note a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.5);text-underline-offset:2px;transition:color .2s ease;}
.hx-note a:hover{color:#FC9700;}

@media(max-width:980px){
  .hx-grid{grid-template-columns:repeat(2,1fr);}
}
@media(max-width:620px){
  .hx-sec{padding:4rem 1.1rem;}
  .hx-grid{grid-template-columns:1fr;}
  .hx-flow--right svg{transform:rotate(90deg);}
  .hx-step:hover .hx-flow--right svg{transform:rotate(90deg) translateX(4px);}
}
@media(prefers-reduced-motion:reduce){
  .hx-step,.hx-flow svg,.hx-num,.hx-cta__link,.hx-cta__link svg{transition:none;}
  .hx-step:hover{transform:none;}
}
</style><section class="hx-sec">
  <div class="hx-wrap">
    <div class="hx-head">
      <p class="hx-eyebrow">The managed difference</p>
      <h2 class="hx-h2">What to Expect From <em>Start to Finish</em></h2>
      <p class="hx-lead">Fully managed storage is designed to take the heavy lifting &mdash; literally and figuratively &mdash; off your plate. From the first phone call to the day your belongings come home, one dedicated team handles every step, so you always know who you&rsquo;re dealing with and exactly what happens next. Here&rsquo;s what working with us actually looks like.</p>
    </div>

    <div class="hx-grid">

      <article class="hx-step">
        <div class="hx-top">
          <span class="hx-num">1</span>
          <span class="hx-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 18c1.5 0 2.4-.9 2.4-2 0-1-.8-1.6-2.2-2-1.2-.3-1.8-.7-1.8-1.4 0-.7.7-1.2 1.6-1.2.9 0 1.5.4 1.7 1"/><path d="M10 15.3h3"/></svg>
          </span>
          <span class="hx-flow hx-flow--right" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>
        </div>
        <p class="hx-kicker">Step one</p>
        <h3 class="hx-title">It starts with an honest quote</h3>
        <p class="hx-summary">A clear, fixed price within 24 hours.</p>
        <p class="hx-body">Tell us roughly what you need to store and your timescale, and we&rsquo;ll send a clear, fixed quote within 24 hours &mdash; from just &pound;15 a week, with no deposit and no hidden fees. Not sure how much space you&rsquo;ll need? Use our <a href="storage-size-guide.html">storage size guide</a> or the calculator on our <a href="pricing.html">pricing page</a> to estimate it in a couple of minutes, or simply tell us the rooms involved and we&rsquo;ll work it out for you.</p>
        <p class="hx-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>Within 24 hours</p>
      </article>

      <article class="hx-step">
        <div class="hx-top">
          <span class="hx-num">2</span>
          <span class="hx-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/><path d="M7.5 5.5l9 5"/></svg>
          </span>
          <span class="hx-flow hx-flow--right" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>
        </div>
        <p class="hx-kicker">Step two</p>
        <h3 class="hx-title">We pack, wrap and collect</h3>
        <p class="hx-summary">We bring the materials and pack it all for you.</p>
        <p class="hx-body">On collection day we arrive with all the materials &mdash; boxes, tape, blankets and wrapping &mdash; and pack your belongings properly, paying particular attention to furniture, electronics and anything fragile. Everything is loaded and sealed into your own wooden container at your door, so there&rsquo;s no van for you to hire and nothing to carry down a shared corridor. As a LAPADA-accredited team, we&rsquo;re trusted with antiques and high-value items as readily as everyday boxes.</p>
        <p class="hx-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 7l-8-4-8 4 8 4 8-4z"/><path d="M4 7v8l8 4 8-4V7"/></svg>Materials included</p>
      </article>

      <article class="hx-step">
        <div class="hx-top">
          <span class="hx-num">3</span>
          <span class="hx-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/><rect x="9" y="11" width="6" height="5" rx="1"/><path d="M10 11V9.5a2 2 0 0 1 4 0V11"/></svg>
          </span>
          <span class="hx-flow hx-flow--down" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="M6 13l6 6 6-6"/></svg></span>
        </div>
        <p class="hx-kicker">Step three</p>
        <h3 class="hx-title">Your belongings stay sealed and secure</h3>
        <p class="hx-summary">Sealed, logged and untouched the whole stay.</p>
        <p class="hx-body">Your sealed container is transported to our alarmed Ashington warehouse, logged, and stacked in a dry, ventilated, 24/7 CCTV-monitored facility. It stays sealed and undisturbed for the whole of its stay &mdash; we don&rsquo;t open it, and the public can&rsquo;t access it. That&rsquo;s what keeps your things protected from damp, dust and tampering, whether they&rsquo;re with us for a fortnight or several years.</p>
        <p class="hx-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/></svg>24/7 CCTV, alarmed</p>
      </article>

      <article class="hx-step">
        <div class="hx-top">
          <span class="hx-num">4</span>
          <span class="hx-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h10v9H3z"/><path d="M13 9h4l3 3v3h-7z"/><circle cx="7" cy="17" r="1.6"/><circle cx="17" cy="17" r="1.6"/></svg>
          </span>
          <span class="hx-flow hx-flow--right" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>
        </div>
        <p class="hx-kicker">Step four</p>
        <h3 class="hx-title">Access and redelivery on your terms</h3>
        <p class="hx-summary">Back to your door on 24 hours&rsquo; notice.</p>
        <p class="hx-body">Need something back, or finished with storage altogether? Give us 24 hours&rsquo; notice and we&rsquo;ll redeliver to your door anywhere across <a href="areas-we-cover.html">West Sussex</a>. Terms are flexible and rolling, so you can extend or end whenever suits &mdash; ideal for <a href="short-term-storage.html">short-term</a> needs like a move or renovation, or <a href="long-term-storage.html">long-term</a> storage while you&rsquo;re away. When you&rsquo;re ready, <a href="contact.html">get a free quote</a> and we&rsquo;ll take care of the rest.</p>
        <p class="hx-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>24h notice</p>
      </article>

      <article class="hx-step">
        <div class="hx-top">
          <span class="hx-num">5</span>
          <span class="hx-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>
          </span>
          <span class="hx-flow hx-flow--right" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>
        </div>
        <p class="hx-kicker">Step five</p>
        <h3 class="hx-title">Built around your move or project</h3>
        <p class="hx-summary">Flexible storage that fits any situation.</p>
        <p class="hx-body">Because we fit around you rather than the other way round, managed storage works for almost any situation &mdash; bridging a delayed completion, clearing a home for sale or renovation, making room for a new arrival, or holding a loved one&rsquo;s belongings after a bereavement. Whatever&rsquo;s behind it, the process stays the same: simple, fully insured, and handled with genuine care from start to finish.</p>
        <p class="hx-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M16 3v4M8 3v4M4 11h16"/></svg>Rolling terms, no tie-in</p>
      </article>

      <article class="hx-cta">
        <span class="hx-cta__mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3v18"/><path d="M5 4h11l-2 3 2 3H5"/><circle cx="5" cy="21" r="0"/></svg>
        </span>
        <p class="hx-cta__tag">Destination</p>
        <p class="hx-cta__txt">And that&rsquo;s it &mdash; <em>your things are home</em></p>
        <a class="hx-cta__link" href="contact.html">Get a free quote
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>
        </a>
      </article>

    </div>

    <p class="hx-note">Have a question we haven&rsquo;t answered yet? Just call us on <a href="tel:+441903893731">01903 893731</a> &mdash; you&rsquo;ll speak to the same family team that will handle your storage, and we&rsquo;re always happy to talk through the options before you commit to anything. You can also see what fits in a container with our <a href="storage-size-guide.html">size guide</a> or browse the full range of <a href="storage-solutions.html">storage solutions</a> we offer across West Sussex.</p>
  </div>
</section>''',
        faq([("How quickly can you collect?","Often within a few days &mdash; tell us your timescale on your free quote."),("How do I access my belongings?","Give us 24 hours&rsquo; notice and we redeliver to your door across West Sussex."),("What&rsquo;s included?","Packing materials, professional packing, collection, secure container storage and redelivery.")]),
        cta_band("Ready to Get Started?",IMG("gallery-warehouse-b.webp")),
      ]))
    # PRICING
    P.append(dict(file="pricing.html",slug="pricing",nav="Pricing",
      title="Storage Prices West Sussex | Wolves Storage Sussex",
      meta="Transparent storage prices in West Sussex from £15/week. No deposit or hidden fees, flexible weekly & 4-week terms, collection included.",
      hero=IMG(HERO_WAREHOUSE[0]),faqs=[("How much is storage?","From &pound;15 per week per container with no deposit and no hidden fees."),("Are there any extra fees?","No hidden fees. Optional extras are extended insurance cover and help unpacking."),("Is collection included?","Yes &mdash; collection and redelivery across West Sussex are included.")],
      sections=[
        hero(IMG(HERO_WAREHOUSE[0]),HERO_WAREHOUSE[1],"Simple, Transparent Storage Prices",
          "Storage from just &pound;15 per week with no deposit and no hidden fees. You only pay for the container space you use &mdash; collection and redelivery included.",
          ["From &pound;15 per week, no deposit","Flexible weekly &amp; 4-week terms","Collection &amp; redelivery included","Free quote within 24 hours"],big=False),
        '''<style>
.pw-pricing{background:#F7F5EF;color:#46505a;padding:clamp(56px,8vw,108px) 20px;}
.pw-pricing *{box-sizing:border-box;}
.pw-wrap{max-width:1060px;margin:0 auto;}@media(min-width:768px){.pw-wrap{columns:2;column-gap:56px}.pw-eyebrow,.pw-h2,.pw-intro,.pw-stats,.pw-estimator,.pw-compare{-webkit-column-span:all;column-span:all}.pw-h3{-webkit-column-break-after:avoid;break-after:avoid}.pw-body{margin-bottom:0}}
.pw-eyebrow{display:flex;align-items:center;gap:14px;text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;color:#FC9700;margin:0 0 18px;}
.pw-rule{width:28px;height:2px;background:#FC9700;display:inline-block;flex:0 0 auto;}
.pw-h2{color:#23282d;font-size:clamp(1.9rem,4vw,2.9rem);line-height:1.1;font-weight:800;letter-spacing:-.01em;margin:0 0 22px;}
.pw-h2 em{font-style:normal;color:#FC9700;}
.pw-intro{font-size:clamp(1.05rem,1.7vw,1.25rem);line-height:1.7;color:#46505a;margin:0;max-width:780px;}
.pw-stats{display:flex;flex-wrap:wrap;align-items:center;gap:0;margin:30px 0 0;}
.pw-stat{padding-right:22px;margin-right:22px;border-right:1px solid rgba(35,40,45,.13);font-size:.95rem;color:#46505a;line-height:1.4;margin-top:8px;}
.pw-stat:last-child{border-right:0;margin-right:0;padding-right:0;}
.pw-stat strong{display:block;color:#FC9700;font-weight:800;font-size:1.3rem;letter-spacing:-.01em;}

.pw-h3{color:#23282d;font-size:clamp(1.25rem,2.2vw,1.6rem);line-height:1.25;font-weight:800;letter-spacing:-.01em;margin:clamp(36px,4.5vw,56px) 0 12px;}
.pw-body{font-size:1.05rem;line-height:1.78;color:#46505a;margin:0;max-width:780px;}
.pw-body a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.55);text-decoration-thickness:1.5px;text-underline-offset:3px;transition:color .2s ease,text-decoration-color .2s ease;}
.pw-body a:hover,.pw-body a:focus-visible{color:#FC9700;text-decoration-color:#FC9700;}
.pw-body strong{color:#FC9700;font-weight:700;}

/* Estimator — framed by hairlines, not a card */
.pw-estimator{margin:clamp(22px,3vw,34px) 0 clamp(8px,2vw,16px);padding:clamp(26px,3.5vw,40px) 0;border-top:1px solid rgba(35,40,45,.13);border-bottom:1px solid rgba(35,40,45,.13);}
.pw-est-lead{font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;font-weight:700;color:#23282d;margin:0 0 18px;}
.pw-est-lead span{color:#FC9700;}
.pw-choices{display:flex;flex-wrap:wrap;gap:2px;margin:0 0 30px;border-bottom:1px solid rgba(35,40,45,.13);}
.pw-choice{flex:1 1 140px;min-width:130px;background:transparent;border:0;border-bottom:2px solid transparent;margin-bottom:-1px;padding:12px 10px 14px;text-align:left;cursor:pointer;transition:border-color .2s ease;}
.pw-choice-label{display:block;font-weight:700;font-size:1.02rem;color:#46505a;transition:color .2s ease;}
.pw-choice-sub{display:block;font-size:.82rem;color:#828c96;margin-top:3px;line-height:1.35;}
.pw-choice:hover .pw-choice-label{color:#23282d;}
.pw-choice--active{border-bottom-color:#FC9700;}
.pw-choice--active .pw-choice-label{color:#23282d;}
.pw-choice:focus-visible{outline:2px solid #FC9700;outline-offset:2px;border-radius:2px;}

.pw-result{display:flex;flex-wrap:wrap;align-items:center;gap:clamp(22px,5vw,56px);}
.pw-boxes{display:flex;align-items:center;gap:12px;min-height:60px;}
.pw-box{width:52px;height:52px;color:#FC9700;opacity:.16;transform:translateY(6px) scale(.88);transition:opacity .45s ease,transform .45s ease;}
.pw-box svg{width:100%;height:100%;display:block;}
.pw-box--on{opacity:1;transform:translateY(0) scale(1);}
.pw-box-plus{font-size:2rem;font-weight:800;color:#FC9700;line-height:1;align-self:center;}
.pw-price-wrap{min-width:200px;}
.pw-price{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px;}
.pw-price-band{width:100%;font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;font-weight:700;color:#828c96;margin-bottom:2px;}
.pw-price-amount{font-size:clamp(2.5rem,6.5vw,3.7rem);font-weight:800;color:#23282d;line-height:.95;letter-spacing:-.02em;}
.pw-price-per{font-size:1.05rem;font-weight:700;color:#46505a;}
.pw-result-meta{width:100%;font-size:.98rem;line-height:1.6;color:#46505a;margin:10px 0 0;max-width:520px;}
.pw-result-meta strong{color:#FC9700;font-weight:800;}

/* Managed vs self — hairline ledger with a cross-out reveal, not a card */
.pw-compare{margin:clamp(18px,2.5vw,26px) 0 0;max-width:780px;}
.pw-cinstruct{margin:0 0 16px;font-size:.9rem;color:#6b7480;}
.pw-toggle{position:relative;display:flex;background:#ECE8DE;border:1px solid rgba(35,40,45,.12);border-radius:999px;padding:5px;max-width:440px;}
.pw-tbtn{position:relative;z-index:1;flex:1;background:none;border:0;padding:13px 14px;font-size:.97rem;font-weight:700;color:#5a636c;cursor:pointer;border-radius:999px;transition:color .25s ease;}
.pw-tbtn.pw-on{color:#fff;}
.pw-tbtn:focus-visible{outline:2px solid #23282d;outline-offset:2px;}
.pw-tslider{position:absolute;top:5px;left:5px;width:calc(50% - 5px);height:calc(100% - 10px);background:#FC9700;border-radius:999px;transition:transform .32s cubic-bezier(.4,0,.2,1);}
.pw-tslider-right{transform:translateX(100%);}
.pw-ledger{margin:26px 0 0;border-top:1px solid rgba(35,40,45,.13);}
.pw-row{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:15px 2px;border-bottom:1px solid rgba(35,40,45,.13);}
.pw-rowlabel{font-weight:600;color:#3b434b;font-size:1rem;}
.pw-rowvals{display:flex;align-items:baseline;gap:12px;text-align:right;flex:none;justify-content:flex-end;}
.pw-cost{font-weight:700;color:#23282d;transition:color .35s ease,opacity .35s ease,text-decoration-color .35s ease;font-variant-numeric:tabular-nums;}
.pw-cost.pw-struck{text-decoration:line-through;text-decoration-color:rgba(35,40,45,.45);text-decoration-thickness:2px;color:#9aa1a8;font-weight:600;}
.pw-incl{font-weight:800;color:#FC9700;font-variant-numeric:tabular-nums;}
.pw-bottom{margin:24px 0 0;font-size:1.06rem;line-height:1.7;color:#3b434b;min-height:1.7em;}
.pw-bottom strong{color:#FC9700;font-weight:800;}

@media (max-width:560px){
  .pw-stat{font-size:.9rem;}
  .pw-choice{flex:1 1 46%;}
}
@media (max-width:640px){
  .pw-row{flex-direction:column;align-items:flex-start;gap:6px;}
  .pw-rowvals{text-align:left;justify-content:flex-start;}
  .pw-toggle{max-width:none;}
}
@media (prefers-reduced-motion:reduce){
  .pw-box,.pw-choice,.pw-choice-label,.pw-body a,.pw-tslider,.pw-cost,.pw-tbtn{transition:none !important;}
}
</style><section class="pw-pricing" x-data="pwPricing()">
  <div class="pw-wrap">
    <div class="pw-eyebrow"><span class="pw-rule" aria-hidden="true"></span>How pricing works</div>
    <h2 class="pw-h2">How Our Storage <em>Pricing</em> Works</h2>
    <p class="pw-intro">Storage with us starts at just &pound;15 a week, and the way we price it is refreshingly straightforward &mdash; you pay a low weekly rate for each wooden container your belongings fill, and nothing else. Each container holds around 250 cubic feet, roughly the contents of a one-bedroom flat or a single, well-packed room. If you have more to store we simply add another container, so you only ever pay for the space you actually use rather than renting an oversized room and paying for empty air. There is no deposit, no joining fee and no hidden charges &mdash; the price we quote is the price you pay.</p>

    <div class="pw-stats" aria-hidden="true">
      <span class="pw-stat"><strong>&pound;15</strong> starting weekly rate</span>
      <span class="pw-stat"><strong>250</strong> cu ft per container</span>
      <span class="pw-stat"><strong>24h</strong> notice to change</span>
    </div>

    <h3 class="pw-h3">What affects your price</h3>
    <p class="pw-body">Three things shape your final figure: how much you store, how long you store it, and whether you add any optional extras. The number of containers reflects your volume, so a few boxes between moves costs far less than the contents of a whole house going into long-term storage. Terms are flexible and rolling &mdash; pay weekly or in four-week blocks, whichever suits &mdash; and you can extend or end whenever you like, so a fortnight between completion dates and several years working abroad are both easy to budget for. Optional extras such as professional packing materials, extended insurance cover for higher-value items, or a hand unpacking when your belongings come home are added only if you want them, and always quoted upfront.</p>

    <h3 class="pw-h3">What storage typically costs</h3>
    <p class="pw-body">As a rough guide, a single container suits a one-bedroom flat, a home-office clear-out or a few rooms of furniture during a renovation; a two- or three-bedroom house usually fills two to three containers; and a business archiving stock or paperwork might use anything from one container upward. Because every order is collected, packed and redelivered for you, the figure we quote is genuinely all-in &mdash; there are no surprise add-ons for mileage, access or handling, and no charge for the time our team spends loading and wrapping your belongings.</p>

    <div class="pw-estimator">
      <p class="pw-est-lead"><span>What will it cost me?</span> Pick the closest match and watch your estimate update.</p>
      <div class="pw-choices" role="group" aria-label="Choose the situation closest to yours">
        <template x-for="(s,i) in scenarios" :key="s.id">
          <button type="button" class="pw-choice" :class="{'pw-choice--active': selected===i}" :aria-pressed="(selected===i).toString()" @click="select(i)">
            <span class="pw-choice-label" x-text="s.label"></span>
            <span class="pw-choice-sub" x-text="s.sub"></span>
          </button>
        </template>
      </div>

      <div class="pw-result">
        <div class="pw-boxes" aria-hidden="true">
          <template x-for="n in 3" :key="n">
            <span class="pw-box" :class="{'pw-box--on': n <= current.boxes}">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"></path><path d="M3 7.5 12 12l9-4.5M12 12v9"></path></svg>
            </span>
          </template>
          <span class="pw-box-plus" x-show="current.plus" x-cloak>+</span>
        </div>
        <div class="pw-price-wrap" aria-live="polite">
          <div class="pw-price">
            <span class="pw-price-band" x-text="current.band"></span>
            <span class="pw-price-amount">&pound;<span x-text="displayPrice"></span></span>
            <span class="pw-price-per">/week</span>
          </div>
          <p class="pw-result-meta">That is roughly <strong><span x-text="current.boxes"></span> container<span x-show="current.boxes > 1" x-cloak>s</span><span x-show="current.plus" x-cloak>+</span></strong> of secure space &mdash; you only ever pay for the volume your belongings actually fill, with collection and redelivery included.</p>
        </div>
      </div>
    </div>

    <h3 class="pw-h3">Managed storage vs a self-storage unit</h3>
    <p class="pw-body">A drive-up self-storage unit can look cheaper on the headline rate, but the real cost adds up quickly once you factor in van hire, fuel, the hours spent driving back and forth, and paying for floor space you never fully use. With our managed model there is nothing to hire and nothing to carry: collection from your door and redelivery are built into the price, our team packs and loads everything for you, and because we stack sealed containers efficiently in a secure warehouse you pay only for the volume your belongings take up. For most households and businesses across West Sussex it works out cleaner, more secure and better value &mdash; with none of the heavy lifting.</p>
    <div class="pw-compare" x-data="{mode:'self'}">
      <p class="pw-cinstruct">Toggle to see what a self-storage unit really costs &mdash; then watch the hidden charges fall away.</p>
      <div class="pw-toggle" role="group" aria-label="Compare a self-storage unit with our managed storage">
        <span class="pw-tslider" :class="{'pw-tslider-right':mode==='managed'}" aria-hidden="true"></span>
        <button type="button" class="pw-tbtn" :class="{'pw-on':mode==='self'}" :aria-pressed="(mode==='self').toString()" @click="mode='self'">Self-storage unit</button>
        <button type="button" class="pw-tbtn" :class="{'pw-on':mode==='managed'}" :aria-pressed="(mode==='managed').toString()" @click="mode='managed'">Managed (us)</button>
      </div>
      <div class="pw-ledger">
        <div class="pw-row">
          <span class="pw-rowlabel">Headline rate</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">Cheap on paper</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>From &pound;15/week</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Van hire</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">&pound;60&ndash;&pound;100</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>Included</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Fuel &amp; mileage</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">On top</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>Included</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Hours driving back and forth</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">Your weekends</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>None</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Floor space you never fully use</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">Paid for in full</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>Only the volume you use</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Packing &amp; loading</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">You do the lifting</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>Our team, included</span>
          </span>
        </div>
        <div class="pw-row">
          <span class="pw-rowlabel">Collection &amp; redelivery</span>
          <span class="pw-rowvals">
            <span class="pw-cost" :class="{'pw-struck':mode==='managed'}">Not offered</span>
            <span class="pw-incl" x-show="mode==='managed'" x-cloak x-transition>Built into the price</span>
          </span>
        </div>
      </div>
      <p class="pw-bottom" aria-live="polite">
        <span x-show="mode==='self'">A low headline rate &mdash; then van hire, fuel, your time and floor space you never fully use stack up on top.</span>
        <span x-show="mode==='managed'" x-cloak>One all-in weekly price from <strong>&pound;15</strong> &mdash; collection, packing and redelivery built in, and you pay only for the volume your belongings take up.</span>
      </p>
    </div>

    <h3 class="pw-h3">No deposit, no tie-in, no surprises</h3>
    <p class="pw-body">We keep everything transparent because that is how we would want to be treated. Every quote is clear and fixed, there is no deposit and no minimum contract, and you deal with the same family team from your first call to the day your things come back. Your belongings are fully insured throughout, stored in a dry, alarmed, 24/7 CCTV-monitored facility, and handled by a LAPADA-accredited team trusted with antiques and high-value items as readily as everyday boxes. If your circumstances change, you can scale up, scale down or finish entirely with just 24 hours&rsquo; notice.</p>

    <h3 class="pw-h3">Get an exact price for your storage</h3>
    <p class="pw-body">Not sure how many containers you&rsquo;ll need? Use the calculator on this page for an instant estimate, take a couple of minutes with our <a href="storage-size-guide.html">storage size guide</a>, or simply tell us the rooms involved and we&rsquo;ll work it out for you. Either way we&rsquo;ll send a clear, no-obligation quote within 24 hours, covering collection and redelivery anywhere across <a href="areas-we-cover.html">West Sussex</a>. Browse our full range of <a href="storage-solutions.html">storage solutions</a> or <a href="contact.html">get a free quote</a> to see exactly what your storage will cost.</p>
  </div>

  <script>
    document.addEventListener('alpine:init', () => {
      Alpine.data('pwPricing', () => ({
        selected: 0,
        displayPrice: 15,
        scenarios: [
          { id:'flat1',  label:'1-bed flat',  sub:'or a single, packed room', boxes:1, price:15, band:'from', plus:false },
          { id:'house2', label:'2-bed house', sub:'a typical family move',     boxes:2, price:30, band:'from', plus:false },
          { id:'house3', label:'3-bed house', sub:'a fuller household',        boxes:3, price:45, band:'from', plus:false },
          { id:'biz',    label:'Business',     sub:'stock or paperwork',        boxes:1, price:15, band:'from', plus:true  }
        ],
        get current() { return this.scenarios[this.selected] || this.scenarios[0]; },
        select(i) {
          this.selected = i;
          this.animatePrice(this.current.price);
        },
        animatePrice(target) {
          var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          if (reduce) { this.displayPrice = target; return; }
          var start = this.displayPrice, t0 = performance.now(), dur = 480, self = this;
          var step = function(t) {
            var p = Math.min(1, (t - t0) / dur);
            self.displayPrice = Math.round(start + (target - start) * p);
            if (p < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
        },
        init() { this.displayPrice = this.current.price; }
      }));
    });
  </script>
</section>''',
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
    for _lab,_items in area_groups:
        for _slug,_tn,_pc,_tag in _items:
            TOWN_INFO[_slug]={"pc":_pc,"tag":_tag,"group":_lab}
    LOC_CSS=('<style>'
      '.loc-sec{position:relative;overflow:hidden;background:#697783}'
      '.loc-sec::before{content:none}'
      '.loc-sec::after{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#FC9700,#FC9700,#FC9700)}'
      '.loc-blob{display:none}'
      '.loc-wrap{position:relative;z-index:1;max-width:74rem;margin:0 auto;text-align:left}'
      '.loc-head{text-align:center;max-width:52rem;margin:0 auto}'
      '.loc-ey{display:inline-flex;align-items:center;gap:.5rem;color:#FC9700;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;margin-bottom:.65rem}'
      '.loc-ey::before,.loc-ey::after{content:"";width:18px;height:1px;background:rgba(252,151,0,.55)}'
      '.loc-h2{color:#fff;font-weight:800;font-size:1.85rem;line-height:1.12;margin:0}'
      '@media(min-width:1024px){.loc-h2{font-size:2.25rem}}'
      '.loc-rule{width:62px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FC9700,#FC9700);margin:1.05rem auto 0}'
      '.loc-lead{font-size:1.08rem;line-height:1.65;color:#ece9df;max-width:46rem;margin:1.05rem auto 0;text-align:center}'
      '.loc-stats{display:grid;grid-template-columns:1fr 1fr;gap:1rem 0;margin:2.2rem auto 0;max-width:58rem;position:relative;overflow:hidden;background:linear-gradient(120deg,rgba(255,255,255,.10),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.16);border-radius:1.2rem;padding:1.3rem 1rem}'
      '.loc-stats::after{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,#FC9700,#FC9700,#FC9700)}'
      '@media(min-width:680px){.loc-stats{grid-template-columns:repeat(4,1fr);padding:1.4rem 1.3rem}}'
      '.loc-stat{position:relative;text-align:center}'
      '.loc-stat-n{display:block;font-weight:800;font-size:1.7rem;line-height:1;color:#FC9700}'
      '.loc-stat-l{display:block;margin-top:.35rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:#e7e4d8}'
      '@media(min-width:680px){.loc-stat+.loc-stat::before{content:"";position:absolute;left:0;top:14%;bottom:14%;width:1px;background:rgba(255,255,255,.18)}}'
      # ---- interactive map layout ----
      '.lm-mapwrap{position:relative;margin-top:2.4rem;border:1px solid rgba(255,255,255,.16);border-radius:1.2rem;overflow:hidden;background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015));box-shadow:0 24px 48px -28px rgba(0,0,0,.6)}'
      '.lm-mapwrap::after{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:#FC9700;z-index:2}'
      '.lm-map{height:460px;width:100%;background:#e7ecf0;border-radius:1.2rem;z-index:1}'
      '@media(max-width:879px){.lm-map{height:360px}}'
      # directory card grid (cream/white tiles)
      '.dt-group{margin-top:2.3rem}'
      '.dt-ghead{display:flex;align-items:center;gap:.7rem;margin-bottom:1.05rem}'
      '.dt-gpin{flex:none;width:30px;height:30px;border-radius:8px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);display:grid;place-items:center;color:#FC9700}'
      '.dt-gpin svg{width:16px;height:16px}'
      '.dt-glabel{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.09em;color:#FC9700;white-space:nowrap}'
      '.dt-grule{flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.2),transparent)}'
      '.dt-cards{display:grid;grid-template-columns:1fr;gap:1rem}'
      '@media(min-width:560px){.dt-cards{grid-template-columns:1fr 1fr}}'
      '@media(min-width:1024px){.dt-cards{grid-template-columns:repeat(4,1fr)}}'
      '.dt-card{display:flex;flex-direction:column;gap:.7rem;padding:1.1rem;border-radius:.9rem;text-decoration:none;border:1px solid rgba(0,0,0,.06);box-shadow:0 4px 14px -8px rgba(0,0,0,.5);transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}'
      '.dt-card--white{background:#fff}'
      '.dt-card--cream{background:#F0ECDF}'
      '.dt-card:hover{transform:translateY(-3px);box-shadow:0 16px 28px -12px rgba(0,0,0,.6);border-color:#FC9700}'
      '.dt-card:focus-visible{outline:none;border-color:#FC9700;box-shadow:0 0 0 3px rgba(252,151,0,.55)}'
      '.dt-top{display:flex;align-items:flex-start;gap:.7rem}'
      '.dt-ic{flex:none;width:38px;height:38px;border-radius:10px;background:#EAE5D6;border:1px solid rgba(0,0,0,.05);display:grid;place-items:center;color:#FC9700;transition:background .15s ease,color .15s ease}'
      '.dt-card--cream .dt-ic{background:#fff}'
      '.dt-card:hover .dt-ic{background:#FC9700;color:#fff}'
      '.dt-ic svg{width:19px;height:19px}'
      '.dt-tt{flex:1;min-width:0}'
      '.dt-name{margin:0;font-size:.97rem;font-weight:800;color:#1f2733;line-height:1.2}'
      '.dt-pc{display:inline-block;margin-top:.35rem;font-size:.6rem;font-weight:800;letter-spacing:.04em;color:#8a4d05;background:rgba(252,151,0,.14);border:1px solid rgba(252,151,0,.55);padding:2px 7px;border-radius:5px}'
      '.dt-tag{margin:0;color:#5d6770;font-size:.82rem;line-height:1.45;flex:1}'
      '.dt-cta{display:inline-flex;align-items:center;gap:.35rem;font-size:.67rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:#FC9700}'
      '.dt-cta svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2.5;transition:transform .15s ease}'
      '.dt-card:hover .dt-cta{color:#C7660A}'
      '.dt-card:hover .dt-cta svg{transform:translateX(3px)}'
      '@media(prefers-reduced-motion:reduce){.dt-card,.dt-ic,.dt-cta svg{transition:none}.dt-card:hover{transform:none}}'
      '.loc-more{margin-top:2.6rem;padding-top:1.6rem;border-top:1px solid rgba(255,255,255,.14)}'
      '.loc-more-h{font-weight:800;color:#fff;margin:0 0 .9rem;font-size:1.02rem}'
      '.loc-pills{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}'
      '.loc-pill{font-size:.84rem;font-weight:600;color:#f0ede3;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:.4rem .85rem;transition:background .2s ease,color .2s ease}'
      '.loc-pill:hover{background:rgba(252,151,0,.18);color:#fff}'
      '.loc-ask{color:#d9dde1;margin:0}.loc-ask a{color:#FC9700;font-weight:700;text-decoration:underline}'
      '@media(prefers-reduced-motion:reduce){.lm-pulse{animation:none;opacity:0}.lm-dot,.lm-ring,.lm-lbl,.lm-trow{transition:none}}'
      '</style>')
    LOC_PIN='<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>'
    LOC_GPIN='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/></svg>'
    LOC_ARR='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg>'
    LOC_CHEV='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    more_towns=["Amberley","Bramber","Upper Beeding","West Chiltington","Wisborough Green","Lindfield","Hassocks","Hurstpierpoint","Pyecombe","Walberton","Small Dole","Ashurst"]
    # ---- interactive West Sussex map: real lat/lng -> SVG viewBox 1000x540 ----
    LM_COORDS={
      "storage-ashington":(50.948,-0.385),"storage-washington":(50.908,-0.402),
      "storage-storrington":(50.918,-0.452),"storage-pulborough":(50.962,-0.510),
      "storage-steyning":(50.888,-0.328),"storage-findon":(50.862,-0.398),
      "storage-billingshurst":(51.022,-0.452),"storage-horsham":(51.063,-0.327),
      "storage-henfield":(50.929,-0.275),"storage-cowfold":(50.992,-0.272),
      "storage-partridge-green":(50.973,-0.318),"storage-crawley":(51.112,-0.187),
      "storage-east-grinstead":(51.126,-0.012),"storage-haywards-heath":(51.005,-0.103),
      "storage-burgess-hill":(50.957,-0.132),"storage-arundel":(50.853,-0.554),
      "storage-littlehampton":(50.808,-0.542),"storage-rustington":(50.808,-0.503),
      "storage-bognor-regis":(50.782,-0.673),"storage-worthing":(50.814,-0.372),
      "storage-lancing":(50.831,-0.330),"storage-shoreham-by-sea":(50.834,-0.272),
      "storage-brighton":(50.827,-0.152),"storage-petworth":(50.986,-0.613),
      "storage-midhurst":(50.986,-0.738),"storage-chichester":(50.836,-0.780),
    }
    LM_MAPICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 20l-6 3V6l6-3 6 3 6-3v17l-6 3-6-3z"/><path d="M9 3v17M15 6v17"/></svg>'
    def area_cards():
        total=sum(len(items) for _,items in area_groups)
        towns_js=json.dumps([{"n":tn,"pc":pc,"tag":tag,"u":slug+".html",
            "lat":LM_COORDS[slug][0],"lng":LM_COORDS[slug][1],"hub":slug=="storage-ashington"}
            for _lab,items in area_groups for slug,tn,pc,tag in items],ensure_ascii=False)
        leaflet=('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" '
            'integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>'
            '<style>'
            '.lm-mapwrap .leaflet-container{font-family:inherit;background:#e7ecf0}'
            '.lm-mapwrap .leaflet-div-icon{background:transparent;border:none}'
            '.lm-mk{display:block;position:relative;width:20px;height:20px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFB04D,#FC9700);border:2.5px solid #fff;box-shadow:0 0 0 1.5px rgba(110,60,0,.3),0 2px 6px rgba(0,0,0,.4);cursor:pointer;transition:transform .12s ease}'
            '.lm-mk:hover{transform:scale(1.22)}'
            '.lm-mk--hub{width:34px;height:34px;border-width:3px;animation:lmhub 2.6s ease-out infinite}'
            '.lm-mk--hub::after{content:"";position:absolute;top:50%;left:50%;width:10px;height:10px;border-radius:50%;background:#fff;transform:translate(-50%,-50%)}'
            '@keyframes lmhub{0%{box-shadow:0 0 0 3px rgba(252,151,0,.5),0 0 0 4px rgba(252,151,0,.4),0 3px 10px rgba(0,0,0,.6)}70%,100%{box-shadow:0 0 0 3px rgba(252,151,0,.5),0 0 0 22px rgba(252,151,0,0),0 3px 10px rgba(0,0,0,.6)}}'
            '@media(prefers-reduced-motion:reduce){.lm-mk--hub{animation:none}.lm-mk{transition:none}}'
            '.lm-mapwrap .leaflet-popup-content-wrapper{background:#1b232b;color:#eef1f4;border:1px solid rgba(255,255,255,.16);border-radius:14px;box-shadow:0 18px 40px -16px rgba(0,0,0,.7)}'
            '.lm-mapwrap .leaflet-popup-tip{background:#1b232b}'
            '.lm-mapwrap .leaflet-popup-content{margin:13px 15px;line-height:1.4}'
            '.lm-mapwrap .leaflet-popup-close-button{color:#cdd3d8}'
            '.lm-pop-t{font-weight:800;color:#fff;font-size:1.02rem}'
            '.lm-pop-pc{display:inline-block;margin-left:.45rem;font-size:.66rem;font-weight:800;letter-spacing:.02em;color:#1f2a12;background:#FC9700;padding:2px 7px;border-radius:5px;vertical-align:middle}'
            '.lm-pop-tag{color:#cdd3d8;font-size:.85rem;margin:.45rem 0 .65rem;max-width:230px}'
            '.lm-pop-btn{display:inline-flex;align-items:center;gap:.3rem;font-weight:800;font-size:.8rem;color:#1f2a12;background:linear-gradient(135deg,#FC9700,#FC9700);padding:.45rem .8rem;border-radius:8px;text-decoration:none}'
            '.lm-pop-btn:hover{filter:brightness(1.07)}'
            '.lm-tt.leaflet-tooltip{background:#1b232b;color:#fff;border:1px solid rgba(255,255,255,.2);border-radius:7px;font-weight:700;font-size:.8rem;box-shadow:0 6px 16px -6px rgba(0,0,0,.6)}'
            '.lm-tt.leaflet-tooltip-top::before{border-top-color:#1b232b}'
            '.lm-mapwrap .leaflet-bar a{background:#fff;color:#333;border-bottom-color:rgba(0,0,0,.12)}'
            '.lm-mapwrap .leaflet-bar a:hover{background:#f2f2f2}'
            '.lm-mapwrap .leaflet-control-attribution{background:rgba(255,255,255,.85);color:#555}'
            '.lm-mapwrap .leaflet-control-attribution a{color:#C77800}'
            '</style>'
            '<div id="lmmap" class="lm-map" role="application" aria-label="Interactive map of West Sussex showing the towns we cover from our Ashington base"></div>'
            '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" '
            'integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin="" defer></script>'
            '<script>(function(){var T='+towns_js+';'
            'function go(){if(!window.L){return setTimeout(go,60);}'
            'var map=L.map("lmmap",{scrollWheelZoom:false,zoomControl:true,attributionControl:true});'
            'L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",'
            '{subdomains:"abcd",maxZoom:20,attribution:\'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>\'}).addTo(map);'
            'var pts=[];T.forEach(function(t){'
            'var ic=L.divIcon({className:"",html:\'<span class="\'+(t.hub?"lm-mk lm-mk--hub":"lm-mk")+\'"></span>\',iconSize:t.hub?[34,34]:[20,20],iconAnchor:t.hub?[17,17]:[10,10]});'
            'var m=L.marker([t.lat,t.lng],{icon:ic,riseOnHover:true,keyboard:true,alt:"Storage in "+t.n}).addTo(map);'
            'var pop=\'<div class="lm-pop"><span class="lm-pop-t">\'+t.n+\'</span><span class="lm-pop-pc">\'+t.pc+\'</span>\''
            '+(t.hub?\'<p class="lm-pop-tag">Our family-run storage base &mdash; we collect &amp; redeliver across West Sussex from here.</p>\':\'<p class="lm-pop-tag">\'+t.tag+\'</p>\')'
            '+\'<a class="lm-pop-btn" href="\'+t.u+\'">View \'+t.n+\' storage &rarr;</a></div>\';'
            'm.bindPopup(pop,{closeButton:true});m.bindTooltip(t.n,{direction:"top",offset:[0,-10],opacity:1,className:"lm-tt"});'
            'pts.push([t.lat,t.lng]);});'
            'map.setView([50.95,-0.34],map.getSize().x<760?9:10);'
            'map.on("focus",function(){map.scrollWheelZoom.enable();});map.on("blur",function(){map.scrollWheelZoom.disable();});}'
            'if(document.readyState!=="loading"){go();}else{document.addEventListener("DOMContentLoaded",go);}})();</script>')
        grid=''
        for label,items in area_groups:
            grid+=(f'<div class="dt-group"><div class="dt-ghead"><span class="dt-gpin">{LOC_GPIN}</span>'
                   f'<span class="dt-glabel">{label}</span><span class="dt-grule"></span></div><div class="dt-cards">')
            for j,(slug,tn,pc,tag) in enumerate(items):
                grid+=(f'<a class="dt-card dt-card--white" href="{slug}.html" aria-label="Storage in {tn} ({pc})">'
                       f'<span class="dt-top"><span class="dt-ic">{LOC_GPIN}</span>'
                       f'<span class="dt-tt"><h3 class="dt-name">Storage in {tn}</h3><span class="dt-pc">{pc}</span></span></span>'
                       f'<span class="dt-tag">{tag}</span>'
                       f'<span class="dt-cta">View {tn} storage {LOC_ARR}</span></a>')
            grid+='</div></div>'
        out=(LOC_CSS+'<section class="loc-sec relative w-full pt-10 lg:pt-20 pb-10 lg:pb-20 border-border"><span class="loc-blob"></span><div class="container"><div class="loc-wrap">'
             '<div class="loc-head"><span class="loc-ey">Areas we cover</span>'
             '<h2 class="loc-h2">Find Storage in Your Sussex Town</h2><div class="loc-rule"></div>'
             '<p class="loc-lead">Everything ships from our family-run hub in Ashington. Tap a pin on the map &mdash; or pick your town from the list &mdash; for local storage details, or get a free quote.</p></div>'
             '<div class="loc-stats">'
             f'<div class="loc-stat"><span class="loc-stat-n">{total}</span><span class="loc-stat-l">Towns covered</span></div>'
             f'<div class="loc-stat"><span class="loc-stat-n">{len(area_groups)}</span><span class="loc-stat-l">Local areas</span></div>'
             '<div class="loc-stat"><span class="loc-stat-n">&pound;15</span><span class="loc-stat-l">Per week, no deposit</span></div>'
             '<div class="loc-stat"><span class="loc-stat-n">24hr</span><span class="loc-stat-l">Redelivery notice</span></div>'
             '</div>'
             '<div class="lm-mapwrap">'+leaflet+'</div>'+grid+
             '<div class="loc-more"><p class="loc-more-h">Also serving across West Sussex</p><div class="loc-pills">'
             +"".join(f'<span class="loc-pill">{t}</span>' for t in more_towns)+'</div>'
             '<p class="loc-ask">Don&rsquo;t see your town? <a href="contact.html">Just ask</a> &mdash; if it&rsquo;s in West Sussex, we almost certainly cover it.</p></div>'
             '</div></div></section>')
        return out
    area_itemlist=('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"ItemList","name":"Storage locations across West Sussex",
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":"Storage in "+tn,"url":BASE+slug+".html"}
          for i,(slug,tn,pc,tag) in enumerate([x for _,items in area_groups for x in items])]},ensure_ascii=False)+'</script>')
    P.append(dict(file="areas-we-cover.html",slug="areas",nav="Areas We Cover",
      title="Storage Across West Sussex | Wolves Storage Sussex",
      meta="Managed storage across West Sussex — Ashington, Storrington, Pulborough, Horsham, Worthing & more. We collect & redeliver from £15/week.",
      hero=IMG(HERO_AERIAL[0]),extra_schema=area_itemlist,
      sections=[
        hero(IMG(HERO_AERIAL[0]),HERO_AERIAL[1],"Storage Across West Sussex",
          "Based in Ashington, we collect from and redeliver across West Sussex &mdash; the managed model means we come to you, wherever you are. Find your town below.",
          ["We collect and redeliver to your door","Dedicated pages for towns across West Sussex","Local, family-run service","From &pound;15/week, no deposit"],big=False),
        area_cards(),
        split("bg-white","Local &amp; Family-Run Matters",["Because we&rsquo;re based in the heart of West Sussex, we know the area inside out &mdash; and we treat your belongings like our own.","The managed model means there&rsquo;s no unit to drive to: we come to you, pack and seal everything, and bring it back on 24 hours&rsquo; notice."],IMG("gallery-van.webp"),"Wolves storage van serving towns across West Sussex"),
        ('<style>'
         '.cc-sec{position:relative;background:#F7F5EF}'
         '.cc-wrap{max-width:74rem;margin:0 auto}'
         '.cc-grid{display:grid;grid-template-columns:1fr;gap:2.2rem}'
         '@media(min-width:980px){.cc-grid{grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:3.4rem;align-items:start}}'
         '@media(min-width:980px){.cc-aside{position:sticky;top:2rem}}'
         '.cc-eyebrow{display:inline-flex;align-items:center;gap:.6rem;color:#FC9700;font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.8rem}'
         '.cc-eyebrow::before{content:"";width:28px;height:2px;background:#FC9700;display:inline-block}'
         '.cc-h2{font-size:clamp(1.9rem,4.2vw,2.7rem);line-height:1.08;font-weight:800;color:#23282d;margin:1rem 0 0;letter-spacing:-.01em}'
         '.cc-h2 em{font-style:normal;color:#FC9700}'
         '.cc-lead{margin-top:1.4rem;font-size:1.12rem;line-height:1.72;color:#404952}'
         '.cc-lead::first-letter{float:left;font-size:3.6rem;line-height:.82;font-weight:800;color:#FC9700;margin:.3rem .6rem 0 0}'
         '.cc-lead a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.55);text-underline-offset:3px}'
         '.cc-lead a:hover{color:#FC9700}'
         '.cc-cta{display:inline-flex;align-items:center;gap:.5rem;margin-top:1.7rem;background:#FC9700;color:#fff;font-weight:800;font-size:.95rem;padding:.85rem 1.5rem;border-radius:.7rem;text-decoration:none;box-shadow:0 12px 26px -12px rgba(252,151,0,.7);transition:transform .15s ease,box-shadow .15s ease}'
         '.cc-cta svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .15s ease}'
         '.cc-cta:hover{transform:translateY(-2px);box-shadow:0 16px 32px -12px rgba(252,151,0,.8)}'
         '.cc-cta:hover svg{transform:translateX(3px)}'
         '.cc-trust{list-style:none;margin:1.7rem 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.55rem 1.1rem}'
         '.cc-trust li{display:inline-flex;align-items:center;gap:.45rem;font-size:.82rem;font-weight:700;color:#5a636c}'
         '.cc-trust li::before{content:"";width:6px;height:6px;border-radius:50%;background:#FC9700;flex:none}'
         '.cc-body p{font-size:1.02rem;line-height:1.78;color:#46505a;margin:0 0 1.15rem}'
         '.cc-body p:last-child{margin-bottom:0}'
         '@media(min-width:980px){.cc-body{border-left:1px solid rgba(35,40,45,.13);padding-left:3.4rem}}'
         '.cc-body strong{color:#FC9700;font-weight:800;letter-spacing:.01em}'
         '.cc-body a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.5);text-underline-offset:3px}'
         '.cc-body a:hover{color:#FC9700}'
         '@media(prefers-reduced-motion:reduce){.cc-cta,.cc-cta svg{transition:none}.cc-cta:hover{transform:none}}'
         '</style>'
         '<section class="cc-sec relative w-full pt-10 lg:pt-20 pb-10 lg:pb-20 border-border"><div class="container"><div class="cc-wrap"><div class="cc-grid">'
         '<div class="cc-aside">'
         '<span class="cc-eyebrow">County-wide coverage</span>'
         '<h2 class="cc-h2">Local Storage in <em>Every Corner</em> of West Sussex</h2>'
         '<p class="cc-lead">Because every order is collected and redelivered, where you live never limits the storage you can get. From our base in <a href="storage-ashington.html">Ashington</a> we run our own vans right across West Sussex and just over the county line &mdash; so whether you&rsquo;re in a town-centre flat, a Downland village or out on the coast, the same fully managed service comes to your door. There&rsquo;s no unit to drive to and no mileage to worry about: we bring the materials, pack and seal your belongings into their own wooden container, and store them in our alarmed, 24/7 CCTV warehouse.</p>'
         '<a class="cc-cta" href="contact.html">Get a free quote <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg></a>'
         '<ul class="cc-trust"><li>Family-run since 2016</li><li>LAPADA accredited</li><li>Checkatrade verified</li><li>24/7 CCTV monitored</li></ul>'
         '</div>'
         '<div class="cc-body">'
         '<p>Our regular collection routes cover the <strong>RH postcodes</strong> around <a href="storage-horsham.html">Horsham</a>, <a href="storage-crawley.html">Crawley</a> and the Mid Sussex towns, the <strong>BN postcodes</strong> along the <a href="storage-worthing.html">Worthing</a>, <a href="storage-shoreham-by-sea.html">Shoreham</a> and <a href="storage-brighton.html">Brighton</a> coast, the <strong>PO postcodes</strong> around <a href="storage-bognor-regis.html">Bognor Regis</a> and <a href="storage-chichester.html">Chichester</a>, and the <strong>GU villages</strong> near <a href="storage-petworth.html">Petworth</a> and <a href="storage-midhurst.html">Midhurst</a>. If your town isn&rsquo;t listed above, it&rsquo;s almost certainly still on a route we already drive &mdash; just ask.</p>'
         '<p>Households between moves, downsizers, landlords turning over rentals, businesses freeing up floor space and students storing over the holidays all use the same flexible service. Choose <a href="short-term-storage.html">short-term storage</a> for a move or renovation, <a href="long-term-storage.html">long-term storage</a> for months or years away, <a href="business-storage.html">business storage</a> for stock and archives, or dedicated <a href="furniture-storage.html">furniture storage</a> for the pieces that matter most. Every option is fully insured, starts from just &pound;15 a week with no deposit, and includes collection and redelivery.</p>'
         '<p>We&rsquo;ve stored for West Sussex families since 2016, and being local genuinely matters: we know the lanes, the parking and the access quirks of the towns we serve, and as a family-run, <a href="about.html">LAPADA-accredited</a> and Checkatrade-verified team we treat every collection as if it were our own. See exactly <a href="how-it-works.html">how it works</a>, compare our honest <a href="pricing.html">storage prices</a>, or <a href="contact.html">get a free quote</a> for your town today.</p>'
         '</div>'
         '</div></div></div></section>'),
        cta_band("Storing in West Sussex? Get a Free Quote",IMG("gallery-warehouse-b.webp")),
      ]))
    # GALLERY
    P.append(dict(file="gallery.html",slug="gallery",nav="Gallery",
      title="Storage Gallery West Sussex | Wolves Storage Sussex",
      meta="Photos of the Wolves Storage Sussex facility, containers, team and fleet — secure, alarmed, fully insured storage in West Sussex from £15/week.",
      hero=IMG(HERO_ANTIQUE[0]),
      sections=[
        hero(IMG(HERO_ANTIQUE[0]),HERO_ANTIQUE[1],"Our West Sussex Storage Facility",
          "A look inside our secure, alarmed facility &mdash; from our containers and forklift to the friendly family team and fleet.",
          ["Secure, alarmed &amp; 24/7 CCTV","Clean, dry wooden containers","Family-run, LAPADA accredited","From &pound;15/week, no deposit"],big=False),
        gallery([
          (IMG("wolves-van-loading-at-storage-facility.webp"),"Wolves Storage Sussex Luton van loading at our secure West Sussex storage facility","Our secure storage facility"),
          (IMG("gallery-warehouse-a.webp"),"Sealed wooden storage containers stacked inside the alarmed Wolves Storage Sussex warehouse","Sealed containers, securely stacked"),
          (IMG("wolves-operator-forklift-storage-containers.webp"),"A Wolves Storage Sussex operator moving sealed storage containers by forklift","Containers handled by forklift"),
          (IMG("loading-box-up-ramp-into-van.webp"),"Wolves Storage Sussex movers loading packed boxes up the ramp into the van","Door-to-door collection"),
          (IMG("team-positioning-wooden-storage-container.webp"),"Wolves Storage Sussex movers positioning a sealed wooden storage container","Positioning a storage container"),
          (IMG("gallery-warehouse-b.webp"),"Inside the dry, alarmed Wolves Storage Sussex container warehouse","Inside our alarmed warehouse"),
          (IMG("furniture-wrapped-furni-soft-dining-set.webp"),"A dining table and chairs wrapped in Furni-soft padding by Wolves Storage Sussex","Furniture wrapped with care"),
          (IMG("wrapping-framed-picture-furni-soft.webp"),"A Wolves Storage Sussex packer wrapping a framed picture in Furni-soft padding","Artwork wrapped for storage"),
          (IMG("white-glove-antique-painting-handling.webp"),"Wolves Storage Sussex team handling an antique painting with white gloves","Specialist antique handling"),
          (IMG("carrying-furniture-past-storage-van.webp"),"A Wolves Storage Sussex mover carrying furniture past the branded van at a customer&rsquo;s home","Collected from your door"),
          (IMG("careful-packing-sussex-home-removal.webp"),"The Wolves Storage Sussex van fleet ready to collect across West Sussex","Our West Sussex fleet"),
          (IMG("wolves-removals-team-fleet-vans.webp"),"The family-run Wolves Storage Sussex team in front of the van fleet","Our family-run team"),
        ]),
        cta_band("Like What You See? Get a Free Quote",IMG("gallery-warehouse-b.webp")),
      ]))
    # ABOUT
    P.append(dict(file="about.html",slug="about",nav="About",
      title="About Wolves Storage Sussex | West Sussex Storage",
      meta="Family-run, LAPADA-accredited storage business in Ashington, West Sussex with 10+ years' experience. Fully insured, 24/7 CCTV.",
      hero=IMG(HERO_VAN_COLLECT[0]),faqs=[("Are you insured and accredited?","Yes &mdash; fully insured, LAPADA accredited and Checkatrade members."),("How long have you been going?","Over 10 years serving West Sussex as a family-run business.")],
      sections=[
        hero(IMG(HERO_VAN_COLLECT[0]),HERO_VAN_COLLECT[1],"A Trusted Name in West Sussex Storage",
          "Wolves Storage Sussex is part of the family-run Wolves Removals business, serving West Sussex for over a decade from our base in Ashington.",
          ["Family-run, 10+ years&rsquo; experience","LAPADA accredited &amp; Checkatrade","Fully insured, 24/7 CCTV","Trusted by Sussex families &amp; businesses"],big=False),
        split("bg-white","Our Story",["What began as a local removals business grew into trusted, fully managed storage &mdash; built on the same family values of care, honesty and genuine local service.","Today we look after the belongings of hundreds of West Sussex families and businesses, from a few boxes to entire homes."],IMG("gallery-loading.webp"),"Wolves team loading a storage container"),
        split("bg-lightgrey","Why You Can Trust Us",["LAPADA accreditation means we&rsquo;re trusted to pack, store and handle high-value items. Add full insurance, 24/7 CCTV and an alarmed facility, and your belongings are in safe hands.","We&rsquo;re trusted by local estate agents and rated 5.0 from hundreds of reviews."],IMG("gallery-clipboard.webp"),"Wolves Removals and Storage branded clipboard",reverse=True),
        """<style>
.ab-section{background:#F7F5EF;color:#46505a;padding:4.5rem 1.25rem;line-height:1.65}
.ab-wrap{max-width:1080px;margin:0 auto}
.ab-eyebrow{display:inline-flex;align-items:center;gap:.85rem;font-size:.78rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#FC9700;margin:0 0 1.1rem}
.ab-eyebrow::before{content:"";display:inline-block;width:28px;height:2px;background:#FC9700}
.ab-h2{font-size:clamp(2rem,4.6vw,3.1rem);line-height:1.08;font-weight:800;color:#23282d;letter-spacing:-.01em;margin:0 0 1.6rem;max-width:20ch}
.ab-h2 em{font-style:normal;color:#FC9700}
.ab-lead{font-size:clamp(1.12rem,1.9vw,1.32rem);line-height:1.6;color:#3a444d;max-width:62ch;margin:0 0 2.2rem}
.ab-lead::first-letter{float:left;font-size:3.6rem;line-height:.78;font-weight:800;color:#FC9700;padding:.3rem .6rem 0 0}
.ab-feature{display:grid;grid-template-columns:1fr;gap:1.9rem;padding:2.4rem 0 0;border-top:1px solid rgba(35,40,45,.13)}
.ab-figure{margin:0}
.ab-figure img{display:block;width:100%;height:auto;border-radius:6px;box-shadow:0 18px 40px -22px rgba(35,40,45,.45)}
.ab-cap{display:block;margin-top:.7rem;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:#7d8790;font-weight:600}
.ab-kicker{display:block;font-size:.78rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#FC9700;margin-bottom:.7rem}
.ab-h3{font-size:clamp(1.35rem,2.4vw,1.85rem);line-height:1.15;font-weight:800;color:#23282d;letter-spacing:-.01em;margin:0 0 .9rem}
.ab-body{margin:0;max-width:60ch;color:#46505a}
.ab-body strong{color:#FC9700;font-weight:700}
.ab-body a{color:#23282d;font-weight:700;text-decoration:underline;text-decoration-color:rgba(252,151,0,.5);text-underline-offset:3px;transition:color .15s}
.ab-body a:hover{color:#FC9700}
.ab-cta{display:inline-flex;align-items:center;gap:.55rem;margin-top:1.6rem;background:#FC9700;color:#fff;font-weight:700;font-size:1rem;letter-spacing:.01em;padding:.85rem 1.7rem;border-radius:7px;text-decoration:none;box-shadow:0 12px 24px -12px rgba(252,151,0,.7);transition:transform .15s,box-shadow .15s}
.ab-cta svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .15s}
.ab-cta:hover{transform:translateY(-2px);box-shadow:0 16px 30px -12px rgba(252,151,0,.8)}
.ab-cta:hover svg{transform:translateX(3px)}
.ab-trust{list-style:none;margin:1.5rem 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.55rem 1.15rem}
.ab-trust li{display:inline-flex;align-items:center;gap:.45rem;font-size:.82rem;font-weight:700;color:#5a636c}
.ab-trust li::before{content:"";width:6px;height:6px;border-radius:50%;background:#FC9700;flex:none}
.ab-stats{display:flex;flex-wrap:wrap;border-top:1px solid rgba(35,40,45,.13);border-bottom:1px solid rgba(35,40,45,.13);margin:3.5rem 0;padding:0}
.ab-stat{flex:1 1 0;min-width:160px;padding:1.7rem 1.5rem;border-left:1px solid rgba(35,40,45,.13)}
.ab-stat:first-child{border-left:0}
.ab-stat b{display:block;font-size:clamp(1.7rem,3.2vw,2.4rem);font-weight:800;color:#FC9700;line-height:1;letter-spacing:-.01em}
.ab-stat span{display:block;margin-top:.5rem;font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:#7d8790;font-weight:600}
.ab-topics{margin-top:1rem}
.ab-topic{display:grid;grid-template-columns:1fr;gap:1.6rem;padding:2.9rem 0;border-top:1px solid rgba(35,40,45,.13)}
.ab-num{display:block;font-size:clamp(3.4rem,7vw,5.4rem);font-weight:800;line-height:.8;color:rgba(252,151,0,.2);letter-spacing:-.02em;margin-bottom:.6rem}
.ab-end{text-align:center;padding:3rem 0 0;border-top:1px solid rgba(35,40,45,.13);margin-top:1rem}
.ab-end .ab-cta{margin-top:0}
@media(max-width:620px){
.ab-stat{flex:1 1 45%}
.ab-stat:nth-child(2n+1){border-left:0}
.ab-stat:nth-child(n+3){border-top:1px solid rgba(35,40,45,.13)}
}
@media(min-width:880px){
.ab-feature{grid-template-columns:.78fr 1fr;gap:3.2rem;align-items:center}
.ab-topic{grid-template-columns:1fr 1fr;gap:3.2rem;align-items:center}
.ab-topic .ab-text{order:1}
.ab-topic .ab-figure{order:2}
.ab-flip .ab-text{order:2}
.ab-flip .ab-figure{order:1}
}
@media(prefers-reduced-motion:reduce){.ab-cta,.ab-cta svg{transition:none}.ab-cta:hover{transform:none}.ab-cta:hover svg{transform:none}}
</style><section class="ab-section" aria-labelledby="ab-title">
  <div class="ab-wrap">
    <p class="ab-eyebrow">About Wolves Storage Sussex</p>
    <h2 class="ab-h2" id="ab-title">Storage Built on <em>Family Values</em>, Not Self-Service</h2>
    <p class="ab-lead">Wolves Storage Sussex is a family-run, fully managed storage company based at Doryln House on the London Road in Ashington, right in the middle of West Sussex. We&rsquo;ve looked after local people&rsquo;s belongings for over ten years, and in that time one thing hasn&rsquo;t changed: we treat every collection as if it were our own family&rsquo;s. That&rsquo;s the real difference between us and a drive-up self-storage unit &mdash; you get real people who pack, protect and store your things properly, not just a key to an empty metal room.</p>

    <div class="ab-feature">
      <figure class="ab-figure">
        <img src="/images/wolves-operator-forklift-storage-containers.webp" width="1200" height="1600" loading="lazy" alt="A Wolves Storage Sussex operator moving sealed storage containers by forklift in our secure West Sussex warehouse">
      </figure>
      <div class="ab-text">
        <span class="ab-num" aria-hidden="true">01</span>
        <span class="ab-kicker">How we work</span>
        <h3 class="ab-h3">Fully managed, container-based storage</h3>
        <p class="ab-body">Everything we store goes into its own clean, dry wooden container of around 250 cubic feet &mdash; roughly the contents of a one-bedroom flat. We bring the packing materials to you, wrap and load your belongings, seal the container and bring it back to our warehouse. When you want it back, we redeliver to your door on 24 hours&rsquo; notice. You never hire a van, drive across town or carry boxes down a shared corridor &mdash; you only ever pay for the space you use, from just &pound;15 a week with no deposit.</p>
        <a class="ab-cta" href="contact.html">Get a free quote <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg></a>
        <ul class="ab-trust">
          <li>Family-run since 2016</li>
          <li>LAPADA accredited</li>
          <li>Checkatrade verified</li>
          <li>Fully insured</li>
        </ul>
      </div>
    </div>

    <div class="ab-topics">
      <article class="ab-topic">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">02</span>
          <h3 class="ab-h3">A secure, monitored West Sussex facility</h3>
          <p class="ab-body">Our Ashington warehouse is dry, ventilated and alarmed, with 24/7 CCTV and staff-controlled access &mdash; not a public self-access site. Your container stays sealed for its entire stay, protected from the damp, dust and temperature swings that affect unheated metal units through a Sussex winter. Whether you&rsquo;re storing for a few weeks between moves or for several years while you work away, your belongings come back in the same condition they arrived in.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/gallery-warehouse-b.webp" width="900" height="1200" loading="lazy" alt="Inside the dry, alarmed Wolves Storage Sussex container warehouse">
          <figcaption class="ab-cap">Inside our alarmed store</figcaption>
        </figure>
      </article>

      <article class="ab-topic ab-flip">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">03</span>
          <h3 class="ab-h3">Accredited, insured and genuinely trusted</h3>
          <p class="ab-body">We&rsquo;re accredited by LAPADA &mdash; the Association of Art &amp; Antiques Dealers &mdash; so we&rsquo;re trusted to handle fragile, antique and high-value pieces, not just boxes. We&rsquo;re also Checkatrade-verified and fully insured throughout, and we&rsquo;re recommended by respected local estate agents across the region. Our customers have rated us 5.0 out of 5 across hundreds of reviews, and most of our work comes from word of mouth and repeat bookings &mdash; the clearest sign we get the small details right.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/white-glove-antique-painting-handling.webp" width="600" height="564" loading="lazy" alt="Wolves Storage Sussex team handling an antique painting with white gloves">
          <figcaption class="ab-cap">Specialist antique care</figcaption>
        </figure>
      </article>

      <article class="ab-topic">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">04</span>
          <h3 class="ab-h3">Whatever you need to store</h3>
          <p class="ab-body">We store for every kind of situation: families between house moves or renovations, downsizers keeping the pieces they&rsquo;re not ready to part with, people working away or abroad, landlords turning over rentals, and businesses freeing up expensive floor space for stock and archives. We also handle furniture, antiques and one-off valuables with specialist care. Whatever the reason, you get the same flexible terms &mdash; store for a single week or several years, with no long tie-in and no hidden charges.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/hero-containers-van.webp" width="1440" height="1080" loading="lazy" alt="Sealed wooden storage containers and the Wolves Storage Sussex van at our West Sussex facility">
          <figcaption class="ab-cap">Stored your way</figcaption>
        </figure>
      </article>
    </div>

    <div class="ab-stats">
      <div class="ab-stat"><b>&pound;15</b><span>per week, no deposit</span></div>
      <div class="ab-stat"><b>250 cu ft</b><span>per private container</span></div>
      <div class="ab-stat"><b>5.0&#9733;</b><span>from 478 reviews</span></div>
      <div class="ab-stat"><b>24/7</b><span>CCTV &amp; fully insured</span></div>
    </div>

    <div class="ab-topics">
      <article class="ab-topic ab-flip">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">05</span>
          <h3 class="ab-h3">Local to every corner of West Sussex</h3>
          <p class="ab-body">From our central Ashington base we collect from and redeliver across the whole county and just over the border &mdash; from <a href="storage-horsham.html">Horsham</a> and <a href="storage-crawley.html">Crawley</a> in the north to <a href="storage-worthing.html">Worthing</a>, <a href="storage-littlehampton.html">Littlehampton</a> and <a href="storage-chichester.html">Chichester</a> on the coast. See every <a href="areas-we-cover.html">area we cover</a>, explore our <a href="storage-solutions.html">storage solutions</a>, or <a href="contact.html">get a free quote</a> and our family team will be in touch within 24 hours.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/wolves-van-loading-at-storage-facility.webp" width="1600" height="1200" loading="lazy" alt="Wolves Storage Sussex Luton van loading at our secure West Sussex facility">
          <figcaption class="ab-cap">Door-to-door across Sussex</figcaption>
        </figure>
      </article>

      <article class="ab-topic">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">06</span>
          <h3 class="ab-h3">Why managed storage beats a self-storage unit</h3>
          <p class="ab-body">It&rsquo;s easy to assume a drive-up self-storage unit is the cheaper option, but the costs quietly add up &mdash; van hire, fuel, the hours spent driving back and forth, and paying for floor space you never fully use. With our managed model there&rsquo;s nothing to hire and nothing to carry: collection and redelivery are built into the price, and because we stack sealed containers efficiently in a secure warehouse rather than renting you an oversized room, you only pay for the space your belongings actually take up. It&rsquo;s usually cleaner, more secure and better value &mdash; your things sit in a dry, alarmed building instead of an unheated metal room you have to visit yourself.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/gallery-warehouse-a.webp" width="900" height="1200" loading="lazy" alt="Sealed wooden storage containers stacked inside the alarmed Wolves Storage Sussex warehouse">
          <figcaption class="ab-cap">Sealed &amp; stacked securely</figcaption>
        </figure>
      </article>

      <article class="ab-topic ab-flip">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">07</span>
          <h3 class="ab-h3">Honest pricing and genuinely flexible terms</h3>
          <p class="ab-body">We keep things simple and straightforward, because that&rsquo;s how we&rsquo;d want to be treated. Storage starts at just &pound;15 a week with no deposit and no hidden fees, and terms are flexible and rolling &mdash; store for a single week between moves or for several years while you&rsquo;re abroad, and extend or end whenever it suits you. Every quote is clear and fixed, you deal with the same family team throughout, and there&rsquo;s never any pressure or obligation. If you&rsquo;re weighing up your options, we&rsquo;ll give you honest, practical advice &mdash; even if that means pointing you somewhere else.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/loading-box-up-ramp-into-van.webp" width="762" height="726" loading="lazy" alt="Wolves Storage Sussex movers loading packed boxes up the ramp into the van">
          <figcaption class="ab-cap">Collected from your door</figcaption>
        </figure>
      </article>

      <article class="ab-topic">
        <div class="ab-text">
          <span class="ab-num" aria-hidden="true">08</span>
          <h3 class="ab-h3">Packed properly, protected throughout</h3>
          <p class="ab-body">Good storage starts with good packing, and that&rsquo;s where a managed service really earns its keep. We bring professional-grade materials to every collection &mdash; double-walled boxes, bubble wrap, furniture blankets, mattress covers and tape &mdash; and our team wraps and loads everything methodically, so nothing shifts, scratches or settles damp over the weeks and months ahead. Sofas and mattresses are covered, mirrors and pictures are corner-protected, and drawers, appliances and flat-pack furniture are secured before they go anywhere near the container. Once a container is full it&rsquo;s sealed and logged, and it isn&rsquo;t opened again until it comes back to you. It&rsquo;s the same standard of care we&rsquo;d want for our own family&rsquo;s belongings &mdash; and a big part of why customers across West Sussex trust us with antiques, electronics, business equipment and the things that simply can&rsquo;t be replaced.</p>
        </div>
        <figure class="ab-figure">
          <img src="/images/furniture-wrapped-furni-soft-dining-set.webp" width="762" height="726" loading="lazy" alt="A dining table and chairs wrapped in Furni-soft padding by Wolves Storage Sussex">
          <figcaption class="ab-cap">Wrapped with care</figcaption>
        </figure>
      </article>
    </div>

    <div class="ab-end">
      <a class="ab-cta" href="contact.html">Get a free quote <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M12 5l7 7-7 7"/></svg></a>
    </div>
  </div>
</section>""",
        faq([("Are you insured and accredited?","Yes &mdash; fully insured, LAPADA accredited and Checkatrade members."),("How long have you been going?","Over 10 years serving West Sussex as a family-run business.")]),
        cta_band("Store With a Family You Can Trust",IMG("gallery-warehouse-b.webp")),
      ]))
    # CONTACT
    P.append(dict(file="contact.html",slug="contact",nav="Contact",
      title="Contact Wolves Storage Sussex | Free Storage Quote",
      meta="Contact Wolves Storage Sussex for a free storage quote within 24 hours. Call 01903 893731 / 07789 390421 or email.",
      hero=IMG(HERO_VAN_COLLECT[0]),
      sections=[
        hero(IMG(HERO_VAN_COLLECT[0]),HERO_VAN_COLLECT[1],"Get a Free Storage Quote",
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
         '<div class="col-span-12 lg:col-span-7"><iframe title="Wolves Storage Sussex location" src="https://www.google.com/maps?q=RH20%203JT&t=&z=13&ie=UTF8&iwloc=&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" class="block w-full rounded-xl shadow-custom" style="border:0;height:380px"></iframe></div></div></div></section>'),
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
      "How Wolves Storage Sussex collects, uses and protects your personal data when you enquire about storage.",
      "Privacy Policy","How we handle and protect your personal information.",PRIVACY_BODY))
    P.append(legal_page("terms.html","Terms &amp; Conditions",
      "Terms & Conditions | Wolves Storage Sussex",
      "The terms for using the Wolves Storage Sussex website, our quotes and storage calculator, intellectual property, liability and governing law.",
      "Terms &amp; Conditions","The terms for using our website and services.",TERMS_BODY))
    # 404
    P.append(dict(file="404.html",slug="404",nav="Page not found",
      title="Page Not Found (404) | Wolves Storage Sussex",
      meta="Sorry, we couldn't find that page. Return to Wolves Storage Sussex for secure managed storage in West Sussex from £15/week.",
      hero=IMG(HERO_VAN_COLLECT[0]),
      sections=[centered("bg-white","Page Not Found","Sorry, we couldn&rsquo;t find that page. Let&rsquo;s get you back to storing safely in West Sussex.",
        f'<div class="flex flex-wrap gap-3 justify-center">{btn("Back to Home","/","px-8 lg:px-10")}{btn("Contact Us","contact.html","px-8 lg:px-10")}</div>')]))

    for d in P:
        if d["slug"] not in ("404","legal") and d["file"]!="contact.html":
            d["sections"].insert(1, TRUSTINDEX_SECTION)
        if d["file"] in WHYUS:
            d["sections"].insert(2, WHYUS[d["file"]])
        if d["file"] in ("pricing.html","storage-size-guide.html"):
            d["sections"].insert(1, CALC_SECTION)
        if d["file"] in CONTAINER_HTML:
            d["sections"].insert(len(d["sections"])-1, CONTAINER_HTML[d["file"]])
        if d["file"] in SILO_PAGES:
            d["sections"].insert(len(d["sections"])-1, all_towns_strip())
    for d in P:
        html=page(d)
        if d["file"]=="404.html":
            html=html.replace('<meta name="robots" content="index, follow">','<meta name="robots" content="noindex, follow">')
            html=html.replace('<h2 class="relative leading-tight text-black">Page Not Found</h2>','<h1 class="relative leading-tight text-black">Page Not Found</h1>')
        html=fix_amps(html)
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
        sm+=f'  <url><loc>{BASE}{d["file"]}</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n'
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
          f"- [Home]({BASE}): {home['meta']}\n\n")
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
