"""All site content in one place. Edit here, then run `python3 _build/build.py`."""

SITE = {
    "name": "NAF Properties Limited",
    "legal": "Nigerian Air Force Properties Limited",
    "url": "https://www.nafproperties.com.ng",
    "address": "Plot 156 Aminu Kano Crescent, Wuse II, FCT-Abuja",
    "maps": "https://www.google.com/maps/search/?api=1&query=Plot+156+Aminu+Kano+Crescent+Wuse+II+Abuja",
    "phones": ["+234 707 829 8067", "+234 902 322 8661", "+234 812 687 9899"],
    "email": "customerservice@nafproperties.com.ng",
    "enquiry_email": "enquiry@nafproperties.com.ng",
    "sales_email": "propnafilsales@gmail.com",
    # TODO(client): replace Facebook / YouTube with the company's real page URLs.
    "facebook": "https://facebook.com",
    "x": "https://x.com/propnafilsales",
    "youtube": "https://www.youtube.com/",
    "founded": 2011,
}

VIDEOS = {
    "diaspora": {"title": "Real estate investment opportunities for Nigerians in the diaspora",
                 "url": "https://www.youtube.com/watch?v=2bRG621wa8M", "poster": "valley-aerial-wide.jpg", "src": "YouTube"},
    "dell_drone": {"title": "Drone video of the NAF Dell Estate site",
                   "url": "https://www.youtube.com/watch?v=0njV1sB_Iwc", "poster": "dell-duplex-render.jpg", "src": "YouTube"},
    "dell_3d": {"title": "3D animation of NAF Dell Estate when completed",
                "url": "https://player.cloudinary.com/embed/?cloud_name=dv0tvko3q&public_id=3D_ANIMATION_ghya2m",
                "poster": "pf-dell.jpg", "src": "3D tour"},
}
BROCHURE = "https://nafproperties.com.ng/uploads/NAFDELLBROCHURE.pdf"

# city slug -> (label, airport code, state)
CITIES = {
    "abuja": ("Abuja", "ABV", "FCT"),
    "lagos": ("Lagos", "LOS", "Lagos State"),
    "ilorin": ("Ilorin", "ILR", "Kwara State"),
    "port-harcourt": ("Port Harcourt", "PHC", "Rivers State"),
}

AMENITY_ICONS = {
    "Elevators": "elevator", "Parking spaces": "car", "Gymnasium": "dumbbell",
    "Green areas": "leaf", "Estate security": "shield", "Retail spaces": "store",
    "High foot traffic": "users", "Secure community": "shield", "Office space": "building",
}

PROPERTIES = [
    {
        "slug": "dell-estate", "id": 6, "name": "NAF Dell Estate", "city": "abuja",
        "area": "Katampe Extension, Abuja", "type": "Apartments", "category": "residential",
        "status": "Under construction", "building": True,
        "tagline": "…where elegance meets serenity.",
        "summary": "Our newest residential development: modern apartments in Katampe Extension, one of Abuja's fastest-growing districts.",
        "desc": [
            "NAF Dell Estate is the newest residential development from NAF Properties, set in Katampe Extension, Abuja. The estate brings together contemporary architecture, quiet streets and the security that comes with a Nigerian Air Force-backed developer.",
            "Apartments are served by elevators, dedicated parking and a residents' gym. Watch the 3D animation to see the finished estate, follow construction through the drone footage, and download the brochure for the full list of units.",
        ],
        "img": "prop-dell.jpg",
        "hero": "dell-duplex-render.jpg",
        "gallery": ["dell-duplex-render.jpg", "prop-dell.jpg", "pf-dell.jpg", "dell-site-aerial.jpg", "dell-site-1.jpg", "dell-site-3.jpg"],
        "progress": ["dell-site-1.jpg", "dell-site-2.jpg", "dell-site-3.jpg", "dell-site-4.jpg", "dell-site-5.jpg"],
        "amenities": ["Elevators", "Parking spaces", "Gymnasium"],
        "phones": ["+234 707 829 8067"], "email": "enquiry@nafproperties.com.ng",
        "videos": ["dell_3d", "dell_drone"], "brochure": True,
    },
    {
        "slug": "valley-estate", "id": 3, "name": "NAF Valley Estate", "city": "abuja",
        "area": "Asokoro, Abuja", "type": "Duplexes", "category": "residential",
        "status": "Completed", "building": False,
        "tagline": "Security, luxury and safety.",
        "summary": "A prestigious residential enclave in Asokoro, built for families who value elegance and peace of mind.",
        "desc": [
            "Experience the blend of security and luxury at NAF Valley Estate, Asokoro, a prestigious residential enclave designed for people who value elegance and peace of mind.",
            "Set in a prime location, the estate offers strong security, well-crafted homes and premium amenities. Whether you want a secure home for your family or a high-value investment, NAF Valley Estate delivers comfort, exclusivity and long-term value. The estate's Facility Management Office is on site.",
        ],
        "img": "prop-valley.jpg",
        "hero": "valley-aerial-wide.jpg",
        "gallery": ["valley-aerial.jpg", "prop-valley.jpg", "valley-aerial-wide.jpg", "valley-fm-office.jpg", "estate-rooftops.jpg", "pf-valley.jpg"],
        "amenities": ["Estate security", "Green areas", "Parking spaces"],
        "phones": ["+234 803 596 9347", "+234 805 119 5693", "+234 806 548 8949"], "email": "propnafilsales@gmail.com",
    },
    {
        "slug": "super-tucano-estate", "id": 4, "name": "Super Tucano Estate", "city": "port-harcourt",
        "area": "Chief G.U. Ake Road, Port Harcourt", "type": "Duplexes", "category": "residential",
        "status": "Completed", "building": False,
        "tagline": "Modern duplex living in Port Harcourt.",
        "summary": "Contemporary duplexes on Chief G.U. Ake Road, Port Harcourt, set among landscaped green areas.",
        "desc": [
            "Sharing its name with the Nigerian Air Force's A-29 Super Tucano aircraft, Super Tucano Estate offers contemporary duplexes on Chief G.U. Ake Road, Port Harcourt, Rivers State.",
            "The estate is laid out around landscaped green areas, giving residents a calm, family-friendly setting with easy access to the city.",
        ],
        "img": "prop-tucano.jpg",
        "hero": "tucano-render-wide.jpg",
        "gallery": ["tucano-render-wide.jpg", "prop-tucano.jpg"],
        "amenities": ["Green areas", "Parking spaces"],
        "phones": ["+234 803 596 9347", "+234 805 119 5693"], "email": "propnafilsales@gmail.com",
    },
    {
        "slug": "shopping-complex-ikeja", "id": 1, "name": "NAF Shopping Complex", "city": "lagos",
        "area": "Sam Ethnan Air Force Base, Ikeja, Lagos", "type": "Retail & offices", "category": "commercial",
        "status": "Completed", "building": False,
        "tagline": "A community of businesses in one secure complex.",
        "summary": "A secure commercial hub inside Sam Ethnan Air Force Base, Ikeja, with prime retail space and high foot traffic.",
        "desc": [
            "NAF Properties Shopping Complex, Ikeja is a commercial hub that gives businesses a strategic, thriving place to trade. It offers modern facilities, prime retail spaces and high foot traffic.",
            "With a focus on convenience, security and accessibility, the complex suits entrepreneurs and established brands alike, and gives shoppers a safe, rewarding place to visit.",
        ],
        "img": "prop-shopping.jpg",
        "hero": "prop-shopping.jpg",
        "gallery": ["prop-shopping.jpg", "pf-shopping.jpg", "pf-valley-shopping.jpg"],
        "amenities": ["Retail spaces", "Parking spaces", "Secure community", "High foot traffic"],
        "phones": ["+234 703 632 6018", "+234 806 548 8949"], "email": "propnafilsales@gmail.com",
    },
    {
        "slug": "golden-estate-ilorin", "id": 2, "name": "NAF Golden Estate", "city": "ilorin",
        "area": "Ilorin, Kwara State", "type": "Apartments", "category": "residential",
        "status": "Completed", "building": False,
        "tagline": "Quality, affordable and safe housing.",
        "summary": "A residential community in Ilorin designed for comfort, security and long-term value.",
        "desc": [
            "NAF Golden Estate, Ilorin is a residential community designed for comfort, security and long-term value. It sits in a thriving neighbourhood and offers modern homes, good amenities and a quiet environment.",
            "It suits homeowners, tenants and investors alike. Whether you want a family home or a sound investment, NAF Golden Estate offers quality living and strong returns.",
        ],
        "img": "prop-golden.jpg",
        "hero": "prop-golden.jpg",
        "gallery": ["prop-golden.jpg", "golden-gate.jpg", "golden-wall.jpg"],
        "amenities": ["Green areas", "Secure community"],
        "phones": ["+234 803 596 9347", "+234 805 119 5693"], "email": "propnafilsales@gmail.com",
    },
    {
        "slug": "microfinance-bank-building", "id": 5, "name": "NAF Microfinance Bank Building", "city": "abuja",
        "area": "NAF Valley Estate, Asokoro, Abuja", "type": "Commercial building", "category": "commercial",
        "status": "Completed", "building": False,
        "tagline": "Commercial space inside NAF Valley Estate.",
        "summary": "A purpose-built commercial building within NAF Valley Estate, home to NAF Microfinance Bank.",
        "desc": [
            "This commercial building sits within NAF Valley Estate, Asokoro, Abuja and houses NAF Microfinance Bank.",
            "It shows the kind of commercial space NAF Properties delivers inside its estates: secure, accessible and with dedicated parking for staff and customers.",
        ],
        "img": "prop-mfb.jpg",
        "hero": "prop-mfb.jpg",
        "gallery": ["prop-mfb.jpg", "mfb-front.jpg", "valley-aerial.jpg"],
        "amenities": ["Office space", "Parking spaces", "Estate security"],
        "phones": ["+234 707 829 8067"], "email": "enquiry@nafproperties.com.ng",
    },
]

PORTFOLIO = [
    {"name": "NAF Dell Estate", "where": "Katampe Extension, Abuja", "img": "pf-dell.jpg", "status": "development",
     "line": "…where elegance meets serenity.",
     "text": "Our newest residential development in Katampe Extension, Abuja, with apartments served by elevators, parking and a residents' gym.",
     "link": "property-dell-estate.html"},
    {"name": "NAF Lavida Tower", "where": "Oniru Close, Lagos", "img": "pf-lavida.jpg", "status": "development",
     "line": "Virtual impression of the proposed tower.",
     "text": "A high-rise development planned for Oniru Close, Lagos. The image shows a virtual impression of the completed towers."},
    {"name": "NAF Valley Estate Shopping Complex", "where": "Asokoro, Abuja", "img": "pf-valley-shopping.jpg", "status": "completed",
     "line": "Everything you want in one building.",
     "text": "A shopping complex serving residents of NAF Valley Estate and the wider Asokoro community."},
    {"name": "NAF Golden Estate", "where": "Ilorin, Kwara State", "img": "prop-golden.jpg", "status": "completed",
     "line": "Quality, affordable and safe housing.",
     "text": "A residential community designed for comfort, security and long-term value, suited to homeowners, tenants and investors.",
     "link": "property-golden-estate-ilorin.html"},
    {"name": "NAF Valley Estate", "where": "Asokoro, Abuja", "img": "pf-valley.jpg", "status": "completed",
     "line": "Security, luxury and safety.",
     "text": "A prestigious residential enclave with strong security, well-crafted homes and premium amenities.",
     "link": "property-valley-estate.html"},
    {"name": "NAF Properties Shopping Complex", "where": "Ikeja, Lagos", "img": "pf-shopping.jpg", "status": "completed",
     "line": "A commercial hub with high foot traffic.",
     "text": "Modern facilities and prime retail space inside Sam Ethnan Air Force Base, Ikeja, built for convenience, security and accessibility.",
     "link": "property-shopping-complex-ikeja.html"},
]

LEADERS = [
    {"rank": "Air Vice Marshal", "name": "R.K. Olanrewaju", "abbr": "MD", "role": "Managing Director", "img": "lead-olanrewaju.jpg"},
    {"rank": "Air Vice Marshal", "name": "S.A. Bukar", "abbr": "DOF", "role": "Director of Finance", "img": "lead-bukar.jpg"},
    {"rank": "Air Commodore", "name": "H. Badamasi", "abbr": "DOW", "role": "Director of Works", "img": "lead-badamasi.jpg"},
    {"rank": "Wing Commander", "name": "M. Saleh", "abbr": "DLS", "role": "Director of Legal Services", "img": "lead-saleh.jpg"},
    {"rank": "Flight Lieutenant", "name": "T.E. Akerele", "abbr": "CSLA", "role": "Company Secretary / Legal Adviser", "img": "lead-akerele.png"},
]

TEAM = [
    {"rank": "Group Captain", "name": "Y.Y. Tai-Medubi", "role": "General Manager, Properties", "img": "team-tai-medubi.jpg"},
    {"rank": "Flight Lieutenant", "name": "D.N. Abraham", "role": "General Manager, Finance", "img": "team-abraham.jpg"},
    {"rank": "Flight Lieutenant", "name": "T.E. Akerele", "role": "General Manager, Administration", "img": "team-akerele.jpg"},
    {"rank": "Squadron Leader", "name": "M.T. Mustapha", "role": "Company Legal Secretary", "img": "team-mustapha.jpg"},
    {"rank": "Squadron Leader", "name": "E. Okunbor", "role": "Works Officer 1", "img": "team-okunbor.jpg"},
    {"rank": "Squadron Leader", "name": "G. David", "role": "Works Officer 2", "img": "team-david.jpg"},
    {"rank": "Flight Lieutenant", "name": "N. Salisu", "role": "Works Officer 3", "img": "team-salisu.jpg"},
    {"rank": "Flight Lieutenant", "name": "E.O. Araoye", "role": "ICT Officer", "img": "team-araoye.jpg"},
    {"rank": "Mrs", "name": "Stephen Ijeoma Blessing", "role": "Internal Auditor", "img": "team-stephen.jpg"},
]

SERVICES = [
    {"id": "facility-management", "icon": "key", "title": "Facility Management",
     "short": "Secure, well-maintained estates that hold their value.",
     "text": "We optimise revenue through efficient property management. Our teams keep environments secure and well maintained, and improve facilities through renovation, security, landscaping and energy efficiency, while putting tenant retention, infrastructure development and community engagement first.",
     "chips": ["Renovation", "Security", "Landscaping", "Energy efficiency"]},
    {"id": "building-civil-works", "icon": "hardhat", "title": "Building & Civil Engineering Works",
     "short": "New housing, roads, streetlights and infrastructure.",
     "text": "We have delivered building and civil engineering projects across our estates, creating modern, comfortable and sustainable living spaces. Our work includes new housing units, infrastructure development, streetlights, renovations and road construction.",
     "chips": ["Housing units", "Road construction", "Streetlights", "Renovations"]},
    {"id": "building-consultancy", "icon": "clipboard", "title": "Building Consultancy",
     "short": "Expert guidance from feasibility to handover.",
     "text": "Since 2011 our consultancy team has guided clients through feasibility studies, design, procurement and project management, with a focus on quality, safety and innovation.",
     "chips": ["Feasibility studies", "Design", "Procurement", "Project management"]},
    {"id": "post-housing-solutions", "icon": "home", "title": "Post-Housing Scheme Solutions",
     "short": "Services that keep communities thriving after handover.",
     "text": "Our post-housing services improve residents' quality of life, protect property value and strengthen community engagement. They cover property management, facility management, waste management, security and community development.",
     "chips": ["Property management", "Waste management", "Security", "Community development"]},
    {"id": "lease-of-facilities", "icon": "building", "title": "Lease of Facilities",
     "short": "Commercial, residential and recreational spaces to lease.",
     "text": "We lease convenient, secure and well-appointed spaces, including commercial, residential, recreational and community facilities, to individuals and organisations.",
     "chips": ["Commercial", "Residential", "Recreational", "Community"]},
    {"id": "outdoor-advertising", "icon": "tower", "title": "Outdoor Advertising & Telecom Masts",
     "short": "Ad placement and mast installation across our estates.",
     "text": "We manage outdoor advertising across our estates, covering placement, design and maintenance, and we handle the design, installation and maintenance of telecommunication masts, balancing advertising impact with estate aesthetics.",
     "chips": ["Ad placement", "Ad design", "Mast installation", "Maintenance"]},
    {"id": "affordable-housing", "icon": "homeplus", "title": "Affordable Housing Delivery",
     "short": "Quality homes within reach for personnel and the public.",
     "text": "We deliver quality, affordable housing through design, construction, flexible financing options and infrastructure development, providing comfortable homes for NAF personnel and the general public.",
     "chips": ["Design", "Construction", "Financing options", "Infrastructure"]},
    {"id": "public-private-partnership", "icon": "handshake", "title": "Public–Private Partnership",
     "short": "Collaborations that deliver infrastructure at scale.",
     "text": "Through Public–Private Partnerships we work with investors, developers and institutions to deliver quality infrastructure and services that neither side could deliver as well alone.",
     "chips": ["Joint ventures", "Infrastructure", "Development partners"]},
    {"id": "building-materials", "icon": "truck", "title": "Sales of Building Materials",
     "short": "Cement, roofing sheets, iron rods and more at competitive prices.",
     "text": "We sell and supply building materials, including cement, roofing sheets, polystyrene, iron rods, chippings and stone dust, at competitive prices to NAF and the general public.",
     "chips": ["Cement", "Roofing sheets", "Polystyrene", "Iron rods", "Chippings", "Stone dust"]},
]

PARTNERS = [
    ("partner-dangote.jpg", "Dangote"),
    ("partner-nafil-housing.jpg", "NAFIL Housing & Construction"),
    ("partner-naf-mfb.jpg", "NAF Microfinance Bank"),
    ("partner-nafil-ltd.jpg", "NAF Investment Limited"),
]

STATS = [(6000, "+", "Finished homes"), (5000, "+", "Happy customers"), (15, "+", "Years since 2011"), (95, "", "Skilled professionals")]
