import app as core

# DIGIBIZ MVP header: separate login entry points for each user type.
old_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''
new_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a class="btn ghost" href="/login?type=business">Business Login</a><a class="btn ghost" href="/login?type=professional">Professional / Agency Login</a><a class="btn dark" href="/login?admin=1">Admin Login</a>{% endif %}</div>'''
core.BASE = core.BASE.replace(old_header, new_header)

# Remove the duplicate Business / Professional / Admin buttons from the homepage hero.
# Login actions now live only in the header.
old_hero_buttons = '''<a class="btn green" href="/register/business">I’m a Business Owner</a> <a class="btn light" href="/register/pro">I’m a Professional / Agency</a> <a class="btn" href="/login?admin=1">Admin Login</a>'''
core.home.__globals__['page'] = core.page
original_home = core.home

def clean_home():
    response = original_home()
    if isinstance(response, str):
        return response.replace(old_hero_buttons, '')
    return response
core.app.view_functions['home'] = clean_home

# Role-specific login page headings.
original_login = core.login
def typed_login():
    if core.request.method == 'POST':
        return original_login()
    if core.request.args.get('admin'):
        heading='Admin Login'; sub='Secure access to DIGIBIZ administration and verification.'
    elif core.request.args.get('type') == 'business':
        heading='Business Owner Login'; sub='Manage requirements, matches and expert requests.'
    elif core.request.args.get('type') == 'professional':
        heading='Professional / Agency Login'; sub='Manage your profile, verification and opportunities.'
    else:
        heading='Welcome back'; sub='Access your DIGIBIZ workspace.'
    note='<p class="muted">Prototype admin: admin@digibiz.in / admin123</p>' if core.request.args.get('admin') else ''
    return core.page('Login',f'''<div class="form card"><h1>{heading}</h1><p class="muted">{sub}</p><form method="post"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Login</button></form>{note}</div>''')
core.app.view_functions['login']=typed_login

core.BASE=core.BASE.replace('</style></head>','''<style>@media(max-width:1050px){.actions{gap:6px}.actions .btn{padding:9px 11px;font-size:12px}}@media(max-width:760px){.nav{height:auto;min-height:68px;padding:10px 0;flex-wrap:wrap}.actions{width:100%;overflow-x:auto;padding-bottom:2px}.actions .btn{white-space:nowrap}.logo{font-size:23px}}</style></head>''')

app=core.app
