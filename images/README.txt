==========================================================================
 WOLVES STORAGE SUSSEX — IMAGES GUIDE
==========================================================================

HOW IMAGES WORK ON THIS SITE
----------------------------------------------------------------------
Every photo on the site loads from Unsplash (free stock photos) when you
are ONLINE. If a photo can't load (e.g. you're offline, or you want to
swap it), the page automatically falls back to one of the branded SVG
placeholders in this folder, so the layout always looks intentional:

   placeholder-hero.svg   -> wide hero / banner images (16:9-ish)
   placeholder-4x3.svg    -> standard cards / content images
   placeholder-1x1.svg    -> square images / avatars

You do NOT need to do anything for the site to work. To make it truly
yours, replace the stock photos with your own (see below).

----------------------------------------------------------------------
RECOMMENDED: USE YOUR OWN PHOTOS (best for trust / EEAT + SEO)
----------------------------------------------------------------------
Real photos of YOUR containers, facility, van, team and CCTV build far
more trust than stock images. To swap one in:

  1. Save your photo into this /images folder, e.g.  storage-facility.jpg
  2. In the relevant .html file, find the <img ...> tag and change:
        src="https://images.unsplash.com/...."
     to:
        src="images/storage-facility.jpg"
  3. Keep (or update) the alt="..." text to describe the photo — good for
     SEO and accessibility.

Photos to capture for the strongest result:
  - Your storage containers (inside and stacked in the facility)
  - The secure facility exterior + the alarmed door / gate
  - A CCTV camera (reinforces the 24/7 CCTV claim)
  - Your van + team collecting/packing boxes
  - The family / team (the "About" page — humanises the brand)
  - LAPADA and Checkatrade logos (place near trust sections / footer)

----------------------------------------------------------------------
STOCK PHOTO SOURCES (free, commercial-use)
----------------------------------------------------------------------
If you'd rather keep stock photos, grab themed ones here and download
them into this folder, then point the src at the local file:

  Unsplash:  https://unsplash.com/s/photos/storage
             https://unsplash.com/s/photos/moving-boxes
             https://unsplash.com/s/photos/warehouse
             https://unsplash.com/s/photos/removals-van
  Pexels:    https://www.pexels.com/search/storage/
             https://www.pexels.com/search/moving%20house/

NOTE: The Unsplash URLs used in the HTML are examples. Some may change
over time — if one ever fails it simply shows the branded placeholder,
so nothing breaks. Replacing them with your own images is recommended.

----------------------------------------------------------------------
LOGO / FAVICON
----------------------------------------------------------------------
A simple SVG logo mark is built into the header/footer, and favicon.svg
is the browser-tab icon. To use your real Wolves logo, drop it in here
(e.g. logo.png) and replace the inline SVG logo in the header — ask and
I can wire that up for you.
==========================================================================
