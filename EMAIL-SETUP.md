# Contact form email setup (Resend + Cloudflare Pages)

The contact/quote form posts to a Cloudflare Pages Function (`functions/api/contact.js`)
which sends **two** emails via [Resend](https://resend.com):

1. **Owner notification** → `info@sussexstoragecompany.co.uk` (reply-to = the customer, so you can just hit Reply).
2. **Customer confirmation** → the visitor's email (a different, friendly branded message).

Both are branded (Wolves Storage Sussex colours + logo).

## One-time setup

### 1. Verify your sending domain in Resend
- Sign in at https://resend.com → **Domains** → **Add Domain** → `sussexstoragecompany.co.uk`.
- Add the DNS records Resend gives you (SPF, DKIM, DMARC) to that domain.
- Wait for it to show **Verified**.

> The "from" address is `info@sussexstoragecompany.co.uk` (set at the top of
> `functions/api/contact.js`). Change `FROM` / `OWNER_TO` there if you want different addresses.
> The from-domain **must** be the verified one.

### 2. Create a Resend API key
- Resend → **API Keys** → **Create API Key** (Sending access) → copy it (`re_…`).

### 3. Add the key to Cloudflare Pages
- Cloudflare dashboard → your Pages project → **Settings → Environment variables**.
- Add **`RESEND_API_KEY`** = the `re_…` value, for **Production** (and Preview if you want).
- **(Optional, like wolves-removals) `CONTACT_TO`** = the inbox that should receive enquiry notifications (e.g. `info@sussexstoragecompany.co.uk` or your own Gmail). If unset, defaults to `info@sussexstoragecompany.co.uk`.
- **(Optional) `CONTACT_FROM`** = the verified sender, e.g. `Wolves Storage Sussex <info@sussexstoragecompany.co.uk>`. If unset, uses that default (its domain must be Resend-verified).
- **Redeploy** (Deployments → Retry deployment) so the variables take effect.

That's it — submissions now email you and auto-reply to the customer. (Tip: if you already run Resend for wolves-removals, you can reuse the same `RESEND_API_KEY`; just verify `sussexstoragecompany.co.uk` as a domain in the same Resend account.)

## Test
Submit the form on the live site. You should receive the owner email at
`info@sussexstoragecompany.co.uk`, and the address you entered should receive the confirmation.
If the form shows the red error, check: domain Verified, `RESEND_API_KEY` set, deployment redeployed.

## Notes
- The contact form has a **"Would you like us to collect your goods?"** toggle. When set to **Yes**, collection-address fields (line 1/2, town, postcode) appear and are required; the owner email then shows a **Collection** line with the address (or "No — customer will drop off").
- If the visitor arrives from the **size calculator** ("Get a quote"), their item list is handed over (via `sessionStorage`) and shown as a **visual inventory panel** on the form; it's also rendered as a **Storage inventory** block (capacity + category-grouped items) in the owner email.
- The form has a hidden honeypot field (`company`); bot submissions are silently dropped.
- All form fields are HTML-escaped before being placed in the emails.
- Any form with `class="enquiry-form"` is wired automatically (contact form today, future quote forms too).
