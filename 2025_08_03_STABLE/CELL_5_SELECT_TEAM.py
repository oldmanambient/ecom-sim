# --- select team

import gradio as gr
import pandas as pd
import requests
from io import StringIO
import random

# --- Constants ---
ASSET_BASE = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/"
TEAM_CSV_URL = ASSET_BASE + "team_roles.csv"
IMG_HR = ASSET_BASE + "HRMON.png"
IMG_BANKER = ASSET_BASE + "banker.png"

# --- Load Roles ---
def load_roles():
    response = requests.get(TEAM_CSV_URL)
    return pd.read_csv(StringIO(response.text))

roles_df = load_roles()

# --- Session Defaults ---
session_state.setdefault("initial_budget", 100000)
session_state.setdefault("team_selections", {})
session_state.setdefault("banker_called_round0", False)
session_state.setdefault("board_toughness", 0)

# --- Cost + Display Helpers ---
def calculate_costs():
    total_cost = 0
    for _, row in roles_df.iterrows():
        role = row["ROLE"]
        count = session_state["team_selections"].get(role, 0)
        cost = row["MONTHLY_COST"]
        total_cost += count * cost
    return total_cost

def render_budget_text():
    monthly_budget = session_state["initial_budget"] // 12
    used = calculate_costs()
    remaining = max(monthly_budget - used, 0)
    return f"💼 Monthly Budget: £{monthly_budget:,} | ✅ Used: £{used:,} | 💰 Remaining: £{remaining:,}"

# --- UI ---
with gr.Blocks() as team_ui:
    gr.Markdown("## 👥 Step 3: Build Your Team")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(value=IMG_HR, show_label=False, width=96)
        with gr.Column(scale=4):
            gr.Markdown(
                "You can hire team members using your <b>monthly budget</b> (startup budget ÷ 12).<br>"
                "Adjust the number of hires per role. Stay within budget to avoid penalties."
            )

    gr.Markdown("---")
    gr.Markdown("### 🧑‍💼 Team Roles")

    budget_display = gr.Markdown(render_budget_text())
    count_displays = {}

    for _, row in roles_df.iterrows():
        role = row["ROLE"]
        cost = row["MONTHLY_COST"]
        session_state["team_selections"].setdefault(role, 0)

        with gr.Row():
            gr.Markdown(f"**{role}**<br>£{cost:,}/mo")
            count_display = gr.Markdown(f"<center>{session_state['team_selections'][role]}</center>")
            count_displays[role] = count_display

            plus_btn = gr.Button("➕")
            minus_btn = gr.Button("➖")

            def make_add_fn(r=role):
                def inner():
                    cost_per_role = roles_df.loc[roles_df["ROLE"] == r, "MONTHLY_COST"].values[0]
                    current_total = calculate_costs()
                    monthly_budget = session_state["initial_budget"] // 12

                    if current_total + cost_per_role > monthly_budget:
                        return render_budget_text() + "<br><span style='color:red;'>❌ Cannot add — over monthly budget!</span>", f"<center>{session_state['team_selections'][r]}</center>"

                    session_state["team_selections"][r] += 1
                    return render_budget_text(), f"<center>{session_state['team_selections'][r]}</center>"
                return inner

            def make_remove_fn(r=role):
                def inner():
                    if session_state["team_selections"][r] > 0:
                        session_state["team_selections"][r] -= 1
                    return render_budget_text(), f"<center>{session_state['team_selections'][r]}</center>"
                return inner

            plus_btn.click(fn=make_add_fn(role), outputs=[budget_display, count_display])
            minus_btn.click(fn=make_remove_fn(role), outputs=[budget_display, count_display])

    gr.Markdown("---")

    # ✅ Confirm Team Button and Display
    confirm_output = gr.Markdown(visible=False)

    def confirm_team():
        selections = session_state.get("team_selections", {})
        selected_team = {role: count for role, count in selections.items() if count > 0}
        total_cost = calculate_costs()
        monthly_budget = session_state["initial_budget"] // 12
        remaining = max(monthly_budget - total_cost, 0)

        session_state["team"] = selected_team
        session_state["monthly_team_cost"] = total_cost
        session_state["net_monthly_budget_remaining"] = remaining

        return gr.update(value=f"✅ Initial Team Locked In — Remaining Budget: £{remaining:,}", visible=True)

    gr.Button("✅ Confirm Team").click(fn=confirm_team, outputs=[confirm_output])

    gr.Markdown("### 💰 Need More Budget?")

    banker_btn = gr.Button("📞 Call the Banker")
    banker_dialog = gr.HTML(visible=False)
    banker_img = gr.Image(value=IMG_BANKER, width=64, show_label=False, visible=False)
    accept_offer = gr.Button("✅ Accept Banker Offer", visible=True)

    def summon_the_banker():
        if session_state.get("banker_called_round0", False):
            return gr.update(value="❌ You already used the banker this round, maybe next round...", visible=True), gr.update(visible=True)

        current_budget = session_state["initial_budget"]
        reroll_amount = random.randint(int(current_budget * 0.25), int(current_budget * 2.5))
        session_state["pending_offer"] = reroll_amount
        dialog = f"💸 Banker Offer:<br>I'm willing to offer you £{reroll_amount:,} in additional funding.<br><br>But remember... for every extra £1,000, the board gets tougher.<br><br>Do you accept?"
        return gr.update(value=dialog, visible=True), gr.update(visible=True)

    def accept_banker_offer():
        offer = session_state.get("pending_offer", 0)
        session_state["initial_budget"] += offer
        session_state["board_toughness"] += offer // 1000
        session_state["banker_called_round0"] = True
        monthly = session_state["initial_budget"] // 12
        dialog = f"✅ You accepted £{offer:,}.<br>📈 Board Toughness +{offer//1000}<br>💰 New Total Budget: £{session_state['initial_budget']:,}<br>📆 New Monthly Budget: £{monthly:,}"
        return gr.update(value=dialog, visible=True), gr.update(visible=True)

    banker_btn.click(fn=summon_the_banker, inputs=[], outputs=[banker_dialog, banker_img])
    accept_offer.click(fn=accept_banker_offer, inputs=[], outputs=[banker_dialog, banker_img])

    gr.Markdown("""
    <style>
    button {
        min-width: 60px !important;
        max-width: 100px;
    }
    </style>
    """)

team_ui.launch()
