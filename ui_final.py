def install(site):
    core = site.core

    # Official BUZENT logo lockup: navy B, gold rising connection, two people.
    logo_svg = '''<svg class="bzOfficialMark" viewBox="0 0 92 92" aria-hidden="true">
      <path fill="#09274B" d="M18 8h39c14 0 24 9 24 22 0 9-5 16-13 20 9 4 15 11 15 21 0 5-1 9-4 13H63c3-4 4-8 4-12 0-9-7-15-18-15H35V24h21c6 0 10 4 10 9s-4 9-10 9H35v42H18V8z"/>
      <path fill="#D99A20" d="M10 73C18 47 32 27 56 14 43 28 34 42 29 56c-3 8-4 16-4 25-8-1-13-4-15-8z"/>
      <circle cx="40" cy="65" r="6" fill="#09274B"/><circle cx="57" cy="65" r="6" fill="#D99A20"/>
      <path fill="#09274B" d="M28 84c1-10 6-15 13-15 5 0 8 3 11 6 2-3 6-6 11-6 7 0 12 5 13 15H63c-1-5-3-7-6-7-2 0-3 1-5 3-1 1-3 1-4 0-2-2-3-3-5-3-3 0-5 2-6 7H28z"/>
      <path fill="#D99A20" d="M51 79c2 0 3-1 5-3 1-1 3-2 5-2 4 0 7 3 8 10h7c-1-10-6-15-13-15-5 0-9 3-12 7z"/>
    </svg>'''

    # Replace current header logo with the approved full mark + name.
    import re
    core.BASE = re.sub(r'<a class="logo buzent-logo".*?</a>',
        '<a class="logo buzent-logo finalBrand" href="/" aria-label="BUZENT Home">'+logo_svg+'<span class="finalWord">BU<span>Z</span>ENT</span></a>',
        core.BASE, count=1, flags=re.S)

    categories = [
      ('Digital Marketing','↗','blue'),
      ('Creative & Production','✦','gold'),
      ('Web & Technology','◇','blue'),
      ('Sales & Promotion','◎','gold'),
      ('Influencers & Creators','◉','blue'),
      ('Professional Business Services','✓','gold'),
      ('Agencies','◆','blue')
    ]
    def role_cards():
        cards=[]
        for idx,(name,icon,tone) in enumerate(categories,1):
            roles=core.ROLES.get(name,[])
            text=' • '.join(roles[:5]) + (' • more' if len(roles)>5 else '')
            cards.append(f'''<article class="categoryCard {tone}"><div class="catTop"><span class="catNo">0{idx}</span><span class="catIcon">{icon}</span></div><h3>{name}</h3><p>{text}</p></article>''')
        return ''.join(cards)

    def home():
        body='''
<section class="globalHero finalHero">
 <div class="networkDust"></div>
 <div class="heroCopy">
  <span class="eyebrow">WORLDWIDE BUSINESS × PROFESSIONAL NETWORK</span>
  <h1>Where the right business<br>meets the <span>right talent.</span></h1>
  <p>BUZENT connects business owners with professionals, agencies and growth specialists worldwide — creating relevant opportunities, trusted collaboration and mutual growth on one platform.</p>
  <div class="heroActions"><a class="btn heroBusiness" href="/register/business">Join as a Business</a><a class="btn heroTalent" href="/register/pro">Join as Professional / Agency</a></div>
 </div>
 <div class="connectionStage finalStage">
  <div class="sideNode businessNode"><div class="nodeIcon businessIcon">▦</div><b>BUSINESS OWNERS</b><span>Discover the right expertise to build, market and grow your business.</span></div>
  <div class="hubLines leftLines"></div>
  <div class="globalHub finalHub"><div class="hubOfficial">'''+logo_svg+'''<strong>BU<span>Z</span>ENT</strong></div><small>GLOBAL CONNECTION PLATFORM</small></div>
  <div class="hubLines rightLines"></div>
  <div class="sideNode talentNode"><div class="nodeIcon talentIcon">◎</div><b>PROFESSIONAL TALENT</b><span>Connect with relevant businesses, projects and opportunities worldwide.</span></div>
 </div>
 <div class="worldLine"><span>BUSINESS</span><i></i><b>BUZENT</b><i></i><span>OPPORTUNITY</span></div>
</section>
<section class="valueStrip" id="how"><div><b>01</b><span>Discover</span><small>Find expertise or opportunities by real business need.</small></div><div><b>02</b><span>Connect</span><small>Bring the right business and professional together.</small></div><div><b>03</b><span>Grow</span><small>Build partnerships designed for mutual growth.</small></div></section>
<section class="section categorySection" id="roles"><div class="head"><div><span class="sectionKicker">7 PROFESSIONAL CATEGORIES</span><h2>The people behind every growing business</h2><p class="muted">Structured expertise across marketing, creative, technology, sales, influence, professional services and agencies.</p></div></div><div class="categoryGrid">'''+role_cards()+'''</div></section>
<section class="whyBuzent" id="trust"><span>WHY BUZENT</span><h2>One worldwide platform. Better opportunities for both sides.</h2><p>Businesses find relevant capability. Professionals find relevant opportunity. BUZENT creates the connection for stronger collaboration and sustainable mutual growth.</p></section>'''
        return core.page('Home',body)
    core.app.view_functions['home']=home

    # Footer with official contact details.
    core.BASE = re.sub(r'<div class="footer">.*?</div>', '''<footer class="footer finalFooter"><div><b>BU<span>Z</span>ENT</b><small>Worldwide Business × Professional Talent Network</small></div><div class="footerContact"><span>✉ buzentofficial@gmail.com</span><span>Instagram&nbsp; @buzentofficial</span></div></footer>''', core.BASE, count=1, flags=re.S)

    # Final corporate design overrides. Gold is #D99A20; headings use navy #09274B.
    core.BASE = core.BASE.replace('</style></head>','''<style>
    :root{--bzNavy:#09274B;--bzBlue:#1E73C9;--bzGold:#D99A20;--bzGoldSoft:#FFF5DF}
    .finalBrand{display:flex!important;align-items:center!important;gap:10px!important;min-width:210px!important}.bzOfficialMark{width:48px;height:48px;display:block;flex:0 0 auto}.finalWord{font-family:'Manrope';font-size:24px;font-weight:800;letter-spacing:.18em;color:var(--bzNavy);white-space:nowrap}.finalWord span{color:var(--bzGold)}
    .finalHero{background:radial-gradient(circle at 50% 65%,rgba(30,115,201,.28),transparent 30%),radial-gradient(circle at 82% 18%,rgba(217,154,32,.16),transparent 24%),linear-gradient(135deg,#04172D 0%,#07325F 55%,#0A4177 100%)}
    .finalStage .sideNode{border-color:rgba(255,255,255,.16);box-shadow:0 14px 40px rgba(0,0,0,.12)}.businessIcon{color:#61B5FF!important}.talentIcon{color:#F0B33C!important}.finalHub{padding:22px}.hubOfficial{display:flex;flex-direction:column;align-items:center}.hubOfficial .bzOfficialMark{width:78px;height:78px}.hubOfficial strong{font-family:'Manrope';font-size:22px;letter-spacing:.17em;color:#fff}.hubOfficial strong span{color:var(--bzGold)}
    .categorySection{margin-top:54px}.sectionKicker{display:block;color:var(--bzGold);font-weight:800;font-size:12px;letter-spacing:.12em;margin-bottom:8px}.categoryGrid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.categoryCard{position:relative;background:#fff;border:1px solid #E3E9F1;border-radius:20px;padding:24px;min-height:245px;box-shadow:0 12px 35px rgba(9,39,75,.055);overflow:hidden}.categoryCard:before{content:'';position:absolute;left:0;top:0;width:100%;height:5px}.categoryCard.blue:before{background:linear-gradient(90deg,#0B4F91,#2C8CE3)}.categoryCard.gold:before{background:linear-gradient(90deg,#B9780E,#E7AD38)}.catTop{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px}.catNo{font-family:'Manrope';font-size:12px;font-weight:800;letter-spacing:.1em;color:#94A3B8}.catIcon{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;font-size:20px;font-weight:800}.blue .catIcon{background:#EAF4FF;color:#1769B5}.gold .catIcon{background:var(--bzGoldSoft);color:#B77910}.categoryCard h3{font-size:21px;line-height:1.25;margin:0 0 15px}.categoryCard.blue h3{color:#0B4F91}.categoryCard.gold h3{color:#A96E0B}.categoryCard p{color:#667085;font-size:15px;line-height:1.6;margin:0}
    .finalFooter{display:flex;justify-content:space-between;align-items:center;gap:24px;text-align:left;background:#061B33;color:#D7E4F2;border:0;padding:30px max(4%,calc((100% - 1180px)/2))}.finalFooter b{display:block;font-family:'Manrope';font-size:20px;letter-spacing:.16em;color:#fff}.finalFooter b span{color:var(--bzGold)}.finalFooter small{display:block;margin-top:5px;color:#8FAAC5}.footerContact{display:flex;gap:24px;flex-wrap:wrap;color:#fff;font-weight:600}
    @media(max-width:1050px){.categoryGrid{grid-template-columns:repeat(2,1fr)}}@media(max-width:700px){.finalBrand{min-width:auto!important}.bzOfficialMark{width:40px;height:40px}.finalWord{font-size:18px}.categoryGrid{grid-template-columns:1fr}.finalFooter{flex-direction:column;align-items:flex-start}.footerContact{flex-direction:column;gap:8px}}
    </style></head>''')
