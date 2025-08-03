# 🛍️ Cell 6 — Product Category Selection + Optional Market Research (Hard Limit 2 Categories)

import gradio as gr
import random

# --- Constants ---
IMG_PRODUCT = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/product_price.png"
ALL_CATEGORIES = [
    "Apparel", "Footwear", "Accessories", "Beauty", "Homeware", "Fitness",
    "Tech Gadgets", "Kitchen", "Pets", "Toys", "Stationery", "Automotive",
    "Garden", "Travel", "Music", "Gaming", "Books", "Health", "Food & Drink", "Baby"
]

# --- Generate categories based on seed ---
def get_available_categories():
    seed = session_state.get("world", {}).get("seed", "default")
    random.seed(seed)
    return random.sample(ALL_CATEGORIES, 8)

# --- Generate market potential per category based on seed ---
def get_market_data(categories):
    seed = session_state.get("world", {}).get("seed", "default")
    potentials = {}
    for cat in categories:
        combined_seed = seed + cat
        random.seed(combined_seed)
        potentials[cat] = random.randint(30, 95)
    return potentials

# --- Handle market research purchase ---
def purchase_research(_):
    current_budget = session_state.get("initial_budget", 60000)
    if session_state.get("research_purchased", False):
        return (
            "🧠 Market research already purchased.",
            gr.update(visible=True),
            gr.update(visible=False)
        )
    if current_budget < 5000:
        return (
            "❌ Not enough budget to purchase research.",
            gr.update(visible=False),
            gr.update(visible=False)
        )

    session_state["initial_budget"] -= 5000
    session_state["research_purchased"] = True

    # Recalculate net monthly budget
    monthly_total = session_state["initial_budget"] // 12
    net_remaining = monthly_total - session_state.get("monthly_team_cost", 0) - session_state.get("platform_opex", 0)
    session_state["net_monthly_budget_remaining"] = net_remaining

    return (
        "✅ Research purchased! Market potential unlocked below.",
        gr.update(visible=True),
        gr.update(visible=False)
    )

# --- Confirm categories (safe fallback) ---
def confirm_categories(selected):
    if not selected or len(selected) != 2:
        return "❌ You must select exactly 2 product categories.", gr.update(visible=False)

    session_state["product_categories"] = selected
    return (
        f"✅ Categories confirmed: <b>{selected[0]}</b> and <b>{selected[1]}</b>.",
        gr.update(visible=True)
    )

# --- Enforce limit on selection live ---
def enforce_two_limit(selected):
    if len(selected) <= 2:
        return selected, ""
    else:
        limited = selected[:2]
        return limited, "⚠️ Only 2 categories allowed. Extra selections removed."

# --- Start UI ---
available_categories = get_available_categories()
market_potentials = get_market_data(available_categories)

with gr.Blocks() as product_ui:
    gr.Markdown("## 🧬 Step 4: Choose Your Product Categories")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(value=IMG_PRODUCT, width=96, show_label=False, show_download_button=False)

        with gr.Column(scale=4):
            gr.Markdown("Before choosing your product categories, you may optionally purchase **market research** for £5,000 to see potential demand.")
            budget_display = gr.Markdown(f"💼 Total Budget: £{session_state['initial_budget']:,}")
            monthly_display = gr.Markdown(f"📆 Net Monthly Budget Remaining: £{session_state['net_monthly_budget_remaining']:,}")

    gr.Markdown("---")

    research_btn = gr.Button("📊 Purchase Market Research (£5,000)")
    research_status = gr.Markdown("")
    research_table = gr.HTML(visible=False)

    def reveal_market_data():
        rows = []
        for cat in available_categories:
            rows.append(f"<tr><td>{cat}</td><td>{market_potentials[cat]}%</td></tr>")
        table = "<table><tr><th>Category</th><th>Market Potential</th></tr>" + "".join(rows) + "</table>"
        return gr.update(value=table, visible=True)

    research_btn.click(fn=purchase_research, inputs=[research_btn], outputs=[research_status, research_table, research_btn])
    research_btn.click(fn=reveal_market_data, outputs=[research_table])

    gr.Markdown("---")

    category_select = gr.CheckboxGroup(
        label="🛒 Select 2 Categories (blind if no research)",
        choices=available_categories
    )
    warning_note = gr.Markdown("", visible=False)

    def update_checkboxes(selected):
        limited, msg = enforce_two_limit(selected)
        return gr.update(value=limited), gr.update(value=msg, visible=bool(msg))

    category_select.change(fn=update_checkboxes, inputs=[category_select], outputs=[category_select, warning_note])

    confirm_btn = gr.Button("✅ Confirm Categories")
    feedback = gr.Markdown("")
    next_note = gr.Markdown("📦 Categories locked. You're ready to set pricing & margin!", visible=False)

    confirm_btn.click(fn=confirm_categories, inputs=[category_select], outputs=[feedback, next_note])

product_ui.launch()