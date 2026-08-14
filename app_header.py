import os, json, time, secrets, smtplib
from email.message import EmailMessage
import sqlite3
import app as core
from production_db import install

# Production database adapter (PostgreSQL when DATABASE_URL is configured).
initialize_database = install(core)

@core.app.before_request
def ensure_database():
    initialize_database()

# ---------- BUZENT BRAND ----------
original_page = core.page

def branded_page(title, body):
    body = body.replace('DIGIBIZ','BUZENT').replace('Digibiz','BUZENT').replace('Climbzy','BUZENT').replace('CLIMBZY','BUZENT')
    html = original_page(title, body)
    return html.replace('DIGIBIZ','BUZENT').replace('Digibiz','BUZENT').replace('Climbzy','BUZENT').replace('CLIMBZY','BUZENT')

core.page = branded_page

# Clean, aligned header logo and only TWO public login choices.
old_logo = '''<a class="logo" href="/">DIGIBIZ<span class="dot">.</span></a>'''
new_logo = '''<a class="buzent-brand" href="/" aria-label="BUZENT Home"><span class="brand-mark"><b>B</b><i></i><em>●</em><strong>●</strong></span><span class="brand-name">BU<span>Z</span>ENT</span></a>'''
core.BASE = core.BASE.replace(old_logo,new_logo).replace('Why DIGIBIZ','Why BUZENT')

old_actions = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''
new_actions = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a class="btn ghost" href="/login?type=business">Business Login</a><a class="btn dark" href="/login?type=professional">Professional / Agency Login</a>{% endif %}</div>'''
core.BASE = core.BASE.replace(old_actions,new_actions)
core.BASE = core.BASE.replace('DIGIBIZ • Verified Experts. Smarter Business Growth.','BUZENT • Global Business × Professional Talent Network &nbsp; | &nbsp; buzentofficial@gmail.com &nbsp; | &nbsp; @buzentofficial')

core.BASE = core.BASE.replace('</style></head>','''<style>
:root{--bznavy:#071a34;--bzblue:#0b4b91;--bzgold:#d99a20;--bzsoft:#edf4fb}
.nav{height:84px;gap:28px}.buzent-brand{display:flex;align-items:center;gap:12px;min-width:190px}.brand-mark{width:46px;height:46px;position:relative;display:block}.brand-mark b{position:absolute;inset:0;color:var(--bznavy);font:800 46px/46px 'Manrope';letter-spacing:-5px}.brand-mark i{position:absolute;width:31px;height:11px;background:var(--bzgold);transform:rotate(-52deg);left:3px;top:19px;border-radius:10px 2px 2px 10px}.brand-mark em,.brand-mark strong{position:absolute;bottom:4px;font-style:normal;font-size:9px}.brand-mark em{left:18px;color:var(--bznavy)}.brand-mark strong{left:29px;color:var(--bzgold)}.brand-name{font:800 23px/1 'Manrope';letter-spacing:.17em;color:var(--bznavy)}.brand-name span{color:var(--bzgold)}.links{gap:31px;margin-left:auto;margin-right:auto}.links a{font-size:14px;white-space:nowrap}.actions{gap:9px}.footer{line-height:1.8}
.corp-hero{position:relative;overflow:hidden;background:linear-gradient(120deg,#061a35 0%,#0b427b 48%,#17365c 100%);border-radius:30px;padding:62px 52px;color:white;box-shadow:0 30px 80px rgba(7,26,52,.18)}.corp-hero:after{content:'';position:absolute;width:440px;height:440px;border-radius:50%;right:-120px;top:-180px;background:radial-gradient(circle,rgba(217,154,32,.22),transparent 68%)}.corp-kicker{display:inline-flex;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.08);border-radius:999px;padding:8px 13px;font-size:12px;font-weight:700;letter-spacing:.04em}.corp-hero h1{font-size:55px;line-height:1.05;max-width:850px;margin:18px 0}.corp-hero>p{max-width:840px;color:#dce9f6;font-size:18px;line-height:1.65}.connection-grid{display:grid;grid-template-columns:1fr 170px 1fr;align-items:center;gap:18px;margin-top:38px}.side-panel{border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.075);border-radius:22px;padding:25px;min-height:190px}.side-panel h3{font-size:21px;margin:0 0 10px}.side-panel p{color:#d8e5f3;line-height:1.55}.hub{width:154px;height:154px;border-radius:50%;margin:auto;display:grid;place-items:center;text-align:center;background:radial-gradient(circle at 50% 38%,#174c87,#071a34 70%);border:2px solid #e2aa39;box-shadow:0 0 0 8px rgba(217,154,32,.08),0 0 42px rgba(217,154,32,.28);position:relative}.hub:before,.hub:after{content:'';position:absolute;top:50%;width:45px;height:2px;background:linear-gradient(90deg,transparent,#e2aa39)}.hub:before{right:100%}.hub:after{left:100%;transform:rotate(180deg)}.hub b{font:800 18px 'Manrope';letter-spacing:.18em}.hub small{display:block;color:#e9b64d;font-size:10px;margin-top:5px}.platform-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}.platform-strip div{background:#fff;border:1px solid var(--line);border-radius:17px;padding:18px}.platform-strip b{display:block;margin-bottom:5px}.account-shell{max-width:860px;margin:20px auto;background:#fff;border:1px solid var(--line);border-radius:22px;padding:28px;box-shadow:var(--shadow)}.phone-row{display:grid;grid-template-columns:180px 1fr;gap:10px}.verify-card{max-width:520px;margin:35px auto}.secure-note{font-size:12px;color:var(--muted);margin-top:8px}.admin-entry{font-size:12px;color:#98a2b3;text-align:center;margin-top:22px}
@media(max-width:1000px){.links{gap:16px}.connection-grid{grid-template-columns:1fr}.hub:before,.hub:after{display:none}.corp-hero h1{font-size:45px}}
@media(max-width:760px){.nav{height:auto;padding:10px 0;flex-wrap:wrap}.buzent-brand{min-width:auto}.brand-name{font-size:19px}.brand-mark{width:40px;height:40px}.brand-mark b{font-size:40px;line-height:40px}.links{order:3;width:100%;display:flex;overflow-x:auto;margin:0;padding:5px 0 7px}.actions{width:100%;overflow-x:auto}.actions .btn{white-space:nowrap}.corp-hero{padding:35px 24px}.corp-hero h1{font-size:37px}.platform-strip{grid-template-columns:1fr}.phone-row{grid-template-columns:1fr}}
</style></head>''')

# ---------- CORPORATE HOME ----------
def home_new():
    roles=''.join('<div class="card role"><h3>%s</h3><p class="muted">%s</p></div>'%(c,' • '.join(rs[:5])+(' • more' if len(rs)>5 else '')) for c,rs in core.ROLES.items())
    body='''<section class="corp-hero"><span class="corp-kicker">GLOBAL BUSINESS × PROFESSIONAL TALENT NETWORK</span><h1>Where businesses and the right people find each other.</h1><p>BUZENT is building a worldwide professional ecosystem where business owners discover the people who can move their business forward, while marketers, agencies, creators, influencers, promoters, CAs, developers, consultants and other specialists discover relevant opportunities. One platform designed for trusted connections and mutual growth.</p><div class="connection-grid"><div class="side-panel"><h3>For Business Owners</h3><p>Define what your business needs. Discover relevant professionals and agencies based on role, capability and proof.</p><a class="btn light" href="/register/business">Create Business Account</a></div><div class="hub"><div><b>BU<span style="color:#d99a20">Z</span>ENT</b><small>CONNECT • MATCH • GROW</small></div></div><div class="side-panel"><h3>For Professionals & Agencies</h3><p>Build a credible profile, demonstrate your capability and connect with businesses looking for your expertise.</p><a class="btn light" href="/register/pro">Create Professional Account</a></div></div></section><section class="platform-strip" id="how"><div><b>01 — Define</b><span class="muted">Businesses specify the exact expertise they need.</span></div><div><b>02 — Verify</b><span class="muted">Professionals build credibility through role-specific evidence.</span></div><div><b>03 — Connect</b><span class="muted">BUZENT brings relevant opportunities and expertise together.</span></div></section><section class="section" id="roles"><div class="head"><div><h2>The people behind every growing business</h2><p class="muted">Marketing, creative, technology, finance, sales, influence, consulting and agency expertise — in one professional network.</p></div></div><div class="grid">'''+roles+'''</div></section><section class="section" id="trust"><div class="card"><h2>Why BUZENT</h2><p class="muted">The future of professional business collaboration is not endless searching. It is finding the right opportunity, the right expertise and the right fit. BUZENT is being built for businesses and professionals worldwide to create stronger partnerships and grow mutually.</p></div></section>'''
    return core.page('Home',body)
core.app.view_functions['home']=home_new

# ---------- OTP / ACCOUNT HELPERS ----------
COUNTRIES=[('India','+91'),('United States','+1'),('United Kingdom','+44'),('UAE','+971'),('Saudi Arabia','+966'),('Singapore','+65'),('Australia','+61'),('Canada','+1'),('Germany','+49'),('France','+33'),('Netherlands','+31'),('Ireland','+353'),('New Zealand','+64'),('South Africa','+27'),('Malaysia','+60'),('Indonesia','+62'),('Philippines','+63'),('Japan','+81'),('South Korea','+82'),('Qatar','+974'),('Kuwait','+965'),('Oman','+968'),('Bahrain','+973'),('Sri Lanka','+94'),('Nepal','+977'),('Bangladesh','+880')]
COUNTRY_LIST=''.join(f'<option value="{code} — {name}"></option>' for name,code in COUNTRIES)

def normalize_code(raw): return raw.split('—')[0].strip().replace(' ','')
def full_phone(code,number): return normalize_code(code)+''.join(ch for ch in number if ch.isdigit())

def send_otp(email,otp):
    user=os.getenv('SMTP_USER','buzentofficial@gmail.com'); password=os.getenv('SMTP_PASSWORD',''); host=os.getenv('SMTP_HOST','smtp.gmail.com'); port=int(os.getenv('SMTP_PORT','587'))
    if not password: return False
    msg=EmailMessage(); msg['Subject']='Your BUZENT verification code'; msg['From']=user; msg['To']=email
    msg.set_content(f'Your BUZENT verification code is {otp}. It expires in 10 minutes. Do not share this code with anyone.')
    with smtplib.SMTP(host,port,timeout=15) as s:
        s.starttls(); s.login(user,password); s.send_message(msg)
    return True

def begin_pending(payload):
    db=core.con(); token=secrets.token_urlsafe(24); otp=f'{secrets.randbelow(1000000):06d}'
    db.execute('INSERT INTO pending_registrations(token,payload,otp_hash,expires_at) VALUES(?,?,?,?)',(token,json.dumps(payload),core.generate_password_hash(otp),int(time.time())+600)); db.commit()
    if not send_otp(payload['email'],otp):
        db.execute('DELETE FROM pending_registrations WHERE token=?',(token,)); db.commit(); return None
    return token

# ---------- REGISTRATION ----------
def common_fields():
    return f'''<div class="two"><div><label>Full Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div><label>Primary Mobile Number</label><div class="phone-row"><div><input name="country_code" list="countryCodes" placeholder="Search country / + code" value="+91 — India" required><datalist id="countryCodes">{COUNTRY_LIST}</datalist></div><input name="phone" inputmode="numeric" placeholder="Mobile number" required></div><label>Alternate Mobile Number <span class="muted">(optional)</span></label><div class="phone-row"><input name="alt_country_code" list="countryCodes" placeholder="Country code"><input name="alternate_phone" inputmode="numeric" placeholder="Alternate number"></div><div class="two"><div><label>Create Password</label><input type="password" name="password" minlength="8" required></div><div><label>Confirm Password</label><input type="password" name="confirm_password" minlength="8" required></div></div><p class="secure-note">Your email will be verified with a one-time password before the account is activated.</p>'''

def reg_business_new():
    core.init()
    if core.request.method=='POST':
        f=core.request.form
        if f['password']!=f['confirm_password']: core.flash('Passwords do not match.'); return core.redirect('/register/business')
        phone=full_phone(f['country_code'],f['phone']); email=f['email'].strip().lower()
        if core.con().execute('SELECT id FROM users WHERE email=? OR phone=?',(email,phone)).fetchone(): core.flash('Email or mobile number is already registered.'); return core.redirect('/register/business')
        alt=full_phone(f.get('alt_country_code',''),f.get('alternate_phone','')) if f.get('alternate_phone') else ''
        payload={'type':'business','name':f['name'],'email':email,'country_code':normalize_code(f['country_code']),'phone':phone,'alternate_phone':alt,'password':core.generate_password_hash(f['password']),'business':f['business'],'industry':f.get('industry',''),'city':f.get('city',''),'website':f.get('website','')}
        token=begin_pending(payload)
        if token: return core.redirect('/verify-email/'+token)
        core.flash('Email OTP service is not configured yet. Add SMTP_PASSWORD in Vercel Environment Variables.'); return core.redirect('/register/business')
    return core.page('Business Registration',f'''<div class="account-shell"><h1>Create a Business Account</h1><p class="muted">Join BUZENT to find the right professionals for your business.</p><form method="post">{common_fields()}<div class="two"><div><label>Business Name</label><input name="business" required></div><div><label>Industry</label><input name="industry"></div><div><label>City / Region</label><input name="city"></div><div><label>Website / Instagram</label><input name="website"></div></div><br><button class="btn dark">Verify Email & Continue</button></form></div>''')
core.app.view_functions['reg_business']=reg_business_new

def reg_pro_new():
    core.init()
    if core.request.method=='POST':
        f=core.request.form
        if f['password']!=f['confirm_password']: core.flash('Passwords do not match.'); return core.redirect('/register/pro')
        phone=full_phone(f['country_code'],f['phone']); email=f['email'].strip().lower()
        if core.con().execute('SELECT id FROM users WHERE email=? OR phone=?',(email,phone)).fetchone(): core.flash('Email or mobile number is already registered.'); return core.redirect('/register/pro')
        cat,pr=f['combined'].split('|',1); alt=full_phone(f.get('alt_country_code',''),f.get('alternate_phone','')) if f.get('alternate_phone') else ''
        payload={'type':'professional','name':f['name'],'email':email,'country_code':normalize_code(f['country_code']),'phone':phone,'alternate_phone':alt,'password':core.generate_password_hash(f['password']),'account_type':f['account_type'],'category':cat,'primary_role':pr,'experience':f.get('experience',''),'city':f.get('city',''),'industries':f.get('industries',''),'portfolio':f.get('portfolio',''),'pricing':f.get('pricing',''),'bio':f.get('bio','')}
        token=begin_pending(payload)
        if token: return core.redirect('/verify-email/'+token)
        core.flash('Email OTP service is not configured yet. Add SMTP_PASSWORD in Vercel Environment Variables.'); return core.redirect('/register/pro')
    return core.page('Professional Registration',f'''<div class="account-shell"><h1>Create a Professional / Agency Account</h1><p class="muted">Build credibility and connect with relevant business opportunities.</p><form method="post">{common_fields()}<div class="two"><div><label>Account Type</label><select name="account_type"><option>Freelancer / Professional</option><option>Creator / Influencer</option><option>Promoter</option><option>CA / Business Professional</option><option>Agency</option></select></div><div><label>Primary Role</label><select name="combined">{core.opts()}</select></div><div><label>Experience</label><input name="experience"></div><div><label>City / Service Area</label><input name="city"></div><div><label>Industries</label><input name="industries"></div><div><label>Pricing / Engagement</label><input name="pricing"></div></div><label>Portfolio / Social URL</label><input name="portfolio"><label>About Your Expertise</label><textarea name="bio"></textarea><br><button class="btn dark">Verify Email & Continue</button></form></div>''')
core.app.view_functions['reg_pro']=reg_pro_new

@core.app.route('/verify-email/<token>',methods=['GET','POST'])
def verify_email(token):
    core.init(); db=core.con(); row=db.execute('SELECT * FROM pending_registrations WHERE token=?',(token,)).fetchone()
    if not row: return core.page('Verification','<div class="verify-card card"><h2>Verification link expired</h2><p class="muted">Please start registration again.</p></div>')
    if int(row['expires_at'])<int(time.time()): db.execute('DELETE FROM pending_registrations WHERE token=?',(token,)); db.commit(); return core.page('Verification','<div class="verify-card card"><h2>OTP expired</h2><p class="muted">Please start registration again.</p></div>')
    if core.request.method=='POST':
        if not core.check_password_hash(row['otp_hash'],core.request.form['otp'].strip()): core.flash('Incorrect OTP.'); return core.redirect('/verify-email/'+token)
        p=json.loads(row['payload'])
        try:
            role='business' if p['type']=='business' else ('agency' if p.get('account_type')=='Agency' else 'professional')
            c=db.execute('INSERT INTO users(name,email,password,role,phone,alternate_phone,country_code,email_verified) VALUES(?,?,?,?,?,?,?,?)',(p['name'],p['email'],p['password'],role,p['phone'],p.get('alternate_phone',''),p['country_code'],True))
            if p['type']=='business': db.execute('INSERT INTO businesses(user_id,business_name,industry,city,website) VALUES(?,?,?,?,?)',(c.lastrowid,p['business'],p['industry'],p['city'],p['website']))
            else: db.execute('INSERT INTO pros(user_id,account_type,category,primary_role,experience,city,industries,portfolio,pricing,bio) VALUES(?,?,?,?,?,?,?,?,?,?)',(c.lastrowid,p['account_type'],p['category'],p['primary_role'],p['experience'],p['city'],p['industries'],p['portfolio'],p['pricing'],p['bio']))
            db.execute('DELETE FROM pending_registrations WHERE token=?',(token,)); db.commit(); core.flash('Email verified. Your BUZENT account is ready.'); return core.redirect('/login?type='+('business' if role=='business' else 'professional'))
        except sqlite3.IntegrityError: db.rollback(); core.flash('Email or mobile number is already registered.'); return core.redirect('/')
    p=json.loads(row['payload']); return core.page('Verify Email',f'''<div class="verify-card card"><h2>Verify your email</h2><p class="muted">We sent a 6-digit OTP to <b>{p['email']}</b>.</p><form method="post"><label>Verification Code</label><input name="otp" inputmode="numeric" maxlength="6" placeholder="000000" required><br><button class="btn dark">Verify & Create Account</button></form><p class="secure-note">The code expires in 10 minutes.</p></div>''')

# ---------- MOBILE LOGIN ----------
def login_new():
    core.init(); account_type=core.request.args.get('type','business')
    if core.request.method=='POST':
        phone=full_phone(core.request.form['country_code'],core.request.form['phone']); u=core.con().execute('SELECT * FROM users WHERE phone=?',(phone,)).fetchone()
        allowed=('business',) if account_type=='business' else ('professional','agency')
        if u and u['role'] in allowed and core.check_password_hash(u['password'],core.request.form['password']): core.session.clear(); core.session.update(uid=u['id'],role=u['role'],name=u['name']); return core.redirect('/dashboard')
        core.flash('Invalid mobile number or password.')
    title='Business Owner Login' if account_type=='business' else 'Professional / Agency Login'
    signup='/register/business' if account_type=='business' else '/register/pro'
    return core.page('Login',f'''<div class="account-shell"><h1>{title}</h1><p class="muted">Sign in using your registered mobile number.</p><form method="post"><label>Mobile Number</label><div class="phone-row"><input name="country_code" list="loginCountries" value="+91 — India" required><datalist id="loginCountries">{COUNTRY_LIST}</datalist><input name="phone" inputmode="numeric" required></div><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Login to BUZENT</button></form><p class="muted">New to BUZENT? <a href="{signup}" style="color:#2563eb;font-weight:700">Create an account</a></p></div>''')
core.app.view_functions['login']=login_new

# Admin is deliberately NOT shown to public users.
@core.app.route('/admin-access',methods=['GET','POST'])
def admin_access():
    core.init()
    if core.request.method=='POST':
        u=core.con().execute("SELECT * FROM users WHERE email=? AND role='admin'",(core.request.form['email'].lower(),)).fetchone()
        if u and core.check_password_hash(u['password'],core.request.form['password']): core.session.clear(); core.session.update(uid=u['id'],role='admin',name=u['name']); return core.redirect('/admin')
        core.flash('Invalid admin credentials.')
    return core.page('Admin Access','''<div class="verify-card card"><h2>BUZENT Administration</h2><p class="muted">Private administrator access.</p><form method="post"><label>Admin Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Admin Login</button></form></div>''')

app=core.app
