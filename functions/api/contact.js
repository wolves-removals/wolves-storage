// ---- Branded enquiry PDF — hand-rolled (no dependencies; bundles anywhere) ----
function bytesToBase64(bytes) {
  let bin = "";
  const CH = 0x8000;
  for (let i = 0; i < bytes.length; i += CH) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
  return btoa(bin);
}
function getEstimate(raw) {
  let e = raw;
  if (typeof e === "string") { try { e = JSON.parse(e); } catch { e = null; } }
  if (!e || typeof e !== "object") e = {};
  if (!Array.isArray(e.inventory)) e.inventory = [];
  return e;
}
function pdfEsc(v) {
  let s = (v == null ? "" : String(v));
  s = s.replace(/[—–]/g, "-").replace(/[’‘]/g, "'").replace(/[“”]/g, '"')
       .replace(/≈/g, "~").replace(/×/g, "x").replace(/·/g, "-").replace(/…/g, "...")
       .replace(/&mdash;|&ndash;/g, "-").replace(/&pound;/g, "£")
       .replace(/&amp;/g, "&").replace(/&rsquo;|&lsquo;/g, "'");
  // keep ASCII + Latin-1 (so £, é, etc. render via WinAnsiEncoding); drop the rest
  s = s.replace(/[^\x20-\x7E\xA1-\xFF]/g, "");
  return s.replace(/([()\\])/g, "\\$1");
}
function pdfWrap(str, maxChars) {
  const words = String(str == null ? "" : str).split(/\s+/).filter(Boolean);
  const lines = []; let line = "";
  for (const w of words) {
    const t = line ? line + " " + w : w;
    if (line && t.length > maxChars) { lines.push(line); line = w; } else line = t;
  }
  if (line) lines.push(line);
  return lines.length ? lines : [""];
}
function generatePdf(data) {
  const W = 595.28, H = 841.89, M = 40;
  const orange = [0.988, 0.592, 0], gold = [0.965, 0.733, 0.024],
        grey = [0.412, 0.467, 0.514], ink = [0.149, 0.149, 0.149],
        white = [1, 1, 1], greyLt = [0.9, 0.92, 0.94];
  let c = "";
  const T = (str, x, y, size, bold, col) => {
    const [r, g, b] = col;
    c += "BT /" + (bold ? "F2" : "F1") + " " + size + " Tf " + r + " " + g + " " + b + " rg " +
         x.toFixed(2) + " " + y.toFixed(2) + " Td (" + pdfEsc(str) + ") Tj ET\n";
  };
  const R = (x, y, w, h, col) => {
    const [r, g, b] = col;
    c += r + " " + g + " " + b + " rg " + x.toFixed(2) + " " + y.toFixed(2) + " " + w.toFixed(2) + " " + h.toFixed(2) + " re f\n";
  };
  // header band (grey = primary brand colour; orange is only an accent)
  R(0, H - 100, W, 100, grey);
  R(0, H - 104, W, 4, orange);
  T("WOLVES STORAGE SUSSEX", M, H - 50, 20, true, white);
  T("Managed storage across West Sussex", M, H - 70, 10, false, white);
  T("01903 893731", W - 210, H - 38, 10, true, white);
  T("info@sussexstoragecompany.co.uk", W - 210, H - 52, 8.5, false, white);
  T("Doryln House, London Road, Ashington", W - 210, H - 66, 8.5, false, white);
  T("Pulborough, West Sussex RH20 3JT", W - 210, H - 80, 8.5, false, white);
  let y = H - 132;
  T("NEW STORAGE ENQUIRY", M, y, 16, true, ink); y -= 6;
  T("Received " + (data.submitted || ""), M, y - 6, 9, false, grey); y -= 26;
  const section = (title) => {
    y -= 4; T(title, M, y, 10, true, grey); y -= 5; R(M, y, W - 2 * M, 1.4, orange); y -= 16;
  };
  const row = (label, val) => {
    if (!val && val !== 0) return;
    T(label, M, y, 9, true, grey);
    const lines = pdfWrap(val, 74);
    T(lines[0], M + 92, y, 10, false, ink);
    for (let i = 1; i < lines.length; i++) { y -= 13; T(lines[i], M + 92, y, 10, false, ink); }
    y -= 16;
  };
  const est = getEstimate(data.estimate);
  const addr = [data.addr1, data.addr2, data.town, data.postcode].filter(Boolean).join(", ");
  section("CONTACT");
  row("Name", ((data.first || "") + " " + (data.last || "")).trim());
  row("Email", data.email);
  row("Phone", data.phone);
  section("ADDRESS & REQUIREMENTS");
  row("Address", addr);
  row("Collection", data.collect === "Yes" ? "Yes - collect from the address above" : "No - customer will drop off");
  row("Storing", data.enquiry);
  const hasEst = est.pods || est.moveIn || est.duration || est.estCost || (est.inventory && est.inventory.length);
  if (hasEst) {
    section("STORAGE ESTIMATE (from the size calculator)");
    row("Containers", est.pods ? ("~" + Math.ceil(est.pods) + "  (" + (est.cuft || 0) + " cu ft" + (est.cbm ? " / " + est.cbm + " cu m" : "") + ")") : "");
    row("Move-in", est.moveIn);
    row("Move-out", est.moveOut);
    row("Duration", est.duration);
    row("Est. cost", est.estCost);
    row("Cover", est.cover);
    if (est.inventory && est.inventory.length) {
      const total = est.inventory.reduce((a, i) => a + (parseInt(i.qty, 10) || 0), 0);
      const items = est.inventory.map(i => (i.name || "item") + " x" + (i.qty || 1)).join(",  ");
      row("Items (" + total + ")", items);
    }
  }
  if (data.message) {
    section("MESSAGE");
    for (const ln of pdfWrap(data.message, 96)) { T(ln, M, y, 10, false, ink); y -= 13; }
  }
  // footer band
  R(0, 0, W, 40, grey);
  R(0, 40, W, 2.5, orange);
  T("Wolves Storage Sussex - part of the Wolves Removals family", M, 24, 8.5, true, white);
  T("01903 893731  -  info@sussexstoragecompany.co.uk  -  LAPADA accredited  -  Fully insured", M, 13, 7.5, false, greyLt);
  // assemble the PDF (offsets are byte-accurate because all content is ASCII)
  const objs = [
    "<< /Type /Catalog /Pages 2 0 R >>",
    "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
    "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    "<< /Length " + c.length + " >>\nstream\n" + c + "endstream",
  ];
  let pdf = "%PDF-1.4\n";
  const offs = [];
  for (let i = 0; i < objs.length; i++) { offs.push(pdf.length); pdf += (i + 1) + " 0 obj\n" + objs[i] + "\nendobj\n"; }
  const xref = pdf.length;
  pdf += "xref\n0 " + (objs.length + 1) + "\n0000000000 65535 f \n";
  for (const o of offs) pdf += String(o).padStart(10, "0") + " 00000 n \n";
  pdf += "trailer\n<< /Size " + (objs.length + 1) + " /Root 1 0 R >>\nstartxref\n" + xref + "\n%%EOF";
  const bytes = new Uint8Array(pdf.length);
  for (let i = 0; i < pdf.length; i++) bytes[i] = pdf.charCodeAt(i) & 0xff;
  return bytes;
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

  let attachments;
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
  } catch { attachments = undefined; }

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
  return json({ ok:true });
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
