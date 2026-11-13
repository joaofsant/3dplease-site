#!/usr/bin/env python3
"""Build the area pages (3d-printing-*.html), sitemap.xml and robots.txt.

Run from the repo root:  python3 _build_area_pages.py
Files starting with "_" are not published by GitHub Pages (Jekyll skips them).
Prices and postage below must match CONFIG in index.html.
"""
import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

SITE = "https://3dplease.ie"
PHONE = "+353832059510"
EMAIL = "hello@3dplease.ie"
QUOTE_URL = "/?loc=ireland#order"   # home page, Ireland version, scrolled to the quote tool
TODAY = date.today().isoformat()

PRICE_FROM = "€6"
POST_SMALL = "€5"
POST_LARGE = "€9"
POST_SMALL_RULE = "whole order up to 250 g and longest side up to 200 mm"

# ---------------------------------------------------------------- shared copy
FILES_FAQ = (
    "What files can I send?",
    "STL, 3MF, OBJ and STEP all get an instant price. Files up to 25 MB, and parts up to "
    "256 mm on each side. Bigger parts can be printed in sections for you to put together. "
    "If a file can't be read automatically, send it anyway and we'll price it by hand.",
)
PAY_FAQ = (
    "How do I pay?",
    "By Revolut or bank transfer. A person checks your file first, then we send the payment "
    "details with the order confirmation.",
)
NOFILE_FAQ = (
    "I don't have a 3D file. Can you still help?",
    'Most everyday parts already exist as free models on '
    '<a href="https://www.printables.com/" target="_blank" rel="noopener">Printables</a>, '
    '<a href="https://makerworld.com/" target="_blank" rel="noopener">MakerWorld</a> or '
    '<a href="https://www.thingiverse.com/" target="_blank" rel="noopener">Thingiverse</a>. '
    "Download the STL or 3MF and upload it, or send us the link on WhatsApp. If you need "
    "something designed from scratch, message us and we'll recommend a designer we trust.",
)

def delivery_faq(place):
    return (
        f"How long does delivery to {place} take?",
        "Standard prints are ready in 2–3 days. If you choose Next day in the quote, it's included "
        "for prints under 4 hours (+€3 for longer ones, when there's capacity). We post it the day "
        f"it's ready, and An Post usually delivers to {place} the next working day.",
    )

def postage_faq(place):
    q = "How much is postage?" if place.startswith("anywhere") else f"How much is postage to {place}?"
    return (
        q,
        f"{POST_SMALL} if the whole order weighs up to 250 g and its longest side is up to 200 mm, {POST_LARGE} for anything bigger. The price box adds "
        "the right one, so you see the full total before you order.",
    )

def collect_faq(place):
    return (
        f"Can I collect in {place}?",
        f"No, we don't have a pickup point in {place}. Everything is printed in Cork and sent by "
        'An Post. If you\'re ever in Cork, collection in the city centre is free — choose '
        '"Collect in Cork" in the quote.',
    )

REVIEWS = [
    ("Highly professional work and top quality. The pieces came out exactly as I wanted, with a flawless finish and fast delivery. Totally recommend!", "Irene A."),
    ("Amazing service! Ordered a custom piece for my hobbyist RC car and it worked without a hassle!", "fox clock"),
    ("Very nice guy, great communication and quick turn around.", "Richard O."),
]

# ---------------------------------------------------------------- pages
PAGES = [
    {
        "slug": "ireland",
        "place": "Ireland",
        "nav_name": "All of Ireland",
        "area_type": "Country",
        "title": "3D Printing Service Ireland — Instant Price | 3D Please",
        "description": "Online 3D printing for anywhere in Ireland. Upload an STL, 3MF, OBJ or STEP file and see the price in seconds. Printed in Cork, posted by An Post from €5.",
        "tag": "Printed in Cork · Posted all over Ireland",
        "h1": "3D printing service<br><em>for all of Ireland.</em>",
        "body": f"Upload your file and see the price in seconds. We print it in Cork and post it to any address with an Eircode — {POST_SMALL} for small parts, {POST_LARGE} for bigger ones. No account needed.",
        "intro_title": "Online 3D printing, priced on the spot",
        "intro": [
            "Drop your file into the quote tool and the price appears as soon as it loads. Pick PLA or PETG, a colour and a strength, and the price updates as you go. Postage is added before you order, so there are no surprises at the end.",
            "Every file is checked by a person before it prints. If something needs fixing, we tell you before anything happens. You pay by Revolut or bank transfer once we confirm the order.",
        ],
        "uses": [
            ("Replacement parts", "A broken clip, knob, bracket or cover. Most everyday parts already exist as free models — find yours on Printables, MakerWorld or Thingiverse and upload it."),
            ("Prototypes and test parts", "Test a design before you commit to a big batch. Change the file, upload it again and see the new price straight away."),
            ("Projects and hobbies", "Student projects, RC and drone parts, models and organisers. Up to 256 mm prints in one piece; bigger parts are printed in sections."),
        ],
        "faq": [
            ("Which parts of Ireland do you post to?", "Every county in the Republic of Ireland — any address with an Eircode, which the order form asks for. Cities, towns and rural addresses all cost the same to post."),
            ("How long does it take?", delivery_faq("your address")[1]),
            ("How much is postage?", f"{POST_SMALL} if the whole order weighs up to 250 g and its longest side is up to 200 mm, {POST_LARGE} for anything bigger. It's the same price to every address in Ireland, and the price box adds it before you order."),
            ("Can I collect instead?", 'Yes, collection in Cork City centre is free. Choose "Collect in Cork" in the quote.'),
            FILES_FAQ,
            NOFILE_FAQ,
        ],
    },
    {
        "slug": "county-cork",
        "place": "County Cork",
        "nav_name": "County Cork",
        "area_type": "AdministrativeArea",
        "collect": True,
        "title": "3D Printing County Cork — Kinsale, Cobh, Midleton | 3D Please",
        "description": "3D printing for Kinsale, Carrigaline, Cobh, Midleton, Mallow and the rest of County Cork. Instant price, free collection in Cork City or An Post from €5.",
        "tag": "Printed in Cork City · Collect or post",
        "h1": "3D printing for<br><em>all of County Cork.</em>",
        "body": f"From Kinsale to Mallow, Cobh to Clonakilty: upload your file and see the price in seconds. Collect it for free in Cork City centre, or get it posted for {POST_SMALL} (small parts) or {POST_LARGE} (bigger ones).",
        "intro_title": "Collect on your next trip into the city, or get it posted",
        "intro": [
            "If you're in Cork City anyway — for work, college or shopping — choose \"Collect in Cork\" in the quote and pick it up for free. Otherwise An Post brings it to your door, usually the next working day after it's posted.",
            "Standard prints are ready in 2–3 days, or the next day if you choose it (included for prints under 4 hours). A person checks every file before it prints.",
        ],
        "uses": [
            ("Harbour towns: Cobh, Carrigaline, Kinsale", "Mounts, caps and clips for boats, bikes and outdoor gear. Choose PETG for anything that lives outside."),
            ("East, North and West Cork", "Replacement knobs, brackets and covers for the house, the workshop or the farm in Midleton, Youghal, Mallow, Bandon or Clonakilty. Not for safety-critical or load-bearing parts."),
            ("Students and commuters", "Studying or working in the city — UCC, MTU or an office in town? Choose collection and pick your print up on the way home."),
        ],
        "faq": [
            ("Which towns do you cover?", "All of County Cork: Kinsale, Carrigaline, Cobh, Midleton, Ballincollig, Bandon, Mallow, Youghal, Clonakilty, Macroom, Fermoy, Skibbereen and everywhere in between. Any address with an Eircode."),
            ("Can I collect instead of paying for postage?", 'Yes. Collection in Cork City centre is free. Choose "Collect in Cork" in the quote and we agree the pickup with you.'),
            ("How long does it take?", delivery_faq("your town")[1]),
            postage_faq("anywhere in the county"),
            FILES_FAQ,
            PAY_FAQ,
        ],
    },
    {
        "slug": "dublin",
        "place": "Dublin",
        "nav_name": "Dublin",
        "area_type": "City",
        "title": "3D Printing Dublin — Instant Price, Posted | 3D Please",
        "description": "3D printing for Dublin: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to your Dublin address by An Post from €5.",
        "tag": "Printed in Cork · Posted to Dublin",
        "h1": "3D printing for Dublin,<br><em>posted to your door.</em>",
        "body": f"Upload your file and get the price in seconds, any time of day. We print it in Cork and send it to your home, office or college address in Dublin by An Post: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "No waiting for a quote by email",
        "intro": [
            "The price is on the screen the moment your file loads, and ordering takes about a minute. Choose Next day and a small print ordered on Monday is usually made on Tuesday and in Dublin on Wednesday.",
            "A person checks every file before it prints, so a mistake in the model gets caught before you pay for it.",
        ],
        "uses": [
            ("College and course projects", "Brackets, enclosures and models for projects at TU Dublin, Trinity, UCD, DCU or anywhere else. Upload the file and it comes to your door by post."),
            ("Fixes for flats and rentals", "Replacement knobs, shelf pins, cable clips and appliance covers. Find the part as a free model, upload it, and it arrives by post."),
            ("Hardware prototypes", "Enclosures, mounts and test parts for early products. Change the file and get a new price in seconds, without emails back and forth."),
        ],
        "faq": [
            delivery_faq("Dublin"),
            postage_faq("Dublin"),
            ("Can you post to an office or college address?", "Yes, any Dublin address with an Eircode. Put a name and a note on the order so it reaches the right desk or room."),
            collect_faq("Dublin"),
            FILES_FAQ,
            PAY_FAQ,
        ],
    },
    {
        "slug": "limerick",
        "place": "Limerick",
        "nav_name": "Limerick",
        "area_type": "City",
        "title": "3D Printing Limerick — Instant Price, Posted | 3D Please",
        "description": "3D printing for Limerick: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to Limerick by An Post from €5.",
        "tag": "Printed in Cork · Posted to Limerick",
        "h1": "3D printing for Limerick,<br><em>made in Cork.</em>",
        "body": f"Upload your file and see the price in seconds. We print it in Cork and post it to any address in Limerick city or county: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "From your file to your door in Limerick",
        "intro": [
            "Choose Next day in the quote and a small print is made the day after you order and posted the same day; An Post usually delivers the next working day. Standard is 2–3 days, and the quote shows the options for bigger prints.",
            "You see the full price, postage included, before you order. A person checks the file before printing and tells you first if anything needs fixing.",
        ],
        "uses": [
            ("UL and TUS projects", "Final-year builds, robotics parts and enclosures for students at the University of Limerick or TUS. Upload the file and it comes to you by post."),
            ("Workshop and home repairs", "Spacers, brackets, handles and covers that aren't sold any more. Search for the part on Printables or MakerWorld, upload it, done."),
            ("Drones, RC and hobby parts", "Mounts, guards and replacement parts. Choose PETG for anything that takes knocks or sits near heat."),
        ],
        "faq": [
            delivery_faq("Limerick"),
            postage_faq("Limerick"),
            ("Can I get it faster?", "Choose Next day in the quote: it's included for prints under 4 hours, and +€3 for longer ones when there's capacity. If it's really urgent, message us on WhatsApp before you order and we'll tell you honestly what's possible."),
            collect_faq("Limerick"),
            FILES_FAQ,
            NOFILE_FAQ,
        ],
    },
    {
        "slug": "galway",
        "place": "Galway",
        "nav_name": "Galway",
        "area_type": "City",
        "title": "3D Printing Galway — Instant Price, Posted | 3D Please",
        "description": "3D printing for Galway: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to Galway by An Post from €5.",
        "tag": "Printed in Cork · Posted to Galway",
        "h1": "3D printing for Galway,<br><em>priced in seconds.</em>",
        "body": f"Upload your file and the price appears straight away. We print it in Cork and post it to any address in Galway city or county: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "Upload in Galway, printed and posted from Cork",
        "intro": [
            "You choose the material, colour and strength in the quote and see the total with postage before you order. With Next day chosen, small prints are made the next day and posted the same day; An Post usually delivers to Galway the working day after.",
            "Every file is checked by a person before it prints. You pay by Revolut or bank transfer once the order is confirmed.",
        ],
        "uses": [
            ("University of Galway and ATU projects", "Parts for engineering, design and science projects. Upload the file from wherever you are and it arrives by post."),
            ("Product prototypes", "Check fit and form before you commit to a production run. PLA for a clean look, PETG for parts that need to flex or handle heat."),
            ("Outdoor and sports kit", "Clips, mounts, caps and spacers for bikes, boats and camping gear. PETG copes with heat better than PLA."),
        ],
        "faq": [
            delivery_faq("Galway"),
            postage_faq("Galway"),
            ("What if my part is bigger than 256 mm?", "We can print it in sections that you put together afterwards. Send the file on WhatsApp and we'll tell you how we'd split it and what it costs."),
            collect_faq("Galway"),
            FILES_FAQ,
            PAY_FAQ,
        ],
    },
    {
        "slug": "waterford",
        "place": "Waterford",
        "nav_name": "Waterford",
        "area_type": "City",
        "title": "3D Printing Waterford — Instant Price, Posted | 3D Please",
        "description": "3D printing for Waterford: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to Waterford by An Post from €5.",
        "tag": "Printed in Cork · Posted to Waterford",
        "h1": "3D printing for Waterford,<br><em>posted from Cork.</em>",
        "body": f"Upload your file and see the price in seconds. We print it in Cork and post it to any address in Waterford city or county: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "Small parts, small prices",
        "intro": [
            f"Simple parts like hooks, clips and brackets usually come in between {PRICE_FROM} and €12, plus {POST_SMALL} postage. Upload the file to see the exact price for yours.",
            "Standard prints are ready in 2–3 days, or the next day if you choose it (included for prints under 4 hours). An Post usually delivers to Waterford the next working day. A person checks every file before it prints.",
        ],
        "uses": [
            ("SETU projects", "Parts and enclosures for engineering and design students at SETU in Waterford. Upload the file and it comes to you by post."),
            ("Home and garden fixes", "Hooks, brackets, plant labels and replacement caps. Most of these already exist as free models you can upload."),
            ("Models and tabletop gaming", "Terrain, scenery, organisers and display stands. For extra-fine detail, add a note to your order and we'll print it with finer layers."),
        ],
        "faq": [
            delivery_faq("Waterford"),
            postage_faq("Waterford"),
            collect_faq("Waterford"),
            ("PLA or PETG?", "PLA suits most things: clean finish and accurate, for indoor parts, prototypes and models. PETG is stronger and handles heat better, for parts under stress or outdoors. PETG is +€1 per order."),
            FILES_FAQ,
            NOFILE_FAQ,
        ],
    },
    {
        "slug": "kilkenny",
        "place": "Kilkenny",
        "nav_name": "Kilkenny",
        "area_type": "City",
        "title": "3D Printing Kilkenny — Instant Price, Posted | 3D Please",
        "description": "3D printing for Kilkenny: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to Kilkenny by An Post from €5.",
        "tag": "Printed in Cork · Posted to Kilkenny",
        "h1": "3D printing for Kilkenny,<br><em>city and county.</em>",
        "body": f"Upload your file and see the price in seconds. We print it in Cork and post it anywhere An Post delivers in Kilkenny, rural addresses included: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "Same price to post, wherever you are in the county",
        "intro": [
            "Postage depends on the size of the parcel, not the address, so a farm outside Callan pays the same as the city centre. You see the total before you order.",
            "Standard prints are ready in 2–3 days, or the next day if you choose it (included for prints under 4 hours). An Post usually delivers the next working day. A person checks every file before it prints.",
        ],
        "uses": [
            ("Makers and designers", "Jigs, stencils, display stands and small batches for craft and design work. Change the file and see the new price straight away."),
            ("Farm, workshop and machine parts", "Knobs, covers, cable guides and spacers for kit that's out of production. Not for safety-critical or load-bearing parts. PETG is better outdoors or near heat."),
            ("Gifts and personal pieces", "Name tags, keyrings, desk items and models. Upload something you found on Printables or MakerWorld, or a model you made yourself."),
        ],
        "faq": [
            delivery_faq("Kilkenny"),
            postage_faq("Kilkenny"),
            ("Do you post to rural addresses?", "Yes, anywhere An Post delivers. The order form asks for your Eircode, and the postage is the same as for the city."),
            collect_faq("Kilkenny"),
            FILES_FAQ,
            PAY_FAQ,
        ],
    },
    {
        "slug": "wexford",
        "place": "Wexford",
        "nav_name": "Wexford",
        "area_type": "City",
        "title": "3D Printing Wexford — Instant Price, Posted | 3D Please",
        "description": "3D printing for Wexford, Gorey, Enniscorthy and New Ross: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Posted from Cork from €5.",
        "tag": "Printed in Cork · Posted to Wexford",
        "h1": "3D printing for Wexford,<br><em>town and county.</em>",
        "body": f"Upload your file and see the price in seconds. We print it in Cork and post it anywhere in County Wexford — Wexford town, Gorey, Enniscorthy, New Ross: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
        "intro_title": "One price to post, from Gorey to Rosslare",
        "intro": [
            "Upload an STL, 3MF, OBJ or STEP file, choose PLA or PETG and a colour, and the price updates as you go. Postage is added before you order and costs the same to every address in the county.",
            "Standard prints are ready in 2–3 days, or the next day if you choose it (included for prints under 4 hours). An Post usually delivers to Wexford the next working day. A person checks every file before it prints.",
        ],
        "uses": [
            ("Boats, bikes and outdoor kit", "Clips, caps, guides and mounts for gear that lives outside. PETG copes with heat better than PLA. Not for safety-critical parts."),
            ("House, caravan and holiday-home fixes", "Replacement knobs, hooks, covers and organisers. Most of these already exist as free models you can upload."),
            ("Students and makers", "Project parts, enclosures and models. Upload the file from wherever you are and it comes to you by post."),
        ],
        "faq": [
            delivery_faq("Wexford"),
            postage_faq("Wexford"),
            ("Do you post to Gorey, Enniscorthy, New Ross and Rosslare?", "Yes, anywhere in County Wexford with an Eircode, at the same price as Wexford town."),
            collect_faq("Wexford"),
            FILES_FAQ,
            PAY_FAQ,
        ],
    },
    {
        "slug": "sligo",
        "place": "Sligo",
        "nav_name": "Sligo",
        "area_type": "City",
        "title": "3D Printing Sligo — Instant Price, Posted | 3D Please",
        "description": "3D printing for Sligo: upload your STL, 3MF, OBJ or STEP and see the price in seconds. Printed in Cork, posted to Sligo by An Post from €5.",
        "tag": "Printed in Cork · Posted to Sligo",
        "h1": "3D printing for Sligo,<br><em>across the country.</em>",
        "body": f"Sligo is a long way from Cork, but the postage isn't: {POST_SMALL} for small parts, {POST_LARGE} for bigger ones, anywhere in the county. Upload your file and see the price in seconds.",
        "intro_title": "The far side of the country, the same postage",
        "intro": [
            "Postage is priced by the size of the parcel, not the distance, so Sligo pays the same as anywhere else. Standard prints are ready in 2–3 days, or the next day if you choose it (included for prints under 4 hours), and An Post usually delivers the next working day.",
            "Every file is checked by a person before it prints. You pay by Revolut or bank transfer once the order is confirmed.",
        ],
        "uses": [
            ("ATU Sligo projects", "Parts and enclosures for engineering and design projects at ATU Sligo. Upload the file and it comes to you by post."),
            ("Surf, bike and camping gear", "Mounts, clips and caps for kit that lives outdoors. PETG is the better choice for anything outside."),
            ("Replacement parts", "Knobs, brackets and covers that aren't sold any more. Find the model on Printables or MakerWorld and upload it."),
        ],
        "faq": [
            delivery_faq("Sligo"),
            postage_faq("Sligo"),
            ("Why order from Cork if I'm in Sligo?", "You get the price on screen straight away, without emails back and forth, and the postage is the same as anywhere else in Ireland."),
            collect_faq("Sligo"),
            FILES_FAQ,
            NOFILE_FAQ,
        ],
    },
]

# ---------------------------------------------------------------- helpers
def page_url(p):
    return f"{SITE}/3d-printing-{p['slug']}"

def page_path(p):
    return f"/3d-printing-{p['slug']}"

def wa_link(place):
    where = "anywhere in Ireland" if place == "Ireland" else f"to {place}"
    text = f"Hi, I'd like a price for a 3D print posted {where}. Here's my file or link:"
    return "https://wa.me/353832059510?text=" + quote(text, safe="")

def esc(s):
    return html.escape(s, quote=True)

def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)

def jsonld(p):
    area = {"@type": p["area_type"], "name": p["place"]}
    data = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"3D printing for {p['place']}",
            "serviceType": "3D printing",
            "url": page_url(p),
            "areaServed": area,
            "provider": {
                "@type": "LocalBusiness",
                "name": "3D Please",
                "url": SITE,
                "telephone": PHONE,
                "email": EMAIL,
                "image": f"{SITE}/og.png",
                "address": {"@type": "PostalAddress", "addressLocality": "Cork", "addressCountry": "IE"},
            },
            "offers": {
                "@type": "Offer",
                "priceCurrency": "EUR",
                "price": "6.00",
                "description": f"Prints from {PRICE_FROM}. An Post delivery {POST_SMALL} for small parts, {POST_LARGE} for bigger ones.",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "3D Please", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": f"3D printing {p['place']}", "item": page_url(p)},
            ],
        },
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JWLKQWBCTT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-JWLKQWBCTT');
  // Contact clicks: WhatsApp and phone links anywhere on the page
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('wa.me/') !== -1) {
      var designer = h.indexOf('designer') !== -1;
      gtag('event', designer ? 'designer_referral_click' : 'whatsapp_click', { link_place: a.getAttribute('data-place') || 'page' });
    } else if (h.indexOf('tel:') === 0) {
      gtag('event', 'phone_click', { link_place: a.getAttribute('data-place') || 'page' });
    }
  }, true);
</script>"""

FAVICON = """<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2318171a'/%3E%3Ctext x='16' y='22' font-family='-apple-system,BlinkMacSystemFont,system-ui,sans-serif' font-weight='900' font-size='14' fill='%23f6f3ed' text-anchor='middle'%3E3D%3C/text%3E%3C/svg%3E">"""

def area_links_html(current=None, cls="area-links"):
    items = []
    for p in PAGES:
        cur = ' aria-current="page"' if current and p["slug"] == current["slug"] else ""
        items.append(f'<a href="{page_path(p)}"{cur}>{esc(p["nav_name"])}</a>')
    items.append('<a href="/">Cork City (collect free)</a>')
    return f'<div class="{cls}">\n    ' + "\n    ".join(items) + "\n  </div>"

def footer_area_list():
    lis = [f'<li><a href="{page_path(p)}">{esc(p["nav_name"])}</a></li>' for p in PAGES]
    lis.append('<li><a href="/">Cork City</a></li>')
    return "\n        ".join(lis)

def build_page(p):
    place = p["place"]
    to_place = "anywhere in Ireland" if place == "Ireland" else place
    uses = "\n".join(
        f"""    <div class="tile">
      <span class="tile-num">{i:02d}</span>
      <h3>{esc(t)}</h3>
      <p>{esc(b)}</p>
    </div>""" for i, (t, b) in enumerate(p["uses"], 1)
    )
    faq = "\n".join(
        f"""    <details>
      <summary>{esc(q)}</summary>
      <p>{a}</p>
    </details>""" for q, a in p["faq"]
    )
    reviews = "\n".join(
        f"""    <figure class="review">
      <span class="stars" aria-label="5 out of 5 stars">★★★★★</span>
      <blockquote>“{esc(t)}”</blockquote>
      <figcaption>{esc(n)} · Google review</figcaption>
    </figure>""" for t, n in REVIEWS
    )
    intro = "\n".join(f"    <p>{esc(x)}</p>" for x in p["intro"])
    arrive = "An Post usually delivers it to your door." if place == "Ireland" else f"An Post usually delivers it in {place}."
    crumb_name = f"3D printing {place}"
    collect_row = ('<div class="post-row"><div><b>Collect in Cork City</b><small>City centre, pickup agreed with you</small></div><span class="amt">Free</span></div>\n        '
                   if p.get("collect") else "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['description'])}">
<link rel="canonical" href="{page_url(p)}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['description'])}">
<meta property="og:url" content="{page_url(p)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{jsonld(p)}
</script>
{FAVICON}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/area.css">

{GTAG}
</head>
<body>

<nav>
  <a class="nav-brand" href="/" aria-label="3D Please — home">
    <img src="/logo.png" width="560" height="144" alt="3D Please" class="logo-img">
  </a>
  <a class="nav-link" href="/#how">How it works</a>
  <a class="nav-link" href="/#pricing">Pricing</a>
  <a class="nav-link" href="/#faq">FAQ</a>
  <a class="nav-cta" href="{QUOTE_URL}">Instant quote</a>
</nav>

<div class="crumbs"><a href="/">3D Please</a><span>/</span>{esc(crumb_name)}</div>

<section class="hero">
  <div class="hero-left">
    <div class="hero-tag">{esc(p['tag'])}</div>
    <h1 class="hero-title">{p['h1']}</h1>
    <p class="hero-body">{esc(p['body'])}</p>
    <div class="hero-cta-row">
      <a href="{QUOTE_URL}" class="btn-primary">Get an instant price →</a>
      <a href="{wa_link(place)}" class="btn-secondary" target="_blank" rel="noopener" data-place="area-{p['slug']}">Send a file or link on WhatsApp</a>
    </div>
    <div class="hero-stats">
      <div class="stat">
        <span class="stat-label">Prints from</span>
        <span class="stat-value">{PRICE_FROM}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Postage</span>
        <span class="stat-value">{POST_SMALL} / {POST_LARGE}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Google rating</span>
        <span class="stat-value">5.0 <span class="stars">★★★★★</span></span>
      </div>
    </div>
  </div>

  <aside class="hero-right">
    <div class="card">
      <div class="card-title"><span class="dot"></span>{"Collect or post" if p.get("collect") else "Delivery to " + esc(to_place)}</div>
      <div class="post-rows">
        {collect_row}<div class="post-row"><div><b>Small parcel</b><small>{esc(POST_SMALL_RULE.capitalize())}</small></div><span class="amt">{POST_SMALL}</span></div>
        <div class="post-row"><div><b>Bigger parcel</b><small>Anything larger or heavier</small></div><span class="amt">{POST_LARGE}</span></div>
      </div>
      <ol class="timeline">
        <li><b>Today</b> — upload your file, see the price, order.</li>
        <li><b>Next day or 2–3 days</b> — your print is made, checked and posted. Next day is included for prints under 4 hours.</li>
        <li><b>Working day after</b> — {esc(arrive)}</li>
      </ol>
      <a href="{QUOTE_URL}" class="btn-primary">Upload your file →</a>
      <p class="card-note">STL · 3MF · OBJ · STEP — up to 25 MB</p>
      <p class="card-note">Only have a link, or on your phone? <a href="{wa_link(place)}" target="_blank" rel="noopener" data-place="area-{p['slug']}-card">Send it on WhatsApp</a>.</p>
    </div>
  </aside>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">01</span>
      <h2 class="section-label">{esc(p['intro_title'])}</h2>
    </div>
  </div>
  <div class="prose">
{intro}
  </div>
</section>

<section class="section tint">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">02</span>
      <h2 class="section-label">What people get printed</h2>
    </div>
    <p class="section-sub">PLA and PETG, in white, black, grey and natural. Other colours on request.</p>
  </div>
  <div class="cards3">
{uses}
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">03</span>
      <h2 class="section-label">Prices</h2>
    </div>
    <p class="section-sub">A guide. Upload your file for the exact price.</p>
  </div>
  <div class="price-strip">
    <div class="price-cell"><span class="stat-label">Small parts</span><b>€6–€12</b><small>Up to ~80 g. Brackets, clips, hooks.</small></div>
    <div class="price-cell"><span class="stat-label">Medium</span><b>€12–€24</b><small>80–200 g. Enclosures, prototypes.</small></div>
    <div class="price-cell"><span class="stat-label">Large</span><b>€24+</b><small>200 g and up. Models, assemblies.</small></div>
    <div class="price-cell"><span class="stat-label">Postage</span><b>{POST_SMALL} / {POST_LARGE}</b><small>An Post, anywhere in Ireland.</small></div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">04</span>
      <h2 class="section-label">Printed in Cork</h2>
    </div>
    <p class="section-sub">Real parts we've printed. No renders, no stock photos.</p>
  </div>
  <div class="gallery">
    <figure>
      <img src="/print-star-wheel.jpg" width="1200" height="1081" loading="lazy" alt="Large black star-shaped wheel with nine arms and a bolted hub">
      <figcaption>Star wheel with a bolt-pattern hub.</figcaption>
    </figure>
    <figure>
      <img src="/print-brackets.jpg" width="1200" height="900" loading="lazy" alt="Two black 3D-printed mounting brackets with bolt holes, showing fine layer lines">
      <figcaption>Mounting brackets, straight off the printer.</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">05</span>
      <h2 class="section-label">What customers say</h2>
    </div>
    <p class="section-sub">Straight from our Google reviews, word for word.</p>
  </div>
  <div class="rating-row">
    <span class="rating-big">5.0</span>
    <span class="stars" aria-label="Rated 5 out of 5">★★★★★</span>
    <span class="rating-meta">on Google · <a href="https://g.page/r/CYiCOIpLPXshEAE" target="_blank" rel="noopener">See our reviews</a></span>
  </div>
  <div class="reviews-grid">
{reviews}
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">06</span>
      <h2 class="section-label">Questions</h2>
    </div>
    <p class="section-sub">Anything else? <a href="https://wa.me/353832059510" target="_blank" rel="noopener" data-place="area-{p['slug']}">Ask on WhatsApp</a> or call <a href="tel:{PHONE}" style="white-space:nowrap" data-place="area-{p['slug']}">{PHONE}</a>.</p>
  </div>
  <div class="faq">
{faq}
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-head-left">
      <span class="section-num">07</span>
      <h2 class="section-label">We post all over Ireland</h2>
    </div>
  </div>
  {area_links_html(p)}
</section>

<footer>
  <div class="footer-grid">
    <div>
      <a class="footer-brand-logo" href="/" aria-label="3D Please — home">
        <img src="/logo.png" width="560" height="144" alt="3D Please" class="logo-img logo-img-footer">
      </a>
      <p class="footer-tagline">Local 3D printing from Cork City, posted anywhere in Ireland. Prototypes, parts, custom objects.</p>
    </div>
    <div>
      <span class="footer-col-title">Order</span>
      <ul class="footer-links">
        <li><a href="{QUOTE_URL}">Instant quote</a></li>
        <li><a href="https://wa.me/353832059510" target="_blank" rel="noopener" data-place="area-{p['slug']}">WhatsApp</a></li>
        <li><a href="tel:{PHONE}" data-place="area-{p['slug']}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="https://www.instagram.com/3dplease/" target="_blank" rel="noopener">Instagram @3dplease</a></li>
      </ul>
    </div>
    <div>
      <span class="footer-col-title">Info</span>
      <ul class="footer-links">
        <li><a href="/#how">How it works</a></li>
        <li><a href="/#reviews">Reviews</a></li>
        <li><a href="/#pricing">Pricing</a></li>
        <li><a href="/#materials">Materials</a></li>
        <li><a href="/#faq">FAQ</a></li>
      </ul>
    </div>
    <div>
      <span class="footer-col-title">We post to</span>
      <ul class="footer-links">
        {footer_area_list()}
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span class="footer-copy">© 2026 3D Please — Cork, Ireland</span>
    <span class="footer-copy">{PHONE} · {EMAIL}</span>
  </div>
</footer>

</body>
</html>
"""

def build_sitemap():
    urls = [(f"{SITE}/", "1.0")] + [(page_url(p), "0.8") for p in PAGES]
    rows = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'

ROBOTS = f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
"""

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    for p in PAGES:
        out = root / f"3d-printing-{p['slug']}.html"
        out.write_text(build_page(p), encoding="utf-8")
        print("wrote", out.name)
    (root / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
    (root / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")
