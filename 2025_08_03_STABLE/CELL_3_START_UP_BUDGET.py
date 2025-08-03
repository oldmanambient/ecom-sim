# 💰 Cell 3 — Phase 2: Set Your Start-Up Budget (with banker character)

def generate_budget(_):
    if "budget_rolls_remaining" not in session_state:
        session_state["budget_rolls_remaining"] = 3

    remaining = session_state["budget_rolls_remaining"]

    if remaining == 0:
        locked_budget = session_state["initial_budget"]
        return (
            f"<b>🎯 Budget Locked:</b> £{locked_budget:,.0f} (no more rolls)",
            gr.update(visible=True),
            f"🎲 Rolls remaining: 0 (locked)"
        )

    # Roll a new budget
    new_budget = random.randint(1000, 100000)
    session_state["initial_budget"] = new_budget
    session_state["budget_rolls_remaining"] -= 1
    remaining_after = session_state["budget_rolls_remaining"]

    return (
        f"<b>💰 Your Starting Budget:</b> £{new_budget:,.0f}",
        gr.update(visible=True),
        f"🎲 Rolls remaining: {remaining_after}"
    )

def confirm_budget():
    return "✅ Budget locked in. Proceed to platform selection.", gr.update(visible=True)

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("## 💰 Set Your Start-Up Budget")

    with gr.Row():
        # Column 1: Banker Profile (small)
        with gr.Column(scale=0.5):
            gr.Image(value=IMG_BANKER, width=64, show_label=False, show_download_button=False)

        # Column 2: Budget Controls
        with gr.Column(scale=2):
            budget_btn = gr.Button("🎲 Generate Budget")
            budget_display = gr.HTML()
            roll_counter = gr.Markdown("🎲 Rolls remaining: 3")
            confirm_btn = gr.Button("✅ Confirm Budget")
            next_note = gr.Markdown(visible=False)

            budget_btn.click(
                fn=generate_budget,
                inputs=[budget_btn],
                outputs=[budget_display, confirm_btn, roll_counter]
            )
            confirm_btn.click(fn=confirm_budget, inputs=None, outputs=[next_note, confirm_btn])

    gr.Markdown("<hr>")

demo.launch()