# jungle_score_app/app.py
import streamlit as st
import json
import os
import pandas as pd

# Load data
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

# Save data
def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

# Save to Excel
def save_to_excel(teams, members):
    team_data = [{"Team": t["name"], "Score": t["score"]} for t in teams.values()]
    member_data = [{"Member": m["name"], "Team": teams[m["team_id"]]["name"], "Score": m["score"]} for m in members.values()]
    df_teams = pd.DataFrame(team_data)
    df_members = pd.DataFrame(member_data)
    with pd.ExcelWriter("scores.xlsx") as writer:
        df_teams.to_excel(writer, sheet_name="Teams", index=False)
        df_members.to_excel(writer, sheet_name="Members", index=False)

# Setup
TEAM_FILE = "Sodasyat.json"
MEMBER_FILE = "Memebers.json"

teams = load_json(TEAM_FILE)
members = load_json(MEMBER_FILE)

# Style
st.set_page_config(page_title="🦁 Jungle Score System", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background-color: #fdf6e3;
        }
        .jungle-title {
            font-size: 48px;
            color: #fff;
            background-color: #2e7d32;
            padding: 10px;
            border-radius: 12px;
            text-align: center;
        }
        .stButton>button {
            background-color: #388e3c;
            color: white;
            font-weight: bold;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #2e7d32;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="jungle-title">🦁 Jungle Score System</h1>', unsafe_allow_html=True)

# Scoring categories
CATEGORIES = {
    "Attendance": 10,
    "On Time": 10,
    "Zey": 10,
    "Daleel": 10,
    "Odas": 10,
    "Bonus": 10,
    "Negative": -2
}

# Score input form
st.subheader("🏅 Add Score")
team_names = {t['name']: tid for tid, t in teams.items()}
selected_team = st.selectbox("Select Team", list(team_names.keys()))
team_id = team_names[selected_team]

team_members = {mid: m for mid, m in members.items() if m['team_id'] == team_id}
member_names = {m['name']: mid for mid, m in team_members.items()}
selected_member = st.selectbox("Select Member", list(member_names.keys()))
member_id = member_names[selected_member]

selected_category = st.selectbox("Select Score Category", list(CATEGORIES.keys()))
points = CATEGORIES[selected_category]

if st.button("✅ Submit Score"):
    members[member_id]['score'] += points
    teams[team_id]['score'] += points if points > 0 else 0
    save_json(MEMBER_FILE, members)
    save_json(TEAM_FILE, teams)
    save_to_excel(teams, members)
    st.success(f"{selected_category} score of {points} added to {members[member_id]['name']}!")

st.subheader("🎖️ Team Members")
for m in team_members.values():
    st.write(f"{m['name']}: {m['score']} pts")

# Leaderboard
st.markdown("---")
st.subheader("📊 Leaderboards")

st.subheader("🏆 Team Leaderboard")
sorted_teams = sorted(teams.items(), key=lambda x: x[1]['score'], reverse=True)
for i, (tid, t) in enumerate(sorted_teams, 1):
    st.markdown(f"**{i}. {t['name']}** — {t['score']} points")

st.subheader("👑 Individual Leaderboard")
sorted_members = sorted(members.items(), key=lambda x: x[1]['score'], reverse=True)
for i, (mid, m) in enumerate(sorted_members, 1):
    tname = teams[m['team_id']]['name']
    st.markdown(f"**{i}. {m['name']}** (Team {tname}) — {m['score']} points")