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

# Replace old brand text everywhere rendered through the shared page function.
original_page = core.page
def branded_page(title, body):
    body = body.replace('DIGIBIZ', 'BUZENT').replace('Digibiz', 'BUZENT').replace('digibiz', 'buzent')
    html = original_page(title, body)
    html = html.replace('DIGIBIZ', 'BUZENT').replace('Digibiz', 'BUZENT')
    return html
core.page = branded_page
core.home.__globals__['page'] = branded_page

# Corporate BUZENT wordmark in the header: compact B mark + BUZENT, with gold Z.
old_logo = '''<a class="logo" href="/">DIGIBIZ<span class="dot">.</span></a>'''
new_logo = '''<a class="logo buzent-logo" href="/" aria-label="BUZENT Home"><span class="bz-mark">B</span><span class="bz-word">BU<span class="bz-gold">Z</span>ENT</span></a>'''
core.BASE = core.BASE.replace(old_logo, new_logo)
core.BASE = core.BASE.replace('Why DIGIBIZ', 'Why BUZENT')
core.BASE = core.BASE.replace('DIGIBIZ • Verified Experts. Smarter Business Growth.', 'BUZENT • Where Businesses Meet Marketing Talent. &nbsp; | &nbsp; buzentofficial@gmail.com &nbsp; | &nbsp; Instagram: @buzentofficial')

# Separate login entry points in the header.
old_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''
new_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a class="btn ghost" href="/login?type=business">Business Login</a><a class="btn ghost" href="/login?type=professional">Professional / Agency Login</a><a class="btn dark" href="/login?admin=1">Admin Login</a>{% endif %}</div>'''
core.BASE = core.BASE.replace(old_header, new_header)

# Remove duplicate login buttons from the homepage hero.
old_hero_buttons = '''<a class="btn green" href="/register/business">I’m a Business Owner</a> <a class="btn light" href="/register/pro">I’m a Professional / Agency</a> <a class="btn" href="/login?admin=1">Admin Login</a>'''
original_home = core.home
def clean_home():
    response = original_home()
    if isinstance(response, str):
        return response.replace(old_hero_buttons, '').replace('DIGIBIZ', 'BUZENT')
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

# BUZENT corporate header styling.
core.BASE = core.BASE.replace('</style></head>','''<style>
.buzent-logo{display:flex;align-items:center;gap:9px;letter-spacing:.12em}.bz-mark{width:36px;height:36px;border-radius:9px;background:#0b1f3a;color:#fff;display:grid;place-items:center;font-family:'Manrope';font-size:24px;font-weight:800;position:relative}.bz-mark:after{content:'↗';position:absolute;color:#d99a20;font-size:17px;transform:rotate(-8deg)}.bz-word{font-size:22px;font-weight:800;color:#0b1f3a}.bz-gold{color:#d99a20}.footer{line-height:1.8}@media(max-width:1050px){.actions{gap:6px}.actions .btn{padding:9px 11px;font-size:12px}}@media(max-width:760px){.nav{height:auto;min-height:68px;padding:10px 0;flex-wrap:wrap}.actions{width:100%;overflow-x:auto;padding-bottom:2px}.actions .btn{white-space:nowrap}.bz-word{font-size:19px}.bz-mark{width:32px;height:32px;font-size:21px}}
</style></head>''')

app = core.app
