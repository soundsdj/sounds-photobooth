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
.landing-page .how-media{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:end}
.landing-page .how-media video,.landing-page .how-media img{width:100%;border-radius:12px;display:block;object-fit:cover}
.landing-page .how-media video{aspect-ratio:9/16}.landing-page .how-media img{aspect-ratio:4/5}
.landing-page video.hero-image{pointer-events:none}
@media(max-width:760px){.landing-page video.hero-image{display:none}.landing-page .hero{background:#171715 url(assets/hero-booth-mobile.jpg) 50% 30%/cover}}
@media(prefers-reduced-motion:reduce){.landing-page video.hero-image{display:none}.landing-page .hero{background:#171715 url(assets/hero-booth.jpg) center/cover}}
.landing-page .how-steps{margin-top:28px;display:grid;gap:22px}
.landing-page .how-step{display:flex;gap:18px;align-items:baseline}
.landing-page .how-step span{font-size:13px;color:#806333;font-weight:800;min-width:24px}
.landing-page .how-step h3{font-size:19px;margin:0 0 4px}.landing-page .how-step p{margin:0;color:var(--muted)}
.landing-page .occasions{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:32px}
.landing-page .occasion{border:1px solid #e4dccf;border-radius:10px;background:white;overflow:hidden}
.landing-page .occasion img{width:100%;aspect-ratio:8/5;height:auto;object-fit:cover;object-position:center 30%;display:block}
.landing-page .occasion div{padding:18px 20px}.landing-page .occasion h3{font-size:18px;margin:0 0 6px}.landing-page .occasion p{font-size:14px;color:var(--muted);margin:0}
.landing-page .also{margin-top:22px;color:var(--muted);font-size:15px}
.landing-page .backdrops{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:32px}
.landing-page .backdrops figure{margin:0}.landing-page .backdrops img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block;border:1px solid #e4dccf}
.landing-page .backdrops figcaption{font-size:13px;color:var(--muted);margin-top:8px;text-align:center}
.landing-page .more-backdrops{margin-top:18px}.landing-page .more-backdrops summary{cursor:pointer;font-weight:700;color:#806333;font-size:15px;padding:8px 0;list-style:none}.landing-page .more-backdrops summary::-webkit-details-marker{display:none}.landing-page .more-backdrops summary:after{content:" ↓"}.landing-page .more-backdrops[open] summary:after{content:" ↑"}.landing-page .more-backdrops .backdrops{margin-top:14px}
.landing-page .included{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:32px}
@media(max-width:960px){.landing-page .grid.three{grid-template-columns:1fr;gap:30px}.landing-page .how{grid-template-columns:1fr;gap:36px}.landing-page .occasions,.landing-page .included{grid-template-columns:1fr 1fr}.landing-page .backdrops{grid-template-columns:repeat(4,1fr)}}
@media(max-width:560px){.landing-page .occasions,.landing-page .included{grid-template-columns:1fr}.landing-page .backdrops{grid-template-columns:repeat(2,1fr);gap:10px}}
"""

TITLE = "Photo Booth Rental for Parties & Events | The Sounds"
DESCRIPTION = ("Digital selfie booth rental across Southern Ontario for Christmas parties, birthdays, Sweet 16s, "
               "theme parties and corporate events. From $400 for 2 hours. Photos sent instantly by text, email or AirDrop.")
HERO_ALT = "Two guests laughing as they tap the screen of the selfie booth"

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
       ("You get every single image", "After the event you receive the full collection, so you have every photo your guests took.")]

OCCASIONS = [("new-year.jpg", "Christmas & New Year’s parties", "Office parties, family gatherings, holiday galas and the countdown to midnight."),
             ("glitter-party.jpg", "Theme parties", "Branded to your theme, whether that’s the ’80s, Hollywood or a winter wonderland."),
             ("sweet-16.jpg", "Sweet 16s & Quinceañeras", "Their friends will be in that booth all night."),
             ("disco-ball.jpg", "Birthdays & milestones", "40ths, 50ths, retirements, anniversaries and everything in between.")]
ALSO = "Also great for corporate events, school dances and proms, grad parties, stag and does, fundraisers and weddings."

EXTRAS = [("Branded to your event", "Your name, date, logo or theme on every photo, designed to match your colours."),
          ("Easy for every age", "Kids, teens and grandparents all figure it out in seconds."),
          ("Fully digital by default", "No waiting around for prints. Photos are shared the moment they’re taken."),
          ("Prints when you want them", "Add unlimited on-site prints and a dedicated attendant for $200.")]

BACKDROPS = ["Glitter Gold", "Glitter Silver", "Glitter Rose Gold", "Silver Snowflake", "White Art Deco", "Paper Flowers",
             "Floral", "Greenery", "Rustic Wood", "Metal Tread", "Marble White", "Marble Black"]

FAQS = [("Do I need to book a DJ to get the photo booth?", "No. The photo booth is its own booking. If you’d like music too, The Sounds also offers DJ services, and both can be quoted together."),
        ("How do guests get their photos?", "Right at the booth. Guests send their photos to their own phone by text, email or AirDrop, so they can share them that night."),
        ("Do we get all the photos afterwards?", "Yes. After the event you receive every image taken at the booth."),
        ("Can the photos match our theme?", "Yes. Every booth includes custom branding, so the photos carry your name, date, logo or theme in your colours."),
        ("Can we get printed photos?", "Yes. Add unlimited on-site prints and a dedicated attendant for $200. Otherwise the booth is fully digital."),
        ("Which package should we pick?", "Most parties choose 3 hours. If guests are arriving over a long evening, or it’s a gala or holiday party, up to 5 hours means nobody misses it."),
        ("How do we book?", "Send your date, the occasion and how long you’d like the booth through the form below. You’ll get a confirmation of availability and an agreement to sign online. A 50% booking fee reserves your date.")]

STEPS = [("Share the details", "Your date, the occasion, and how long you’d like the booth."),
         ("Get a quick reply", "You’ll hear back with availability and pricing for your date."),
         ("Make it yours", "Choose a backdrop and approve the branding for your photos.")]


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
    fig = lambda n: (f'<figure><img src="assets/backdrops/{n.lower().replace(" ", "-")}.jpg" alt="{e(n)} photo booth backdrop" loading="lazy"><figcaption>{e(n)}</figcaption></figure>')
    bd = "".join(fig(n) for n in BACKDROPS[:4])
    bd_more = "".join(fig(n) for n in BACKDROPS[4:])
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
<meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}assets/hero-booth.jpg"><meta property="og:image:alt" content="{e(HERO_ALT)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(TITLE)}"><meta name="twitter:description" content="{e(DESCRIPTION)}"><meta name="twitter:image" content="{BASE}assets/hero-booth.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Karla:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}{css}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body>
<div class="landing-page"><header class="nav"><div class="wrap nav-inner"><img class="brand-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"><a class="button" href="#check">Check My Date</a></div></header><main>
<section class="hero"><video class="hero-image" autoplay muted loop playsinline preload="auto" poster="assets/video/confetti-poster.jpg" aria-hidden="true"><source src="assets/video/confetti.mp4" type="video/mp4" media="(min-width: 761px)"></video><div class="wrap"><div class="eyebrow">Photo booth rental · Southern Ontario</div><h1>Every great party<br>deserves great memories.</h1><p>A digital selfie booth your guests will actually use. Step in, strike a pose, and the photos land on their phones before the night’s even over.</p><div class="hero-buttons"><a class="button" href="#check">Check My Date <span aria-hidden="true">↗</span></a><a class="button button-outline" href="#pricing">See the Prices <span aria-hidden="true">↓</span></a></div><div class="hero-foot"><span>From $400</span><span>Photos by text, email &amp; AirDrop</span><span>Branded to your theme</span></div></div></section>
<section class="section"><div class="wrap how"><div class="how-media"><video autoplay muted loop playsinline preload="metadata" poster="assets/video/group-props-poster.jpg" aria-label="Four friends posing with signs at the selfie booth"><source src="assets/video/group-props.mp4" type="video/mp4"></video><img src="assets/share-phone.jpg" alt="A guest saving her booth photo to her phone" loading="lazy"></div><div><div class="eyebrow">How it works</div><h2>Easy to use.<br>Instant to share.</h2>{how}</div></div></section>
<section class="section cream" id="pricing" aria-labelledby="packages-title"><div class="wrap"><div class="center"><div class="eyebrow">Simple, all-digital pricing</div><h2 id="packages-title">Pick your time.<br>That’s it.</h2><p class="muted">Every package includes the same booth, the same instant sharing, and every image after the event.</p></div><div class="grid three">{pk}</div><p class="note">Want printed photos? Add unlimited on-site prints and a dedicated attendant for $200. A 50% booking fee reserves your date.</p></div></section>
<section class="section paper"><div class="wrap"><div class="eyebrow">Made for any party</div><h2>Whatever you’re celebrating,<br>there’s a line for the booth.</h2><div class="occasions">{occ}</div><p class="also">{e(ALSO)}</p></div></section>
<section class="section"><div class="wrap"><div class="eyebrow">Every booth includes</div><h2>The little things<br>that make it work.</h2><div class="extras">{extras}</div></div></section>
<section class="section cream"><div class="wrap"><div class="eyebrow">Sample backdrops</div><h2>Set the scene.</h2><p class="muted">A few of the styles available, from glitter and snowflakes to greenery and marble. Ask about matching your theme.</p><div class="backdrops">{bd}</div><details class="more-backdrops"><summary>See {len(BACKDROPS) - 4} more samples</summary><div class="backdrops">{bd_more}</div></details></div></section>
<section class="section"><div class="wrap"><div class="center"><div class="eyebrow">A few helpful details</div><h2>Before you<br>get in touch.</h2></div><div class="faq">{faqs}</div></div></section>
<section class="section inquiry-section cream" id="check" aria-labelledby="inquiry-title"><div class="wrap inquiry-grid"><div><div class="eyebrow">Check my date</div><h2 id="inquiry-title">Let’s get your<br>booth booked.</h2><p class="muted">Share your date, the occasion, and how long you’d like the booth. You’ll hear back soon.</p>{steps}</div><div class="form-shell"><h3>Check My Date</h3>
<iframe src="https://api.profitflo.io/widget/form/{FORM_ID}" style="width:100%;height:1300px;border:none;border-radius:8px;display:block" id="inline-{FORM_ID}" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="{FORM_NAME}" data-height="1300" data-layout-iframe-id="inline-{FORM_ID}" data-form-id="{FORM_ID}" data-cookie-consent="true" data-cookie-consent-provider="auto" title="{FORM_NAME}"></iframe>
<script src="https://api.profitflo.io/js/form_embed.js"></script>
<p class="form-fallback" style="font-size:14px;margin-top:16px">Form not displaying? <a href="{FALLBACK}" style="text-decoration:underline">Open the contact page</a>.</p></div></div></section>
</main><footer class="footer"><div class="wrap"><img class="footer-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"><p>Photo booth rental · Southern Ontario</p><p><a href="tel:+12897688677">289-768-8677</a> · <a href="https://soundsdjevents.com/">soundsdjevents.com</a></p><p>© 2026 The Sounds DJ Services &amp; Entertainment</p></div></footer></div>
<script defer src="tracking.js"></script></body></html>
"""


THANKS_STEPS = [("Check your inbox", "Pricing for 2, 3 and up to 5 hours is already on its way from joe@soundsdj.ca."),
                ("Your date gets checked", "If it’s already booked, you’ll hear that right away instead of being left waiting."),
                ("Reply to hold it", "Ready to go? Reply to the pricing email to hold your date and get your agreement. A 50% booking fee locks it in.")]


def thanks():
    steps = "".join(f'<div class="inquiry-step"><span>{i+1:02d}</span><div><h3>{e(h)}</h3><p>{e(t)}</p></div></div>'
                    for i, (h, t) in enumerate(THANKS_STEPS))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thanks, your request is in | The Sounds Photo Booth</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="icon" href="favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Karla:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}{css}
.landing-page .thanks-hero{{padding:160px 0 90px;min-height:0}}
@media(max-width:760px){{.landing-page .hero.thanks-hero{{background:radial-gradient(ellipse at 95% 0%,#514333,transparent 65%),#171715}}}}
.landing-page .thanks-grid{{display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:start}}
.landing-page .tip{{background:white;border:1px solid #e4dccf;border-radius:12px;padding:28px}}
.landing-page .tip h3{{font-size:19px;margin:0 0 8px}}.landing-page .tip p{{color:var(--muted);margin:0 0 18px}}
@media(max-width:960px){{.landing-page .thanks-grid{{grid-template-columns:1fr;gap:36px}}.landing-page .thanks-hero{{padding:130px 0 60px}}}}
</style>
</head><body>
<div class="landing-page"><header class="nav"><div class="wrap nav-inner"><a href="/"><img class="brand-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"></a></div></header><main>
<section class="hero thanks-hero"><div class="wrap"><div class="eyebrow">Thank you</div><h1>Got it.<br>Your date is on the list.</h1><p>Your photo booth pricing is already on its way to your inbox.</p></div></section>
<section class="section cream"><div class="wrap thanks-grid"><div><div class="eyebrow">What happens next</div><h2>Three quick steps.</h2>{steps}</div>
<div class="tip"><h3>Can’t find the email?</h3><p>Check your Promotions or Junk folder, and add <strong>joe@soundsdj.ca</strong> to your contacts so nothing gets missed.</p>
<h3>Party coming up soon?</h3><p>Call or text <a href="tel:+12897688677">289-768-8677</a>. Short notice is worth a quick conversation.</p>
<a class="button" href="/">Back to the photo booth</a></div></div></section>
</main><footer class="footer"><div class="wrap"><img class="footer-logo" src="assets/logo-white.png" alt="The Sounds DJ Services &amp; Entertainment"><p>Photo booth rental · Southern Ontario</p><p><a href="tel:+12897688677">289-768-8677</a> · <a href="https://soundsdjevents.com/">soundsdjevents.com</a></p><p>© 2026 The Sounds DJ Services &amp; Entertainment</p></div></footer></div>
<script defer src="tracking.js"></script></body></html>
"""


(D / "index.html").write_text(page())
(D / "thanks.html").write_text(thanks())
(D / "CNAME").write_text(HOST + "\n")
(D / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url></urlset>\n')
(D / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
(D / "404.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | The Sounds</title></head><body><h1>That page could not be found.</h1><p><a href="/">Return to the photo booth</a></p></body></html>\n')
t = (G / "sounds-corporate/tracking.js").read_text()
t = t.replace("corporate.soundsdjevents.com", HOST).replace("'corporate'", "'photobooth'")
t = t.replace("['" + HOST + "', 'soundsdjevents.com', 'weddings.soundsdjevents.com']",
              "['" + HOST + "', 'soundsdjevents.com', 'weddings.soundsdjevents.com', 'corporate.soundsdjevents.com']")
t = """/* Analytics + chat for photobooth.soundsdjevents.com. Generated by build.py from the
   corporate page's tracking.js; edit build.py, not this file.

   GA4        G-7EG50CWDVF   (same property as soundsdjevents.com + weddings.)
   Google Ads AW-972541419   (base tag only; no booth conversion action exists yet)
   Clarity    yd28luey3g
   Meta Pixel 860582841130253
   Chat       ProfitFlo widget 6a23a991e53da97e71ee22c1 ("Master DJ AI")

   Events sent:
     check_date_click   any click on a Check My Date / See the Prices CTA
     phone_click        any click-to-call
     generate_lead      the /thanks page loading, i.e. a real booth form submission
                        (value 600 = the 3-hour package). Meta gets a browser Lead too;
                        the booth form has no Conversions API step, so it isn't counted twice.
""" + t[t.index("*/"):]
t = t.replace("function sdjLoadLater(fn){\n", "function sdjLoadLater(fn){\n  if (/^\\/thanks(\\.html)?\\/?$/.test(location.pathname)) { fn(); return; }\n", 1)
t += """
/* The booth form redirects here on success, so this page loading IS the lead. */
if (/^\\/thanks(\\.html)?\\/?$/.test(location.pathname)) {
  gtag('event', 'generate_lead', { 'page_name': 'photobooth_thanks', 'currency': 'CAD', 'value': 600 });
  if (window.fbq) fbq('track', 'Lead', { content_name: 'Photo booth inquiry', currency: 'CAD', value: 600 });
}
"""
(D / "tracking.js").write_text(t)
print("built", D)
