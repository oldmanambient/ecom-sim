# 💸 Cell 7 — Pricing, Margin & Sensitivity + Summary

import gradio as gr

IMG_PRODUCT = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/product_price.png"
selected_categories = session_state.get("product_categories", [])

def calculate_pricing(margin, markup):
    try:
        cost = round(margin / (markup / 100), 2)
        price = round(cost + margin, 2)
        return cost, price
    except:
        return 0.0, 0.0

# Save logic + build summary
def save_pricing_and_show_summary(*args):
    pricing_data = {}
    summary_html = "<b>Pricing Summary</b><br><table><tr><th>Category</th><th>Avg Price (£)</th><th>Margin %</th><th>Margin £</th></tr>"

    for i, cat in enumerate(selected_categories):
        margin = args[i * 3]
        markup = args[i * 3 + 1]
        sensitivity = args[i * 3 + 2]
        cost, price = calculate_pricing(margin, markup)
        margin_pct = round((margin / price) * 100, 1) if price > 0 else 0.0

        pricing_data[cat] = {
            "margin": margin,
            "markup_percent": markup,
            "cost": cost,
            "price": price,
            "sensitivity": sensitivity
        }

        summary_html += f"<tr><td>{cat}</td><td>£{price:,.2f}</td><td>{margin_pct:.1f}%</td><td>£{margin:,.2f}</td></tr>"

    summary_html += "</table>"

    session_state["pricing"] = pricing_data
    return "✅ Pricing and sensitivity saved!", gr.update(value=summary_html, visible=True)

# --- UI ---
with gr.Blocks() as pricing_ui:
    gr.Markdown("## 💸 Step 5: Set Target Margin, Pricing, and Sensitivity")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(value=IMG_PRODUCT, width=96, show_label=False, show_download_button=False)
        with gr.Column(scale=4):
            gr.Markdown(
                "For each product category, set:<br>"
                "- Your <b>target margin per item</b><br>"
                "- Your <b>markup %</b><br>"
                "- The category's <b>price sensitivity</b><br><br>"
                "We'll calculate your cost and selling price automatically.")

    gr.Markdown("---")

    inputs = []
    outputs = []

    for cat in selected_categories:
        gr.Markdown(f"### {cat}")
        with gr.Row():
            margin_input = gr.Number(label="Target Margin (£)", value=20)
            markup_input = gr.Number(label="Markup %", value=100)
            sensitivity_slider = gr.Slider(label="Price Sensitivity (0–100)", minimum=0, maximum=100, value=50)
        with gr.Row():
            cost_output = gr.Number(label="Cost Price (£)", interactive=False)
            price_output = gr.Number(label="Selling Price (£)", interactive=False)

        def make_updater():
            def updater(margin, markup):
                return calculate_pricing(margin, markup)
            return updater

        updater_fn = make_updater()
        margin_input.change(fn=updater_fn, inputs=[margin_input, markup_input], outputs=[cost_output, price_output])
        markup_input.change(fn=updater_fn, inputs=[margin_input, markup_input], outputs=[cost_output, price_output])

        inputs.extend([margin_input, markup_input, sensitivity_slider])
        outputs.extend([cost_output, price_output])

    save_btn = gr.Button("✅ Save Pricing & Sensitivity")
    save_status = gr.Markdown("")
    summary_table = gr.HTML(visible=False)

    save_btn.click(fn=save_pricing_and_show_summary, inputs=inputs, outputs=[save_status, summary_table])

pricing_ui.launch()