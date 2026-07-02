// ============================================================================
//  ADD TO THE TOP of functions/api/contact.js — import + PDF helpers.
//  Place the import as the FIRST line of the file (before the existing
//  `const OWNER_TO = ...`). contact.js is already an ESM module (it uses
//  `export async function onRequestPost`), so a top-level import is valid.
//  StandardFonts only => no @pdf-lib/fontkit, no custom TTF => bundle stays
//  ~250KB gzip (< Pages Free 1MB cap). DO NOT add fontkit or a custom font.
// ============================================================================
import { PDFDocument, StandardFonts, rgb } from "pdf-lib";

// ---- brand palette as pdf-lib rgb() (0..1) --------------------------------
// Named PC to avoid colliding with the existing `C` string-hex palette.
const PC = {
  orange: rgb(0.98824, 0.59216, 0),        // #FC9700
  gold:   rgb(0.96471, 0.73333, 0.02353),  // #F6BB06
  grey:   rgb(0.41176, 0.46667, 0.51373),  // #697783
  ink:    rgb(0.14902, 0.14902, 0.14902),  // #262626
  beige:  rgb(0.90980, 0.90196, 0.85490),  // #E8E6DA
  light:  rgb(0.97647, 0.97255, 0.96471),  // #F9F8F6
  border: rgb(0.90588, 0.90588, 0.90588),  // #E7E7E7
  white:  rgb(1, 1, 1),
  greyLt: rgb(0.90, 0.92, 0.94),
};

// ---- WinAnsi-safe text: StandardFonts throw on un-encodable glyphs ---------
function pdfSafe(v) {
  let s = (typeof v === "string" ? v : v == null ? "" : String(v));
  const map = {
    "≈": "approx ", "×": "x", "–": "-", "—": "-",
    "•": "-", "·": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...", "→": "->",
    "★": "*", "☆": "*", "✓": "y", " ": " ",
  };
  s = s.replace(/[≈×–—•·‘’“”…→★☆✓ ]/g,
                m => map[m]);
  // drop anything outside Latin-1 and any control chars (keep \n for splitting).
  // This range EXCLUDES 0x80-0x9F (WinAnsi-unsafe C1 controls) by construction.
  return s.replace(/[^\x20-\x7E\xA1-\xFF\n]/g, "");
}

// ---- Uint8Array -> base64 (no Node Buffer; chunked for safety) ------------
function bytesToBase64(bytes) {
  let bin = "";
  const CH = 0x8000;
  for (let i = 0; i < bytes.length; i += CH) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
  }
  return btoa(bin);
}

// ---- normalise the estimate JSON (object or string) -----------------------
function getEstimate(raw) {
  let e = raw;
  if (typeof e === "string") { try { e = JSON.parse(e); } catch { e = null; } }
  if (!e || typeof e !== "object") e = {};
  if (!Array.isArray(e.inventory)) e.inventory = [];
  return e;
}

// ===========================================================================
//  generatePdf(data) -> Promise<Uint8Array>
//  data: { first,last,email,phone, addr1,addr2,town,postcode,
//          enquiry, collect, estimate (object|JSON string), message, submitted }
// ===========================================================================
async function generatePdf(data) {
  const PAGE = { w: 595.28, h: 841.89 };
  const M = 44;                       // side margin
  const CW = PAGE.w - M * 2;          // content width (507.28)
  const HEADER_H = 118, FOOTER_H = 46;
  const TOP_Y = PAGE.h - HEADER_H - 26;
  const BOT_Y = FOOTER_H + 26;

  const pdf = await PDFDocument.create();
  pdf.setTitle("Storage Enquiry - Wolves Storage Sussex");
  pdf.setAuthor("Wolves Storage Sussex");
  pdf.setProducer("Wolves Storage Sussex enquiry system");
  pdf.setCreator("sussexstoragecompany.co.uk");

  const F = {
    reg:  await pdf.embedFont(StandardFonts.Helvetica),
    bold: await pdf.embedFont(StandardFonts.HelveticaBold),
    ital: await pdf.embedFont(StandardFonts.HelveticaOblique),
  };

  // logo — runtime fetch + embedPng, never fatal
  let logo = null;
  try {
    const r = await fetch("https://www.sussexstoragecompany.co.uk/images/email-logo.png");
    if (r.ok) logo = await pdf.embedPng(await r.arrayBuffer());
  } catch { /* keep going without the logo */ }

  // ---- shared cursor state --------------------------------------------------
  let page, y;

  const draw = (str, x, yy, o = {}) =>
    page.drawText(pdfSafe(str), {
      x, y: yy, size: o.size || 10, font: o.font || F.reg, color: o.color || PC.ink,
    });

  const textW = (str, font, size) => font.widthOfTextAtSize(pdfSafe(str), size);

  function wrap(str, font, size, maxW) {
    const words = pdfSafe(str).split(/\s+/).filter(Boolean);
    const lines = [];
    let line = "";
    for (let w of words) {
      // hard-break a single word wider than the column
      while (font.widthOfTextAtSize(w, size) > maxW && w.length > 1) {
        let cut = w.length;
        while (cut > 1 && font.widthOfTextAtSize(w.slice(0, cut), size) > maxW) cut--;
        if (line) { lines.push(line); line = ""; }
        lines.push(w.slice(0, cut));
        w = w.slice(cut);
      }
      const t = line ? line + " " + w : w;
      if (line && font.widthOfTextAtSize(t, size) > maxW) { lines.push(line); line = w; }
      else line = t;
    }
    if (line) lines.push(line);
    return lines.length ? lines : [""];
  }

  function drawHeader(pg) {
    pg.drawRectangle({ x: 0, y: PAGE.h - HEADER_H, width: PAGE.w, height: HEADER_H, color: PC.orange });
    pg.drawRectangle({ x: 0, y: PAGE.h - HEADER_H - 4, width: PAGE.w, height: 4, color: PC.gold });
    // logo chip (white for contrast)
    const chipW = 150, chipH = 66;
    const cx = M, cy = PAGE.h - HEADER_H / 2 - chipH / 2;
    if (logo) {
      pg.drawRectangle({ x: cx, y: cy, width: chipW, height: chipH, color: PC.white });
      const s = logo.scaleToFit(chipW - 22, chipH - 18);
      pg.drawImage(logo, { x: cx + (chipW - s.width) / 2, y: cy + (chipH - s.height) / 2, width: s.width, height: s.height });
    } else {
      pg.drawText("WOLVES STORAGE SUSSEX", { x: cx, y: PAGE.h - HEADER_H / 2 - 6, size: 15, font: F.bold, color: PC.white });
    }
    // NAP block, right-aligned white
    const rx = PAGE.w - M;
    const rows = [
      { t: "Wolves Storage Sussex", f: F.bold, s: 13 },
      { t: "Doryln House, London Road, Ashington", f: F.reg, s: 9 },
      { t: "Pulborough, West Sussex RH20 3JT", f: F.reg, s: 9 },
      { t: "01903 893731  -  info@sussexstoragecompany.co.uk", f: F.reg, s: 9 },
    ];
    let ly = PAGE.h - 40;
    for (const r of rows) {
      pg.drawText(pdfSafe(r.t), { x: rx - textW(r.t, r.f, r.s), y: ly, size: r.s, font: r.f, color: PC.white });
      ly -= r.s + 4;
    }
  }

  function drawFooter(pg) {
    pg.drawRectangle({ x: 0, y: 0, width: PAGE.w, height: FOOTER_H, color: PC.grey });
    pg.drawRectangle({ x: 0, y: FOOTER_H, width: PAGE.w, height: 3, color: PC.orange });
    pg.drawText(pdfSafe("Wolves Storage Sussex  -  part of the Wolves Removals family"),
      { x: M, y: FOOTER_H - 16, size: 9, font: F.bold, color: PC.white });
    pg.drawText(pdfSafe("01903 893731   -   info@sussexstoragecompany.co.uk   -   sussexstoragecompany.co.uk"),
      { x: M, y: FOOTER_H - 28, size: 8, font: F.reg, color: PC.greyLt });
    pg.drawText(pdfSafe("LAPADA accredited  -  Checkatrade  -  Fully insured"),
      { x: M, y: FOOTER_H - 39, size: 8, font: F.reg, color: PC.greyLt });
  }

  function newPage() {
    page = pdf.addPage([PAGE.w, PAGE.h]);
    drawHeader(page);
    drawFooter(page);
    y = TOP_Y;
  }
  const ensure = (h) => { if (y - h < BOT_Y) newPage(); };

  function sectionTitle(label) {
    ensure(34);
    y -= 8;
    draw(String(label).toUpperCase(), M, y, { font: F.bold, size: 11, color: PC.grey });
    y -= 6;
    page.drawRectangle({ x: M, y: y, width: CW, height: 2, color: PC.gold });
    y -= 16;
  }

  function kvRow(label, value) {
    const labelW = 120, valX = M + labelW, valMaxW = CW - labelW;
    const src = Array.isArray(value) ? value : [value];
    let lines = [];
    src.forEach(v => wrap((v === "" || v == null) ? "" : String(v), F.reg, 11, valMaxW).forEach(l => lines.push(l)));
    if (!lines.length || (lines.length === 1 && !lines[0])) lines = ["-"];
    const rowH = lines.length * 15 + 10;
    ensure(rowH + 4);
    const top = y;
    draw(label, M, top - 12, { font: F.bold, size: 10, color: PC.grey });
    let ly = top - 12;
    for (const l of lines) { draw(l, valX, ly, { font: F.reg, size: 11, color: PC.ink }); ly -= 15; }
    const b = top - rowH;
    page.drawLine({ start: { x: M, y: b }, end: { x: M + CW, y: b }, thickness: 0.75, color: PC.border });
    y = b - 6;
  }

  function estimatePanel(est) {
    const pods = Math.ceil(Number(est.pods) || 0);
    const cuft = Number(est.cuft) || 0, cbm = Number(est.cbm) || 0;
    const rows = [];
    const container = pods
      ? "approx " + pods + " container" + (pods === 1 ? "" : "s") +
        (cuft ? "   ~" + cuft + " cu ft" : "") + (cbm ? "  /  " + cbm + " cu m" : "")
      : "";
    if (container)     rows.push(["Container size", container]);
    if (est.moveIn)    rows.push(["Move-in date", String(est.moveIn)]);
    if (est.moveOut)   rows.push(["Move-out date", String(est.moveOut)]);
    if (est.duration)  rows.push(["Duration", String(est.duration)]);
    if (est.cover)     rows.push(["Cover level", String(est.cover)]);

    const hasStats = pods > 0 || !!est.estCost;
    if (!hasStats && !rows.length) return;

    const padX = 16;
    const topPad = 12, statH = hasStats ? 48 : 0;
    const gap = rows.length ? 8 : 0;
    const rowsH = rows.length * 18, botPad = 12;
    const panelH = topPad + statH + gap + rowsH + botPad;

    ensure(panelH + 8);
    const top = y, bottom = top - panelH;

    page.drawRectangle({ x: M, y: bottom, width: CW, height: panelH, color: PC.light, borderColor: PC.border, borderWidth: 1 });
    page.drawRectangle({ x: M, y: top - 4, width: CW, height: 4, color: PC.orange });

    if (hasStats) {
      if (pods > 0) {
        draw(String(pods), M + padX, top - topPad - 30, { font: F.bold, size: 28, color: PC.orange });
        draw("CONTAINERS", M + padX, top - topPad - 44, { font: F.bold, size: 8, color: PC.grey });
      }
      if (est.estCost) {
        const cx = M + CW / 2;
        draw(String(est.estCost), cx, top - topPad - 26, { font: F.bold, size: 18, color: PC.ink });
        draw("ESTIMATED COST", cx, top - topPad - 44, { font: F.bold, size: 8, color: PC.grey });
      }
    }

    let ry = top - topPad - statH - gap;
    if (rows.length && hasStats) {
      page.drawLine({ start: { x: M + padX, y: ry + 4 }, end: { x: M + CW - padX, y: ry + 4 }, thickness: 0.75, color: PC.border });
    }
    for (const [k, v] of rows) {
      draw(k, M + padX, ry - 12, { font: F.bold, size: 9, color: PC.grey });
      draw(v, M + padX + 120, ry - 12, { font: F.reg, size: 10, color: PC.ink });
      ry -= 18;
    }
    y = bottom - 12;
  }

  function inventoryTable(inv) {
    if (!inv.length) return;
    const count = inv.reduce((a, i) => a + (parseInt(i.qty, 10) || 0), 0);
    sectionTitle("Inventory (" + count + " item" + (count === 1 ? "" : "s") + ")");

    const qtyW = 46, catW = 140, itemW = CW - qtyW - catW;
    const header = () => {
      ensure(24);
      const top = y;
      page.drawRectangle({ x: M, y: top - 20, width: CW, height: 20, color: PC.beige });
      draw("ITEM", M + 10, top - 14, { font: F.bold, size: 9, color: PC.grey });
      draw("CATEGORY", M + itemW + 8, top - 14, { font: F.bold, size: 9, color: PC.grey });
      draw("QTY", M + CW - 10 - textW("QTY", F.bold, 9), top - 14, { font: F.bold, size: 9, color: PC.grey });
      y = top - 20;
    };
    header();

    let zebra = 0;
    for (const it of inv) {
      const nameLines = wrap(String(it.name || "-"), F.reg, 10, itemW - 18);
      const catLines = wrap(String(it.cat || "-"), F.reg, 9, catW - 12);
      const n = Math.max(nameLines.length, catLines.length, 1);
      const rowH = n * 13 + 8;
      if (y - rowH < BOT_Y) { newPage(); header(); zebra = 0; }
      const top = y;
      if (zebra % 2 === 1) page.drawRectangle({ x: M, y: top - rowH, width: CW, height: rowH, color: PC.light });
      let ny = top - 12;
      for (const l of nameLines) { draw(l, M + 10, ny, { font: F.reg, size: 10, color: PC.ink }); ny -= 13; }
      let cyy = top - 12;
      for (const l of catLines) { draw(l, M + itemW + 8, cyy, { font: F.reg, size: 9, color: PC.grey }); cyy -= 13; }
      const qty = String(parseInt(it.qty, 10) || it.qty || 1);
      draw(qty, M + CW - 10 - textW(qty, F.bold, 10), top - 12, { font: F.bold, size: 10, color: PC.orange });
      page.drawLine({ start: { x: M, y: top - rowH }, end: { x: M + CW, y: top - rowH }, thickness: 0.5, color: PC.border });
      y = top - rowH;
      zebra++;
    }
    y -= 6;
  }

  function messageBlock(msg) {
    if (!msg) return;
    sectionTitle("Message");
    const padX = 14, innerW = CW - padX * 2, perLine = 15;
    let lines = [];
    String(msg).split(/\r?\n/).forEach(p => {
      if (!p.trim()) lines.push("");
      else wrap(p, F.reg, 11, innerW).forEach(l => lines.push(l));
    });
    let idx = 0;
    while (idx < lines.length) {
      ensure(perLine + 26);
      const avail = y - BOT_Y;
      const fit = Math.max(1, Math.floor((avail - 20) / perLine));
      const chunk = lines.slice(idx, idx + fit);
      const boxH = chunk.length * perLine + 16;
      const top = y;
      page.drawRectangle({ x: M, y: top - boxH, width: CW, height: boxH, color: PC.light, borderColor: PC.border, borderWidth: 1 });
      page.drawRectangle({ x: M, y: top - boxH, width: 3, height: boxH, color: PC.orange });
      let ly = top - 16;
      for (const l of chunk) { draw(l, M + padX, ly, { font: F.reg, size: 11, color: PC.ink }); ly -= perLine; }
      y = top - boxH - 10;
      idx += chunk.length;
      if (idx < lines.length) newPage();
    }
  }

  // ---- normalise inputs -----------------------------------------------------
  const first = pdfSafe(data.first), last = pdfSafe(data.last);
  const fullName = (first + " " + last).trim() || "-";
  const est = getEstimate(data.estimate != null ? data.estimate : data.inventory);
  const collectTxt = data.collect === "Yes" ? "Yes - collect from the address below"
                   : data.collect === "No"  ? "No - customer will drop off"
                   : (data.collect || "-");
  const addrLines = [data.addr1, data.addr2, [data.town, data.postcode].filter(Boolean).join(" ")]
    .map(x => pdfSafe(x)).filter(Boolean);
  if (!addrLines.length) addrLines.push("-");

  // stable reference from a tiny hash of email + timestamp + name
  const seed = pdfSafe((data.email || "") + (data.submitted || "") + fullName);
  let h = 0; for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  const ref = "WSS-" + h.toString(36).toUpperCase().padStart(6, "0").slice(0, 6);

  const estHasAny = !!(Math.ceil(Number(est.pods) || 0) || Number(est.cuft) ||
    est.moveIn || est.moveOut || est.duration || est.estCost || est.cover);

  // ---- build ---------------------------------------------------------------
  newPage();

  // title block (page 1)
  draw("New Storage Enquiry", M, y - 20, { font: F.bold, size: 24, color: PC.ink });
  y -= 32;
  draw("Reference " + ref, M, y - 10, { font: F.bold, size: 10, color: PC.orange });
  if (data.submitted) {
    const t = "Submitted " + pdfSafe(data.submitted);
    draw(t, M + CW - textW(t, F.reg, 9), y - 10, { font: F.reg, size: 9, color: PC.grey });
  }
  y -= 20;
  page.drawRectangle({ x: M, y: y, width: CW, height: 2, color: PC.gold });
  y -= 14;

  sectionTitle("Enquiry details");
  kvRow("Name", fullName);
  kvRow("Email", data.email || "");
  kvRow("Phone", data.phone || "");
  kvRow("Storing", data.enquiry || "");
  kvRow("Collection", collectTxt);
  kvRow("Address", addrLines);

  if (estHasAny) {
    sectionTitle("Storage estimate");
    draw("From the online size calculator", M, y - 9, { font: F.ital, size: 9, color: PC.grey });
    y -= 16;
    estimatePanel(est);
  }

  inventoryTable(est.inventory);
  messageBlock(data.message || "");

  // stamp "Page X of N" once total is known
  const pages = pdf.getPages(), N = pages.length;
  pages.forEach((pg, i) => {
    const t = "Page " + (i + 1) + " of " + N;
    pg.drawText(t, { x: PAGE.w - M - F.reg.widthOfTextAtSize(t, 8), y: 14, size: 8, font: F.reg, color: PC.white });
  });

  return await pdf.save();   // Uint8Array
}

// Cloudflare Pages Function — handles POST /api/contact
// Sends two branded emails via Resend: an owner notification (to the inbox)
// and a separate customer confirmation. Requires env var RESEND_API_KEY.
//
// SETUP (see EMAIL-SETUP.md):
//   1. Verify the FROM domain (sussexstoragecompany.co.uk) in Resend.
//   2. Cloudflare Pages → Settings → Environment variables → add RESEND_API_KEY.

const OWNER_TO = "info@sussexstoragecompany.co.uk";                       // where enquiries land
const FROM     = "Wolves Storage Sussex <info@sussexstoragecompany.co.uk>"; // verified Resend domain
const SITE     = "https://www.sussexstoragecompany.co.uk";
const LOGO     = SITE + "/images/email-logo.png";
const PHONE    = "01903 893731";

// brand tokens
const C = { ink:"#262626", grey:"#697783", beige:"#E8E6DA", light:"#F9F8F6", orange:"#FC9700", border:"#E7E7E7" };

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); }
  catch { return json({ ok:false, error:"Bad request." }, 400); }

  // honeypot — silently accept (don't tip off bots), send nothing
  if (data.company) return json({ ok:true });

  const first = clean(data.first_name);
  const last  = clean(data.last_name);
  const email = clean(data.email);
  const phone = clean(data.phone);
  const message = clean(data.message);
  const page  = clean(data.page);
  const collect = clean(data.collect_goods);
  const addr = [clean(data.addr1), clean(data.addr2), clean(data.town), clean(data.postcode)].filter(Boolean).join(", ");
  const inventory = clean(data.inventory);
  let submitted = "";
  try { submitted = new Date().toLocaleString("en-GB", { timeZone:"Europe/London", day:"2-digit", month:"short", year:"numeric", hour:"2-digit", minute:"2-digit" }); }
  catch { try { submitted = new Date().toISOString(); } catch {} }
  let enquiry = data.enquiry;
  if (Array.isArray(enquiry)) enquiry = enquiry.join(", ");
  enquiry = clean(enquiry);

  if (!first || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ ok:false, error:"Please provide your name and a valid email address." }, 400);
  }
  if (!env || !env.RESEND_API_KEY) {
    return json({ ok:false, error:"Email is not configured yet." }, 500);
  }

  // Optional env overrides (like wolves-removals) — set CONTACT_TO / CONTACT_FROM in
  // Cloudflare to route notifications to any inbox / change the sender, without editing code.
  const to   = clean(env.CONTACT_TO)   || OWNER_TO;
  const from = clean(env.CONTACT_FROM) || FROM;

  let attachments, pdfStatus = "skip";
  try {
    const bytes = await generatePdf({
      first, last, email, phone,
      addr1: clean(data.addr1), addr2: clean(data.addr2),
      town: clean(data.town), postcode: clean(data.postcode),
      enquiry, collect, estimate: inventory,
      message, submitted,
    });
    const safeName = (last || first || "customer").replace(/[^A-Za-z0-9]/g, "") || "customer";
    attachments = [{
      filename: `storage-enquiry-${safeName}.pdf`,
      content: bytesToBase64(bytes),
      content_type: "application/pdf",
    }];
    pdfStatus = "ok:" + bytes.length;
  } catch (e) { attachments = undefined; pdfStatus = "err:" + (e && e.message ? e.message : String(e)); }

  const owner = await sendEmail(env.RESEND_API_KEY, {
    from,
    to: [to],
    reply_to: email,
    subject: `New storage enquiry — ${first} ${last}`.trim(),
    html: ownerEmail({ first, last, email, phone, enquiry, message, page, collect, addr, inventory, submitted }),
    ...(attachments ? { attachments } : {}),
  });

  // customer confirmation (different email) — best-effort; don't fail the whole request if it bounces
  await sendEmail(env.RESEND_API_KEY, {
    from,
    to: [email],
    reply_to: to,
    subject: "Thanks for contacting Wolves Storage Sussex",
    html: customerEmail({ first, enquiry, message, collect, addr }),
  });

  if (!owner.ok) return json({ ok:false, error:"Could not send your message. Please call us." }, 502);
  return json({ ok:true, v:"pdf-diag-1", pdfStatus });
}

// ---------- helpers ----------
function clean(v){ return (typeof v === "string" ? v : v == null ? "" : String(v)).trim(); }
function esc(s){ return clean(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function nl2br(s){ return esc(s).replace(/\r?\n/g,"<br>"); }
function json(obj, status=200){
  return new Response(JSON.stringify(obj), { status, headers:{ "Content-Type":"application/json" } });
}
async function sendEmail(key, payload){
  try {
    const res = await fetch("https://api.resend.com/emails", {
      method:"POST",
      headers:{ "Authorization":`Bearer ${key}`, "Content-Type":"application/json" },
      body: JSON.stringify(payload),
    });
    return { ok: res.ok, status: res.status };
  } catch { return { ok:false, status:0 }; }
}

// ---------- branded email shell ----------
function shell(inner){
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:${C.light};font-family:Arial,Helvetica,sans-serif;color:${C.ink};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.light};padding:24px 12px;">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:#ffffff;border:1px solid ${C.border};border-radius:14px;overflow:hidden;">
<tr><td style="background:${C.grey};padding:22px 32px;text-align:center;">
<img src="${LOGO}" alt="Wolves Storage Sussex" width="120" style="display:inline-block;width:120px;height:auto;border:0;">
</td></tr>
<tr><td style="height:5px;line-height:5px;font-size:0;background:${C.orange};">&nbsp;</td></tr>
<tr><td style="padding:30px 32px;">${inner}</td></tr>
<tr><td style="padding:20px 32px;background:${C.light};border-top:1px solid ${C.border};font-size:12px;line-height:1.7;color:${C.grey};text-align:center;">
<strong style="color:${C.ink};">Wolves Storage Sussex</strong> &middot; part of the Wolves Removals family<br>
Doryln House, London Road, Ashington, Pulborough, West Sussex RH20 3JT<br>
${PHONE} &middot; ${OWNER_TO}<br>
LAPADA accredited &middot; Checkatrade &middot; Fully insured &middot; 5.0&#9733; from 616 reviews
</td></tr>
</table>
</td></tr></table></body></html>`;
}
function row(label, value){
  if(!value) return "";
  return `<tr>
<td style="padding:10px 0;border-bottom:1px solid ${C.border};font-size:13px;color:${C.grey};font-weight:bold;width:120px;vertical-align:top;">${label}</td>
<td style="padding:10px 0;border-bottom:1px solid ${C.border};font-size:15px;color:${C.ink};">${value}</td>
</tr>`;
}

function estimateBlock(estimateJson){
  if(!estimateJson) return "";
  let d; try { d = JSON.parse(estimateJson); } catch { return ""; }
  const inv = (d && Array.isArray(d.inventory)) ? d.inventory : [];
  const cuft = d.cuft || 0, cbm = d.cbm || 0, pods = Math.ceil(d.pods || 0);
  if(!(pods || cuft || inv.length || d.moveIn || d.duration || d.estCost)) return "";
  const count = inv.reduce((a,i)=>a+(parseInt(i.qty,10)||0),0);
  const container = pods ? `&asymp;${pods} container${pods===1?"":"s"}${cuft?` &middot; ~${cuft} cu ft`:""}${cbm?` / ${cbm} cu m`:""}` : "";
  const rows = [
    ["Container size", container],
    ["Move-in date", esc(d.moveIn)],
    ["Move-out date", esc(d.moveOut)],
    ["Duration", esc(d.duration)],
    ["Estimated cost", esc(d.estCost)],
    ["Cover level", esc(d.cover)],
  ].filter(r=>r[1]).map(r=>row(r[0], r[1])).join("");
  let items = "";
  if(inv.length){
    const groups = {}, order = [];
    inv.forEach(i=>{ const c = clean(i.cat) || "Items"; if(!groups[c]){ groups[c]=[]; order.push(c); } groups[c].push(i); });
    const cats = order.map(c=>{
      const chips = groups[c].map(i=>`<span style="display:inline-block;background:#ffffff;border:1px solid ${C.border};border-radius:14px;padding:4px 10px;margin:0 6px 6px 0;font-size:13px;color:${C.ink};">${esc(i.name)} <b style="color:${C.orange};">&times;${esc(i.qty)}</b></span>`).join("");
      return `<p style="margin:12px 0 6px;font-size:11px;font-weight:bold;letter-spacing:.08em;text-transform:uppercase;color:${C.grey};">${esc(c)}</p>${chips}`;
    }).join("");
    items = `<p style="margin:14px 0 6px;font-size:12px;color:${C.grey};font-weight:bold;">Items (${count})</p><div style="background:#ffffff;border:1px solid ${C.border};border-radius:8px;padding:12px 14px 6px;">${cats}</div>`;
  }
  return `<p style="margin:24px 0 6px;font-size:13px;color:${C.grey};font-weight:bold;">Storage estimate <span style="color:${C.grey};font-weight:normal;">(from the size calculator)</span></p>
<div style="background:${C.light};border:1px solid ${C.border};border-radius:10px;padding:6px 16px 14px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}</table>
${items}</div>`;
}

function ownerEmail({ first, last, email, phone, enquiry, message, page, collect, addr, inventory, submitted }){
  const inner = `
<h1 style="margin:0 0 4px;font-size:20px;color:${C.ink};">New website enquiry</h1>
<p style="margin:0 0 22px;font-size:14px;color:${C.grey};">A customer has submitted the contact form${page ? ` on <strong style="color:${C.ink};">${esc(page)}</strong>` : ""}.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
${row("Name", esc(`${first} ${last}`.trim()))}
${row("Email", `<a href="mailto:${esc(email)}" style="color:${C.orange};text-decoration:none;">${esc(email)}</a>`)}
${row("Phone", phone ? `<a href="tel:${esc(phone)}" style="color:${C.orange};text-decoration:none;">${esc(phone)}</a>` : "")}
${row("Storing", esc(enquiry))}
${row("Address", esc(addr))}
${row("Collection", collect === "Yes" ? "Yes &mdash; collect from the address above" : "No &mdash; customer will drop off")}
</table>
${estimateBlock(inventory)}
${message ? `<p style="margin:22px 0 6px;font-size:13px;color:${C.grey};font-weight:bold;">Message</p>
<div style="background:${C.light};border:1px solid ${C.border};border-radius:10px;padding:16px;font-size:15px;line-height:1.6;color:${C.ink};">${nl2br(message)}</div>` : ""}
<p style="margin:24px 0 4px;font-size:14px;color:${C.grey};">Just hit <strong style="color:${C.ink};">Reply</strong> to respond to ${esc(first)} directly.</p>
${submitted ? `<p style="margin:0;font-size:12px;color:${C.grey};">Submitted ${esc(submitted)}${page ? ` &middot; ${esc(page)}` : ""}</p>` : ""}`;
  return shell(inner);
}

function customerEmail({ first, enquiry, message, collect, addr }){
  const inner = `
<h1 style="margin:0 0 14px;font-size:22px;color:${C.ink};">Thanks, ${esc(first)} — we&rsquo;ve got your enquiry</h1>
<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:${C.ink};">Thanks for getting in touch with <strong>Wolves Storage Sussex</strong>. A member of our friendly, family-run team will get back to you shortly &mdash; and we&rsquo;ll send your free, no-obligation quote within 24 hours.</p>
${(enquiry || message || collect === "Yes") ? `<p style="margin:0 0 8px;font-size:13px;color:${C.grey};font-weight:bold;">What you sent us</p>
<div style="background:${C.light};border:1px solid ${C.border};border-radius:10px;padding:16px;font-size:15px;line-height:1.6;color:${C.ink};">
${enquiry ? `<strong>Storing:</strong> ${esc(enquiry)}<br>` : ""}${(collect === "Yes" && addr) ? `<strong>Collection from:</strong> ${esc(addr)}<br>` : ""}${message ? nl2br(message) : ""}
</div>` : ""}
<p style="margin:22px 0;font-size:15px;line-height:1.6;color:${C.ink};">Need us sooner? Give us a call &mdash; we&rsquo;re happy to help.</p>
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:${C.orange};border-radius:999px;">
<a href="tel:+441903893731" style="display:inline-block;padding:13px 28px;color:#ffffff;font-size:15px;font-weight:bold;text-decoration:none;letter-spacing:.3px;">Call ${PHONE}</a>
</td></tr></table>
<p style="margin:26px 0 0;font-size:15px;color:${C.ink};">Speak soon,<br><strong>The Wolves Storage Sussex team</strong></p>`;
  return shell(inner);
}

// Reject non-POST
export async function onRequestGet(){ return json({ ok:false, error:"Method not allowed." }, 405); }
