# Cell 4 Select Platform

import gradio as gr
import pandas as pd
import requests
from io import StringIO

# --- Constants ---
ASSET_BASE = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/"
PLATFORM_CSV_URL = ASSET_BASE + "platforms.csv"
DEFAULT_LOGO = ASSET_BASE + "placeholder_logo.png"
IMG_TECH = ASSET_BASE + "tech.png"

# --- Session State ---
session_state.setdefault("initial_budget", 100000)
session_state.setdefault("platform_choice", None)
session_state.setdefault("preview_selection", None)

# --- Load Platform Data ---
def smart_read_csv(url):
    response = requests.get(url)
    return pd.read_csv(StringIO(response.text))

def validate_logo_url(filename):
    url = ASSET_BASE + filename
    try:
        if requests.head(url).status_code == 200:
            return url
    except:
        pass
    return DEFAULT_LOGO

platforms_df = smart_read_csv(PLATFORM_CSV_URL)

# --- Platform Summaries ---
summaries = {
    "TradeCloud": "Great for small brands with SaaS features. Monthly license.",
    "MegaShop OS": "Scales well, strong SEO. Fixed license.",
    "SimpleCart": "Quick setup for solo founders. Fixed monthly.",
    "HyperScaleX": "Enterprise-grade features. High upfront cost.",
    "ForgeEngine": "Modular & dev-friendly. License + optional hosting.",
    "FlexiShopper": "Built for WordPress users. Plugin model.",
    "PixelStore": "Creative-first, easy builder. Flat fee.",
    "ConnectCart": "Good SME support. Simple subscription.",
    "VisiMart": "Agency-led. Rev share + fixed.",
    "MinrCore": "Open core, no license. High setup cost. At your own RISK - with great power comes great rewards (sometimes)"
}

# --- Logic ---
def preview_selection(name):
    session_state["preview_selection"] = name
    row = platforms_df[platforms_df["Fictional Name"] == name]
    if row.empty:
        return f"❌ Unknown platform.", f"💰 Budget: £{session_state['initial_budget']:,}"

    cost = int(row.iloc[0]["Implementation Cost"])
    if cost > session_state["initial_budget"]:
        return f"❌ You can't afford {name}.", f"💰 Budget: £{session_state['initial_budget']:,}"

    return f"✅ You selected: {name}", f"💰 Budget after setup: £{session_state['initial_budget'] - cost:,}"

def confirm_selection():
    name = session_state.get("preview_selection")
    if not name:
        return "❌ No platform selected.", f"💰 Budget: £{session_state['initial_budget']:,}", gr.update(visible=False)

    row = platforms_df[platforms_df["Fictional Name"] == name]
    if row.empty:
        return "❌ Unknown platform.", f"💰 Budget: £{session_state['initial_budget']:,}", gr.update(visible=False)

    cost = int(row.iloc[0]["Implementation Cost"])
    if cost > session_state["initial_budget"]:
        return f"❌ You can't afford {name}. Choose another.", f"💰 Budget: £{session_state['initial_budget']:,}", gr.update(visible=False)

    session_state["initial_budget"] -= cost
    session_state["platform_choice"] = name
    final_msg = f"🎉 You selected **{name}**. You now have **£{session_state['initial_budget']:,}** available for hiring and operations!"
    return f"✅ Platform confirmed: {name}", f"💰 Remaining Budget: £{session_state['initial_budget']:,}", gr.update(value=final_msg, visible=True)

# --- UI ---
with gr.Blocks() as platform_ui:
    gr.Markdown("## 🧩 Step 2: Select Your Platform")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(IMG_TECH, show_label=False, width=128)
        with gr.Column(scale=5):
            budget_display = gr.Markdown(f"💰 Budget: £{session_state['initial_budget']:,}")

    gr.Markdown("---")
    selection_status = gr.Markdown("")

    with gr.Column():
        with gr.Row():
            gr.Markdown("Logo")
            gr.Markdown("Platform")
            gr.Markdown("Costs")
            gr.Markdown("Summary")
            gr.Markdown("Choose")

        for _, row in platforms_df.iterrows():
            name = row["Fictional Name"]
            logo = validate_logo_url(row["Logo File"])
            setup_cost = int(row["Implementation Cost"])
            monthly_type = row["Month Cost Type"]
            monthly_val = row["Monthly Cost Variable"]
            monthly_str = f"{monthly_val}% rev" if monthly_type == "variable" else f"£{monthly_val}/mo"
            summary = summaries.get(name, "No summary available.")

            with gr.Row():
                gr.Image(value=logo, show_label=False, width=50, height=50, container=False, interactive=False)
                gr.Markdown(f"<div style='text-align: center;'>{name}</div>")
                gr.Markdown(f"<div style='text-align: center;'>£{setup_cost:,} setup<br>{monthly_str}</div>")
                gr.Markdown(f"<div style='text-align: center;'>{summary}</div>")

                def make_click(name=name):
                    return lambda: preview_selection(name)

                btn = gr.Button(value="Select", size="sm")
                btn.click(fn=make_click(), inputs=[], outputs=[selection_status, budget_display])

    confirm_btn = gr.Button("✅ Confirm Platform")
    final_confirmation = gr.Markdown(visible=False)

    confirm_btn.click(
        fn=confirm_selection,
        inputs=[],
        outputs=[selection_status, budget_display, final_confirmation]
    )

    # Place confirmation message just below the confirm button
    with gr.Row():
        final_confirmation

platform_ui.launch()