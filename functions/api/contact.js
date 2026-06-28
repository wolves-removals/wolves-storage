// Cloudflare Pages Function — handles POST /api/contact
// Sends two branded emails via Resend: an owner notification (to the inbox)
// and a separate customer confirmation. Requires env var RESEND_API_KEY.
//
// SETUP (see EMAIL-SETUP.md):
//   1. Verify the FROM domain (sussexstoragecompany.co.uk) in Resend.
//   2. Cloudflare Pages → Settings → Environment variables → add RESEND_API_KEY.

const OWNER_TO = "info@sussexstoragecompany.co.uk";                       // where enquiries land
const FROM     = "Wolves Storage Sussex <enquiries@sussexstoragecompany.co.uk>"; // verified Resend domain
const SITE     = "https://www.wolvesstoragesussex.co.uk";
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
  let enquiry = data.enquiry;
  if (Array.isArray(enquiry)) enquiry = enquiry.join(", ");
  enquiry = clean(enquiry);

  if (!first || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ ok:false, error:"Please provide your name and a valid email address." }, 400);
  }
  if (!env || !env.RESEND_API_KEY) {
    return json({ ok:false, error:"Email is not configured yet." }, 500);
  }

  const owner = await sendEmail(env.RESEND_API_KEY, {
    from: FROM,
    to: [OWNER_TO],
    reply_to: email,
    subject: `New storage enquiry — ${first} ${last}`.trim(),
    html: ownerEmail({ first, last, email, phone, enquiry, message, page }),
  });

  // customer confirmation (different email) — best-effort; don't fail the whole request if it bounces
  await sendEmail(env.RESEND_API_KEY, {
    from: FROM,
    to: [email],
    reply_to: OWNER_TO,
    subject: "Thanks for contacting Wolves Storage Sussex",
    html: customerEmail({ first, enquiry, message }),
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
LAPADA accredited &middot; Checkatrade &middot; Fully insured &middot; 5.0&#9733; from 478 reviews
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

function ownerEmail({ first, last, email, phone, enquiry, message, page }){
  const inner = `
<h1 style="margin:0 0 4px;font-size:20px;color:${C.ink};">New website enquiry</h1>
<p style="margin:0 0 22px;font-size:14px;color:${C.grey};">A customer has submitted the contact form${page ? ` on <strong style="color:${C.ink};">${esc(page)}</strong>` : ""}.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
${row("Name", esc(`${first} ${last}`.trim()))}
${row("Email", `<a href="mailto:${esc(email)}" style="color:${C.orange};text-decoration:none;">${esc(email)}</a>`)}
${row("Phone", phone ? `<a href="tel:${esc(phone)}" style="color:${C.orange};text-decoration:none;">${esc(phone)}</a>` : "")}
${row("Storing", esc(enquiry))}
</table>
${message ? `<p style="margin:22px 0 6px;font-size:13px;color:${C.grey};font-weight:bold;">Message</p>
<div style="background:${C.light};border:1px solid ${C.border};border-radius:10px;padding:16px;font-size:15px;line-height:1.6;color:${C.ink};">${nl2br(message)}</div>` : ""}
<p style="margin:24px 0 0;font-size:14px;color:${C.grey};">Just hit <strong style="color:${C.ink};">Reply</strong> to respond to ${esc(first)} directly.</p>`;
  return shell(inner);
}

function customerEmail({ first, enquiry, message }){
  const inner = `
<h1 style="margin:0 0 14px;font-size:22px;color:${C.ink};">Thanks, ${esc(first)} — we&rsquo;ve got your enquiry</h1>
<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:${C.ink};">Thanks for getting in touch with <strong>Wolves Storage Sussex</strong>. A member of our friendly, family-run team will get back to you shortly &mdash; and we&rsquo;ll send your free, no-obligation quote within 24 hours.</p>
${(enquiry || message) ? `<p style="margin:0 0 8px;font-size:13px;color:${C.grey};font-weight:bold;">What you sent us</p>
<div style="background:${C.light};border:1px solid ${C.border};border-radius:10px;padding:16px;font-size:15px;line-height:1.6;color:${C.ink};">
${enquiry ? `<strong>Storing:</strong> ${esc(enquiry)}<br>` : ""}${message ? nl2br(message) : ""}
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
