import os, sqlite3
from functools import wraps
from flask import Flask, request, redirect, session, flash, render_template_string, g
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY','digibiz-dev-change-me')
DB=os.getenv('DB_PATH','/tmp/digibiz.db')

ROLES={
'Digital Marketing':['Digital Marketing Manager','Performance Marketer','Meta Ads Specialist','Google Ads / PPC Specialist','SEO Specialist','Local SEO / GBP Specialist','Social Media Manager','Content Strategist','Email Marketer','WhatsApp Marketer','E-commerce Marketer','Lead Generation Specialist','Marketing Strategist'],
'Creative & Production':['Graphic Designer','Brand Designer','UI/UX Designer','Video Editor','Reels Editor','Motion Graphics Designer','Photographer','Videographer','Content Creator','Copywriter','UGC Creator'],
'Web & Technology':['Website Designer','WordPress Developer','Shopify Developer','Web Developer','Landing Page Specialist','App Developer','AI Automation Expert','Chatbot Developer','No-Code Developer','Pixel / Tracking Specialist'],
'Sales & Promotion':['Sales Executive','Business Development Executive','Appointment Setter','Telecaller','Sales Closer','Field Promoter','Brand Promoter','Event Promoter','Product Promoter','Growth Consultant'],
'Influencers & Creators':['Nano Influencer','Micro Influencer','Macro Influencer','Instagram Creator','YouTube Creator','Regional Influencer','Food Influencer','Fashion Influencer','Tech Influencer','Finance Influencer','Education Influencer','Local / City Influencer'],
'Professional Business Services':['Chartered Accountant (CA)','Accountant','GST Consultant','Tax Consultant','Company Registration Consultant','Financial Consultant','Legal / Compliance Professional'],
'Agencies':['Digital Marketing Agency','Creative Agency','Advertising Agency','Social Media Agency','Influencer Marketing Agency','Web Development Agency','Video Production Agency','Branding Agency','Lead Generation Agency']}

def con():
    if 'db' not in g:
        g.db=sqlite3.connect(DB); g.db.row_factory=sqlite3.Row
    return g.db

@app.teardown_appcontext
def close(_=None):
    d=g.pop('db',None)
    if d:d.close()

def init():
    d=con(); d.executescript('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password TEXT,role TEXT);
    CREATE TABLE IF NOT EXISTS businesses(user_id INTEGER PRIMARY KEY,business_name TEXT,industry TEXT,city TEXT,website TEXT);
    CREATE TABLE IF NOT EXISTS pros(user_id INTEGER PRIMARY KEY,account_type TEXT,category TEXT,primary_role TEXT,experience TEXT,city TEXT,industries TEXT,portfolio TEXT,pricing TEXT,bio TEXT,status TEXT DEFAULT 'Not Verified',score INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS requirements(id INTEGER PRIMARY KEY AUTOINCREMENT,business_id INTEGER,title TEXT,category TEXT,required_role TEXT,goal TEXT,budget TEXT,timeline TEXT,description TEXT,status TEXT DEFAULT 'Open');
    CREATE TABLE IF NOT EXISTS assessments(id INTEGER PRIMARY KEY AUTOINCREMENT,pro_id INTEGER,response TEXT,evidence TEXT,status TEXT DEFAULT 'Pending',score INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,requirement_id INTEGER,business_id INTEGER,pro_id INTEGER,status TEXT DEFAULT 'Requested');''')
    if not d.execute("SELECT id FROM users WHERE email='admin@digibiz.in'").fetchone():
        d.execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',('DIGIBIZ Admin','admin@digibiz.in',generate_password_hash('admin123'),'admin'))
    d.commit()

def auth(*roles):
    def dec(fn):
        @wraps(fn)
        def w(*a,**k):
            if not session.get('uid'):return redirect('/login')
            if roles and session.get('role') not in roles:return redirect('/dashboard')
            return fn(*a,**k)
        return w
    return dec

CSS='''@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
:root{--ink:#0a1020;--navy:#0b1f3a;--blue:#2563eb;--green:#10b981;--red:#dc2626;--bg:#f7f9fc;--muted:#667085;--line:#e6eaf0;--soft:#eef4ff;--shadow:0 18px 50px rgba(15,23,42,.08)}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}a{text-decoration:none;color:inherit}nav{position:sticky;top:0;z-index:20;background:rgba(247,249,252,.94);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}.nav{width:min(1180px,92%);height:72px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px}.logo{font-family:'Manrope';font-size:25px;font-weight:800;letter-spacing:-1px;color:var(--navy)}.dot{color:var(--blue)}.links,.actions{display:flex;gap:18px;align-items:center}.links{color:#475467;font-weight:600}.wrap{width:min(1180px,92%);margin:auto;padding:30px 0 60px}.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;align-items:center;background:linear-gradient(135deg,#07182f,#0b2c59 55%,#174c87);border-radius:32px;padding:68px;color:#fff;box-shadow:0 24px 80px rgba(8,31,66,.18)}.hero h1{font-family:'Manrope';font-size:58px;line-height:1.02;letter-spacing:-2.5px;margin:18px 0}.hero p{font-size:19px;line-height:1.65;color:#d9e7f7}.eyebrow{display:inline-flex;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);font-size:13px;font-weight:700}.heroPanel{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:20px}.stat{display:flex;justify-content:space-between;padding:16px;border-bottom:1px solid rgba(255,255,255,.12)}.stat:last-child{border:0}.stat b{font-family:'Manrope';font-size:23px}.btn{display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:12px;padding:11px 16px;background:var(--blue);color:#fff;font-weight:700;cursor:pointer}.green{background:var(--green)}.light{background:#fff;color:var(--navy)}.dark{background:var(--navy)}.ghost{background:var(--soft);color:var(--blue)}.danger{background:var(--red)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 8px 30px rgba(15,23,42,.035)}.section{margin-top:46px}.head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:18px}.head h2,h1,h2,h3{font-family:'Manrope';letter-spacing:-.5px}.head h2{font-size:32px;margin:0}.muted{color:var(--muted)}.trust{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}.trust>div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}.role{min-height:160px}.icon{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#e9f0ff,#eafcf8);display:grid;place-items:center;margin-bottom:14px}.form{max-width:780px;margin:20px auto}label{display:block;font-weight:700;margin:14px 0 7px;font-size:14px}input,select,textarea{width:100%;padding:13px;border:1px solid #d5dbe5;border-radius:12px;background:#fff;font:inherit}textarea{min-height:105px}.pill{display:inline-flex;padding:7px 10px;border-radius:999px;background:#eaf9f3;color:#067647;font-size:12px;font-weight:700}.score{font-family:'Manrope';font-size:34px;font-weight:800;color:var(--blue)}.item{border:1px solid var(--line);border-radius:15px;padding:15px;margin:10px 0;background:#fff}.flash{background:#eef6ff;border:1px solid #cfe2ff;color:#194d86;padding:12px;border-radius:12px;margin:14px 0}.tablewrap{overflow:auto;background:#fff;border:1px solid var(--line);border-radius:18px}.table{width:100%;border-collapse:collapse;min-width:900px}.table th,.table td{text-align:left;padding:13px 14px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}.table th{background:#f8fafc;color:#475467;font-size:12px;text-transform:uppercase;letter-spacing:.04em}.table tr:last-child td{border-bottom:0}.adminnav{display:flex;gap:9px;flex-wrap:wrap;margin:20px 0}.adminnav a{padding:9px 12px;border-radius:10px;background:#fff;border:1px solid var(--line);font-weight:700;font-size:13px}.adminnav a:hover{background:var(--soft);color:var(--blue)}.footer{text-align:center;border-top:1px solid var(--line);padding:28px;color:#7a8595;font-size:13px}@media(max-width:900px){.hero{grid-template-columns:1fr;padding:42px}.hero h1{font-size:46px}.heroPanel,.links{display:none}.trust{grid-template-columns:1fr}}@media(max-width:720px){.two{grid-template-columns:1fr}.hero{padding:30px}.hero h1{font-size:38px}.head{align-items:flex-start;flex-direction:column}}'''

BASE='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} | DIGIBIZ</title><style>'''+CSS+'''</style></head><body><nav><div class="nav"><a class="logo" href="/">DIGIBIZ<span class="dot">.</span></a><div class="links"><a href="/#roles">Explore Roles</a><a href="/#how">How It Works</a><a href="/#trust">Why DIGIBIZ</a></div><div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div></div></nav><main class="wrap">{% for m in get_flashed_messages() %}<div class="flash">{{m}}</div>{% endfor %}{{body|safe}}</main><div class="footer">DIGIBIZ • Verified Experts. Smarter Business Growth.</div></body></html>'''

def page(t,b):return render_template_string(BASE,title=t,body=b)
def opts():return ''.join('<optgroup label="%s">%s</optgroup>'%(c,''.join('<option value="%s|%s">%s</option>'%(c,r,r) for r in rs)) for c,rs in ROLES.items())

def admin_nav():
    return '''<div class="adminnav"><a href="/admin">Overview</a><a href="/admin/businesses">Business Owners</a><a href="/admin/professionals">Professionals & Agencies</a><a href="/admin/requirements">Requirements</a><a href="/admin/contacts">Contact Requests</a><a href="/admin/assessments">Assessments</a></div>'''

@app.route('/')
def home():
    icons=['◎','✦','⌘','↗','◉','✓','◆'];groups=''.join('<div class="card role"><div class="icon">%s</div><h3>%s</h3><p class="muted">%s</p></div>'%(icons[i%7],c,' • '.join(rs[:5])+(' • more' if len(rs)>5 else '')) for i,(c,rs) in enumerate(ROLES.items()))
    return page('Home','''<section class="hero"><div><span class="eyebrow">✓ Proof-first business growth network</span><h1>Find the right expert. Grow with confidence.</h1><p>DIGIBIZ helps businesses discover verified marketers, creators, developers, promoters, influencers, CAs and agencies — matched by capability, relevance and evidence.</p><a class="btn green" href="/register/business">I’m a Business Owner</a> <a class="btn light" href="/register/pro">I’m a Professional / Agency</a> <a class="btn" href="/login?admin=1">Admin Login</a></div><div class="heroPanel"><div class="stat"><span>Expert categories</span><b>7</b></div><div class="stat"><span>Verification model</span><b>Proof-first</b></div><div class="stat"><span>Matching</span><b>Role-based</b></div></div></section><section class="trust" id="how"><div><b>01 — Prove</b><p class="muted">Role-specific evidence.</p></div><div><b>02 — Verify</b><p class="muted">Admin review and score.</p></div><div><b>03 — Match</b><p class="muted">Relevant experts for business needs.</p></div></section><section class="section" id="roles"><div class="head"><div><h2>Every role your business may need</h2><p class="muted">One network for business growth.</p></div></div><div class="grid">'''+groups+'''</div></section>''')

@app.route('/register/business',methods=['GET','POST'])
def reg_business():
    init()
    if request.method=='POST':
        f=request.form
        try:
            c=con().execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',(f['name'],f['email'].lower(),generate_password_hash(f['password']),'business'));con().execute('INSERT INTO businesses VALUES(?,?,?,?,?)',(c.lastrowid,f['business'],f.get('industry',''),f.get('city',''),f.get('website','')));con().commit();flash('Account created. Login now.');return redirect('/login')
        except sqlite3.IntegrityError:flash('Email already registered.')
    return page('Business Registration','''<div class="form card"><h1>Create your business account</h1><form method="post"><div class="two"><div><label>Owner Name</label><input name="name" required></div><div><label>Business Name</label><input name="business" required></div><div><label>Industry</label><input name="industry"></div><div><label>City</label><input name="city"></div></div><label>Website / Instagram</label><input name="website"><div class="two"><div><label>Email</label><input type="email" name="email" required></div><div><label>Password</label><input type="password" name="password" required></div></div><br><button class="btn green">Create Business Account</button></form></div>''')

@app.route('/register/pro',methods=['GET','POST'])
def reg_pro():
    init()
    if request.method=='POST':
        f=request.form;cat,pr=f['combined'].split('|',1);role='agency' if f['account_type']=='Agency' else 'professional'
        try:
            c=con().execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',(f['name'],f['email'].lower(),generate_password_hash(f['password']),role));con().execute('INSERT INTO pros(user_id,account_type,category,primary_role,experience,city,industries,portfolio,pricing,bio) VALUES(?,?,?,?,?,?,?,?,?,?)',(c.lastrowid,f['account_type'],cat,pr,f.get('experience',''),f.get('city',''),f.get('industries',''),f.get('portfolio',''),f.get('pricing',''),f.get('bio','')));con().commit();flash('Profile created. Login to verify your skill.');return redirect('/login')
        except sqlite3.IntegrityError:flash('Email already registered.')
    return page('Professional Registration','''<div class="form card"><h1>Create your expert profile</h1><form method="post"><div class="two"><div><label>Name / Agency</label><input name="name" required></div><div><label>Account Type</label><select name="account_type"><option>Freelancer / Professional</option><option>Creator / Influencer</option><option>Promoter</option><option>CA / Business Professional</option><option>Agency</option></select></div></div><label>Primary Role</label><select name="combined">'''+opts()+'''</select><div class="two"><div><label>Experience</label><input name="experience"></div><div><label>City / Service Area</label><input name="city"></div><div><label>Industries</label><input name="industries"></div><div><label>Pricing</label><input name="pricing"></div></div><label>Portfolio / Social URL</label><input name="portfolio"><label>About / Evidence</label><textarea name="bio"></textarea><div class="two"><div><label>Email</label><input type="email" name="email" required></div><div><label>Password</label><input type="password" name="password" required></div></div><br><button class="btn green">Create Expert Profile</button></form></div>''')

@app.route('/login',methods=['GET','POST'])
def login():
    init()
    if request.method=='POST':
        u=con().execute('SELECT * FROM users WHERE email=?',(request.form['email'].lower(),)).fetchone()
        if u and check_password_hash(u['password'],request.form['password']):session.clear();session.update(uid=u['id'],role=u['role'],name=u['name']);return redirect('/dashboard')
        flash('Invalid email or password.')
    note='<p class="muted">Prototype admin: admin@digibiz.in / admin123</p>' if request.args.get('admin') else ''
    return page('Login','<div class="form card"><h1>Welcome back</h1><form method="post"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Login</button></form>'+note+'</div>')

@app.route('/logout')
def logout():session.clear();return redirect('/')
@app.route('/dashboard')
@auth()
def dash():return redirect('/admin' if session['role']=='admin' else '/business' if session['role']=='business' else '/professional')

@app.route('/business')
@auth('business')
def business():
    b=con().execute('SELECT * FROM businesses WHERE user_id=?',(session['uid'],)).fetchone();rs=con().execute('SELECT * FROM requirements WHERE business_id=? ORDER BY id DESC',(session['uid'],)).fetchall();rows=''.join('<div class="item"><b>%s</b><p class="muted">%s • %s</p><a class="btn ghost" href="/matches/%s">Find Matches</a></div>'%(r['title'],r['required_role'],r['budget'] or 'Budget not set',r['id']) for r in rs) or '<p class="muted">No requirements yet.</p>'
    return page('Business Dashboard','<div class="head"><div><h2>%s</h2><p class="muted">Business Owner Dashboard</p></div><a class="btn green" href="/requirement">+ Post Requirement</a></div><div class="card"><h3>Your Requirements</h3>%s</div>'%(b['business_name'],rows))

@app.route('/requirement',methods=['GET','POST'])
@auth('business')
def requirement():
    if request.method=='POST':
        f=request.form;cat,rr=f['combined'].split('|',1);c=con().execute('INSERT INTO requirements(business_id,title,category,required_role,goal,budget,timeline,description) VALUES(?,?,?,?,?,?,?,?)',(session['uid'],f['title'],cat,rr,f.get('goal',''),f.get('budget',''),f.get('timeline',''),f.get('description','')));con().commit();return redirect('/matches/%s'%c.lastrowid)
    return page('Post Requirement','<div class="form card"><h1>What does your business need?</h1><form method="post"><label>Requirement</label><input name="title" required><label>Expert Role</label><select name="combined">'+opts()+'</select><div class="two"><div><label>Goal</label><input name="goal"></div><div><label>Budget</label><input name="budget"></div></div><label>Timeline</label><input name="timeline"><label>Description</label><textarea name="description"></textarea><br><button class="btn green">Post & Find Experts</button></form></div>')

@app.route('/matches/<int:rid>')
@auth('business')
def matches(rid):
    r=con().execute('SELECT * FROM requirements WHERE id=? AND business_id=?',(rid,session['uid'])).fetchone()
    if not r:return 'Not found',404
    ps=con().execute('SELECT u.name,p.* FROM pros p JOIN users u ON u.id=p.user_id WHERE p.primary_role=? OR p.category=? ORDER BY p.score DESC',(r['required_role'],r['category'])).fetchall();cards=''.join('<div class="card"><span class="pill">%s</span><h3>%s</h3><p><b>%s</b></p><div class="score">%s/100</div><p class="muted">%s</p><form method="post" action="/contact/%s/%s"><button class="btn green">Request Contact</button></form></div>'%(p['status'],p['name'],p['primary_role'],p['score'],p['pricing'] or 'Pricing on request',rid,p['user_id']) for p in ps) or '<div class="card">No matching experts yet.</div>'
    return page('Matches','<div class="head"><div><h2>Recommended Experts</h2><p class="muted">%s</p></div></div><div class="grid">%s</div>'%(r['required_role'],cards))

@app.post('/contact/<int:rid>/<int:pid>')
@auth('business')
def contact(rid,pid):con().execute('INSERT INTO contacts(requirement_id,business_id,pro_id) VALUES(?,?,?)',(rid,session['uid'],pid));con().commit();flash('Contact request sent.');return redirect('/matches/%s'%rid)

@app.route('/professional')
@auth('professional','agency')
def professional():
    p=con().execute('SELECT * FROM pros WHERE user_id=?',(session['uid'],)).fetchone();ass=con().execute('SELECT * FROM assessments WHERE pro_id=? ORDER BY id DESC',(session['uid'],)).fetchall();hist=''.join('<div class="item"><b>%s</b> • %s/100</div>'%(a['status'],a['score']) for a in ass) or '<p class="muted">No assessment yet.</p>';guide='Submit social metrics, audience geography and collaboration evidence.' if p['category']=='Influencers & Creators' else 'Submit applicable credentials and professional service proof.' if p['category']=='Professional Business Services' else 'Submit location, language and field campaign proof.' if p['category']=='Sales & Promotion' else 'Solve a practical role-specific business problem and provide evidence.'
    return page('Professional Dashboard','<div class="head"><div><h2>%s</h2><p class="muted">%s • %s</p></div></div><div class="grid"><div class="card"><h3>Status</h3><span class="pill">%s</span></div><div class="card"><h3>DIGIBIZ Score</h3><div class="score">%s/100</div></div><div class="card"><h3>Primary Role</h3><p>%s</p></div></div><div class="two section"><div class="card"><h3>Get Verified</h3><p class="muted">%s</p><form method="post" action="/assessment"><label>Practical Response</label><textarea name="response" required></textarea><label>Evidence</label><input name="evidence"><br><button class="btn green">Submit for Review</button></form></div><div class="card"><h3>Assessment History</h3>%s</div></div>'%(session['name'],p['account_type'],p['category'],p['status'],p['score'],p['primary_role'],guide,hist))

@app.post('/assessment')
@auth('professional','agency')
def assessment():con().execute('INSERT INTO assessments(pro_id,response,evidence) VALUES(?,?,?)',(session['uid'],request.form['response'],request.form.get('evidence','')));con().commit();flash('Assessment submitted.');return redirect('/professional')

@app.route('/admin')
@auth('admin')
def admin():
    b=con().execute("SELECT count(*) c FROM users WHERE role='business'").fetchone()['c'];p=con().execute("SELECT count(*) c FROM users WHERE role IN ('professional','agency')").fetchone()['c'];r=con().execute('SELECT count(*) c FROM requirements').fetchone()['c'];a=con().execute("SELECT count(*) c FROM assessments WHERE status='Pending'").fetchone()['c'];c=con().execute('SELECT count(*) c FROM contacts').fetchone()['c']
    recent_b=con().execute('SELECT u.name,u.email,b.* FROM businesses b JOIN users u ON u.id=b.user_id ORDER BY b.user_id DESC LIMIT 5').fetchall();recent_p=con().execute('SELECT u.name,u.email,p.* FROM pros p JOIN users u ON u.id=p.user_id ORDER BY p.user_id DESC LIMIT 5').fetchall()
    rb=''.join('<div class="item"><b>%s</b><div class="muted">%s • %s • %s</div></div>'%(x['business_name'],x['name'],x['industry'] or '-',x['city'] or '-') for x in recent_b) or '<p class="muted">No businesses yet.</p>';rp=''.join('<div class="item"><b>%s</b><div class="muted">%s • %s • %s/100</div></div>'%(x['name'],x['primary_role'],x['status'],x['score']) for x in recent_p) or '<p class="muted">No professionals yet.</p>'
    return page('Admin Dashboard',admin_nav()+'''<div class="head"><div><h2>DIGIBIZ Admin Dashboard</h2><p class="muted">Full marketplace overview.</p></div></div><div class="grid"><div class="card"><h3>Business Owners</h3><div class="score">%s</div><a href="/admin/businesses">View all →</a></div><div class="card"><h3>Professionals / Agencies</h3><div class="score">%s</div><a href="/admin/professionals">View all →</a></div><div class="card"><h3>Requirements</h3><div class="score">%s</div><a href="/admin/requirements">View all →</a></div><div class="card"><h3>Pending Reviews</h3><div class="score">%s</div><a href="/admin/assessments">Review →</a></div><div class="card"><h3>Contact Requests</h3><div class="score">%s</div><a href="/admin/contacts">View all →</a></div></div><div class="two section"><div class="card"><h3>Recent Businesses</h3>%s</div><div class="card"><h3>Recent Professionals</h3>%s</div></div>'''%(b,p,r,a,c,rb,rp))

@app.route('/admin/businesses')
@auth('admin')
def admin_businesses():
    rows=con().execute('SELECT u.id,u.name,u.email,b.* FROM businesses b JOIN users u ON u.id=b.user_id ORDER BY u.id DESC').fetchall();body=''.join('<tr><td>%s</td><td><b>%s</b><br><span class="muted">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(x['id'],x['business_name'],x['name'],x['email'],x['industry'] or '-',x['city'] or '-',x['website'] or '-') for x in rows) or '<tr><td colspan="6">No businesses registered.</td></tr>'
    return page('Business Owners',admin_nav()+'<div class="head"><div><h2>Business Owners</h2><p class="muted">All registered business accounts and profile details.</p></div></div><div class="tablewrap"><table class="table"><tr><th>ID</th><th>Business / Owner</th><th>Email</th><th>Industry</th><th>City</th><th>Website</th></tr>'+body+'</table></div>')

@app.route('/admin/professionals')
@auth('admin')
def admin_professionals():
    rows=con().execute('SELECT u.id,u.name,u.email,u.role,p.* FROM pros p JOIN users u ON u.id=p.user_id ORDER BY u.id DESC').fetchall();body=''.join('<tr><td>%s</td><td><b>%s</b><br><span class="muted">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s/100</td><td>%s</td><td>%s</td></tr>'%(x['id'],x['name'],x['account_type'],x['email'],x['category'],x['primary_role'],x['experience'] or '-',x['score'],x['status'],x['city'] or '-') for x in rows) or '<tr><td colspan="9">No professionals registered.</td></tr>'
    return page('Professionals',admin_nav()+'<div class="head"><div><h2>Professionals & Agencies</h2><p class="muted">Profiles, roles, scores and verification status.</p></div></div><div class="tablewrap"><table class="table"><tr><th>ID</th><th>Name / Type</th><th>Email</th><th>Category</th><th>Role</th><th>Experience</th><th>Score</th><th>Status</th><th>City</th></tr>'+body+'</table></div>')

@app.route('/admin/requirements')
@auth('admin')
def admin_requirements():
    rows=con().execute('SELECT r.*,u.name owner,b.business_name FROM requirements r JOIN users u ON u.id=r.business_id JOIN businesses b ON b.user_id=r.business_id ORDER BY r.id DESC').fetchall();body=''.join('<tr><td>%s</td><td><b>%s</b><br><span class="muted">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(x['id'],x['business_name'],x['owner'],x['title'],x['required_role'],x['goal'] or '-',x['budget'] or '-',x['timeline'] or '-',x['status']) for x in rows) or '<tr><td colspan="8">No requirements posted.</td></tr>'
    return page('Requirements',admin_nav()+'<div class="head"><div><h2>Business Requirements</h2><p class="muted">Everything businesses have requested.</p></div></div><div class="tablewrap"><table class="table"><tr><th>ID</th><th>Business</th><th>Requirement</th><th>Role</th><th>Goal</th><th>Budget</th><th>Timeline</th><th>Status</th></tr>'+body+'</table></div>')

@app.route('/admin/contacts')
@auth('admin')
def admin_contacts():
    rows=con().execute('''SELECT c.*,r.title,b.business_name,bu.name business_owner,pu.name pro_name,p.primary_role FROM contacts c JOIN requirements r ON r.id=c.requirement_id JOIN businesses b ON b.user_id=c.business_id JOIN users bu ON bu.id=c.business_id JOIN users pu ON pu.id=c.pro_id JOIN pros p ON p.user_id=c.pro_id ORDER BY c.id DESC''').fetchall();body=''.join('<tr><td>%s</td><td><b>%s</b><br><span class="muted">%s</span></td><td>%s</td><td><b>%s</b><br><span class="muted">%s</span></td><td>%s</td></tr>'%(x['id'],x['business_name'],x['business_owner'],x['title'],x['pro_name'],x['primary_role'],x['status']) for x in rows) or '<tr><td colspan="5">No contact requests.</td></tr>'
    return page('Contact Requests',admin_nav()+'<div class="head"><div><h2>Contact Requests</h2><p class="muted">Which business requested which professional.</p></div></div><div class="tablewrap"><table class="table"><tr><th>ID</th><th>Business</th><th>Requirement</th><th>Professional</th><th>Status</th></tr>'+body+'</table></div>')

@app.route('/admin/assessments')
@auth('admin')
def admin_assessments():
    pending=con().execute("SELECT a.*,u.name,u.email,p.category,p.primary_role FROM assessments a JOIN users u ON u.id=a.pro_id JOIN pros p ON p.user_id=u.id ORDER BY a.id DESC").fetchall();cards=''.join('<div class="card"><span class="pill">%s</span><h3>%s</h3><p class="muted">%s • %s • %s</p><p><b>Response:</b> %s</p><p><b>Evidence:</b> %s</p>%s</div>'%(x['status'],x['name'],x['email'],x['category'],x['primary_role'],x['response'],x['evidence'] or 'Not supplied',('<form method="post" action="/review/%s"><label>Score 0–100</label><input type="number" name="score" min="0" max="100" value="80"><br><button class="btn green">Verify & Save</button></form>'%x['id']) if x['status']=='Pending' else '<div class="score">%s/100</div>'%x['score']) for x in pending) or '<div class="card">No assessments yet.</div>'
    return page('Assessments',admin_nav()+'<div class="head"><div><h2>Assessment & Verification</h2><p class="muted">Review practical proof, evidence and final scores.</p></div></div>'+cards)

@app.post('/review/<int:aid>')
@auth('admin')
def review(aid):
    a=con().execute('SELECT * FROM assessments WHERE id=?',(aid,)).fetchone()
    if not a:return 'Not found',404
    score=max(0,min(100,int(request.form['score'])));status='Verified Pro' if score>=85 else 'Skill Verified' if score>=65 else 'Needs Improvement';con().execute("UPDATE assessments SET score=?,status='Reviewed' WHERE id=?",(score,aid));con().execute('UPDATE pros SET score=?,status=? WHERE user_id=?',(score,status,a['pro_id']));con().commit();flash('Verification updated.');return redirect('/admin/assessments')

if __name__=='__main__':
    with app.app_context():init()
    app.run(debug=True,port=5000)
