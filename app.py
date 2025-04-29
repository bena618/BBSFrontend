from flask import Flask, render_template, redirect, url_for, session
from flask_discord import DiscordOAuth2Session
import csv
import os

app = Flask(__name__, static_folder='static', static_url_path='/')

app.secret_key = os.environ.get('APP_SECRET_KEY')
app.config["DISCORD_CLIENT_ID"] = int(os.environ.get('DISCORD_CLIENT_ID'))
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get('DISCORD_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = os.environ.get('DISCORD_REDIRECT_URI')
app.config["DISCORD_BOT_TOKEN"] = os.environ.get('DISCORD_BOT_TOKEN')

discord = DiscordOAuth2Session(app)

GUILD_ID = 1187465028400599060
VIP_ROLES = {'Super Admin', 'Moderator', 'Verified', 'IB'} 

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login/')
def login():
    return discord.create_session(scope=["identify", "guilds", "guilds.members.read"])

@app.route('/callback')
def callback():
    discord.callback()
    if discord.authorized:
        user = discord.fetch_user()
        print(user)
        session['username'] = user.username
        print(session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if discord.authorized:
        discord.revoke()
    session.pop('username', None)
    return redirect(url_for('index'))

def user_is_vip():
    if not discord.authorized:
        return False
    user = discord.fetch_user()
    member = discord.bot_request(f"/guilds/{GUILD_ID}/members/{user.id}")

    if not member or "roles" not in member:
        return False

    roles = discord.bot_request(f"/guilds/{GUILD_ID}/roles")
    if not roles:
        return False

    role_id_to_name = {role["id"]: role["name"] for role in roles}
    member_role_names = {role_id_to_name.get(rid) for rid in member["roles"]}
    print(member_role_names)

    return bool(member_role_names.intersection(VIP_ROLES))


@app.context_processor
def inject_username():
    return dict(username=session.get('username'))


@app.route('/mlb')
def mlb():
    vip = user_is_vip()

    with open('model_outputs/nrfi_yrfi_picks.csv', newline='') as f:
        nrfi_reader = csv.reader(f)
        nrfi_rows = list(nrfi_reader)
    nrfi_header = nrfi_rows[0]
    nrfi_data = nrfi_rows[1:]

    with open('model_outputs/hit_picks.csv', newline='') as f:
        hits_reader = csv.reader(f)
        hits_rows = list(hits_reader)
    hits_header = hits_rows[0]
    hits_data = hits_rows[1:]

    with open('model_outputs/strikeout_preds.csv', newline='') as f:
        ks_reader = csv.reader(f)
        ks_rows = list(ks_reader)
    ks_header = ks_rows[0]
    ks_data = ks_rows[1:]

    with open('model_outputs/f5_picks.csv', newline='') as f:
        f5_reader = csv.reader(f)
        f5_rows = list(f5_reader)
    f5_header = f5_rows[0]
    f5_data = f5_rows[1:]

    if not vip:
        nrfi_data = nrfi_data[-2:]
        nrfi_data.append(('Join','Vip','For','Full','Access','To','The','Chart'))

        hits_data = hits_data[:5]
        hits_data.append(('Join Vip For Full Chart Access','BBS','22:22 PM ET',0.0,+999))

        ks_data = ks_data[:2]
        ks_data.append(('Join', 'Vip', 'For', 'Full', 'Access','To', 'F5', 'ML','Chart'))

        f5_data = f5_data[:5]
        f5_data.append(('Join', 'Vip', 'For', 'Full', 'Chat','Access'))


    return render_template('baseball.html',
                           nrfi_header=nrfi_header,
                           nrfi_data=nrfi_data,
                           hits_header=hits_header,
                           hits_data=hits_data,
                           ks_header=ks_header,
                           ks_data=ks_data,
                           f5_header=f5_header,
                           f5_data=f5_data,
                           vip=vip)

@app.route('/nba')
@app.route('/nfl')
@app.route('/ncaaf')
@app.route('/nhl')
def comingsoon():
    return render_template('comingsoon.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404