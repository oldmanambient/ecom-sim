# 🌍 Cell 2 — Phase 1: Generate Your Sandbox (with GitHub-hosted world image)

def generate_world(seed):
    seed_int = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % (10 ** 8)
    random.seed(seed_int)

    population = random.randint(20_000_000, 150_000_000)
    buyer_pct = round(random.uniform(0.45, 0.75), 2)
    avg_income = random.randint(20000, 60000)
    regions = random.sample([
        "Northland", "Coastia", "Hintermark", "Urbanis", "Midreach", "Sunmere", "Eastmark", "Zephyr Bay"
    ], 3)

    return {
        "seed": seed,
        "population": population,
        "buyer_count": int(population * buyer_pct),
        "avg_income": avg_income,
        "regions": regions,
    }

def sandbox_step(seed, _):
    world = generate_world(seed)
    session_state["world"] = world

    info = (
        f"<b>Seed:</b> {seed}<br>"
        f"<b>Population:</b> {world['population']:,}<br>"
        f"<b>Estimated Buyers:</b> {world['buyer_count']:,}<br>"
        f"<b>Avg Income:</b> £{world['avg_income']:,}<br>"
        f"<b>Regions:</b> {', '.join(world['regions'])}<br><br>"
        "<i>🔒 Persona and category data hidden — purchase market research to unlock.</i>"
    )
    return info, gr.update(visible=True)

def accept_sandbox():
    return "✅ Sandbox accepted. Ready to set your budget.", gr.update(visible=True)

# --- Build UI ---
with gr.Blocks() as demo:
    gr.Markdown("## 🌍 Generate Your Sandbox")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image(value=IMG_WORLD, label="Your World", width=256)

        with gr.Column(scale=2):
            seed_dropdown = gr.Dropdown(
                choices=sorted(artist_seeds),
                value="Prince",
                label="🎵 Choose a Seed"
            )
            regen_btn = gr.Button("🔁 Regenerate")
            sandbox_info = gr.HTML()
            accept_btn = gr.Button("✅ Accept Sandbox")
            next_step_note = gr.Markdown(visible=False)

            regen_btn.click(fn=sandbox_step, inputs=[seed_dropdown, regen_btn], outputs=[sandbox_info, accept_btn])
            seed_dropdown.change(fn=sandbox_step, inputs=[seed_dropdown, regen_btn], outputs=[sandbox_info, accept_btn])
            accept_btn.click(fn=accept_sandbox, inputs=None, outputs=[next_step_note, accept_btn])

    gr.Markdown("<hr>")

demo.launch()