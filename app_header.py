import app as core

# BUZENT brand layer for the existing MVP.
# Keeps the current routes, dashboards and database behaviour intact.

# Migrate the prototype admin identity to the BUZENT brand.
original_init = core.init
def buzent_init():
    original_init()
    d = core.con()
    old = d.execute("SELECT id FROM users WHERE email='admin@digibiz.in' AND role='admin'").fetchone()
    new = d.execute("SELECT id FROM users WHERE email='buzentofficial@gmail.com' AND role='admin'").fetchone()
    if old and not new:
        d.execute("UPDATE users SET name=?, email=? WHERE id=?", ('BUZENT Admin', 'buzentofficial@gmail.com', old['id']))
        d.commit()
core.init = buzent_init

# Replace legacy brand text everywhere rendered through the shared page function.
original_page = core.page
def branded_page(title, body):
    body = body.replace('DIGIBIZ', 'BUZENT').replace('Digibiz', 'BUZENT').replace('digibiz', 'buzent').replace('Climbzy', 'BUZENT').replace('CLIMBZY', 'BUZENT')
    html = original_page(title, body)
    html = html.replace('DIGIBIZ', 'BUZENT').replace('Digibiz', 'BUZENT').replace('Climbzy', 'BUZENT').replace('CLIMBZY', 'BUZENT')
    return html
core.page = branded_page
core.home.__globals__['page'] = branded_page

# Compact official BUZENT logo for the website header.
# The inline SVG mirrors the approved navy/white/gold B + connection symbol.
old_logo = '''<a class="logo" href="/">DIGIBIZ<span class="dot">.</span></a>'''
new_logo = '''<a class="logo buzent-logo" href="/" aria-label="BUZENT Home">
<svg class="bz-icon" viewBox="0 0 64 64" role="img" aria-label="BUZENT logo">
  <path d="M16 8h25c9 0 15 6 15 14 0 6-3 10-8 12 6 2 10 7 10 13 0 6-3 10-7 13V43c0-6-4-10-10-10H28V18h13c3 0 5 2 5 5s-2 5-5 5H28v27H16V8z" fill="#0b1f3a"/>
  <path d="M10 48C18 29 27 18 40 13c-8 8-14 17-18 27-2 5-3 10-3 15-5-1-8-3-9-7z" fill="#d99a20"/>
  <circle cx="28" cy="45" r="4.5" fill="#ffffff"/>
  <circle cx="41" cy="45" r="4.5" fill="#d99a20"/>
  <path d="M21 56c1-6 4-9 8-9 3 0 5 2 7 4 2-2 4-4 7-4 4 0 7 3 8 9H43c-1-3-2-4-4-4-1 0-2 1-3 2-1 1-2 1-3 0-1-1-2-2-3-2-2 0-3 1-4 4h-5z" fill="#0b1f3a"/>
  <path d="M36 54c1 0 2 0 3-1 1-1 2-1 3-1 2 0 3 1 4 4h5c-1-6-4-9-8-9-3 0-5 2-7 4z" fill="#d99a20"/>
</svg>
<span class="bz-word">BU<span class="bz-gold">Z</span>ENT</span></a>'''
core.BASE = core.BASE.replace(old_logo, new_logo)
core.BASE = core.BASE.replace('Why DIGIBIZ', 'Why BUZENT')
core.BASE = core.BASE.replace('DIGIBIZ • Verified Experts. Smarter Business Growth.', 'BUZENT • A global platform for businesses and professional talent. &nbsp; | &nbsp; buzentofficial@gmail.com &nbsp; | &nbsp; Instagram: @buzentofficial')

# Separate login entry points in the header.
old_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''
new_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a class="btn ghost" href="/login?type=business">Business Login</a><a class="btn ghost" href="/login?type=professional">Professional / Agency Login</a><a class="btn dark" href="/login?admin=1">Admin Login</a>{% endif %}</div>'''
core.BASE = core.BASE.replace(old_header, new_header)

# Remove duplicate login buttons from the homepage hero and update the global positioning.
old_hero_buttons = '''<a class="btn green" href="/register/business">I’m a Business Owner</a> <a class="btn light" href="/register/pro">I’m a Professional / Agency</a> <a class="btn" href="/login?admin=1">Admin Login</a>'''
original_home = core.home
def clean_home():
    response = original_home()
    if isinstance(response, str):
        response = response.replace(old_hero_buttons, '')
        response = response.replace('Find the right expert. Grow with confidence.', 'Where businesses and the right talent find each other.')
        response = response.replace(
            'BUZENT helps businesses discover verified marketers, creators, developers, promoters, influencers, CAs and agencies — matched by capability, relevance and evidence.',
            'BUZENT is a global professional platform built for businesses and the people who help them grow. Business owners discover the right marketers, agencies, creators, influencers, promoters, CAs, developers, consultants and specialists — while professionals connect with relevant opportunities. Better connections. Mutual growth. Worldwide.'
        )
        response = response.replace('✓ Proof-first business growth network', 'Global Business × Professional Talent Network')
        response = response.replace('Every role your business may need', 'The people behind every growing business')
        response = response.replace('One network for business growth.', 'Discover the right expertise. Build trusted partnerships. Grow together.')
        return response.replace('DIGIBIZ', 'BUZENT').replace('Climbzy', 'BUZENT')
    return response
core.app.view_functions['home'] = clean_home

# Role-specific login headings.
original_login = core.login
def typed_login():
    core.init()
    if core.request.method == 'POST':
        return original_login()
    if core.request.args.get('admin'):
        heading='Admin Login'; sub='Secure access to BUZENT administration and verification.'
    elif core.request.args.get('type') == 'business':
        heading='Business Owner Login'; sub='Manage requirements, matches and professional connections.'
    elif core.request.args.get('type') == 'professional':
        heading='Professional / Agency Login'; sub='Manage your profile, verification and business opportunities.'
    else:
        heading='Welcome back'; sub='Access your BUZENT workspace.'
    note='<p class="muted">Prototype admin: buzentofficial@gmail.com / admin123</p>' if core.request.args.get('admin') else ''
    return core.page('Login',f'''<div class="form card"><h1>{heading}</h1><p class="muted">{sub}</p><form method="post"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Login</button></form>{note}</div>''')
core.app.view_functions['login'] = typed_login

# Corporate spacing and typography for a clean international platform interface.
core.BASE = core.BASE.replace('</style></head>','''<style>
.nav{height:82px;gap:28px}.buzent-logo{display:flex;align-items:center;gap:11px;min-width:190px}.bz-icon{width:43px;height:43px;display:block;filter:drop-shadow(0 4px 10px rgba(11,31,58,.10))}.bz-word{font-family:'Manrope';font-size:24px;font-weight:800;letter-spacing:.16em;color:#0b1f3a;white-space:nowrap}.bz-gold{color:#d99a20}.links{gap:30px;margin-left:auto;margin-right:auto}.links a{font-size:14px;white-space:nowrap}.actions{gap:9px}.hero{background:radial-gradient(circle at 78% 25%,rgba(217,154,32,.18),transparent 28%),linear-gradient(135deg,#07182f,#0b2c59 58%,#173e6b);border-radius:28px}.hero h1{max-width:760px}.footer{line-height:1.8}
@media(max-width:1120px){.links{gap:18px}.actions{gap:5px}.actions .btn{padding:9px 10px;font-size:12px}.bz-word{font-size:21px}.buzent-logo{min-width:165px}}
@media(max-width:900px){.nav{height:auto;min-height:72px;padding:10px 0;flex-wrap:wrap}.links{order:3;width:100%;justify-content:center;margin:0;padding-bottom:8px;overflow-x:auto}.actions{margin-left:auto}.bz-icon{width:38px;height:38px}.bz-word{font-size:20px}}
@media(max-width:760px){.links{display:flex}.actions{width:100%;overflow-x:auto;padding-bottom:3px}.actions .btn{white-space:nowrap}.buzent-logo{min-width:auto}.bz-word{font-size:18px}.bz-icon{width:35px;height:35px}}
</style></head>''')

app = core.app
