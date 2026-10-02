#!/usr/bin/env python3
"""Static site generator for the NAF Properties redesign.

Run from anywhere:  python3 _build/build.py
Writes every page into the project root (index.html, about.html, …).
Content lives in content.py; styles in assets/css; scripts in assets/js.
"""
import json
import os
import re
from html import escape as e

from content import (AMENITY_ICONS, BROCHURE, CITIES, LEADERS, PARTNERS, PORTFOLIO,
                     PROPERTIES, SERVICES, SITE, STATS, TEAM, VIDEOS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "assets/img/"

# --------------------------------------------------------------------------- icons
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "homeplus": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M12 11v6M9 14h6"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4M2 7h20"/>',
    "layers": '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65M22 12.65l-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "hardhat": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6M14 6a6 6 0 0 1 6 6v3"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "checkc": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
    "tower": '<path d="M4.9 16.1C1 12.2 1 5.8 4.9 1.9M7.8 4.7a6.14 6.14 0 0 0-.8 7.5M16.2 4.8c2 2 2.26 5.11.8 7.47M19.1 1.9a9.96 9.96 0 0 1 0 14.1"/><circle cx="12" cy="9" r="2"/><path d="m8.5 22 3.5-11 3.5 11M9.5 18h5"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2M15 18H9M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "dumbbell": '<path d="M6 6v12M18 6v12M3 9v6M21 9v6M6 12h12"/>',
    "elevator": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="m9 9 3-3 3 3M9 15l3 3 3-3"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "chev-l": '<path d="m15 18-6-6 6-6"/>',
    "chev-r": '<path d="m9 18 6-6-6-6"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "images": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>',
    "external": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "eye": '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
    "sparkle": '<path d="M9.94 14.06 4 20M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/>',
    "play": '<path d="M7 4v16l13-8z"/>',
    "facebook": '<path d="M14 9h3V5h-3c-2.76 0-4 1.79-4 4.5V11H7v4h3v8h4v-8h3l1-4h-4V9.5c0-.28.22-.5.5-.5z"/>',
    "xlogo": '<path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.78zm-1.08 16.2h1.7L7.4 4.72H5.58z"/>',
    "youtube": '<path fill-rule="evenodd" d="M23 7.5a3 3 0 0 0-2.1-2.1C19 5 12 5 12 5s-7 0-8.9.4A3 3 0 0 0 1 7.5 31 31 0 0 0 .6 12 31 31 0 0 0 1 16.5a3 3 0 0 0 2.1 2.1C5 19 12 19 12 19s7 0 8.9-.4a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-4.5 31 31 0 0 0-.4-4.5zM9.75 15V9l5.2 3z"/>',
}
FILLED = {"play", "facebook", "xlogo", "youtube"}


CUR = ' aria-current="page"'
ACTIVE = ' class="active"'
FIRST = ' class="active" fetchpriority="high"'
EAGER = ' fetchpriority="high"'
LAZY = ' loading="lazy"'


def chips(items):
    return "".join(f'<span class="chip">{c}</span>' for c in items)


def ic(name, cls=""):
    c = "icon" + (" fill" if name in FILLED else "") + (" " + cls if cls else "")
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def tel(p):
    return "tel:" + "".join(ch for ch in p if ch.isdigit() or ch == "+")


def prop_url(p):
    return f"property-{p['slug']}.html"


# --------------------------------------------------------------------------- layout
NAV = [
    ("index.html", "Home"),
    ("about", "About Us"),  # dropdown
    ("communities.html", "Communities"),
    ("portfolio.html", "Portfolio"),
    ("services.html", "Services"),
    ("adverts.html", "Ads"),
    ("contact.html", "Contact"),
]
ABOUT_SUB = [
    ("about.html", "Company overview", "Who we are and how we work", "building"),
    ("leadership.html", "Leadership", "The directors who guide NAF Properties", "award"),
    ("mission.html", "Vision, mission & values", "What we stand for", "target"),
    ("team.html", "Meet the team", "The managers and officers behind every estate", "users"),
]
ABOUT_PAGES = {a[0] for a in ABOUT_SUB}


def socials():
    return (f'<div class="socials">'
            f'<a href="{SITE["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{ic("facebook")}</a>'
            f'<a href="{SITE["x"]}" target="_blank" rel="noopener" aria-label="X (Twitter) @propnafilsales">{ic("xlogo")}</a>'
            f'<a href="{SITE["youtube"]}" target="_blank" rel="noopener" aria-label="YouTube">{ic("youtube")}</a>'
            f'</div>')


def brand():
    return (f'<a class="brand" href="index.html" aria-label="NAF Properties Limited, home">'
            f'<img src="{IMG}logo.png" alt="" width="46" height="46">'
            f'<span class="brand-text"><strong>NAF Properties</strong><small>Limited · Est. 2011</small></span></a>')


def header(active):
    items = []
    for href, label in NAV:
        if href == "about":
            cur = "is-current" if active in ABOUT_PAGES else ""
            sub = "".join(
                f'<li><a href="{h}"{CUR if h == active else ""}>{ic(i)}<span><strong>{t}</strong><small>{d}</small></span></a></li>'
                for h, t, d, i in ABOUT_SUB)
            items.append(f'<li class="has-dropdown"><button type="button" class="{cur}" aria-expanded="false" aria-haspopup="true">{label} {ic("chev")}</button><ul class="dropdown">{sub}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{CUR if href == active else ""}>{label}</a></li>')
    drawer_links = []
    for href, label in NAV:
        if href == "about":
            for h, t, _, _ in ABOUT_SUB:
                cls = "" if h == "about.html" else ' class="sub"'
                txt = "About Us" if h == "about.html" else t
                drawer_links.append(f'<a href="{h}"{cls}{CUR if h == active else ""}>{txt} {ic("chev-r")}</a>')
        else:
            drawer_links.append(f'<a href="{href}"{CUR if href == active else ""}>{label} {ic("chev-r")}</a>')
    return f'''
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container"><div class="nav">
    {brand()}
    <nav aria-label="Main"><ul class="nav-links">{"".join(items)}</ul></nav>
    <div class="nav-cta">
      <button type="button" class="btn btn-gold btn-sm btn-book-desktop" data-book="">Book a Visit {ic("arrow", "arrow")}</button>
      <button type="button" class="menu-toggle" data-menu aria-label="Open menu" aria-controls="drawer">{ic("menu")}</button>
    </div>
  </div></div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-backdrop" data-close></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer-top">{brand()}<button type="button" class="close-btn" data-close aria-label="Close menu">{ic("x")}</button></div>
    <nav aria-label="Mobile">{"".join(drawer_links)}</nav>
    <button type="button" class="btn btn-gold btn-block" data-book="">Book a Visit {ic("arrow", "arrow")}</button>
    <div class="drawer-contact">
      <span>{SITE["address"]}</span>
      <a href="{tel(SITE["phones"][0])}">{SITE["phones"][0]}</a>
      <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>
    </div>
  </div>
</div>'''


def footer():
    estates = "".join(f'<li><a href="{prop_url(p)}">{e(p["name"])}</a></li>' for p in PROPERTIES)
    phones = "".join(f'<a href="{tel(p)}">{p}</a><br>' for p in SITE["phones"])
    return f'''
<footer class="site-footer">
  <div class="container">
    <div class="footer-cta">
      <h2>Let's find your next address.</h2>
      <div class="actions">
        <button type="button" class="btn btn-gold" data-book="">Book a Visit {ic("arrow", "arrow")}</button>
        <a class="btn btn-glass" href="contact.html">Contact us</a>
      </div>
    </div>
    <div class="footer-grid">
      <div class="footer-brand">
        {brand()}
        <p>NAF Properties Limited is the property development and facility management subsidiary of the Nigerian Air Force Investment Limited Group, building secure homes and commercial spaces across Nigeria since 2011.</p>
        {socials()}
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="leadership.html">Leadership</a></li>
          <li><a href="mission.html">Vision, mission &amp; values</a></li>
          <li><a href="team.html">Meet the team</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="portfolio.html">Portfolio</a></li>
          <li><a href="adverts.html">Advertise with us</a></li>
        </ul>
      </div>
      <div>
        <h4>Estates</h4>
        <ul>{estates}</ul>
      </div>
      <div>
        <h4>Head office</h4>
        <ul class="footer-contact">
          <li>{ic("pin")}<span>{SITE["address"]}</span></li>
          <li>{ic("phone")}<span>{phones}</span></li>
          <li>{ic("mail")}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 {SITE["legal"]}. All rights reserved.</span>
      <a href="#main" class="back-top" data-top>Back to top {ic("arrow-up")}</a>
    </div>
  </div>
  <div class="footer-word" aria-hidden="true">NAF PROPERTIES</div>
</footer>'''


def estate_options(selected=""):
    opts = ['<option value="">Not sure yet / any estate</option>']
    for p in PROPERTIES:
        s = " selected" if p["slug"] == selected else ""
        opts.append(f'<option value="{p["slug"]}"{s}>{e(p["name"])}, {CITIES[p["city"]][0]}</option>')
    return "".join(opts)


def field(id_, label, kind="text", name=None, required=True, full=False, placeholder="", options=None, auto=""):
    name = name or id_.split("-", 1)[-1]
    req = " required" if required else ""
    cls = "field full" if full else "field"
    lab = label + ("" if required else ' <span class="muted">(optional)</span>')
    ac = f' autocomplete="{auto}"' if auto else ""
    ph = f' placeholder="{e(placeholder)}"' if placeholder else ""
    if kind == "select":
        ctl = f'<select id="{id_}" name="{name}"{req}>{options}</select>'
    elif kind == "textarea":
        ctl = f'<textarea id="{id_}" name="{name}"{req}{ph}></textarea>'
    else:
        ctl = f'<input id="{id_}" name="{name}" type="{kind}"{req}{ph}{ac}>'
    return f'<div class="{cls}"><label for="{id_}">{lab}</label>{ctl}<span class="err" aria-live="polite"></span></div>'


def success(title, body):
    return (f'<div class="form-success" hidden role="status"><h3>{ic("checkc")} {title}</h3><p>{body}</p>'
            f'<button type="button" class="btn btn-outline btn-sm" data-reset-form>Send another</button></div>')


def book_modal():
    return f'''
<div class="modal" id="book-modal" aria-hidden="true">
  <div class="modal-backdrop" data-close></div>
  <div class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="bv-title">
    <div class="modal-head">
      <div><span class="eyebrow">Site inspection</span><h2 id="bv-title">Book a visit</h2>
      <p>Tell us which estate you'd like to see and when. Our sales team will call to confirm.</p></div>
      <button type="button" class="close-btn" data-close aria-label="Close">{ic("x")}</button>
    </div>
    <div class="modal-body">
      <form data-form class="form-grid" action="#" method="post">
        <input type="hidden" name="category" value="Book Visit">
        {field("bv-name", "Full name", auto="name")}
        {field("bv-phone", "Phone", "tel", auto="tel", placeholder="+234")}
        {field("bv-email", "Email", "email", full=True, auto="email")}
        {field("bv-estate", "Estate", "select", name="page", required=False, full=True, options=estate_options())}
        {field("bv-date", "Preferred date", "date", name="date")}
        {field("bv-time", "Preferred time", "select", name="time", options='<option value="">Choose a time</option><option>Morning</option><option>Afternoon</option>')}
        {field("bv-msg", "Anything we should know?", "textarea", name="report", required=False, full=True)}
        <div class="full"><button class="btn btn-primary btn-block" type="submit">Request visit {ic("arrow", "arrow")}</button></div>
      </form>
      {success('Request received', 'Thank you, <span data-who>there</span>. Our sales team will call you to confirm your visit.')}
    </div>
  </div>
</div>'''


def lightbox():
    return f'''
<div class="modal lightbox" id="lightbox" aria-hidden="true">
  <div class="modal-backdrop" data-close></div>
  <div class="modal-dialog" role="dialog" aria-modal="true" aria-label="Image viewer">
    <button type="button" class="close-btn" data-close aria-label="Close">{ic("x")}</button>
    <figure><img src="" alt=""><figcaption><strong></strong><span></span></figcaption></figure>
    <button type="button" class="lb-nav prev" aria-label="Previous image">{ic("chev-l")}</button>
    <button type="button" class="lb-nav next" aria-label="Next image">{ic("chev-r")}</button>
  </div>
</div>'''


def backdrop(body):
    keys = list(dict.fromkeys(re.findall(r'data-bg="([^"]+)"', body)))
    imgs = "".join(
        f'<img src="{IMG}{k}" alt="" data-key="{k}" decoding="async"{FIRST if i == 0 else ""}>'
        for i, k in enumerate(keys))
    return f'<div class="backdrop" aria-hidden="true">{imgs}<div class="backdrop-shade"></div><div class="backdrop-grain"></div></div>'


def page(filename, title, description, body, active=None, og_image="pf-dell.jpg", extra_head=""):
    active = active or filename
    full_title = f"{title} | NAF Properties Limited" if filename != "index.html" else "NAF Properties Limited | Secure Homes & Estates in Nigeria"
    html = f'''<!doctype html>
<html lang="en-NG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#0A1238">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NAF Properties Limited">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE["url"]}/{IMG}{og_image}">
<link rel="icon" type="image/png" href="{IMG}logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Raleway:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.classList.add("js");setTimeout(function(){{document.querySelectorAll(".reveal").forEach(function(el){{el.classList.add("in")}})}},4000);</script>
{extra_head}
</head>
<body>
{backdrop(body)}
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{book_modal()}
{lightbox()}
<button type="button" class="to-top" aria-label="Back to top"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="26"/></svg>{ic("arrow-up")}</button>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="assets/js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


# --------------------------------------------------------------------------- components
def sheet(*sections):
    return '<div class="sheet">' + "".join(sections) + "</div>"


def section(inner, cls=""):
    return f'<section class="section {cls}"><div class="container">{inner}</div></section>'


def window(bg, inner, cls="", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<section class="window {cls}"{i} data-bg="{bg}"><div class="container">{inner}</div></section>'


def page_hero(bg, eyebrow, title, lead, crumbs, extra=""):
    cr = '<li><a href="index.html">Home</a></li>' + "".join(
        f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for h, t in crumbs)
    return f'''
<section class="window page-hero" data-bg="{bg}">
  <div class="container">
    <nav aria-label="Breadcrumb"><ol class="crumbs">{cr}</ol></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p>{lead}</p>
    {extra}
  </div>
</section>'''


def about_subnav(active):
    links = "".join(f'<a href="{h}"{CUR if h == active else ""}>{t}</a>' for h, t, _, _ in ABOUT_SUB)
    return f'<nav class="subnav" aria-label="About us">{links}</nav>'


def section_head(eyebrow, title, lead="", center=False, action=""):
    if action:
        return f'<div class="section-head split reveal"><div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{f"<p>{lead}</p>" if lead else ""}</div>{action}</div>'
    cls = "section-head center" if center else "section-head"
    return f'<div class="{cls} reveal"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{f"<p>{lead}</p>" if lead else ""}</div>'


def d(i):
    return f' style="--d:{(i % 4) * 0.08:.2f}s"'


def estate_card(p, i=0, wide=False):
    city, code, _ = CITIES[p["city"]]
    alt = next((g for g in p["gallery"] if g != p["img"]), None)
    alt_img = f'<img class="alt" src="{IMG}{alt}" alt="" loading="lazy">' if alt else ""
    status_cls = "status-tag building" if p["building"] else "status-tag"
    n = len(set(p["gallery"]) | {p["img"]})
    return f'''
<a class="estate-card reveal{' wide' if wide else ''}" href="{prop_url(p)}" data-tags="{p["city"]} {p["category"]}"{d(i)}>
  <img src="{IMG}{p["img"]}" alt="{e(p["name"])}, {e(p["area"])}" loading="lazy">{alt_img}
  <div class="ec-top"><span class="code-tag" title="{city}">{code}</span><span class="{status_cls}">{p["status"]}</span></div>
  <div class="ec-body glass">
    <span class="type">{p["type"]} · {n} photos</span>
    <h3>{e(p["name"])}</h3>
    <span class="loc">{ic("pin")}{e(p["area"])}</span>
    <span class="orb" aria-hidden="true">{ic("arrow")}</span>
  </div>
</a>'''


def stats_band(light=False):
    items = "".join(
        f'<div class="stat reveal"{d(i)}><b><span data-count="{n}">{n:,}</span>{s}</b><span>{l}</span></div>'
        for i, (n, s, l) in enumerate(STATS))
    return f'<div class="stats{" on-light" if light else ""}">{items}</div>'


def partners_block():
    items = "".join(f'<div class="partner reveal"{d(i)}><img src="{IMG}{img}" alt="{n} logo" loading="lazy"><span>{n}</span></div>' for i, (img, n) in enumerate(PARTNERS))
    return section_head("Partners", "Organisations that work with us", "We build alongside respected names in Nigerian business and finance.", center=True) + f'<div class="partners">{items}</div>'


def cta_window(bg, title="Ready to see an estate in person?", text="Book a guided site visit with our sales team, or call us to talk through your options."):
    return window(bg, f'''
  <div class="reveal"><span class="eyebrow">Book a visit</span><h2 style="margin-top:18px">{title}</h2><p>{text}</p></div>
  <div class="actions reveal">
    <button type="button" class="btn btn-gold" data-book="">Book a Visit {ic("arrow", "arrow")}</button>
    <a class="btn btn-glass" href="{tel(SITE["phones"][0])}">{ic("phone")} {SITE["phones"][0]}</a>
  </div>''', "cta-window")


def video_tile(key):
    v = VIDEOS[key]
    return f'''<a class="video-tile reveal" href="{v["url"]}" target="_blank" rel="noopener">
  <img src="{IMG}{v["poster"]}" alt="" loading="lazy">
  <span class="play">{ic("play")}</span>
  <span class="cap"><strong>{v["title"]}</strong><small>{v["src"]} {ic("external")}</small></span>
  <span class="sr-only">(opens in a new tab)</span>
</a>'''


def bento(items, group):
    """items: list of (img, caption, size_class)."""
    out = "".join(
        f'<button type="button" class="{cls} reveal" data-lightbox="{group}" data-title="{e(cap)}" data-text=""{d(i)}><img src="{IMG}{img}" alt="{e(cap)}" loading="lazy"><span class="cap">{e(cap)}</span></button>'
        for i, (img, cap, cls) in enumerate(items))
    return f'<div class="bento">{out}</div>'


def marquee(items):
    figs = "".join(f'<figure><img src="{IMG}{img}" alt="" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>' for img, cap in items)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{figs}{figs}</div></div>'


ALL_HOMES = [
    ("dell-duplex-render.jpg", "NAF Dell Estate, Katampe"),
    ("prop-valley.jpg", "NAF Valley Estate, Asokoro"),
    ("tucano-render-wide.jpg", "Super Tucano Estate, Port Harcourt"),
    ("prop-dell.jpg", "NAF Dell Estate, Katampe"),
    ("valley-fm-office.jpg", "NAF Valley Estate, Asokoro"),
    ("prop-mfb.jpg", "NAF Microfinance Bank, Asokoro"),
    ("prop-golden.jpg", "NAF Golden Estate, Ilorin"),
    ("prop-tucano.jpg", "Super Tucano Estate, Port Harcourt"),
    ("pf-lavida.jpg", "NAF Lavida Tower, Lagos"),
    ("prop-shopping.jpg", "NAF Shopping Complex, Ikeja"),
    ("valley-aerial.jpg", "NAF Valley Estate, Asokoro"),
    ("mfb-front.jpg", "NAF Microfinance Bank, Asokoro"),
    ("pf-valley-shopping.jpg", "Valley Shopping Complex, Asokoro"),
    ("estate-rooftops.jpg", "Residential estate, aerial view"),
]

OFFER = [
    ("home", "Residential", "Secure estates for homeowners, tenants and investors, built to deliver value for money.", "communities.html#residential"),
    ("store", "Commercial", "Shopping complexes, offices and lease spaces in prime, high-traffic locations.", "communities.html#commercial"),
    ("layers", "Infrastructure", "Design, development and delivery of roads, utilities and comprehensive civil works.", "services.html#building-civil-works"),
]

WHY = [
    ("shield", "Reliable partner", "A trustworthy, dependable developer that delivers stylish, high-quality homes and properties."),
    ("trend", "Strong returns", "Prime, growing locations, including Asokoro, Katampe, Ikeja, Ilorin and Port Harcourt, positioned for long-term value."),
    ("award", "Excellence", "The highest standard in every part of our business, from a talented, driven and dedicated team."),
    ("compass", "Forward-thinking", "Modern design and new technology, like drone footage that lets you see a development before it's finished."),
]

# Gallery mosaics: 4-column grid; every layout fills complete rows.
# b-big 2x2, b-big3 3x2, b-half 2x2, b-wide 2x1, b-tall 1x2, "" 1x1.
# Portrait photos only go in b-tall slots; panoramas in b-wide slots.
PROPERTY_MOSAIC = {
    "dell-estate": [("dell-duplex-render.jpg", "b-big"), ("prop-dell.jpg", ""), ("pf-dell.jpg", ""),
                    ("dell-site-aerial.jpg", "b-wide"), ("dell-site-1.jpg", "b-wide"), ("dell-site-3.jpg", "b-wide")],
    "valley-estate": [("valley-aerial.jpg", "b-big"), ("prop-valley.jpg", ""), ("valley-fm-office.jpg", ""),
                      ("valley-aerial-wide.jpg", "b-wide"), ("estate-rooftops.jpg", "b-wide"), ("pf-valley.jpg", "b-wide")],
    "super-tucano-estate": [("tucano-render-wide.jpg", "b-half"), ("prop-tucano.jpg", "b-half")],
    "shopping-complex-ikeja": [("prop-shopping.jpg", "b-big"), ("pf-shopping.jpg", "b-wide"), ("pf-valley-shopping.jpg", "b-wide")],
    "golden-estate-ilorin": [("prop-golden.jpg", "b-big"), ("golden-gate.jpg", "b-tall"), ("golden-wall.jpg", "b-tall")],
    "microfinance-bank-building": [("prop-mfb.jpg", "b-big3"), ("mfb-front.jpg", "b-tall")],
}

TOUR_BG = {"dell-estate": "prop-dell.jpg", "valley-estate": "valley-aerial-wide.jpg", "super-tucano-estate": "tucano-render-wide.jpg",
           "shopping-complex-ikeja": "prop-shopping.jpg", "golden-estate-ilorin": "prop-golden.jpg", "microfinance-bank-building": "prop-mfb.jpg"}


# --------------------------------------------------------------------------- pages
def build_home():
    city_opts = '<option value="all">All locations</option>' + "".join(f'<option value="{k}">{v[0]}</option>' for k, v in CITIES.items())
    offer = "".join(f'<a class="offer-item" href="{h}"><span class="icon-well">{ic(i)}</span><span><h3>{t}</h3><p>{dd}</p></span>{ic("arrow", "arrow")}</a>' for i, t, dd, h in OFFER)

    total = len(PROPERTIES)
    chapters = ""
    for n, p in enumerate(PROPERTIES, 1):
        city, code, state = CITIES[p["city"]]
        thumbs = "".join(f'<img src="{IMG}{g}" alt="" loading="lazy">' for g in [x for x in p["gallery"] if x != TOUR_BG[p["slug"]]][:3])
        amen = chips(p["amenities"][:3])
        chapters += f'''
<section class="window chapter" id="tour-{p["slug"]}" data-bg="{TOUR_BG[p["slug"]]}">
  <div class="container">
    <div class="chapter-card glass reveal">
      <div class="count"><span><b>{n:02d}</b> / {total:02d}</span><span class="status-tag{" building" if p["building"] else ""}">{p["status"]}</span></div>
      <h3>{e(p["name"])}</h3>
      <span class="loc">{ic("pin")}{e(p["area"])}</span>
      <p>{e(p["summary"])}</p>
      <div class="chips">{amen}</div>
      {f'<div class="chapter-thumbs">{thumbs}</div>' if thumbs else ""}
      <div class="actions">
        <a class="btn btn-gold btn-sm" href="{prop_url(p)}">View estate {ic("arrow", "arrow")}</a>
        <button type="button" class="btn btn-glass btn-sm" data-book="{p["slug"]}">Book a visit</button>
      </div>
    </div>
    <div class="chapter-code outline-text" aria-hidden="true">{code}</div>
  </div>
</section>'''
    rail = "".join(f'<a href="#tour-{p["slug"]}"><span>{e(p["name"])}</span>{CITIES[p["city"]][1]}</a>' for p in PROPERTIES)

    gallery = bento([
        ("dell-duplex-render.jpg", "NAF Dell Estate, Katampe", "b-big"),
        ("prop-valley.jpg", "NAF Valley Estate, Asokoro", ""),
        ("prop-mfb.jpg", "NAF Microfinance Bank building", ""),
        ("tucano-render-wide.jpg", "Super Tucano Estate, Port Harcourt", "b-wide"),
        ("prop-golden.jpg", "NAF Golden Estate, Ilorin", ""),
        ("pf-lavida.jpg", "NAF Lavida Tower, Lagos", ""),
        ("valley-aerial-wide.jpg", "NAF Valley Estate, Asokoro", "b-wide"),
    ], "home-gallery")

    why = "".join(f'<div class="feature reveal"{d(i)}><span class="icon-well">{ic(ii)}</span><h3>{t}</h3><p>{dd}</p></div>' for i, (ii, t, dd) in enumerate(WHY))
    svcs = "".join(f'<a class="svc-card reveal" href="services.html#{s["id"]}"{d(i)}><span class="icon-well">{ic(s["icon"])}</span><h3>{s["title"]}</h3><p>{s["short"]}</p><span class="link-arrow">Learn more {ic("arrow")}</span></a>' for i, s in enumerate(SERVICES[:6]))
    pf = PORTFOLIO
    pf_cards = (
        f'<button type="button" class="pf-card wide reveal" data-lightbox="home-pf" data-title="{e(pf[1]["name"])}, {pf[1]["where"]}" data-text="{e(pf[1]["text"])}"><img src="{IMG}{pf[1]["img"]}" alt="{e(pf[1]["name"])}" loading="lazy"><span class="pf-body"><small>In development</small><strong>{pf[1]["name"]}</strong><span>{pf[1]["where"]}</span></span></button>'
        + "".join(f'<button type="button" class="pf-card reveal" data-lightbox="home-pf" data-title="{e(x["name"])}, {x["where"]}" data-text="{e(x["text"])}"{d(i+1)}><img src="{IMG}{x["img"]}" alt="{e(x["name"])}" loading="lazy"><span class="pf-body"><small>{"Completed" if x["status"] == "completed" else "In development"}</small><strong>{x["name"]}</strong><span>{x["where"]}</span></span></button>' for i, x in enumerate((pf[2], pf[3])))
    )
    ld = {
        "@context": "https://schema.org", "@type": "RealEstateAgent", "name": SITE["legal"],
        "alternateName": "NAF Properties", "url": SITE["url"], "logo": SITE["url"] + "/" + IMG + "logo.png",
        "email": SITE["email"], "telephone": SITE["phones"][0], "foundingDate": "2011-04",
        "address": {"@type": "PostalAddress", "streetAddress": "Plot 156 Aminu Kano Crescent, Wuse II",
                    "addressLocality": "Abuja", "addressRegion": "FCT", "addressCountry": "NG"},
        "sameAs": [SITE["x"]],
    }
    body = f'''
<section class="window hero" data-bg="dell-duplex-render.jpg">
  <div class="container">
    <div class="hero-inner">
      <a class="hero-badge reveal" href="property-dell-estate.html"><b>New</b> NAF Dell Estate, Katampe Extension {ic("arrow")}</a>
      <h1 class="reveal" style="--d:.08s">Modern homes, built to <em>Air Force standards.</em></h1>
      <p class="lead reveal" style="--d:.16s">Secure residential estates and commercial spaces across Abuja, Lagos, Ilorin and Port Harcourt, from the property company of the Nigerian Air Force.</p>
      <div class="actions reveal" style="--d:.24s">
        <a class="btn btn-gold" href="#tour-dell-estate">Take the estate tour {ic("arrow", "arrow")}</a>
        <button type="button" class="btn btn-glass" data-book="">{ic("calendar")} Book a Visit</button>
      </div>
    </div>
    <div class="hero-foot">
      <form class="finder glass reveal" id="finder" style="--d:.32s">
        <div class="f-field"><label for="f-city">Location</label><select id="f-city">{city_opts}</select></div>
        <div class="f-field"><label for="f-type">Property type</label><select id="f-type"><option value="all">All types</option><option value="residential">Residential</option><option value="commercial">Commercial</option></select></div>
        <button class="btn btn-primary" type="submit">Search estates {ic("arrow", "arrow")}</button>
      </form>
      <div class="scroll-cue" aria-hidden="true"><span></span>Scroll</div>
    </div>
  </div>
</section>

{sheet(section(f"""
  <div class="intro-grid">
    <div class="prose reveal">
      <span class="eyebrow">Who we are</span>
      <h2>The property company of the Nigerian Air Force</h2>
      <p class="lead">We give real value to every client, from first-time homeowners and tenants to investors at home and abroad.</p>
      <p>Incorporated in 2011 as a subsidiary of the Nigerian Air Force Investment Limited Group, NAF Properties builds and manages estates with the discipline, security and accountability the Air Force is known for.</p>
      <div class="offer-list">{offer}</div>
    </div>
    <div class="collage reveal" style="--d:.1s">
      <img src="{IMG}prop-dell.jpg" alt="NAF Dell Estate townhouses, Katampe" loading="lazy">
      <img src="{IMG}valley-fm-office.jpg" alt="Facility Management Office at NAF Valley Estate" loading="lazy">
      <img src="{IMG}tucano-render-wide.jpg" alt="Super Tucano Estate, Port Harcourt" loading="lazy">
      <div class="since-stamp glass"><b>2011</b><span>Established</span></div>
    </div>
  </div>"""))}

<section class="window tour-intro" data-bg="prop-dell.jpg">
  <div class="container">
    {section_head("The estate tour", "Six addresses. One standard.", "Scroll to tour every NAF Properties estate and commercial building, from Katampe to Port Harcourt.")}
  </div>
</section>
{chapters}
<nav class="tour-rail" aria-label="Estate tour">{rail}</nav>

{sheet(section(section_head("Gallery", "Modern living, NAF style", "A closer look at our homes and estates. Select any photo to enlarge it.", action=f'<a class="btn btn-outline" href="communities.html">Browse all estates {ic("arrow", "arrow")}</a>') + gallery), '<section class="section tight" style="padding-top:0">' + marquee(ALL_HOMES) + '</section>')}

{window("valley-aerial.jpg", section_head("By the numbers", "A track record you can see", "Fifteen years of homes, estates and infrastructure across Nigeria.") + f'<div class="glass" style="padding:clamp(24px,3vw,44px)">{stats_band()}</div>')}

{sheet(section(section_head("Why choose us", "Built on trust, delivered with discipline", "Our team brings deep industry knowledge and a commitment to continuous improvement to every project.") + f'<div class="features">{why}</div>'),
       section(section_head("What we do", "Services across the property lifecycle", "From feasibility studies to facility management, we cover every stage of a property's life.", action=f'<a class="btn btn-outline" href="services.html">All 9 services {ic("arrow", "arrow")}</a>') + f'<div class="grid grid-3">{svcs}</div>'))}

{window("pf-dell.jpg", f"""
  <div class="split-band">
    <div class="prose reveal">
      <span class="eyebrow">Diaspora investors</span>
      <h2>Own property at home, wherever you live</h2>
      <p class="lead">Real estate investment opportunities for Nigerians in the diaspora, from a developer backed by the Nigerian Air Force.</p>
      <ul class="check-list">
        <li>{ic("check")}<span>Verified listings on every estate</span></li>
        <li>{ic("check")}<span>Videos and drone footage, so you can see a development before you fly in</span></li>
        <li>{ic("check")}<span>Dedicated sales lines for each estate</span></li>
      </ul>
      <div class="actions">
        <a class="btn btn-gold" href="contact.html#diaspora">Talk to our sales team {ic("arrow", "arrow")}</a>
        <a class="btn btn-glass" href="{BROCHURE}" target="_blank" rel="noopener">{ic("download")} Dell Estate brochure</a>
      </div>
    </div>
    <div class="video-tiles">
      {video_tile("diaspora")}
      <div class="video-tiles two">{video_tile("dell_3d")}{video_tile("dell_drone")}</div>
    </div>
  </div>""")}

{window("pf-lavida.jpg", section_head("Portfolio", "Projects that shape skylines", "A selection of completed and upcoming developments.", action=f'<a class="btn btn-glass" href="portfolio.html">See full portfolio {ic("arrow", "arrow")}</a>') + f'<div class="pf-grid">{pf_cards}</div>')}

{sheet(section(partners_block()), section(f"""
  <div class="cta-panel reveal">
    <img src="{IMG}prop-shopping.jpg" alt="" loading="lazy">
    <div>
      <span class="eyebrow" style="color:var(--gold-2)">Join our community</span>
      <h2 style="margin-top:14px">Advertise your business on our estates</h2>
      <p>Earn extra income and unlock new opportunities by reaching residents and shoppers across NAF estates.</p>
    </div>
    <div>
      <form data-form class="form-grid" action="#" method="post">
        <input type="hidden" name="category" value="Advert">
        {field("ad-name", "Full name", auto="name", full=True)}
        {field("ad-email", "Email", "email", auto="email")}
        {field("ad-phone", "Phone", "tel", auto="tel")}
        <div class="full"><button class="btn btn-gold btn-block" type="submit">Get advertising details {ic("arrow", "arrow")}</button></div>
      </form>
      {success("Thanks for your interest", "Our advertising team will contact you with available spaces and rates.")}
    </div>
  </div>""", "tight"))}
<div style="height:var(--sheet-gap)"></div>'''
    page("index.html", "Home",
         "NAF Properties Limited builds and manages secure residential estates and commercial spaces in Abuja, Lagos, Ilorin and Port Harcourt. Book a site visit today.",
         body, og_image="dell-duplex-render.jpg", extra_head=f'<script type="application/ld+json">{json.dumps(ld)}</script>')


GAP = '<div style="height:var(--sheet-gap)"></div>'


def build_about():
    offer = "".join(f'<a class="svc-card reveal" href="{h}"{d(n)}><span class="icon-well">{ic(i)}</span><h3>{t}</h3><p>{dd}</p><span class="link-arrow">Learn more {ic("arrow")}</span></a>' for n, (i, t, dd, h) in enumerate(OFFER))
    explore = "".join(
        f'<a class="explore-card reveal" href="{h}"{d(n)}><img src="{IMG}{img}" alt="" loading="lazy"><strong>{t} {ic("arrow")}</strong><span>{dd}</span></a>'
        for n, ((h, t, dd, _), img) in enumerate(zip(ABOUT_SUB[1:], ["lead-olanrewaju.jpg", "valley-aerial.jpg", "team-group.jpg"])))
    body = f'''
{page_hero("valley-aerial-wide.jpg", "About us", "Building homes and communities since 2011", "We are the property development and facility management company of the Nigerian Air Force Investment Limited Group.", [(None, "About us")])}
{sheet(section(about_subnav("about.html") + f"""
  <div class="intro-grid">
    <div class="prose reveal">
      <span class="eyebrow">Who we are</span>
      <h2>Welfare-driven, commercially minded</h2>
      <p class="lead">Nigerian Air Force Investment Limited Properties (NAFILPROP) was incorporated in April 2011 as a subsidiary of the Nigerian Air Force Investment Limited Group of Companies (NAFILGC).</p>
      <p>The Nigerian Air Force established NAF Properties to provide welfare-oriented services that boost the morale and combat readiness of NAF personnel. Today we also serve the general public, delivering secure homes, commercial spaces and infrastructure across the country.</p>
      <p>We have built a reputation for high-end properties and infrastructure, and for an experience our clients value, whether they are buying, leasing or investing.</p>
    </div>
    <div class="collage reveal">
      <img src="{IMG}valley-aerial.jpg" alt="Aerial view of NAF Valley Estate, Asokoro" loading="lazy">
      <img src="{IMG}prop-mfb.jpg" alt="NAF Microfinance Bank building" loading="lazy">
      <img src="{IMG}site-inspection-2.jpg" alt="NAF Properties officers on site" loading="lazy">
      <div class="since-stamp glass"><b>2011</b><span>Incorporated</span></div>
    </div>
  </div>"""),
  section(section_head("What we offer", "Three areas of expertise", "Everything we do falls under residential, commercial or infrastructure development.") + f'<div class="grid grid-3">{offer}</div>'))}
{window("tucano-render-wide.jpg", section_head("By the numbers", "15 years of quality, successful projects", "Backed by more than a decade of insight, we take each project from first study to long-term management.") + f'<div class="glass" style="padding:clamp(24px,3vw,44px)">{stats_band()}</div>')}
{sheet(section(section_head("How we work", "From first study to long-term care") + """
  <div class="steps light">
    <div class="step reveal"><h3>Feasibility &amp; planning</h3><p>We study the site, the market and the numbers before anything is designed.</p></div>
    <div class="step reveal" style="--d:.08s"><h3>Design &amp; procurement</h3><p>Our consultants and engineers design the scheme and source materials and contractors.</p></div>
    <div class="step reveal" style="--d:.16s"><h3>Construction</h3><p>Our works team builds homes, roads, streetlights and utilities to a high standard.</p></div>
    <div class="step reveal" style="--d:.24s"><h3>Facility management</h3><p>After handover we keep estates secure, clean and well maintained.</p></div>
  </div>"""),
  section(section_head("Get to know us", "The people and principles behind NAF Properties") + f'<div class="grid grid-3">{explore}</div>'),
  section(partners_block()))}
{cta_window("dell-duplex-render.jpg")}'''
    page("about.html", "About Us", "Learn about NAF Properties Limited, the property development subsidiary of the Nigerian Air Force Investment Limited Group, incorporated in 2011.", body, og_image="valley-aerial-wide.jpg")


def build_leadership():
    md = LEADERS[0]
    others = "".join(
        f'<article class="person reveal"{d(i)}><div class="person-photo"><img src="{IMG}{p["img"]}" alt="{p["rank"]} {p["name"]}" loading="lazy"><span class="badge">{p["abbr"]}</span></div>'
        f'<div><span class="rank">{p["rank"]}</span><h3>{p["name"]}</h3><p class="role">{p["role"]}</p></div></article>'
        for i, p in enumerate(LEADERS[1:]))
    body = f'''
{page_hero("prop-valley.jpg", "Leadership", "Experienced leadership, Air Force discipline", "Senior officers of the Nigerian Air Force guide NAF Properties' strategy, finance, works and governance.", [("about.html", "About us"), (None, "Leadership")])}
{sheet(section(about_subnav("leadership.html") + f"""
  <div class="leader-hero">
    <div class="person-photo reveal"><img src="{IMG}{md["img"]}" alt="{md["rank"]} {md["name"]}"><span class="badge">{md["abbr"]}</span></div>
    <div class="prose reveal" style="--d:.1s">
      <span class="eyebrow">{md["role"]}</span>
      <h2>{md["rank"]} {md["name"]}</h2>
      <p class="lead">As Managing Director, {md["rank"]} {md["name"]} leads NAF Properties Limited and oversees its estates, commercial assets and development programme across Nigeria.</p>
      <p>The Managing Director works with the directors of finance, works and legal services to deliver on our mission: managing NAF assets well, developing quality property and serving both Air Force personnel and the public.</p>
      <div class="actions"><a class="btn btn-primary" href="mission.html">Our vision &amp; mission {ic("arrow", "arrow")}</a><a class="btn btn-outline" href="team.html">Meet the team</a></div>
    </div>
  </div>"""),
  section(section_head("Directors", "The leadership team", "Each director brings Air Force experience to a core area of the business.") + f'<div class="grid grid-4">{others}</div>'))}
{cta_window("valley-aerial-wide.jpg", "Have a question for our leadership?", "Write to our customer service team and we'll make sure it reaches the right office.")}'''
    page("leadership.html", "Leadership", "Meet the leadership of NAF Properties Limited, including the Managing Director and directors of finance, works and legal services.", body, og_image="lead-olanrewaju.jpg")


def build_mission():
    values = [
        ("Integrity", "We keep our word to residents, investors and partners, with honest, transparent dealings on every transaction.", "shield"),
        ("Excellence", "We hold every home, road and service to a high standard, and keep improving how we work.", "award"),
        ("Professionalism", "We bring Air Force discipline, accountability and respect to every client relationship.", "users"),
    ]
    vals = "".join(f'<div class="value-card glass reveal"{d(i)}><span class="num">Core value 0{i+1}</span><span class="icon-well">{ic(ii)}</span><h3>{t}</h3><p>{dd}</p></div>' for i, (t, dd, ii) in enumerate(values))
    body = f'''
{page_hero("tucano-render-wide.jpg", "Vision, mission & values", "What we stand for", "Our purpose is rooted in service to the Nigerian Air Force and to every Nigerian looking for a secure home.", [("about.html", "About us"), (None, "Vision, mission & values")])}
{sheet(section(about_subnav("mission.html") + f"""
  <div class="vm-grid">
    <div class="vm-card vision reveal">
      <span class="icon-well">{ic("eye")}</span>
      <span class="eyebrow">Our vision</span>
      <p class="statement">To be the <mark>prime military brand</mark> in property development, with a strong sense of corporate social responsibility, within and outside Nigeria.</p>
    </div>
    <div class="vm-card mission reveal" style="--d:.1s">
      <span class="icon-well">{ic("target")}</span>
      <span class="eyebrow">Our mission</span>
      <p class="statement">To manage NAF assets and properties, develop property through <mark>commercial partnerships</mark>, and supply building materials, for the benefit of the NAF and the general public.</p>
    </div>
  </div>"""))}
{window("prop-dell.jpg", section_head("Core values", "Integrity, excellence and professionalism", "Three values guide how we build, sell and manage property.") + f'<div class="grid grid-3">{vals}</div>')}
{sheet(section(f"""
  <div class="two-col">
    <img class="rounded-img reveal" src="{IMG}valley-aerial.jpg" alt="Aerial view of NAF Valley Estate" loading="lazy" style="aspect-ratio:4/3">
    <div class="prose reveal" style="--d:.1s">
      <span class="eyebrow">Our mandate</span>
      <h2>What our mission covers</h2>
      <ul class="check-list">
        <li>{ic("check")}<span><strong>Facility management</strong> of Nigerian Air Force assets and properties.</span></li>
        <li>{ic("check")}<span><strong>Commercial arrangements</strong> for property development, including public–private partnerships.</span></li>
        <li>{ic("check")}<span><strong>Manufacturing, importation and distribution</strong> of building materials for the construction industry.</span></li>
      </ul>
      <a class="link-arrow" href="services.html">Explore our services {ic("arrow")}</a>
    </div>
  </div>"""))}
{cta_window("dell-duplex-render.jpg")}'''
    page("mission.html", "Vision, Mission & Values", "The vision, mission and core values of NAF Properties Limited: integrity, excellence and professionalism.", body, og_image="tucano-render-wide.jpg")


def build_team():
    people = "".join(
        f'<article class="person reveal"{d(i)}><div class="person-photo"><img src="{IMG}{p["img"]}" alt="{p["rank"]} {p["name"]}" loading="lazy"></div>'
        f'<div><span class="rank">{p["rank"]}</span><h3>{p["name"]}</h3><p class="role">{p["role"]}</p></div></article>'
        for i, p in enumerate(TEAM))
    body = f'''
{page_hero("team-group.jpg", "Meet the team", "The people behind every estate", "Our managers, works officers and specialists keep projects on track and residents well served.", [("about.html", "About us"), (None, "Meet the team")])}
{sheet(section(about_subnav("team.html") + f"""
  <div class="two-col">
    <div class="prose reveal">
      <span class="eyebrow">Our people</span>
      <h2>A team of 95 skilled professionals</h2>
      <p class="lead">Serving officers and civilian professionals work side by side at NAF Properties.</p>
      <p>From properties and finance to works, legal, ICT and audit, our team brings the planning and accountability of the Air Force to every development we deliver.</p>
    </div>
    <img class="rounded-img reveal" src="{IMG}team-group.jpg" alt="NAF Properties staff in company uniform" loading="lazy" style="aspect-ratio:16/10">
  </div>"""),
  section(section_head("Management", "Managers and officers", "The people you'll work with on sales, projects and administration.") + f'<div class="grid grid-3">{people}</div>'))}
{cta_window("prop-dell.jpg", "Want to talk to someone on our team?", "Call our head office or send us a message and we'll connect you with the right person.")}'''
    page("team.html", "Meet the Team", "Meet the managers and officers of NAF Properties Limited, from properties and finance to works, ICT and audit.", body, og_image="team-group.jpg")


def build_communities():
    city_btns = '<button type="button" class="filter-btn" data-key="city" data-value="all" aria-pressed="true">All cities</button>' + "".join(
        f'<button type="button" class="filter-btn" data-key="city" data-value="{k}" aria-pressed="false">{v[0]} <span class="count">{sum(1 for p in PROPERTIES if p["city"] == k)}</span></button>'
        for k, v in CITIES.items())
    type_btns = ('<button type="button" class="filter-btn" data-key="type" data-value="all" aria-pressed="true">All types</button>'
                 '<button type="button" class="filter-btn" data-key="type" data-value="residential" aria-pressed="false">Residential</button>'
                 '<button type="button" class="filter-btn" data-key="type" data-value="commercial" aria-pressed="false">Commercial</button>')
    cards = "".join(estate_card(p, i) for i, p in enumerate(PROPERTIES))
    rows = ""
    for k, (city, code, state) in CITIES.items():
        ests = [p for p in PROPERTIES if p["city"] == k]
        names = ", ".join(f'<a href="{prop_url(p)}">{e(p["name"])}</a>' for p in ests)
        building = any(p["building"] for p in ests)
        rows += f'<tr><td><span class="code-tag">{code}</span></td><td><strong>{city}</strong><br><small>{state}</small></td><td>{names}</td><td><span class="status-tag{" building" if building else ""}">{"Now building" if building else "Completed"}</span></td></tr>'
    gal = bento([
        ("estate-rooftops.jpg", "Residential estate, aerial view", "b-big"),
        ("prop-tucano.jpg", "Super Tucano Estate, Port Harcourt", ""),
        ("pf-shopping.jpg", "NAF Shopping Complex, Ikeja", ""),
        ("pf-dell.jpg", "NAF Dell Estate, Katampe", "b-wide"),
        ("prop-golden.jpg", "NAF Golden Estate, Ilorin", ""),
        ("prop-mfb.jpg", "NAF Microfinance Bank building", ""),
        ("valley-fm-office.jpg", "NAF Valley Estate, Asokoro", ""),
        ("pf-valley-shopping.jpg", "Valley Shopping Complex, Asokoro", ""),
    ], "comm-gallery")
    body = f'''
{page_hero("tucano-render-wide.jpg", "Communities", "Estates across four Nigerian cities", "Browse every NAF Properties estate and commercial building. Filter by city or property type.", [(None, "Communities")])}
{sheet(section(f"""
    <div class="filters" data-filter-group="#estate-grid">
      <span class="label">City</span>{city_btns}
      <span class="filter-sep" aria-hidden="true"></span>
      <span class="label">Type</span>{type_btns}
      <span class="result-count" aria-live="polite">{len(PROPERTIES)} results</span>
    </div>
    <div class="grid grid-3" id="estate-grid">{cards}</div>
    <div class="empty-state"><p>No estates match those filters yet.</p><button type="button" class="btn btn-outline btn-sm mt-lg" data-reset-filters>Show all estates</button></div>"""))}
{window("valley-aerial-wide.jpg", section_head("Where we build", "Our locations at a glance", "Each estate is tagged with its city's airport code, so you can spot the location at a glance.") + f'<div class="glass board-wrap reveal"><table class="board"><thead><tr><th>Code</th><th>City</th><th>Estates</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>')}
{sheet(section(section_head("Gallery", "Life across our estates", "Select any photo to enlarge it.") + gal))}
{cta_window("dell-duplex-render.jpg", "Found an estate you like?", "Book a guided visit and our sales team will show you around.")}'''
    page("communities.html", "Communities", "Browse NAF Properties estates in Abuja, Lagos, Ilorin and Port Harcourt: NAF Dell Estate, NAF Valley Estate, Super Tucano Estate and more.", body, og_image="prop-valley.jpg")


def build_portfolio():
    btns = ('<button type="button" class="filter-btn" data-key="s" data-value="all" aria-pressed="true">All projects</button>'
            '<button type="button" class="filter-btn" data-key="s" data-value="completed" aria-pressed="false">Completed</button>'
            '<button type="button" class="filter-btn" data-key="s" data-value="development" aria-pressed="false">In development</button>')
    cards = ""
    for i, x in enumerate(PORTFOLIO):
        st = "Completed" if x["status"] == "completed" else "In development"
        wide = " wide" if i == 0 else ""
        cards += (f'<button type="button" class="pf-card{wide} reveal" data-tags="{x["status"]}" data-lightbox="pf" data-title="{e(x["name"])}, {e(x["where"])}" data-text="{e(x["line"] + " " + x["text"])}"{d(i)}>'
                  f'<img src="{IMG}{x["img"]}" alt="{e(x["name"])}" loading="lazy"><span class="pf-body"><small>{st}</small><strong>{e(x["name"])}</strong><span>{e(x["where"])}</span></span></button>')
    rows = "".join(
        f'<div class="svc-row reveal"><span class="icon-well">{ic("building" if "Complex" in x["name"] or "Tower" in x["name"] else "home")}</span><div><h3>{e(x["name"])}</h3><p style="font-family:var(--font-display);color:var(--blue);font-weight:600;margin-bottom:8px">{e(x["line"])}</p><p>{e(x["text"])}</p>'
        + (f'<p style="margin-top:14px"><a class="link-arrow" href="{x["link"]}">View estate {ic("arrow")}</a></p>' if x.get("link") else "") + '</div></div>'
        for x in PORTFOLIO)
    body = f'''
{page_hero("pf-lavida.jpg", "Portfolio", "Developments we're proud of", "From completed estates in Abuja, Lagos and Ilorin to new towers on the Lagos coastline.", [(None, "Portfolio")])}
{sheet(section(f'<div class="filters" data-filter-group="#pf-grid">{btns}<span class="result-count" aria-live="polite"></span></div><div class="pf-grid" id="pf-grid">{cards}</div><div class="empty-state"><p>No projects match that filter.</p></div>'))}
{window("valley-aerial.jpg", section_head("By the numbers", "Fifteen years of delivery") + f'<div class="glass" style="padding:clamp(24px,3vw,44px)">{stats_band()}</div>')}
{sheet(section(section_head("Project notes", "About each development") + f'<div class="svc-list">{rows}</div>'))}
{cta_window("pf-dell.jpg", "Interested in a development?", "Talk to our sales team about availability, pricing and site visits.")}'''
    page("portfolio.html", "Portfolio", "See the NAF Properties portfolio: NAF Dell Estate, NAF Lavida Tower, NAF Valley Estate, NAF Golden Estate and our shopping complexes.", body, og_image="pf-lavida.jpg")


def build_services():
    index = "".join(f'<a href="#{s["id"]}"><span>{i:02d}</span>{s["title"]}</a>' for i, s in enumerate(SERVICES, 1))
    rows = "".join(
        f'<article class="svc-row reveal" id="{s["id"]}"><span class="icon-well">{ic(s["icon"])}</span><div><h3>{s["title"]}</h3><p>{s["text"]}</p>'
        f'<div class="chips">{chips(s["chips"])}</div>'
        + (f'<p style="margin-top:20px"><a class="btn btn-gold btn-sm" href="contact.html#quote">Request a materials quote {ic("arrow", "arrow")}</a></p>' if s["id"] == "building-materials" else "")
        + (f'<p style="margin-top:20px"><a class="btn btn-outline btn-sm" href="adverts.html">Advertising enquiries {ic("arrow", "arrow")}</a></p>' if s["id"] == "outdoor-advertising" else "")
        + '</div></article>'
        for s in SERVICES)
    body = f'''
{page_hero("dell-site-aerial.jpg", "Services", "Nine services, one trusted partner", "We design, build, lease and manage property, and supply the materials to build it.", [(None, "Services")])}
{sheet(section(f'<div class="svc-detail"><nav class="svc-index" aria-label="Services">{index}</nav><div class="svc-list">{rows}</div></div>'))}
{window("prop-dell.jpg", section_head("Our process", "From first conversation to handover", "Whether you need a single building or a whole estate, we follow the same proven steps.") + """
  <div class="steps">
    <div class="step glass reveal"><h3>Consultation</h3><p>Tell us what you need. We review your goals, budget and timeline.</p></div>
    <div class="step glass reveal" style="--d:.08s"><h3>Feasibility &amp; design</h3><p>Our consultants assess the site and prepare designs and costings.</p></div>
    <div class="step glass reveal" style="--d:.16s"><h3>Build &amp; supply</h3><p>Our works team delivers construction, with materials from our own supply line.</p></div>
    <div class="step glass reveal" style="--d:.24s"><h3>Manage &amp; maintain</h3><p>We stay on as facility managers to protect your investment.</p></div>
  </div>""")}
{cta_window("tucano-render-wide.jpg", "Let's discuss your project", "Tell us about your site or requirement and our team will get back to you.")}'''
    page("services.html", "Services", "NAF Properties services: facility management, building and civil works, consultancy, leasing, advertising, affordable housing, PPP and building materials.", body, og_image="prop-dell.jpg")


def build_contact():
    sales = "".join(
        f'<div class="sales-line"><span class="code-tag dark">{CITIES[p["city"]][1]}</span><div><strong>{e(p["name"])}</strong><small>{e(p["area"])}</small></div><a class="tel" href="{tel(p["phones"][0])}">{p["phones"][0]}</a></div>'
        for p in PROPERTIES)
    phones = "".join(f'<div class="copy-row"><a href="{tel(p)}">{p}</a><button type="button" class="copy-btn" data-copy="{p}">Copy</button></div>' for p in SITE["phones"])
    enquiry = ('<option value="">Choose a topic</option><option value="general">General enquiry</option><option value="visit">Book a site visit</option>'
               '<option value="buy">Buy or lease a property</option><option value="diaspora" data-hash="diaspora">Diaspora investment</option>'
               '<option value="quote" data-hash="quote">Building materials quote</option><option value="advert">Advertise with us</option>'
               '<option value="partnership">Partnership / PPP</option>')
    faqs = [
        ("How do I book a site visit?", "Use the Book a Visit button at the top of any page, or call the sales line for the estate you're interested in. We'll call you to confirm a date and time."),
        ("Can I invest if I live outside Nigeria?", "Yes. We welcome Nigerians in the diaspora. Watch the videos and drone footage of our developments, then contact our sales team to discuss availability and payment."),
        ("Where can I get the NAF Dell Estate brochure?", 'You can download it from the <a href="property-dell-estate.html">NAF Dell Estate page</a>. It lists the available units.'),
        ("Do you sell building materials to the public?", "Yes. We supply cement, roofing sheets, polystyrene, iron rods, chippings and stone dust to NAF and the general public. Choose “Building materials quote” in the form above."),
    ]
    faq = "".join(f'<details class="faq reveal"><summary>{q}{ic("chev")}</summary><p>{a}</p></details>' for q, a in faqs)
    cards = f'''
<div class="contact-cards mt-lg">
  <div class="contact-card glass reveal"><span class="icon-well">{ic("pin")}</span><h3>Visit our head office</h3><p>{SITE["address"]}</p><a class="link-arrow" href="{SITE["maps"]}" target="_blank" rel="noopener" style="color:#fff">Open in Google Maps {ic("arrow")}</a></div>
  <div class="contact-card glass reveal" style="--d:.08s"><span class="icon-well">{ic("phone")}</span><h3>Call us</h3>{phones}</div>
  <div class="contact-card glass reveal" style="--d:.16s"><span class="icon-well">{ic("mail")}</span><h3>Email us</h3>
    <div class="copy-row"><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><button type="button" class="copy-btn" data-copy="{SITE["email"]}">Copy</button></div>
    <div class="copy-row"><a href="mailto:{SITE["sales_email"]}">{SITE["sales_email"]}</a><button type="button" class="copy-btn" data-copy="{SITE["sales_email"]}">Copy</button></div>
  </div>
</div>'''
    body = f'''
{page_hero("dell-duplex-render.jpg", "Contact", "Let's talk about your next property", "Visit our head office in Wuse II, call our team, or send a message and we'll respond promptly.", [(None, "Contact")], cards)}
{sheet(section(f"""
  <div class="contact-layout">
    <div class="panel reveal" id="message">
      <h2>Send us a message</h2>
      <p>Fill in the form and the right team will reply, usually within one working day.</p>
      <form data-form class="form-grid" action="#" method="post">
        <input type="hidden" name="page" value="contact">
        {field("c-name", "Full name", auto="name")}
        {field("c-email", "Email", "email", auto="email")}
        {field("c-phone", "Phone", "tel", auto="tel", placeholder="+234")}
        {field("c-topic", "Topic", "select", name="category", options=enquiry)}
        {field("c-estate", "Estate", "select", name="estate", required=False, full=True, options=estate_options())}
        {field("c-msg", "Message", "textarea", name="report", full=True, placeholder="How can we help?")}
        <div class="full"><button class="btn btn-primary" type="submit">Send message {ic("arrow", "arrow")}</button></div>
      </form>
      {success("Message sent", "Thank you, <span data-who>there</span>. We've received your message and will reply soon.")}
    </div>
    <div style="display:grid;gap:24px" class="reveal">
      <div class="map-card">
        <img src="{IMG}valley-aerial.jpg" alt="" loading="lazy">
        <span class="pin">{ic("pin")}</span>
        <h3>NAF Properties head office</h3>
        <p>{SITE["address"]}</p>
        <a class="btn btn-gold btn-sm" style="width:fit-content" href="{SITE["maps"]}" target="_blank" rel="noopener">Get directions {ic("arrow", "arrow")}</a>
      </div>
      <div>
        <h3 style="margin-bottom:12px">Estate sales lines</h3>
        <div class="sales-lines">{sales}</div>
      </div>
    </div>
  </div>"""), section('<div style="max-width:860px;margin-inline:auto">' + section_head("FAQ", "Common questions", center=True) + f'<div class="faqs">{faq}</div></div>'))}
{GAP}'''
    page("contact.html", "Contact", "Contact NAF Properties Limited at Plot 156 Aminu Kano Crescent, Wuse II, Abuja. Call +234 707 829 8067 or email customerservice@nafproperties.com.ng.", body, og_image="dell-duplex-render.jpg")


def build_adverts():
    why = [
        ("users", "Engaged audiences", "Reach residents, visitors and shoppers across our estates and commercial complexes."),
        ("pin", "Prime locations", "Place your brand in Asokoro, Katampe, Ikeja, Ilorin and Port Harcourt, including high-traffic shopping areas."),
        ("clipboard", "Managed for you", "We handle placement, design and maintenance, so your advert always looks its best."),
    ]
    w = "".join(f'<div class="feature reveal"{d(i)}><span class="icon-well">{ic(ii)}</span><h3>{t}</h3><p>{dd}</p></div>' for i, (ii, t, dd) in enumerate(why))
    types = ('<option value="">Choose a format</option><option>Outdoor billboard</option><option>In-estate signage</option>'
             '<option>Shopping complex signage</option><option>Website advert</option><option>Telecom mast site</option>')
    body = f'''
{page_hero("prop-shopping.jpg", "Ads", "Featured listings and advertising", "See current campaigns from NAF Properties, and learn how your business can advertise on our estates.", [(None, "Ads")])}
{sheet(section(section_head("Now featuring", "Current campaign") + f"""
  <div class="ad-feature">
    <img class="reveal" src="{IMG}pf-dell.jpg" alt="NAF Dell Estate advertisement" loading="lazy">
    <div class="body reveal" style="--d:.1s">
      <span class="status-tag light building" style="width:fit-content">Under construction</span>
      <h2>NAF Dell Estate</h2>
      <p style="font-family:var(--font-display);font-size:1.3rem;color:var(--blue);font-weight:500">…where elegance meets serenity.</p>
      <p>Modern apartments in Katampe Extension, Abuja, with elevators, parking and a residents' gym. Download the brochure to see the full list of units.</p>
      <div class="actions">
        <a class="btn btn-primary" href="property-dell-estate.html">View estate {ic("arrow", "arrow")}</a>
        <a class="btn btn-outline" href="{BROCHURE}" target="_blank" rel="noopener">{ic("download")} Brochure (PDF)</a>
      </div>
    </div>
  </div>"""))}
{window("valley-aerial-wide.jpg", section_head("Advertise with us", "Put your business in front of our communities", "Earn extra income and unlock new opportunities by advertising on NAF estates.") + f'<div class="features three">{w}</div>')}
{sheet(section(f"""
  <div class="two-col" style="align-items:start">
    <div class="prose reveal">
      <span class="eyebrow">Get started</span>
      <h2>Request advertising rates</h2>
      <p class="lead">Tell us about your business and the format you're interested in. Our advertising team will send available spaces and rates.</p>
      <ul class="check-list">
        <li>{ic("check")}<span>Outdoor billboards and in-estate signage</span></li>
        <li>{ic("check")}<span>Signage at our shopping complexes</span></li>
        <li>{ic("check")}<span>Sites for telecommunication masts</span></li>
      </ul>
    </div>
    <div class="panel reveal" style="--d:.1s">
      <form data-form class="form-grid" action="#" method="post">
        <input type="hidden" name="category" value="Advert">
        {field("a-biz", "Business name", name="business", full=True, auto="organization")}
        {field("a-name", "Contact name", auto="name")}
        {field("a-phone", "Phone", "tel", auto="tel", placeholder="+234")}
        {field("a-email", "Email", "email", full=True, auto="email")}
        {field("a-type", "Advert format", "select", name="format", full=True, options=types)}
        {field("a-msg", "Tell us more", "textarea", name="report", required=False, full=True)}
        <div class="full"><button class="btn btn-gold btn-block" type="submit">Request rates {ic("arrow", "arrow")}</button></div>
      </form>
      {success("Request received", "Thank you, <span data-who>there</span>. Our advertising team will be in touch with rates and availability.")}
    </div>
  </div>"""))}
{GAP}'''
    page("adverts.html", "Ads & Advertising", "Current NAF Properties campaigns, including NAF Dell Estate, and how to advertise your business on NAF estates.", body, og_image="pf-dell.jpg")


def build_property(p, idx):
    city, code, state = CITIES[p["city"]]
    imgs = list(dict.fromkeys(p["gallery"]))
    layout = PROPERTY_MOSAIC[p["slug"]]
    gal = bento([(img, p["name"], cls) for img, cls in layout], "gal")
    amen = "".join(f'<div class="amenity">{ic(AMENITY_ICONS[a])}{a}</div>' for a in p["amenities"])
    desc = "".join(f"<p>{x}</p>" for x in p["desc"])
    facts = [("Property type", p["type"]), ("Category", p["category"].title()), ("Location", p["area"].split(",")[0]),
             ("City", f"{city}, {state}"), ("Status", p["status"]), ("Listing", "Verified")]
    fact_html = "".join(f'<div class="fact"><small>{k}</small><b>{v}</b></div>' for k, v in facts)
    extra = ""
    if p.get("videos"):
        extra += f'<section><h2>Videos</h2><div class="video-tiles two">{"".join(video_tile(k) for k in p["videos"])}</div></section>'
    if p.get("brochure"):
        extra += f'<section><div class="doc-card"><span class="icon-well">{ic("file")}</span><div><strong>NAF Dell Estate brochure</strong><small>All available units and listings, in PDF.</small></div><a class="btn btn-gold btn-sm" href="{BROCHURE}" target="_blank" rel="noopener">{ic("download")} Download PDF</a></div></section>'
    if p.get("progress"):
        th = "".join(f'<button type="button" data-lightbox="progress" data-title="Current state of NAF Dell Estate" data-text="Construction progress on site, Katampe Extension, Abuja."><img src="{IMG}{img}" alt="NAF Dell Estate construction progress, photo {i+1}" loading="lazy"></button>' for i, img in enumerate(p["progress"]))
        extra += f'<section><h2>Current state of the site</h2><p class="muted">Recent photos from the construction site at Katampe Extension.</p><div class="thumbs">{th}</div></section>'
    phones = "".join(f'<div class="contact-line">{ic("phone")}<div><small>Sales line</small><a href="{tel(x)}">{x}</a></div></div>' for x in p["phones"])
    nxt = PROPERTIES[(idx + 1) % len(PROPERTIES)]
    maps = f'https://www.google.com/maps/search/?api=1&amp;query={e((p["name"] + " " + p["area"]).replace(",", "").replace(" ", "+"))}'
    body = f'''
<section class="window prop-hero" data-bg="{p["hero"]}">
  <div class="container">
    <nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="index.html">Home</a></li><li><a href="communities.html">Communities</a></li><li aria-current="page">{e(p["name"])}</li></ol></nav>
    <div class="chips reveal"><span class="code-tag">{code}</span><span class="status-tag{" building" if p["building"] else ""}">{p["status"]}</span><span class="status-tag" style="background:rgba(255,255,255,.1)">{p["type"]}</span></div>
    <h1 class="reveal" style="--d:.08s">{e(p["name"])}</h1>
    <p class="tagline reveal" style="--d:.14s">{e(p["tagline"])}</p>
    <div class="meta reveal" style="--d:.2s"><span>{ic("pin")}{e(p["area"])}</span><span>{ic("shield")}Verified listing</span><span>{ic("images")}{len(imgs)} photos</span></div>
    <div class="actions reveal" style="--d:.26s">
      <button type="button" class="btn btn-gold" data-book="{p["slug"]}">Book a Visit {ic("arrow", "arrow")}</button>
      <a class="btn btn-glass" href="#photos">{ic("images")} View photos</a>
    </div>
  </div>
</section>
{sheet(section(f'<div id="photos" style="scroll-margin-top:110px">{gal}</div>', "tight gallery-sec"), section(f"""
  <div class="detail-layout">
    <div class="detail-main">
      <section class="reveal"><h2>Overview</h2><div class="prose">{desc}</div></section>
      <section class="reveal"><h2>Key details</h2><div class="facts">{fact_html}</div></section>
      <section class="reveal"><h2>Amenities</h2><div class="amenities">{amen}</div></section>
      {extra}
      <section class="reveal"><h2>Location</h2><div class="map-card" style="min-height:260px"><img src="{IMG}{p["img"]}" alt="" loading="lazy"><span class="pin">{ic("pin")}</span><h3>{e(p["name"])}</h3><p>{e(p["area"])}</p><a class="btn btn-gold btn-sm" style="width:fit-content" href="{maps}" target="_blank" rel="noopener">Open in Google Maps {ic("arrow", "arrow")}</a></div></section>
    </div>
    <aside class="sidebar">
      <div class="book-card">
        <div class="head"><span class="eyebrow" style="color:var(--gold-2)">Booking</span><h2>Request to book</h2><p>Leave your details and the {e(p["name"])} sales team will call you.</p></div>
        <div class="contact-lines">{phones}<div class="contact-line">{ic("mail")}<div><small>Email</small><a href="mailto:{p["email"]}">{p["email"]}</a></div></div></div>
        <form data-form action="#" method="post">
          <input type="hidden" name="category" value="Booking">
          <input type="hidden" name="page" value="{p["slug"]}">
          {field("pb-name", "Full name", auto="name")}
          {field("pb-email", "Email", "email", auto="email")}
          {field("pb-phone", "Phone", "tel", auto="tel", placeholder="+234")}
          {field("pb-msg", "Message", "textarea", name="report", required=False, placeholder=f"I'm interested in {p['name']}…")}
          <button class="btn btn-primary btn-block" type="submit">Send request {ic("arrow", "arrow")}</button>
        </form>
        {success("Request sent", "Thank you, <span data-who>there</span>. The sales team will call you shortly.")}
      </div>
      <div class="verified">{ic("shield")}<span>Verified listing<small>This property is owned and managed by NAF Properties Limited.</small></span></div>
    </aside>
  </div>"""))}
<section class="window" data-bg="{nxt["hero"]}">
  <div class="container next-estate">
    <div class="reveal"><small>Next estate · {CITIES[nxt["city"]][1]}</small><h2>{e(nxt["name"])}</h2><p style="margin-top:12px">{e(nxt["area"])}</p></div>
    <div class="actions reveal"><a class="btn btn-gold" href="{prop_url(nxt)}">View next estate {ic("arrow", "arrow")}</a><a class="btn btn-glass" href="communities.html">All estates</a></div>
  </div>
</section>'''
    page(prop_url(p), f'{p["name"]}, {city}', f'{p["name"]}, {p["area"]}. {p["summary"]} Book a site visit with NAF Properties.', body, active="communities.html", og_image=p["hero"])


if __name__ == "__main__":
    build_home()
    build_about()
    build_leadership()
    build_mission()
    build_team()
    build_communities()
    build_portfolio()
    build_services()
    build_contact()
    build_adverts()
    for n, prop in enumerate(PROPERTIES):
        build_property(prop, n)
