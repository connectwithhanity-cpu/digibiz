import os
import random
import smtplib
from email.mime.text import MIMEText

import app as core
from werkzeug.security import generate_password_hash, check_password_hash

try:
    import production_db
    production_db.install(core)
except Exception:
    pass

BRAND = 'BUZENT'
ADMIN_PATH = '/admin-access'

COUNTRIES = [
    ('+91','India'),('+1','United States / Canada'),('+44','United Kingdom'),('+971','United Arab Emirates'),
    ('+61','Australia'),('+65','Singapore'),('+49','Germany'),('+33','France'),('+39','Italy'),('+34','Spain'),
    ('+31','Netherlands'),('+353','Ireland'),('+64','New Zealand'),('+966','Saudi Arabia'),('+974','Qatar'),
    ('+965','Kuwait'),('+968','Oman'),('+973','Bahrain'),('+60','Malaysia'),('+62','Indonesia'),('+63','Philippines'),
    ('+66','Thailand'),('+84','Vietnam'),('+81','Japan'),('+82','South Korea'),('+86','China'),('+852','Hong Kong'),
    ('+880','Bangladesh'),('+92','Pakistan'),('+94','Sri Lanka'),('+977','Nepal'),('+27','South Africa'),
    ('+234','Nigeria'),('+254','Kenya'),('+20','Egypt'),('+55','Brazil'),('+52','Mexico'),('+54','Argentina'),
    ('+56','Chile'),('+57','Colombia'),('+7','Russia / Kazakhstan'),('+90','Turkey'),('+972','Israel'),
    ('+48','Poland'),('+46','Sweden'),('+47','Norway'),('+45','Denmark'),('+358','Finland'),('+41','Switzerland'),
    ('+43','Austria'),('+32','Belgium'),('+351','Portugal'),('+30','Greece'),('+40','Romania'),('+420','Czech Republic')
]


def country_datalist():
    return '<datalist id="countryCodes">' + ''.join(
        f'<option value="{code} — {name}">{code} {name}</option>' for code,name in COUNTRIES
    ) + '</datalist>'


def normalize_code(value):
    value = (value or '').strip()
    if '—' in value:
        value = value.split('—',1)[0].strip()
    if ' ' in value:
        value = value.split(' ',1)[0].strip()
    if value and not value.startswith('+'):
        value = '+' + value
    return value


def digits(value):
    return ''.join(ch for ch in (value or '') if ch.isdigit())


def send_otp(email, otp):
    smtp_user = os.getenv('SMTP_USER','').strip()
    smtp_password = os.getenv('SMTP_PASSWORD','').strip()
    if not smtp_user or not smtp_password:
        # Development fallback only; production must configure SMTP variables.
        core.session['dev_otp'] = otp
        return False
    msg = MIMEText(f'''Your BUZENT verification code is {otp}.\n\nThis code is valid for this registration session. Do not share it with anyone.\n\nBUZENT\nConnecting businesses with the right professional opportunities worldwide.''')
    msg['Subject'] = 'BUZENT Email Verification Code'
    msg['From'] = smtp_user
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com',465,timeout=15) as server:
        server.login(smtp_user,smtp_password)
        server.send_message(msg)
    return True


# Keep all legacy branding out of rendered pages.
original_page = core.page
def branded_page(title, body):
    body = body.replace('DIGIBIZ','BUZENT').replace('Digibiz','BUZENT').replace('Climbzy','BUZENT').replace('CLIMBZY','BUZENT')
    html = original_page(title, body)
    html = html.replace('DIGIBIZ','BUZENT').replace('Digibiz','BUZENT').replace('Climbzy','BUZENT').replace('CLIMBZY','BUZENT')
    return html
core.page = branded_page


# Exact brand language and a cleaner header lockup matching the approved B / gold connection concept.
old_logo = '''<a class="logo" href="/">DIGIBIZ<span class="dot">.</span></a>'''
new_logo = '''<a class="logo buzent-logo" href="/" aria-label="BUZENT Home">
<span class="bz-symbol" aria-hidden="true"><span class="bz-b">B</span><span class="bz-rise"></span><span class="bz-person bz-person-a"></span><span class="bz-person bz-person-b"></span></span>
<span class="bz-name">BU<span>Z</span>ENT</span>
</a>'''
core.BASE = core.BASE.replace(old_logo,new_logo)
core.BASE = core.BASE.replace('Why DIGIBIZ','Why BUZENT')
core.BASE = core.BASE.replace('<title>{{title}} | DIGIBIZ</title>','<title>{{title}} | BUZENT</title>')
core.BASE = core.BASE.replace('DIGIBIZ • Verified Experts. Smarter Business Growth.','BUZENT • Connecting businesses and professional talent worldwide. &nbsp; | &nbsp; buzentofficial@gmail.com &nbsp; | &nbsp; @buzentofficial')

# Public visitors see exactly two clearly labelled login choices. Admin remains private.
old_actions = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''
new_actions = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<div class="loginChoice"><small>FOR BUSINESSES</small><a class="btn login-business" href="/login?type=business">Business Login</a></div><div class="loginChoice"><small>FOR TALENT & AGENCIES</small><a class="btn login-talent" href="/login?type=professional">Professional / Agency Login</a></div>{% endif %}</div>'''
core.BASE = core.BASE.replace(old_actions,new_actions)

# If a previous patch already injected public Admin Login, hide it globally.
core.BASE = core.BASE.replace('<a class="btn dark" href="/login?admin=1">Admin Login</a>','')


def role_cards():
    icons=['↗','✦','◇','◎','◌','✓','◆']
    return ''.join(
        '<div class="card role"><div class="icon">%s</div><h3>%s</h3><p class="muted">%s</p></div>' %
        (icons[i % len(icons)], category, ' • '.join(roles[:5]) + (' • more' if len(roles)>5 else ''))
        for i,(category,roles) in enumerate(core.ROLES.items())
    )


def home():
    body = '''
<section class="globalHero">
  <div class="networkDust"></div>
  <div class="heroCopy">
    <span class="eyebrow">GLOBAL BUSINESS × PROFESSIONAL TALENT NETWORK</span>
    <h1>The right business.<br>The right talent.<br><span>One global connection.</span></h1>
    <p>BUZENT brings business owners and the professionals who move businesses forward into one trusted platform — helping both sides discover relevant opportunities, build stronger partnerships and grow together worldwide.</p>
    <div class="heroActions"><a class="btn heroBusiness" href="/register/business">Join as a Business</a><a class="btn heroTalent" href="/register/pro">Join as Professional / Agency</a></div>
  </div>
  <div class="connectionStage" aria-label="BUZENT connects businesses and professional talent">
    <div class="sideNode businessNode"><div class="nodeIcon">▦</div><b>BUSINESS OWNERS</b><span>Find the right expertise for every stage of growth.</span></div>
    <div class="hubLines leftLines"></div>
    <div class="globalHub"><div class="hubLogo"><span class="miniB">B</span><strong>BU<span>Z</span>ENT</strong></div><small>GLOBAL CONNECTION PLATFORM</small></div>
    <div class="hubLines rightLines"></div>
    <div class="sideNode talentNode"><div class="nodeIcon">◎</div><b>PROFESSIONAL TALENT</b><span>Find relevant businesses, projects and opportunities.</span></div>
  </div>
  <div class="worldLine"><span>BUSINESS</span><i></i><b>BUZENT</b><i></i><span>OPPORTUNITY</span></div>
</section>
<section class="valueStrip" id="how"><div><b>01</b><span>Discover</span><small>Search expertise by actual business need.</small></div><div><b>02</b><span>Connect</span><small>Bring the right business and professional together.</small></div><div><b>03</b><span>Grow</span><small>Create value and measurable mutual growth.</small></div></section>
<section class="section" id="roles"><div class="head"><div><h2>The people behind every growing business</h2><p class="muted">From marketing and creative to technology, finance, promotion, sales and specialist business services.</p></div></div><div class="grid">''' + role_cards() + '''</div></section>
<section class="whyBuzent" id="trust"><span>WHY BUZENT</span><h2>Opportunity should not depend on geography.</h2><p>BUZENT is being built as a worldwide professional ecosystem where businesses can identify the right capability and professionals can be discovered for the value they can create.</p></section>'''
    return core.page('Home',body)
core.app.view_functions['home'] = home


# Shared registration UI.
def auth_fields():
    return '''
<div class="formGrid">
  <div><label>Email Address <em>*</em></label><input type="email" name="email" placeholder="name@company.com" required></div>
  <div><label>Country Code <em>*</em></label><input class="codeInput" list="countryCodes" name="country_code" placeholder="Search: +91 India" autocomplete="off" required>''' + country_datalist() + '''</div>
  <div><label>Primary Mobile Number <em>*</em></label><input name="mobile" inputmode="numeric" placeholder="Primary mobile number" minlength="6" maxlength="15" required></div>
  <div><label>Alternate Mobile Number</label><input name="alternate_mobile" inputmode="numeric" placeholder="Optional alternate number" maxlength="15"></div>
  <div><label>Create Password <em>*</em></label><input type="password" name="password" minlength="8" placeholder="Minimum 8 characters" required></div>
  <div><label>Confirm Password <em>*</em></label><input type="password" name="confirm_password" minlength="8" placeholder="Re-enter password" required></div>
</div>'''


def start_pending(kind, f, extras):
    code=normalize_code(f.get('country_code'))
    mobile=digits(f.get('mobile'))
    alt=digits(f.get('alternate_mobile'))
    email=(f.get('email') or '').strip().lower()
    password=f.get('password') or ''
    if not code or not mobile or not email:
        core.flash('Email, country code and primary mobile number are required.'); return None
    if password != (f.get('confirm_password') or ''):
        core.flash('Passwords do not match.'); return None
    if len(password)<8:
        core.flash('Password must contain at least 8 characters.'); return None
    core.init(); d=core.con()
    if d.execute('SELECT id FROM users WHERE email=?',(email,)).fetchone():
        core.flash('This email is already registered.'); return None
    if d.execute('SELECT id FROM users WHERE country_code=? AND mobile=?',(code,mobile)).fetchone():
        core.flash('This mobile number is already registered.'); return None
    otp=str(random.randint(100000,999999))
    core.session['pending_signup']={'kind':kind,'name':f.get('name','').strip(),'email':email,'country_code':code,'mobile':mobile,'alternate_mobile':alt,'password_hash':generate_password_hash(password),'extras':extras,'otp':otp}
    try:
        sent=send_otp(email,otp)
        core.flash('A 6-digit verification code has been sent to your email.' if sent else 'OTP created. Configure SMTP_USER and SMTP_PASSWORD in Vercel for live email delivery.')
    except Exception:
        core.flash('We could not send the verification email. Check the SMTP settings in Vercel.')
        return None
    return core.redirect('/verify-email')


def reg_business():
    core.init()
    if core.request.method=='POST':
        f=core.request.form
        extras={'business':f.get('business','').strip(),'industry':f.get('industry','').strip(),'city':f.get('city','').strip(),'website':f.get('website','').strip()}
        return start_pending('business',f,extras) or core.redirect('/register/business')
    return core.page('Business Registration','''<div class="form card authCard"><div class="formIntro"><span>BUSINESS ACCOUNT</span><h1>Join BUZENT as a Business</h1><p>Find the right professionals, agencies and specialists for your business requirements worldwide.</p></div><form method="post"><div class="formGrid"><div><label>Owner Name <em>*</em></label><input name="name" required></div><div><label>Business Name <em>*</em></label><input name="business" required></div><div><label>Industry</label><input name="industry"></div><div><label>City / Country</label><input name="city"></div></div><label>Website / Social Profile</label><input name="website">'''+auth_fields()+'''<button class="btn submitAuth">Continue & Verify Email</button></form></div>''')
core.app.view_functions['reg_business']=reg_business


def reg_pro():
    core.init()
    if core.request.method=='POST':
        f=core.request.form
        combined=f.get('combined','')
        cat,pr=combined.split('|',1) if '|' in combined else ('','')
        extras={'account_type':f.get('account_type','Professional'),'category':cat,'primary_role':pr,'experience':f.get('experience',''),'city':f.get('city',''),'industries':f.get('industries',''),'portfolio':f.get('portfolio',''),'pricing':f.get('pricing',''),'bio':f.get('bio','')}
        return start_pending('professional',f,extras) or core.redirect('/register/pro')
    return core.page('Professional Registration','''<div class="form card authCard"><div class="formIntro"><span>PROFESSIONAL / AGENCY ACCOUNT</span><h1>Join BUZENT as Talent</h1><p>Build credibility and connect with relevant businesses and professional opportunities worldwide.</p></div><form method="post"><div class="formGrid"><div><label>Name / Agency <em>*</em></label><input name="name" required></div><div><label>Account Type <em>*</em></label><select name="account_type"><option>Freelancer / Professional</option><option>Creator / Influencer</option><option>Promoter</option><option>CA / Business Professional</option><option>Agency</option></select></div></div><label>Primary Role <em>*</em></label><select name="combined">'''+core.opts()+'''</select><div class="formGrid"><div><label>Experience</label><input name="experience"></div><div><label>City / Service Area</label><input name="city"></div><div><label>Industries</label><input name="industries"></div><div><label>Pricing</label><input name="pricing"></div></div><label>Portfolio / Social URL</label><input name="portfolio"><label>Professional Summary / Evidence</label><textarea name="bio"></textarea>'''+auth_fields()+'''<button class="btn submitAuth">Continue & Verify Email</button></form></div>''')
core.app.view_functions['reg_pro']=reg_pro


@core.app.route('/verify-email',methods=['GET','POST'])
def verify_email():
    pending=core.session.get('pending_signup')
    if not pending:
        return core.redirect('/')
    if core.request.method=='POST':
        entered=digits(core.request.form.get('otp'))
        if entered != pending.get('otp'):
            core.flash('Incorrect verification code. Please try again.')
        else:
            d=core.con(); kind=pending['kind']; role='business' if kind=='business' else ('agency' if pending['extras'].get('account_type')=='Agency' else 'professional')
            try:
                cur=d.execute('INSERT INTO users(name,email,password,role,country_code,mobile,alternate_mobile,email_verified) VALUES(?,?,?,?,?,?,?,?)',(pending['name'],pending['email'],pending['password_hash'],role,pending['country_code'],pending['mobile'],pending.get('alternate_mobile',''),True))
                uid=cur.lastrowid
                if kind=='business':
                    e=pending['extras']; d.execute('INSERT INTO businesses(user_id,business_name,industry,city,website) VALUES(?,?,?,?,?)',(uid,e['business'],e['industry'],e['city'],e['website']))
                else:
                    e=pending['extras']; d.execute('INSERT INTO pros(user_id,account_type,category,primary_role,experience,city,industries,portfolio,pricing,bio) VALUES(?,?,?,?,?,?,?,?,?,?)',(uid,e['account_type'],e['category'],e['primary_role'],e['experience'],e['city'],e['industries'],e['portfolio'],e['pricing'],e['bio']))
                d.commit(); core.session.pop('pending_signup',None); core.flash('Email verified. Your BUZENT account is ready.'); return core.redirect('/login?type='+('business' if kind=='business' else 'professional'))
            except Exception:
                d.rollback(); core.flash('We could not create this account. The email or mobile may already be registered.')
    dev_note=''
    if core.session.get('dev_otp'):
        dev_note='<p class="devOtp">Development OTP: <b>%s</b></p>'%core.session['dev_otp']
    return core.page('Verify Email','''<div class="form card otpCard"><span class="otpIcon">✉</span><h1>Verify your email</h1><p>Enter the 6-digit code sent to <b>%s</b>.</p><form method="post"><input class="otpInput" name="otp" inputmode="numeric" maxlength="6" placeholder="000000" required><button class="btn submitAuth">Verify & Create Account</button></form>%s</div>'''%(pending['email'],dev_note))


# Phone + password login for both public account types; private admin remains email + password.
def login():
    core.init()
    admin_mode=core.request.args.get('admin')=='1' or core.request.path==ADMIN_PATH
    requested=core.request.args.get('type','business')
    if core.request.method=='POST':
        if admin_mode:
            email=(core.request.form.get('email') or '').lower().strip(); u=core.con().execute("SELECT * FROM users WHERE email=? AND role='admin'",(email,)).fetchone()
        else:
            code=normalize_code(core.request.form.get('country_code')); mobile=digits(core.request.form.get('mobile')); u=core.con().execute('SELECT * FROM users WHERE country_code=? AND mobile=?',(code,mobile)).fetchone()
            if u and requested=='business' and u['role']!='business': u=None
            if u and requested=='professional' and u['role'] not in ('professional','agency'): u=None
        if u and check_password_hash(u['password'],core.request.form.get('password','')):
            core.session.clear(); core.session.update(uid=u['id'],role=u['role'],name=u['name']); return core.redirect('/dashboard')
        core.flash('Invalid login details.')
    if admin_mode:
        return core.page('Admin Login','''<div class="form card authCard"><div class="formIntro"><span>PRIVATE ADMIN ACCESS</span><h1>BUZENT Administration</h1></div><form method="post"><label>Admin Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><button class="btn submitAuth">Admin Login</button></form></div>''')
    is_business=requested=='business'; heading='Business Login' if is_business else 'Professional / Agency Login'; sub='Access your business requirements and connections.' if is_business else 'Access your profile, verification and opportunities.'
    return core.page(heading,'''<div class="form card authCard"><div class="formIntro"><span>%s</span><h1>%s</h1><p>%s</p></div><form method="post"><label>Country Code <em>*</em></label><input class="codeInput" list="countryCodes" name="country_code" placeholder="Search country or code, e.g. +91 India" autocomplete="off" required>%s<label>Primary Mobile Number <em>*</em></label><input name="mobile" inputmode="numeric" placeholder="Your registered mobile number" required><label>Password <em>*</em></label><input type="password" name="password" required><button class="btn submitAuth">%s</button></form><p class="registerPrompt">New to BUZENT? <a href="%s">Create your account</a></p></div>'''%('BUSINESS ACCOUNT' if is_business else 'PROFESSIONAL / AGENCY ACCOUNT',heading,sub,country_datalist(),heading,'/register/business' if is_business else '/register/pro'))
core.app.view_functions['login']=login
core.app.add_url_rule(ADMIN_PATH,'private_admin_login',login,methods=['GET','POST'])


# Global corporate network styling.
core.BASE = core.BASE.replace('</style></head>','''<style>
:root{--gold:#d99a20;--gold2:#f1bd52;--deep:#041326;--navy2:#082a50;--electric:#1b70d6}.nav{height:88px;gap:30px;background:transparent}.buzent-logo{display:flex;align-items:center;gap:12px;min-width:205px}.bz-symbol{width:46px;height:50px;display:inline-block;position:relative}.bz-b{position:absolute;inset:-4px 0 0 4px;font-family:'Manrope';font-weight:800;font-size:48px;line-height:1;color:var(--navy);letter-spacing:-6px}.bz-rise{position:absolute;width:33px;height:9px;background:linear-gradient(90deg,#b9790e,var(--gold2));border-radius:20px;left:1px;top:23px;transform:rotate(-51deg);transform-origin:center}.bz-person{position:absolute;width:9px;height:9px;border-radius:50%;bottom:8px}.bz-person:after{content:'';position:absolute;width:14px;height:8px;border-radius:9px 9px 2px 2px;top:10px;left:-3px}.bz-person-a{left:16px;background:var(--navy)}.bz-person-a:after{background:var(--navy)}.bz-person-b{left:30px;background:var(--gold)}.bz-person-b:after{background:var(--gold)}.bz-name{font-family:'Manrope';font-weight:800;font-size:25px;letter-spacing:.16em;color:var(--navy);white-space:nowrap}.bz-name span{color:var(--gold)}.links{gap:31px;margin-left:auto;margin-right:auto}.links a{font-size:14px}.loginChoice{display:flex;flex-direction:column;gap:3px;align-items:stretch}.loginChoice small{font-size:9px;letter-spacing:.08em;font-weight:800;color:#7b8797;padding-left:5px}.loginChoice .btn{font-size:12px;padding:10px 12px}.login-business{background:#eaf2ff;color:#1559b7}.login-talent{background:var(--navy);color:#fff}
.globalHero{position:relative;overflow:hidden;min-height:650px;padding:64px;border-radius:34px;color:#fff;background:radial-gradient(circle at 50% 48%,rgba(38,126,220,.26),transparent 28%),radial-gradient(circle at 85% 18%,rgba(217,154,32,.16),transparent 26%),linear-gradient(135deg,#031326 0%,#082b52 52%,#0c3766 100%);box-shadow:0 30px 90px rgba(4,25,50,.22)}.globalHero:before,.globalHero:after{content:'';position:absolute;border:1px solid rgba(93,167,239,.16);border-radius:50%;width:580px;height:580px;right:-190px;top:-180px;box-shadow:0 0 0 55px rgba(90,164,236,.025),0 0 0 110px rgba(90,164,236,.018)}.globalHero:after{width:430px;height:430px;left:-210px;top:290px}.networkDust{position:absolute;inset:0;opacity:.35;background-image:radial-gradient(circle,rgba(115,190,255,.75) 1px,transparent 1px);background-size:32px 32px;mask-image:linear-gradient(90deg,#000,transparent 45%,#000)}.heroCopy{position:relative;z-index:2;max-width:760px}.globalHero .eyebrow{border-color:rgba(255,255,255,.17);background:rgba(255,255,255,.07);letter-spacing:.06em}.globalHero h1{font-family:'Manrope';font-size:55px;line-height:1.04;letter-spacing:-2.5px;margin:18px 0}.globalHero h1 span{color:#f2b845}.globalHero .heroCopy p{font-size:18px;line-height:1.72;color:#d7e6f7;max-width:720px}.heroActions{display:flex;gap:12px;margin-top:25px}.heroBusiness{background:#fff;color:#08284a}.heroTalent{background:linear-gradient(135deg,#b9790e,#e4a62b);color:#fff}.connectionStage{position:relative;z-index:2;display:grid;grid-template-columns:1fr 110px 210px 110px 1fr;align-items:center;gap:8px;margin-top:50px}.sideNode{border:1px solid rgba(255,255,255,.14);background:rgba(4,20,40,.52);backdrop-filter:blur(10px);border-radius:20px;padding:20px;min-height:145px}.sideNode b{display:block;font-size:14px;letter-spacing:.04em;margin:8px 0}.sideNode span{font-size:13px;color:#bdcde0;line-height:1.5}.nodeIcon{font-size:27px;color:#65b4ff}.talentNode .nodeIcon{color:#f1bd52}.hubLines{height:2px;background:linear-gradient(90deg,rgba(64,151,238,.1),#48a2fa,rgba(255,255,255,.85));position:relative}.hubLines:before,.hubLines:after{content:'';position:absolute;width:7px;height:7px;border-radius:50%;top:-3px;background:#72bdff;box-shadow:0 0 14px #5cb2ff}.hubLines:before{left:25%}.hubLines:after{right:18%}.rightLines{background:linear-gradient(90deg,rgba(255,255,255,.85),#e3a42b,rgba(227,164,43,.1))}.rightLines:before,.rightLines:after{background:#f4c15e;box-shadow:0 0 14px #e9b03e}.globalHub{width:210px;height:210px;border-radius:50%;display:grid;place-items:center;text-align:center;padding:35px;background:radial-gradient(circle,#123e6c,#05162b 68%);border:2px solid rgba(255,194,75,.9);box-shadow:0 0 0 7px rgba(65,155,240,.09),0 0 45px rgba(54,150,241,.34),0 0 55px rgba(226,166,45,.22)}.hubLogo strong{display:block;font-family:'Manrope';font-size:23px;letter-spacing:.18em}.hubLogo strong span{color:var(--gold2)}.miniB{font-family:'Manrope';font-size:50px;font-weight:800;color:#fff;line-height:1}.globalHub small{font-size:9px;color:#a9c0d7;letter-spacing:.1em}.worldLine{position:relative;z-index:2;display:flex;align-items:center;justify-content:center;gap:16px;margin-top:30px;color:#a9c2da;font-size:11px;letter-spacing:.15em}.worldLine i{width:70px;height:1px;background:linear-gradient(90deg,transparent,#77bfff,transparent)}.worldLine b{color:#fff}.valueStrip{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.valueStrip>div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}.valueStrip b{color:var(--blue);margin-right:9px}.valueStrip span{font-family:'Manrope';font-weight:800}.valueStrip small{display:block;color:var(--muted);margin-top:8px}.whyBuzent{margin-top:48px;padding:45px;border-radius:24px;background:linear-gradient(135deg,#f7faff,#fff8eb);border:1px solid #e8edf5}.whyBuzent>span{color:#b4760a;font-weight:800;font-size:12px;letter-spacing:.1em}.whyBuzent h2{font-size:34px;margin:8px 0}.whyBuzent p{max-width:780px;line-height:1.7;color:var(--muted)}
.authCard{max-width:850px;padding:34px}.formIntro{padding-bottom:20px;border-bottom:1px solid var(--line);margin-bottom:22px}.formIntro span{font-size:11px;letter-spacing:.11em;font-weight:800;color:#b4760a}.formIntro h1{margin:7px 0}.formIntro p{color:var(--muted)}.formGrid{display:grid;grid-template-columns:1fr 1fr;gap:0 18px}.authCard em{color:#cf2929;font-style:normal}.codeInput{background:#f8fbff;border-color:#bed4ed}.submitAuth{width:100%;margin-top:22px;padding:14px;background:linear-gradient(135deg,#08284a,#155aa2)}.registerPrompt{text-align:center;color:var(--muted)}.registerPrompt a{color:var(--blue);font-weight:800}.otpCard{text-align:center;max-width:520px;padding:42px}.otpIcon{font-size:44px}.otpInput{text-align:center;font-size:30px;letter-spacing:.35em;font-weight:800;margin:15px 0}.devOtp{background:#fff7dc;padding:10px;border-radius:10px;font-size:12px}
@media(max-width:1100px){.links{gap:17px}.buzent-logo{min-width:180px}.bz-name{font-size:21px}.actions{gap:5px}.loginChoice .btn{font-size:11px;padding:9px 9px}.connectionStage{grid-template-columns:1fr 55px 185px 55px 1fr}.globalHub{width:185px;height:185px}.globalHero{padding:48px}}
@media(max-width:900px){.nav{height:auto;min-height:76px;padding:10px 0;flex-wrap:wrap}.links{order:3;width:100%;justify-content:center;margin:0;padding-bottom:6px;overflow-x:auto}.actions{margin-left:auto}.globalHero h1{font-size:44px}.connectionStage{grid-template-columns:1fr 170px 1fr}.hubLines{display:none}.globalHub{width:170px;height:170px}.buzent-logo{min-width:auto}}
@media(max-width:700px){.bz-symbol{width:38px;height:42px}.bz-b{font-size:40px}.bz-name{font-size:18px}.actions{width:100%;display:grid;grid-template-columns:1fr 1fr}.loginChoice small{text-align:center}.links{justify-content:flex-start}.globalHero{padding:30px 22px;border-radius:24px}.globalHero h1{font-size:38px}.heroActions{flex-direction:column}.connectionStage{grid-template-columns:1fr;gap:12px}.globalHub{order:2;margin:auto}.businessNode{order:1}.talentNode{order:3}.valueStrip{grid-template-columns:1fr}.formGrid{grid-template-columns:1fr}.authCard{padding:22px}.worldLine{gap:8px}.worldLine i{width:25px}}
</style></head>''')

app=core.app
