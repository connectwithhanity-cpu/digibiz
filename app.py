import os, sqlite3
from functools import wraps
from flask import Flask, request, redirect, session, flash, render_template_string, g
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__); app.secret_key=os.getenv('SECRET_KEY','digibiz-dev-change-me')
DB=os.getenv('DB_PATH','/tmp/digibiz.db')
ROLES={'Digital Marketing':['Digital Marketing Manager','Performance Marketer','Meta Ads Specialist','Google Ads / PPC Specialist','SEO Specialist','Local SEO / GBP Specialist','Social Media Manager','Content Strategist','Email Marketer','WhatsApp Marketer','E-commerce Marketer','Lead Generation Specialist','Marketing Strategist'],'Creative & Production':['Graphic Designer','Brand Designer','UI/UX Designer','Video Editor','Reels Editor','Motion Graphics Designer','Photographer','Videographer','Content Creator','Copywriter','UGC Creator'],'Web & Technology':['Website Designer','WordPress Developer','Shopify Developer','Web Developer','Landing Page Specialist','App Developer','AI Automation Expert','Chatbot Developer','No-Code Developer','Pixel / Tracking Specialist'],'Sales & Promotion':['Sales Executive','Business Development Executive','Appointment Setter','Telecaller','Sales Closer','Field Promoter','Brand Promoter','Event Promoter','Product Promoter','Growth Consultant'],'Influencers & Creators':['Nano Influencer','Micro Influencer','Macro Influencer','Instagram Creator','YouTube Creator','Regional Influencer','Food Influencer','Fashion Influencer','Tech Influencer','Finance Influencer','Education Influencer','Local / City Influencer'],'Professional Business Services':['Chartered Accountant (CA)','Accountant','GST Consultant','Tax Consultant','Company Registration Consultant','Financial Consultant','Legal / Compliance Professional'],'Agencies':['Digital Marketing Agency','Creative Agency','Advertising Agency','Social Media Agency','Influencer Marketing Agency','Web Development Agency','Video Production Agency','Branding Agency','Lead Generation Agency']}

def con():
 if 'db' not in g: g.db=sqlite3.connect(DB); g.db.row_factory=sqlite3.Row
 return g.db
@app.teardown_appcontext
def close(e=None):
 d=g.pop('db',None)
 if d:d.close()

def init():
 d=con(); d.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password TEXT,role TEXT);CREATE TABLE IF NOT EXISTS businesses(user_id INTEGER PRIMARY KEY,business_name TEXT,industry TEXT,city TEXT,website TEXT);CREATE TABLE IF NOT EXISTS pros(user_id INTEGER PRIMARY KEY,account_type TEXT,category TEXT,primary_role TEXT,experience TEXT,city TEXT,industries TEXT,portfolio TEXT,pricing TEXT,bio TEXT,status TEXT DEFAULT 'Not Verified',score INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS requirements(id INTEGER PRIMARY KEY AUTOINCREMENT,business_id INTEGER,title TEXT,category TEXT,required_role TEXT,goal TEXT,budget TEXT,timeline TEXT,description TEXT,status TEXT DEFAULT 'Open');CREATE TABLE IF NOT EXISTS assessments(id INTEGER PRIMARY KEY AUTOINCREMENT,pro_id INTEGER,response TEXT,evidence TEXT,status TEXT DEFAULT 'Pending',score INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,requirement_id INTEGER,business_id INTEGER,pro_id INTEGER,status TEXT DEFAULT 'Requested');''')
 if not d.execute("SELECT id FROM users WHERE email='admin@digibiz.in'").fetchone(): d.execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',('DIGIBIZ Admin','admin@digibiz.in',generate_password_hash('admin123'),'admin'))
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

CSS='''*{box-sizing:border-box}body{margin:0;font-family:Arial;background:#f4f7fb;color:#172033}a{text-decoration:none;color:inherit}nav{background:#071d38;color:white;padding:16px 5%;display:flex;justify-content:space-between}.logo{font-size:25px;font-weight:900}.wrap{width:min(1180px,92%);margin:28px auto}.hero{background:linear-gradient(135deg,#071d38,#164f91);color:white;border-radius:28px;padding:52px}.hero h1{font-size:48px;margin:0 0 15px}.hero p{color:#dce8f6;font-size:18px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;border:1px solid #dce5ef;border-radius:20px;padding:21px;margin:16px 0}.btn{display:inline-block;border:0;border-radius:11px;padding:11px 16px;background:#1769e0;color:white;font-weight:800;cursor:pointer}.green{background:#12a36d}.light{background:white;color:#071d38}.muted{color:#68758a}label{display:block;font-weight:800;margin:12px 0 6px}input,select,textarea{width:100%;padding:11px;border:1px solid #cbd6e3;border-radius:10px}textarea{min-height:100px}.pill{display:inline-block;background:#e8f7f0;color:#0d7048;border-radius:999px;padding:6px 9px;font-weight:800}.score{font-size:32px;font-weight:900;color:#1769e0}.item{border:1px solid #dce5ef;border-radius:15px;padding:15px;margin:10px 0}.flash{background:#e8f2ff;padding:10px;border-radius:10px}@media(max-width:760px){.two{grid-template-columns:1fr}.hero h1{font-size:33px}}'''
BASE='''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} | DIGIBIZ</title><style>'''+CSS+'''</style><nav><a class="logo" href="/">DIGIBIZ</a><div>{% if session.get('uid') %}<a href="/dashboard">Dashboard</a> &nbsp; <a href="/logout">Logout</a>{% else %}<a href="/login">Login</a>{% endif %}</div></nav><main class="wrap">{% for m in get_flashed_messages() %}<div class="flash">{{m}}</div>{% endfor %}{{body|safe}}</main>'''
def page(t,b):return render_template_string(BASE,title=t,body=b)
def opts():return ''.join('<optgroup label="%s">%s</optgroup>'%(c,''.join('<option value="%s|%s">%s</option>'%(c,r,r) for r in rs)) for c,rs in ROLES.items())

@app.route('/')
def home():
 groups=''.join('<div class="card"><h3>%s</h3><p class="muted">%s</p></div>'%(c,', '.join(rs)) for c,rs in ROLES.items())
 return page('Home','''<section class="hero"><h1>Verified Experts. Smarter Business Growth.</h1><p>DIGIBIZ connects businesses with verified marketers, designers, editors, developers, promoters, influencers, CAs, consultants and agencies based on proof, not promises.</p><a class="btn green" href="/register/business">Business Owner</a> <a class="btn light" href="/register/pro">Professional / Agency</a> <a class="btn" href="/login?admin=1">Admin Login</a></section><div class="grid">'''+groups+'</div>')

@app.route('/register/business',methods=['GET','POST'])
def reg_business():
 init()
 if request.method=='POST':
  f=request.form
  try:
   c=con().execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',(f['name'],f['email'].lower(),generate_password_hash(f['password']),'business')); con().execute('INSERT INTO businesses VALUES(?,?,?,?,?)',(c.lastrowid,f['business'],f.get('industry',''),f.get('city',''),f.get('website',''))); con().commit(); flash('Account created. Login now.'); return redirect('/login')
  except sqlite3.IntegrityError:flash('Email already registered.')
 return page('Business Registration','''<div class="card"><h1>Business Owner Registration</h1><form method="post"><label>Owner Name</label><input name="name" required><label>Business Name</label><input name="business" required><label>Industry</label><input name="industry"><label>City</label><input name="city"><label>Website / Instagram</label><input name="website"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><br><button class="btn green">Create Account</button></form></div>''')

@app.route('/register/pro',methods=['GET','POST'])
def reg_pro():
 init()
 if request.method=='POST':
  f=request.form; cat,pr=f['combined'].split('|',1); role='agency' if f['account_type']=='Agency' else 'professional'
  try:
   c=con().execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',(f['name'],f['email'].lower(),generate_password_hash(f['password']),role)); con().execute('INSERT INTO pros(user_id,account_type,category,primary_role,experience,city,industries,portfolio,pricing,bio) VALUES(?,?,?,?,?,?,?,?,?,?)',(c.lastrowid,f['account_type'],cat,pr,f.get('experience',''),f.get('city',''),f.get('industries',''),f.get('portfolio',''),f.get('pricing',''),f.get('bio',''))); con().commit(); flash('Profile created. Login to verify your skill.'); return redirect('/login')
  except sqlite3.IntegrityError:flash('Email already registered.')
 return page('Professional Registration','''<div class="card"><h1>Professional / Agency Registration</h1><form method="post"><label>Name / Agency</label><input name="name" required><label>Account Type</label><select name="account_type"><option>Freelancer / Professional</option><option>Creator / Influencer</option><option>Promoter</option><option>CA / Business Professional</option><option>Agency</option></select><label>Primary Role</label><select name="combined">'''+opts()+'''</select><label>Experience</label><input name="experience"><label>City / Service Area</label><input name="city"><label>Industries</label><input name="industries"><label>Portfolio / Social URL</label><input name="portfolio"><label>Pricing</label><input name="pricing"><label>About / Evidence</label><textarea name="bio"></textarea><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><br><button class="btn green">Create Profile</button></form></div>''')

@app.route('/login',methods=['GET','POST'])
def login():
 init()
 if request.method=='POST':
  u=con().execute('SELECT * FROM users WHERE email=?',(request.form['email'].lower(),)).fetchone()
  if u and check_password_hash(u['password'],request.form['password']):session.clear();session.update(uid=u['id'],role=u['role'],name=u['name']);return redirect('/dashboard')
  flash('Invalid email or password.')
 note='<p class="muted">Prototype admin: admin@digibiz.in / admin123</p>' if request.args.get('admin') else ''
 return page('Login','<div class="card"><h1>Login</h1><form method="post"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><br><button class="btn">Login</button></form>'+note+'</div>')
@app.route('/logout')
def logout():session.clear();return redirect('/')
@app.route('/dashboard')
@auth()
def dash():return redirect('/admin' if session['role']=='admin' else '/business' if session['role']=='business' else '/professional')

@app.route('/business')
@auth('business')
def business():
 b=con().execute('SELECT * FROM businesses WHERE user_id=?',(session['uid'],)).fetchone(); rs=con().execute('SELECT * FROM requirements WHERE business_id=? ORDER BY id DESC',(session['uid'],)).fetchall(); rows=''.join('<div class="item"><b>%s</b><p class="muted">%s • %s</p><a class="btn" href="/matches/%s">Find Matches</a></div>'%(r['title'],r['required_role'],r['budget'] or '',r['id']) for r in rs) or '<p class="muted">No requirements yet.</p>'
 return page('Business Dashboard','<h1>%s</h1><div class="two"><div class="card"><h2>Grow your business</h2><a class="btn green" href="/requirement">+ Post Requirement</a></div><div class="card"><h2>Your Requirements</h2>%s</div></div>'%(b['business_name'],rows))
@app.route('/requirement',methods=['GET','POST'])
@auth('business')
def requirement():
 if request.method=='POST':
  f=request.form;cat,rr=f['combined'].split('|',1);c=con().execute('INSERT INTO requirements(business_id,title,category,required_role,goal,budget,timeline,description) VALUES(?,?,?,?,?,?,?,?)',(session['uid'],f['title'],cat,rr,f.get('goal',''),f.get('budget',''),f.get('timeline',''),f.get('description','')));con().commit();return redirect('/matches/%s'%c.lastrowid)
 return page('Post Requirement','<div class="card"><h1>What does your business need?</h1><form method="post"><label>Requirement</label><input name="title" required><label>Expert Role</label><select name="combined">'+opts()+'</select><label>Goal</label><input name="goal"><label>Budget</label><input name="budget"><label>Timeline</label><input name="timeline"><label>Description</label><textarea name="description"></textarea><br><button class="btn green">Post & Find Experts</button></form></div>')
@app.route('/matches/<int:rid>')
@auth('business')
def matches(rid):
 r=con().execute('SELECT * FROM requirements WHERE id=? AND business_id=?',(rid,session['uid'])).fetchone()
 if not r:return 'Not found',404
 ps=con().execute('SELECT u.name,p.* FROM pros p JOIN users u ON u.id=p.user_id WHERE p.primary_role=? OR p.category=? ORDER BY p.score DESC',(r['required_role'],r['category'])).fetchall(); cards=''.join('<div class="card"><h3>%s</h3><span class="pill">%s</span><p><b>%s</b></p><div class="score">%s/100</div><p class="muted">%s</p><form method="post" action="/contact/%s/%s"><button class="btn green">Request Contact</button></form></div>'%(p['name'],p['status'],p['primary_role'],p['score'],p['pricing'] or 'Pricing on request',rid,p['user_id']) for p in ps) or '<div class="card">No matching registered experts yet.</div>'
 return page('Matches','<h1>Recommended Experts</h1><p class="muted">%s</p><div class="grid">%s</div>'%(r['required_role'],cards))
@app.post('/contact/<int:rid>/<int:pid>')
@auth('business')
def contact(rid,pid):con().execute('INSERT INTO contacts(requirement_id,business_id,pro_id) VALUES(?,?,?)',(rid,session['uid'],pid));con().commit();flash('Contact request sent.');return redirect('/matches/%s'%rid)

@app.route('/professional')
@auth('professional','agency')
def professional():
 p=con().execute('SELECT * FROM pros WHERE user_id=?',(session['uid'],)).fetchone(); ass=con().execute('SELECT * FROM assessments WHERE pro_id=? ORDER BY id DESC',(session['uid'],)).fetchall(); hist=''.join('<div class="item"><b>%s</b> • %s/100</div>'%(a['status'],a['score']) for a in ass) or '<p class="muted">No assessment yet.</p>'
 guide='Submit social metrics, audience geography and collaboration evidence.' if p['category']=='Influencers & Creators' else 'Submit applicable credentials and professional service proof.' if p['category']=='Professional Business Services' else 'Submit location, language and field campaign proof.' if p['category']=='Sales & Promotion' else 'Solve a practical role-specific business problem and provide evidence.'
 return page('Professional Dashboard','<h1>%s</h1><div class="grid"><div class="card"><h3>Status</h3><span class="pill">%s</span></div><div class="card"><h3>DIGIBIZ Score</h3><div class="score">%s/100</div></div><div class="card"><h3>Role</h3>%s</div></div><div class="two"><div class="card"><h2>Get Verified</h2><p class="muted">%s</p><form method="post" action="/assessment"><label>Practical Response</label><textarea name="response" required></textarea><label>Evidence / Portfolio / Credential</label><input name="evidence"><br><button class="btn green">Submit for Review</button></form></div><div class="card"><h2>History</h2>%s</div></div>'%(session['name'],p['status'],p['score'],p['primary_role'],guide,hist))
@app.post('/assessment')
@auth('professional','agency')
def assessment():con().execute('INSERT INTO assessments(pro_id,response,evidence) VALUES(?,?,?)',(session['uid'],request.form['response'],request.form.get('evidence','')));con().commit();flash('Submitted for admin review.');return redirect('/professional')

@app.route('/admin')
@auth('admin')
def admin():
 d=con(); b=d.execute("SELECT count(*) c FROM users WHERE role='business'").fetchone()['c'];p=d.execute("SELECT count(*) c FROM users WHERE role IN ('professional','agency')").fetchone()['c'];q=d.execute("SELECT count(*) c FROM assessments WHERE status='Pending'").fetchone()['c'];pending=d.execute("SELECT a.*,u.name,p.primary_role FROM assessments a JOIN users u ON u.id=a.pro_id JOIN pros p ON p.user_id=a.pro_id WHERE a.status='Pending' ORDER BY a.id DESC").fetchall(); cards=''.join('<div class="card"><h3>%s</h3><p>%s</p><p class="muted">%s</p><form method="post" action="/review/%s"><label>Score</label><input type="number" min="0" max="100" name="score" value="80"><br><button class="btn green">Verify</button></form></div>'%(a['name'],a['response'],a['primary_role'],a['id']) for a in pending) or '<p class="muted">No pending reviews.</p>'
 return page('Admin','<h1>DIGIBIZ Admin</h1><div class="grid"><div class="card"><h3>Businesses</h3><div class="score">%s</div><p>Target 100</p></div><div class="card"><h3>Professionals / Agencies</h3><div class="score">%s</div><p>Target 300</p></div><div class="card"><h3>Pending Reviews</h3><div class="score">%s</div></div></div><h2>Verification Queue</h2>%s'%(b,p,q,cards))
@app.post('/review/<int:aid>')
@auth('admin')
def review(aid):
 a=con().execute('SELECT * FROM assessments WHERE id=?',(aid,)).fetchone();s=max(0,min(100,int(request.form['score'])));status='Verified Pro' if s>=85 else 'Skill Verified' if s>=65 else 'Needs Improvement';con().execute("UPDATE assessments SET score=?,status='Reviewed' WHERE id=?",(s,aid));con().execute('UPDATE pros SET score=?,status=? WHERE user_id=?',(s,status,a['pro_id']));con().commit();return redirect('/admin')

with app.app_context():init()
if __name__=='__main__':app.run(debug=True,port=5000)
