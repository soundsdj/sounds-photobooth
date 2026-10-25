"""Build the photobooth.soundsdjevents.com landing page (draft 25 Oct 2026).

Styles come from the corporate page, like schools. and private., but the sections are the
booth's own: how it works, three time-based packages, occasions, backdrops, FAQ, form.
Pricing matches the Photo booth slide in the sales consultation deck.

Usage: python3 build.py   (run from anywhere; reads ../sounds-corporate)
Writes index.html, sitemap.xml, robots.txt, 404.html, CNAME, tracking.js.
"""
import html
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
G = D.parent
HOST = "photobooth.soundsdjevents.com"
BASE = f"https://{HOST}/"
FORM_ID = "cAaDQW2JdrfaMKOa3RCq"
FORM_NAME = "Sounds - Photo Booth Inquiry Form"
FALLBACK = "https://soundsdjevents.com/contact-us"
ORG_ID = "https://soundsdjevents.com/#business"
e = html.escape

corp = (G / "sounds-corporate/index.html").read_text()
css = "\n".join(re.findall(r"<style>(.*?)</style>", corp, flags=re.S)).replace(".corporate-page", ".landing-page")
css += """
.landing-page .grid.three{grid-template-columns:repeat(3,1fr)}
.landing-page .grid.three .package{padding:30px;position:relative}
.landing-page .grid.three .price{font-size:42px}
.landing-page .package.featured{border:2px solid var(--gold);box-shadow:0 18px 40px rgba(60,45,20,.12)}
.landing-page .badge{position:absolute;top:-13px;left:30px;background:var(--gold);color:#171713;font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;padding:6px 12px;border-radius:999px}
.landing-page .how{display:grid;grid-template-columns:1.05fr 1fr;gap:64px;align-items:center}
.landing-page .how img{width:100%;border-radius:12px;display:block}
.landing-page .how-steps{margin-top:28px;display:grid;gap:22px}
.landing-page .how-step{display:flex;gap:18px;align-items:baseline}
.landing-page .how-step span{font-size:13px;color:#806333;font-weight:800;min-width:24px}
.landing-page .how-step h3{font-size:19px;margin:0 0 4px}.landing-page .how-step p{margin:0;color:var(--muted)}
.landing-page .occasions{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:32px}
.landing-page .occasion{border:1px solid #e4dccf;border-radius:10px;background:white;overflow:hidden}
.landing-page .occasion img{width:100%;height:170px;object-fit:cover;display:block}
.landing-page .occasion div{padding:18px 20px}.landing-page .occasion h3{font-size:18px;margin:0 0 6px}.landing-page .occasion p{font-size:14px;color:var(--muted);margin:0}
.landing-page .also{margin-top:22px;color:var(--muted);font-size:15px}
.landing-page .backdrops{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-top:32px}
.landing-page .backdrops figure{margin:0}.landing-page .backdrops img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block;border:1px solid #e4dccf}
.landing-page .backdrops figcaption{font-size:13px;color:var(--muted);margin-top:8px;text-align:center}
.landing-page .included{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:32px}
@media(max-width:960px){.landing-page .grid.three{grid-template-columns:1fr;gap:30px}.landing-page .how{grid-template-columns:1fr;gap:36px}.landing-page .occasions,.landing-page .included{grid-template-columns:1fr 1fr}.landing-page .backdrops{grid-template-columns:repeat(4,1fr)}}
@media(max-width:560px){.landing-page .occasions,.landing-page .included{grid-template-columns:1fr}.landing-page .backdrops{grid-template-columns:repeat(3,1fr);gap:10px}}
"""

TITLE = "Photo Booth Rental for Parties & Events | The Sounds"
DESCRIPTION = ("Digital selfie booth rental across Southern Ontario for Christmas parties, birthdays, Sweet 16s, "
               "theme parties and corporate events. From $400 for 2 hours. Photos sent instantly by text, email or AirDrop.")
HERO_ALT = "Friends laughing and celebrating under balloons at a party"

PACKAGES = [
    dict(slug="two-hours", name="2 Hours", tag="The digital selfie booth", price=400,
         copy="Plenty for a birthday, a stag and doe, or an office party that wraps up early.",
         desc="Two hours of digital selfie booth with instant sharing, every image after the event, and custom branding."),
    dict(slug="three-hours", name="3 Hours", tag="Extended coverage", price=600, featured=True,
         copy="The sweet spot for most parties. Guests come back for round two, then three.",
         desc="Three hours of digital selfie booth with instant sharing, every image after the event, and custom branding."),
    dict(slug="five-hours", name="Up to 5 Hours", tag="All night memories", price=800,
         copy="From the first arrivals to the last song. Made for galas, holiday parties and big nights.",
         desc="Up to five hours of digital selfie booth with instant sharing, every image after the event, and custom branding."),
]
INCLUDES = ["Instant sharing by text, email and AirDrop", "Every image after the event", "Custom branding to match your theme"]

HOW = [("Step in and strike a pose", "Tap the screen, grab a prop or a friend, and smile. It’s simple enough that nobody needs instructions."),
       ("Photos land on their phone", "Guests send their photos to themselves by text, email or AirDrop before they’ve even left the booth."),
       ("You get every single image", "After the event I send you the full collection, so you have every photo your guests took.")]

OCCASIONS = [("holiday-party.jpg", "Christmas & holiday parties", "Office parties, family gatherings and holiday galas."),
             ("confetti-party.jpg", "Theme parties", "Branded to your theme, whether that’s the ’80s, Hollywood or a winter wonderland."),
             ("sweet-16.jpg", "Sweet 16s & Quinceañeras", "Their friends will be in that booth all night."),
             ("evening-party.jpg", "Birthdays & milestones", "40ths, 50ths, retirements, anniversaries and everything in between.")]
ALSO = "Also great for corporate events, school dances and proms, grad parties, stag and does, fundraisers and weddings."

EXTRAS = [("Branded to your event", "Your name, date, logo or theme on every photo. I design it to match your colours."),
          ("Easy for every age", "Kids, teens and grandparents all figure it out in seconds."),
          ("Fully digital by default", "No waiting around for prints. Photos are shared the moment they’re taken."),
          ("Prints when you want them", "Add unlimited on-site prints and a dedicated attendant for $200.")]

BACKDROPS = ["Glitter Gold", "Glitter Silver", "Glitter Rose Gold", "Silver Snowflake", "White Art Deco", "Paper Flowers",
             "Floral", "Greenery", "Rustic Wood", "Metal Tread", "Marble White", "Marble Black"]

FAQS = [("Do I need to book a DJ to get the photo booth?", "No. The photo booth is its own booking. If you’d like music too, I’m a DJ and host as well, and I’m happy to quote both together."),
        ("How do guests get their photos?", "Right at the booth. Guests send their photos to their own phone by text, email or AirDrop, so they can share them that night."),
        ("Do we get all the photos afterwards?", "Yes. After the event you receive every image taken at the booth."),
        ("Can the photos match our theme?", "Yes. Every booth includes custom branding, so the photos carry your name, date, logo or theme in your colours."),
        ("Can we get printed photos?", "Yes. Add unlimited on-site prints and a dedicated attendant for $200. Otherwise the booth is fully digital."),
        ("Which package should we pick?", "Most parties choose 3 hours. If guests are arriving over a long evening, or it’s a gala or holiday party, up to 5 hours means nobody misses it."),
        ("How do we book?", "Send your date, the occasion and how long you’d like the booth through the form below. I’ll confirm availability and send an agreement. A 50% booking fee reserves your date.")]

STEPS = [("Tell me about the party", "Your date, the occasion, and how long you’d like the booth."),
         ("I’ll check my calendar", "I’ll get back to you personally, usually the same day."),
         ("Make it yours", "We’ll pick a backdrop and design the branding for your photos.")]


def money(n):
    return f"${n:,}"


def page():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": ORG_ID, "name": "The Sounds DJ Services & Entertainment",
         "url": "https://soundsdjevents.com/", "logo": BASE + "assets/logo-white.png",
         "founder": {"@type": "Person", "name": "Joe Seyler"}},
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "The Sounds Photo Booth", "publisher": {"@id": ORG_ID}},
        {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": TITLE, "description": DESCRIPTION,
         "inLanguage": "en-CA", "isPartOf": {"@id": BASE + "#website"}},
    ]}
    for k in PACKAGES:
        ld["@graph"].append({"@type": "Service", "@id": BASE + "#" + k["slug"], "name": "Photo Booth " + k["name"],
                             "serviceType": "Photo booth rental", "provider": {"@id": ORG_ID},
                             "areaServed": {"@type": "Place", "name": "Southern Ontario"}, "description": k["desc"],
                             "offers": {"@type": "Offer", "price": str(k["price"]), "priceCurrency": "CAD", "url": BASE + "#pricing"}})
    ld["@graph"].append({"@type": "FAQPage", "@id": BASE + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]})

    lis = "".join(f"<li>{e(i)}</li>" for i in INCLUDES)
    pk = "".join(
        f'<article class="package{" featured" if k.get("featured") else ""}" id="{k["slug"]}">'
        + ('<div class="badge">Most popular</div>' if k.get("featured") else "")
        + f'<div class="tag">{e(k["tag"])}</div><h3>{e(k["name"])}</h3><div class="price">{money(k["price"])}</div>'
        f'<p>{e(k["copy"])}</p><ul>{lis}</ul><a class="button" href="#check">Check My Date</a></article>' for k in PACKAGES)
    how = "".join(f'<div class="how-step"><span>{i+1:02d}</span><div><h3>{e(h)}</h3><p>{e(t)}</p></div></div>' for i, (h, t) in enumerate(HOW))
    occ = "".join(f'<article class="occasion"><img src="assets/{img}" alt="{e(h)}" loading="lazy"><div><h3>{e(h)}</h3><p>{e(t)}</p></div></article>'
                  for img, h, t in OCCASIONS)
    extras = "".join(f'<article class="extra"><h3>{e(h)}</h3><p>{e(t)}</p></article>' for h, t in EXTRAS)
    bd = "".join(f'<figure><img src="assets/backdrops/{n.lower().replace(" ", "-")}.jpg" alt="{e(n)} photo booth backdrop" loading="lazy"><figcaption>{e(n)}</figcaption></figure>'
                 for n in BACKDROPS)
    faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQS)
    steps = "".join(f'<div class="inquiry-step"><span>{i+1:02d}</span><div><h3>{e(h)}</h3><p>{e(t)}</p></div></div>' for i, (h, t) in enumerate(STEPS))

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESCRIPTION)}">
<link rel="canonical" href="{BASE}">
<link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="icon" href="favicon.ico"><link rel="apple-touch-icon" href="favicon.svg">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="en_CA">
<meta property="og:site_name" content="The Sounds DJ Services &amp; Entertainment">
<meta property="og:title" content="{e(TITLE)}"><meta property="og:description" content="{e(DESCRIPTION)}">
<meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}assets/hero-party.jpg"><meta property="og:image:alt" content="{e(HERO_ALT)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(TITLE)}"><meta name="twitter:description" content="{e(DESCRIPTION)}"><meta name="twitter:image" content="{BASE}assets/hero-party.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Karla:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}{css}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body>
<div class="landing-page"><header class="nav"><div class="wrap nav-inner"><img class="brand-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"><a class="button" href="#check">Check My Date</a></div></header><main>
<section class="hero"><img class="hero-image" src="assets/hero-party.jpg" alt="{e(HERO_ALT)}" fetchpriority="high"><div class="wrap"><div class="eyebrow">Photo booth rental · Southern Ontario</div><h1>Every great party<br>deserves great memories.</h1><p>A digital selfie booth your guests will actually use. Step in, strike a pose, and the photos land on their phones before the night’s even over.</p><div class="hero-buttons"><a class="button" href="#check">Check My Date <span aria-hidden="true">↗</span></a><a class="button button-outline" href="#pricing">See the Prices <span aria-hidden="true">↓</span></a></div><div class="hero-foot"><span>From $400</span><span>Photos by text, email &amp; AirDrop</span><span>Branded to your theme</span></div></div></section>
<section class="section"><div class="wrap how"><img src="assets/booth.jpg" alt="The Sounds digital selfie booth in front of a pink wall with a balloon arch" loading="lazy"><div><div class="eyebrow">How it works</div><h2>Easy to use.<br>Instant to share.</h2>{how}</div></div></section>
<section class="section cream" id="pricing" aria-labelledby="packages-title"><div class="wrap"><div class="center"><div class="eyebrow">Simple, all-digital pricing</div><h2 id="packages-title">Pick your time.<br>That’s it.</h2><p class="muted">Every package includes the same booth, the same instant sharing, and every image after the event.</p></div><div class="grid three">{pk}</div><p class="note">Want printed photos? Add unlimited on-site prints and a dedicated attendant for $200. A 50% booking fee reserves your date.</p></div></section>
<section class="section paper"><div class="wrap"><div class="eyebrow">Made for any party</div><h2>Whatever you’re celebrating,<br>there’s a line for the booth.</h2><div class="occasions">{occ}</div><p class="also">{e(ALSO)}</p></div></section>
<section class="section"><div class="wrap"><div class="eyebrow">Every booth includes</div><h2>The little things<br>that make it work.</h2><div class="extras">{extras}</div></div></section>
<section class="section cream"><div class="wrap"><div class="eyebrow">Backdrops</div><h2>Set the scene.</h2><p class="muted">Pick the backdrop that suits your party, from glitter and snowflakes to greenery and marble.</p><div class="backdrops">{bd}</div></div></section>
<section class="section meet-joe paper"><div class="wrap joe-grid"><div><img class="joe-image" src="assets/joe.jpeg" alt="Joe Seyler speaking into a microphone at an event" loading="lazy"><p class="photo-caption">Joe Seyler · The Sounds DJ Services &amp; Entertainment</p></div><div class="joe-copy"><div class="eyebrow">Who you’re booking</div><h2>A real person,<br>not a rental counter.</h2><p>I’m Joe. I’ve spent over 30 years at parties, so I know the moments people want to keep. When you book the booth, you deal with me from your first message to the last photo.</p><p>Need music too? I’m also a DJ and host. Ask about pairing the booth with a DJ package.</p><a class="button" href="#check">Check My Date</a></div></div></section>
<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">A few helpful details</div><h2>Before you<br>get in touch.</h2></div><div class="faq">{faqs}</div></div></section>
<section class="section inquiry-section cream" id="check" aria-labelledby="inquiry-title"><div class="wrap inquiry-grid"><div><div class="eyebrow">Check my date</div><h2 id="inquiry-title">Let’s get your<br>booth booked.</h2><p class="muted">Tell me your date, the occasion, and how long you’d like the booth. I’ll get back to you personally.</p>{steps}</div><div class="form-shell"><h3>Check My Date</h3>
<iframe src="https://api.profitflo.io/widget/form/{FORM_ID}" style="width:100%;height:1300px;border:none;border-radius:8px;display:block" id="inline-{FORM_ID}" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="{FORM_NAME}" data-height="1300" data-layout-iframe-id="inline-{FORM_ID}" data-form-id="{FORM_ID}" data-cookie-consent="true" data-cookie-consent-provider="auto" title="{FORM_NAME}"></iframe>
<script src="https://api.profitflo.io/js/form_embed.js"></script>
<p class="form-fallback" style="font-size:14px;margin-top:16px">Form not displaying? <a href="{FALLBACK}" style="text-decoration:underline">Open the contact page</a>.</p></div></div></section>
</main><footer class="footer"><div class="wrap"><img class="footer-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"><p>Photo booth rental · Southern Ontario</p><p><a href="tel:+12897688677">289-768-8677</a> · <a href="https://soundsdjevents.com/">soundsdjevents.com</a></p><p>© 2026 The Sounds DJ Services &amp; Entertainment</p></div></footer></div>
<script defer src="tracking.js"></script></body></html>
"""


(D / "index.html").write_text(page())
(D / "CNAME").write_text(HOST + "\n")
(D / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url></urlset>\n')
(D / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
(D / "404.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | The Sounds</title></head><body><h1>That page could not be found.</h1><p><a href="/">Return to the photo booth</a></p></body></html>\n')
t = (G / "sounds-corporate/tracking.js").read_text()
t = t.replace("corporate.soundsdjevents.com", HOST).replace("'corporate'", "'photobooth'")
t = t.replace("['" + HOST + "', 'soundsdjevents.com', 'weddings.soundsdjevents.com']",
              "['" + HOST + "', 'soundsdjevents.com', 'weddings.soundsdjevents.com', 'corporate.soundsdjevents.com']")
(D / "tracking.js").write_text(t)
print("built", D)
