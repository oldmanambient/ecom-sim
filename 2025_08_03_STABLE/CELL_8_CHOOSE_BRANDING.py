# ---Set Up Branding

import gradio as gr
import numpy as np
from PIL import Image

# Character image
IMG_COMPUTER = "https://raw.githubusercontent.com/oldmanambient/ecom-sim/main/computer.png"

# Web-safe palette
APPROVED_COLORS = {
    "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 128, 0),
    "orange": (255, 165, 0), "purple": (128, 0, 128), "grey": (128, 128, 128),
    "black": (0, 0, 0), "white": (255, 255, 255),
    "turquoise": (64, 224, 208), "indigo": (75, 0, 130)
}

# Syllables for brand name generation
SYLLABLES = ["zor", "tek", "ly", "vox", "neo", "quix", "zen", "tra", "lum", "cy"]

# Generate brand name options
def generate_brand_names():
    category = session_state.get("product_categories", ["item"])[0].lower()
    options = []
    rng = np.random.default_rng()
    for _ in range(5):
        name = "".join(rng.choice(SYLLABLES, size=2))
        options.append(f"{name.capitalize()}{category}.com")
    return options

# Save confirmed brand name
def confirm_brand(name):
    session_state["brand_name"] = name
    return f"✅ Brand name confirmed: {name}"

# Logo generation
def generate_logo_safe(seed=None):
    rng = np.random.default_rng(seed)
    bg_name = rng.choice(list(APPROVED_COLORS.keys()))
    fg_name = rng.choice([c for c in APPROVED_COLORS if c != bg_name])
    bg_color = APPROVED_COLORS[bg_name]
    fg_color = APPROVED_COLORS[fg_name]

    grid_size = 10
    cell_size = 10
    border = 2
    img_size = grid_size * cell_size + border * 2
    img = Image.new("RGB", (img_size, img_size), bg_color)

    for x in range(img_size):
        for y in range(img_size):
            if x < border or y < border or x >= img_size - border or y >= img_size - border:
                img.putpixel((x, y), fg_color)

    for y in range(grid_size):
        half_row = [rng.integers(0, 2) for _ in range(grid_size // 2)]
        full_row = half_row + half_row[::-1]
        for x, val in enumerate(full_row):
            if val:
                for dx in range(cell_size):
                    for dy in range(cell_size):
                        px = border + x * cell_size + dx
                        py = border + y * cell_size + dy
                        img.putpixel((px, py), fg_color)
    return img

# Setup session state
session_state["logo_set"] = [generate_logo_safe(seed=i) for i in range(5)]
session_state["confirmed_logo"] = None
session_state["brand_name"] = None

def regenerate_logos():
    new_logos = [generate_logo_safe(seed=i + np.random.randint(1000)) for i in range(5)]
    session_state["logo_set"] = new_logos
    return new_logos

def confirm_logo(index):
    idx = int(index)
    selected = session_state["logo_set"][idx]
    session_state["confirmed_logo"] = selected
    name = session_state.get("brand_name", "🚫 No brand name selected!")
    img_data = pil_to_base64(selected)

    summary_html = f"""
    <div style='display:flex; align-items:center; gap:20px;'>
        <div><h3>✅ Brand Summary</h3><b>{name}</b></div>
        <div><img src='data:image/png;base64,{img_data}' width='100'></div>
    </div>
    """

    return "✅ Logo confirmed!", selected, gr.update(value=summary_html, visible=True)


# Convert PIL image to base64 for embedding
import base64
from io import BytesIO
def pil_to_base64(pil_img):
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- UI ---
with gr.Blocks() as brand_ui:
    gr.Markdown("## 🧠 Step 6: Build Your Brand Identity")

    with gr.Row():
        with gr.Column(scale=0.5):
            gr.Image(value=IMG_COMPUTER, show_label=False, width=96)
        with gr.Column(scale=2):
            brand_opts = gr.Radio(choices=generate_brand_names(), label="Choose Your Brand Name")
            confirm_name_btn = gr.Button("✅ Confirm Brand Name")
            name_status = gr.Markdown()

    confirm_name_btn.click(fn=confirm_brand, inputs=brand_opts, outputs=name_status)

    gr.Markdown("---")
    gr.Markdown("## 🎨 Choose a Logo")

    with gr.Row():
        regen_btn = gr.Button("🔁 Regenerate Logos")
        logo_selector = gr.Radio(["0", "1", "2", "3", "4"], label="Select Logo")

    with gr.Row():
        img0 = gr.Image(value=session_state["logo_set"][0], show_label=False, width=100)
        img1 = gr.Image(value=session_state["logo_set"][1], show_label=False, width=100)
        img2 = gr.Image(value=session_state["logo_set"][2], show_label=False, width=100)
        img3 = gr.Image(value=session_state["logo_set"][3], show_label=False, width=100)
        img4 = gr.Image(value=session_state["logo_set"][4], show_label=False, width=100)

    def update_all():
        new_imgs = regenerate_logos()
        return tuple(new_imgs)

    regen_btn.click(fn=update_all, inputs=[], outputs=[img0, img1, img2, img3, img4])

    confirm_btn = gr.Button("✅ Confirm Logo")
    logo_status = gr.Markdown()
    confirmed_logo = gr.Image(visible=False)
    summary_text = gr.HTML(visible=False)


    confirm_btn.click(fn=confirm_logo, inputs=[logo_selector], outputs=[logo_status, confirmed_logo, summary_text])

brand_ui.launch()