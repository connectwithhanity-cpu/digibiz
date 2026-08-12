import app as core

# Keep the full DIGIBIZ application in app.py, but improve the public header
# so each user type has a clear login entry point.

old_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a href="/login">Login</a><a class="btn dark" href="/register/business">Get Started</a>{% endif %}</div>'''

new_header = '''<div class="actions">{% if session.get('uid') %}<a class="btn ghost" href="/dashboard">Dashboard</a><a class="btn dark" href="/logout">Logout</a>{% else %}<a class="btn ghost" href="/login?type=business">Business Login</a><a class="btn ghost" href="/login?type=professional">Professional / Agency Login</a><a class="btn dark" href="/login?admin=1">Admin Login</a>{% endif %}</div>'''

core.BASE = core.BASE.replace(old_header, new_header)

# Improve the login page title based on the header button selected.
original_login = core.login

def typed_login():
    if core.request.method == 'POST':
        return original_login()
    if core.request.args.get('admin'):
        heading = 'Admin Login'
        sub = 'Secure access to DIGIBIZ administration and verification.'
    elif core.request.args.get('type') == 'business':
        heading = 'Business Owner Login'
        sub = 'Manage requirements, matches and expert requests.'
    elif core.request.args.get('type') == 'professional':
        heading = 'Professional / Agency Login'
        sub = 'Manage your profile, verification and opportunities.'
    else:
        heading = 'Welcome back'
        sub = 'Access your DIGIBIZ workspace.'

    note = '<p class="muted">Prototype admin: admin@digibiz.in / admin123</p>' if core.request.args.get('admin') else ''
    return core.page('Login', f'''<div class="form card"><h1>{heading}</h1><p class="muted">{sub}</p><form method="post"><label>Email</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><br><button class="btn dark">Login</button></form>{note}</div>''')

# Replace the route endpoint callable while preserving the existing URL rule.
core.app.view_functions['login'] = typed_login

# Better header wrapping on phones and smaller laptops.
core.BASE = core.BASE.replace('</style></head>', '''
<style>
@media(max-width:1050px){.actions{gap:6px}.actions .btn{padding:9px 11px;font-size:12px}}
@media(max-width:760px){.nav{height:auto;min-height:68px;padding:10px 0;flex-wrap:wrap}.actions{width:100%;overflow-x:auto;padding-bottom:2px}.actions .btn{white-space:nowrap}.logo{font-size:23px}}
</style></head>''')

app = core.app
