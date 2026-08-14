import re


def install(site):
    core = site.core

    logo_svg = '''<svg class="bzOfficialMark" viewBox="0 0 120 120" aria-hidden="true">
      <path fill="#FFFFFF" d="M28 12h48c20 0 34 12 34 30 0 12-6 21-16 26 12 5 20 15 20 29 0 4-1 8-3 11H88c2-4 3-7 3-11 0-12-9-20-23-20H48V34h27c7 0 12 5 12 11s-5 11-12 11H48v52H28V12z"/>
      <path fill="#D99A20" d="M16 98C28 65 46 38 78 20 61 39 49 57 42 75c-4 10-6 20-6 31-11-1-18-4-20-8z"/>
      <circle cx="54" cy="84" r="8" fill="#FFFFFF"/><circle cx="76" cy="84" r="8" fill="#D99A20"/>
      <path fill="#FFFFFF" d="M38 111c2-13 8-20 18-20 7 0 12 4 16 8 4-4 9-8 16-8 10 0 17 7 19 20H89c-1-7-4-10-8-10-3 0-5 2-7 4-2 2-4 2-6 0-2-2-5-4-8-4-4 0-7 3-8 10H38z"/>
      <path fill="#D99A20" d="M71 104c3 0 5-2 7-4 2-2 4-3 7-3 5 0 9 4 11 14h11c-2-13-9-20-19-20-7 0-12 4-17 9z"/>
    </svg>'''

    header_logo = '''<a class="logo buzent-logo finalBrand" href="/" aria-label="BUZENT Home"><span class="headerMark">'''+logo_svg+'''</span><span class="finalWord">BU<span>Z</span>ENT</span></a>'''
    core.BASE = re.sub(r'<a class="logo buzent-logo".*?</a>', header_logo, core.BASE, count=1, flags=re.S)

    # Add Blog to the primary navigation without touching login controls.
    core.BASE = core.BASE.replace('<a href="/#trust">Why BUZENT</a>', '<a href="/#trust">Why BUZENT</a><a href="/blog">Blog</a>')

    categories = [
        ('Digital Marketing','DM','blue'),
        ('Creative & Production','CP','gold'),
        ('Web & Technology','WT','blue'),
        ('Sales & Promotion','SP','gold'),
        ('Influencers & Creators','IC','blue'),
        ('Professional Business Services','PB','gold'),
        ('Agencies','AG','blue'),
    ]

    def role_cards():
        out=[]
        for idx,(name,icon,tone) in enumerate(categories,1):
            roles=core.ROLES.get(name,[])
            out.append(f'''<article class="categoryCard {tone}"><div class="catTop"><span class="catNo">0{idx}</span><span class="catIcon">{icon}</span></div><h3>{name}</h3><p>{' • '.join(roles[:6])}{' • more' if len(roles)>6 else ''}</p></article>''')
        return ''.join(out)

    def home():
        body='''
<section class="globalHero finalHero">
 <div class="networkDust"></div>
 <div class="heroCopy">
  <span class="eyebrow">WORLDWIDE BUSINESS × PROFESSIONAL OPPORTUNITY NETWORK</span>
  <h1>Businesses find the right people.<br><span>Professionals find the right clients.</span></h1>
  <p>BUZENT is a global business growth platform connecting business owners with marketers, creators, developers, sales professionals, influencers, CAs, consultants and agencies — while helping those professionals discover relevant clients, projects and long-term opportunities worldwide.</p>
  <div class="heroActions"><a class="btn heroBusiness" href="/register/business">I’m a Business Owner</a><a class="btn heroTalent" href="/register/pro">I’m a Professional / Agency</a></div>
 </div>
 <div class="connectionStage finalStage">
  <div class="sideNode businessNode"><div class="nodeBadge businessBadge">B</div><b>BUSINESS OWNERS</b><span>Find verified expertise for marketing, technology, creative, sales, finance, influence and business growth.</span></div>
  <div class="hubLines leftLines"></div>
  <div class="globalHub finalHub"><div class="hubOfficial">'''+logo_svg+'''<strong>BU<span>Z</span>ENT</strong></div><small>GLOBAL CONNECTION PLATFORM</small></div>
  <div class="hubLines rightLines"></div>
  <div class="sideNode talentNode"><div class="nodeBadge talentBadge">P</div><b>PROFESSIONALS & AGENCIES</b><span>Get discovered by businesses that need your skills, services and measurable value.</span></div>
 </div>
 <div class="worldLine"><span>BUSINESS NEED</span><i></i><b>BUZENT</b><i></i><span>PROFESSIONAL OPPORTUNITY</span></div>
</section>
<section class="purposeStrip" id="how">
 <div><b>01</b><span>Businesses post what they need</span><small>Clear requirements create better matches and reduce random searching.</small></div>
 <div><b>02</b><span>Experts become discoverable</span><small>Professionals and agencies showcase role, capability, proof and relevance.</small></div>
 <div><b>03</b><span>Right-fit connections happen</span><small>BUZENT brings business demand and professional expertise into one trusted network.</small></div>
</section>
<section class="section categorySection" id="roles"><div class="head"><div><span class="sectionKicker">7 CORE PROFESSIONAL CATEGORIES</span><h2>One business can need many experts. BUZENT brings them into one place.</h2><p class="sectionLead">Business owners can discover the people who help them attract customers, build systems, create content, sell, influence audiences, manage compliance and scale operations. Professionals and agencies can position their expertise where real business demand exists.</p></div></div><div class="categoryGrid">'''+role_cards()+'''</div></section>
<section class="whyBuzent" id="trust"><span>WHY BUZENT? ❓</span><h2>The future of business opportunity should be built on the right connection.</h2><p>Finding the right professional should not feel like searching blindly across dozens of platforms. Finding the right client should not depend only on followers, referrals or geography. BUZENT is being built as a worldwide business networking and professional talent platform where businesses can discover relevant expertise and professionals can access genuine business opportunities.</p><p>Our goal is simple: create a trusted ecosystem where business owners can find marketers, agencies, creators, influencers, developers, sales professionals, Chartered Accountants, consultants and other growth specialists based on what the business actually needs — and where those professionals can build visibility around capability, credibility and results.</p><p><strong>Future is BUZENT</strong> means a future where better discovery creates better partnerships, stronger businesses and more meaningful professional opportunities. For searchers looking to find business experts, hire marketing professionals, discover agencies, connect with influencers, find CAs and consultants, or access business growth services worldwide, BUZENT is designed to become the professional bridge between need and expertise.</p><div class="trustSignals"><div><b>For Businesses</b><span>Relevant experts. Clearer choices. Stronger growth partnerships.</span></div><div><b>For Professionals</b><span>Better visibility. Relevant clients. Long-term opportunities.</span></div><div><b>For the Market</b><span>A structured global network built around capability and trust.</span></div></div></section>'''
        return core.page('Home',body)
    core.app.view_functions['home']=home

    def blog():
        body='''<section class="blogHero"><span>BUZENT INSIGHTS</span><h1>Business growth, professional opportunity and the future of work.</h1><p>Practical insights for business owners, marketers, agencies, creators, influencers, consultants and professionals building stronger commercial relationships.</p></section><section class="blogGrid"><article><span>BUSINESS GROWTH</span><h2>How to choose the right professional for your business</h2><p>Define the outcome first, then evaluate expertise, proof, communication and fit. The right expert is not always the biggest profile — it is the person or agency most relevant to the business problem.</p></article><article><span>PROFESSIONAL OPPORTUNITY</span><h2>How professionals can become easier for businesses to trust</h2><p>Clear positioning, relevant proof, transparent capability and outcome-focused communication help businesses understand where you can create value.</p></article><article><span>GLOBAL NETWORK</span><h2>Why the next generation of business platforms will be role-based</h2><p>Businesses increasingly need specialist expertise across marketing, technology, finance, sales, influence and operations. Role-based discovery makes these connections more relevant.</p></article></section>'''
        return core.page('Blog',body)
    if 'blog' not in core.app.view_functions:
        core.app.add_url_rule('/blog','blog',blog)

    # Corporate footer with gold-only contact icons.
    mail_icon='''<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3V5zm1.8 2 7.2 5.3L19.2 7H4.8z" fill="currentColor"/></svg>'''
    insta_icon='''<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg>'''
    footer='''<footer class="footer finalFooter"><div><b>BU<span>Z</span>ENT</b><small>Worldwide Business × Professional Opportunity Network</small></div><div class="footerContact"><a href="mailto:buzentofficial@gmail.com" aria-label="Email BUZENT">'''+mail_icon+'''<span>buzentofficial@gmail.com</span></a><a href="https://instagram.com/buzentofficial" aria-label="BUZENT Instagram">'''+insta_icon+'''<span>@buzentofficial</span></a></div></footer>'''
    core.BASE = re.sub(r'<div class="footer">.*?</div>', footer, core.BASE, count=1, flags=re.S)

    # Private admin gate: animated lightning entry while preserving existing POST authentication.
    original_admin = core.app.view_functions.get('private_admin_login')
    if original_admin:
        def admin_gate():
            if core.request.method == 'POST':
                return original_admin()
            body='''<section class="adminGate"><div class="lightning l1"></div><div class="lightning l2"></div><div class="adminSeal">BU<span>Z</span>ENT</div><span class="adminKicker">PRIVATE ADMINISTRATION</span><h1>Control the network.<br>Protect the trust.</h1><p>Secure access for verification, business activity, professional profiles, requirements, contact requests and platform operations.</p><form method="post"><label>Admin Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><button class="btn adminButton">Enter Admin Console</button></form></section>'''
            return core.page('Admin Access',body)
        core.app.view_functions['private_admin_login']=admin_gate

    # Admin pages inherit a darker command-center architecture.
    core.BASE = core.BASE.replace('</style></head>','''<style>
:root{--bzNavy:#071A33;--bzBlue:#0B4F91;--bzElectric:#2A8BE8;--bzGold:#D99A20;--bzGold2:#F1B74A;--bzPanel:#0A223E;--bzLine:#1A3C60}
body{background:#071421;color:#E9F1F8}nav{background:rgba(5,18,34,.96)!important;border-bottom:1px solid #173654!important}.nav{max-width:1240px}.links a{color:#BDD0E2!important}.links a:hover{color:#fff!important}.finalBrand{display:flex!important;align-items:center!important;gap:11px!important;min-width:218px!important}.headerMark{width:50px;height:50px;border-radius:13px;background:linear-gradient(145deg,#0B2849,#07182D);display:grid;place-items:center;border:1px solid #24496D}.headerMark .bzOfficialMark{width:43px;height:43px}.finalWord{font-family:'Manrope';font-size:24px;font-weight:800;letter-spacing:.18em;color:#fff;white-space:nowrap}.finalWord span{color:var(--bzGold)}.wrap{max-width:1240px}.globalHero.finalHero{background:radial-gradient(circle at 50% 73%,rgba(42,139,232,.26),transparent 33%),radial-gradient(circle at 88% 14%,rgba(217,154,32,.13),transparent 25%),linear-gradient(135deg,#041325 0%,#072846 48%,#0A3A67 100%)!important;border:1px solid #173E64;border-radius:32px;box-shadow:0 35px 90px rgba(0,0,0,.28)}.networkDust{opacity:.28}.heroCopy{max-width:880px}.globalHero h1{font-size:58px!important;line-height:1.03}.globalHero h1 span{color:var(--bzGold2)!important}.globalHero p{color:#D2E1EF!important}.heroBusiness{background:#fff!important;color:#072846!important}.heroTalent{background:linear-gradient(135deg,#B9770B,#E6A92D)!important}.finalStage .sideNode{background:linear-gradient(145deg,rgba(11,40,73,.92),rgba(6,26,49,.92));border:1px solid #214B73;box-shadow:0 16px 44px rgba(0,0,0,.18)}.nodeBadge{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;font-family:'Manrope';font-weight:800;font-size:19px}.businessBadge{background:#0D3D70;color:#70B9FF;border:1px solid #275F92}.talentBadge{background:#4A3510;color:#F1B74A;border:1px solid #76551A}.finalHub{background:radial-gradient(circle,#103E6F,#04172C 72%)!important;border-color:var(--bzGold2)!important}.finalHub .bzOfficialMark{width:92px;height:92px}.hubOfficial{display:flex;flex-direction:column;align-items:center}.hubOfficial strong{font-family:'Manrope';font-size:22px;letter-spacing:.18em;color:#fff}.hubOfficial strong span{color:var(--bzGold2)}.purposeStrip{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px}.purposeStrip>div{background:linear-gradient(145deg,#0B2847,#081D35);border:1px solid #183A5B;border-radius:18px;padding:22px}.purposeStrip b{color:var(--bzGold2);margin-right:10px}.purposeStrip span{font-family:'Manrope';font-weight:800;color:#fff}.purposeStrip small{display:block;color:#AFC3D6;margin-top:8px;line-height:1.5}.sectionKicker{color:var(--bzGold2);font-weight:800;font-size:12px;letter-spacing:.12em}.categorySection .head h2{color:#fff}.sectionLead{max-width:900px;color:#ABC0D4;line-height:1.7}.categoryGrid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.categoryCard{background:linear-gradient(160deg,#0B294A,#081D34);border:1px solid #1A3D60;border-radius:19px;padding:22px;min-height:242px;box-shadow:0 16px 42px rgba(0,0,0,.13)}.catTop{display:flex;justify-content:space-between;align-items:center}.catNo{color:#6F8EAA;font-size:12px;font-weight:800}.catIcon{width:46px;height:46px;border-radius:13px;display:grid;place-items:center;font-size:12px;font-weight:800;letter-spacing:.05em}.blue .catIcon{background:#0E3E70;color:#71BAFF}.gold .catIcon{background:#49340E;color:#F0B64A}.categoryCard h3{font-size:20px;margin:18px 0 12px}.categoryCard.blue h3{color:#63B1F7}.categoryCard.gold h3{color:#EDB346}.categoryCard p{color:#AEC2D4;line-height:1.58}.whyBuzent{margin-top:58px;padding:54px;border-radius:27px;background:radial-gradient(circle at 90% 12%,rgba(217,154,32,.13),transparent 28%),linear-gradient(145deg,#0B2A4B,#071A31);border:1px solid #24486A}.whyBuzent>span{font-size:18px!important;color:var(--bzGold2)!important;font-weight:800;letter-spacing:.08em}.whyBuzent h2{font-size:42px!important;max-width:900px;color:#fff}.whyBuzent p{max-width:980px!important;color:#BFD0DF!important;font-size:17px;line-height:1.8}.whyBuzent strong{color:#fff}.trustSignals{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px}.trustSignals div{padding:20px;border-radius:16px;background:#081D35;border:1px solid #1B4062}.trustSignals b{display:block;color:#fff;margin-bottom:7px}.trustSignals span{color:#AFC3D7;line-height:1.5}.blogHero{padding:58px;border-radius:28px;background:linear-gradient(135deg,#0A2D50,#071A32);border:1px solid #1B4369}.blogHero>span{color:var(--bzGold2);font-weight:800;letter-spacing:.1em}.blogHero h1{font-size:46px;max-width:900px}.blogHero p{max-width:760px;color:#B7CADB;font-size:17px;line-height:1.7}.blogGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}.blogGrid article{background:#0A223D;border:1px solid #1B3F61;border-radius:18px;padding:24px}.blogGrid article>span{font-size:11px;color:var(--bzGold2);font-weight:800}.blogGrid h2{font-size:21px;color:#fff}.blogGrid p{color:#AFC4D6;line-height:1.65}.finalFooter{display:flex;justify-content:space-between;align-items:center;gap:24px;text-align:left;background:#04101F;color:#C7D6E5;border-top:1px solid #17334F;padding:32px max(4%,calc((100% - 1240px)/2))}.finalFooter b{display:block;font-family:'Manrope';font-size:20px;letter-spacing:.16em;color:#fff}.finalFooter b span{color:var(--bzGold2)}.finalFooter small{display:block;color:#7F9CB7;margin-top:6px}.footerContact{display:flex;gap:25px;flex-wrap:wrap}.footerContact a{display:flex;align-items:center;gap:9px;color:var(--bzGold2);font-weight:700}.footerContact svg{width:22px;height:22px;color:var(--bzGold2)}.adminGate{position:relative;overflow:hidden;max-width:720px;margin:45px auto;padding:52px;border-radius:28px;background:radial-gradient(circle at 50% 15%,rgba(42,139,232,.22),transparent 35%),linear-gradient(145deg,#081F39,#040D18);border:1px solid #24486B;box-shadow:0 35px 90px rgba(0,0,0,.4)}.adminSeal{font:800 28px 'Manrope';letter-spacing:.2em}.adminSeal span{color:var(--bzGold2)}.adminKicker{display:block;color:#72BAFA;font-weight:800;font-size:11px;letter-spacing:.16em;margin-top:18px}.adminGate h1{font-size:44px}.adminGate p{color:#AFC4D6;line-height:1.7}.adminGate label{color:#DDEAF5}.adminGate input{background:#061626;border-color:#284A69;color:#fff}.adminButton{width:100%;margin-top:20px;padding:14px;background:linear-gradient(135deg,#0E5DA4,#D99A20)}.lightning{position:absolute;width:2px;height:270px;background:linear-gradient(#65B9FF,#fff,#D99A20);filter:drop-shadow(0 0 8px #65B9FF);opacity:.45;transform:rotate(24deg);animation:flashBolt 2.8s infinite}.l1{right:70px;top:-80px}.l2{left:55px;bottom:-120px;transform:rotate(-20deg);animation-delay:1.1s}@keyframes flashBolt{0%,82%,100%{opacity:.12}84%,88%{opacity:.9}90%{opacity:.2}}.adminnav{background:#071B31;border:1px solid #173A5A;border-radius:14px;padding:10px}.adminnav a{background:#0A2948!important;border-color:#1A4164!important;color:#C9D9E8}.adminnav a:hover{background:#0E3A65!important;color:#fff}.tablewrap,.card,.item{background:#0A223C!important;border-color:#1C4265!important;color:#EAF2F8}.table th{background:#071A30!important;color:#8FB0CD}.table td{border-color:#173B5C!important}.muted{color:#9EB6CB!important}
@media(max-width:1060px){.categoryGrid{grid-template-columns:repeat(2,1fr)}.blogGrid{grid-template-columns:1fr}.trustSignals{grid-template-columns:1fr}.purposeStrip{grid-template-columns:1fr}}
@media(max-width:720px){.finalBrand{min-width:auto!important}.headerMark{width:42px;height:42px}.finalWord{font-size:18px}.globalHero h1{font-size:38px!important}.categoryGrid{grid-template-columns:1fr}.finalFooter{flex-direction:column;align-items:flex-start}.footerContact{flex-direction:column;gap:10px}.whyBuzent{padding:30px}.whyBuzent h2{font-size:32px!important}.adminGate{padding:30px}.adminGate h1{font-size:34px}}
</style></head>''')
