import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import subprocess
import webbrowser
import shutil
import sys
import json

ROOT_PATH = Path("/Users/antoniawinkler/Library/CloudStorage/OneDrive-UniversityofVirginia")
TEMPLATE_PATH = ROOT_PATH / "lumos/image-viewer/image_viewer_template.html"
OUTPUT_HTML = ROOT_PATH / "lumos/image-viewer/viewer_output.html"
IMAGE_OUTPUT_DIR = ROOT_PATH / "lumos/image-viewer/generated_images"



def create_html(image_dir):
    with open(TEMPLATE_PATH, "r") as f:
        html = f.read()

    image_dir = Path(image_dir).absolute()
    output_dir = Path(OUTPUT_HTML).parent

    images = sorted([p.name for p in image_dir.glob("*.png")])

    for img in images:
        src = image_dir / img
        dst = output_dir / img
        shutil.copy(src, dst)

    print("Copied images to:", output_dir)

  
    html = html.replace("IMAGE_FILES", json.dumps(images))
    html = html.replace("IMAGE_DIR/", "")

    with open(OUTPUT_HTML, "w") as f:
        f.write(html)

    return OUTPUT_HTML


def run_processing(config):
    project_dir = Path(__file__).parent
    script_path = project_dir / "12-remove-glucose.py"

    cmd = [
        sys.executable,
        str(script_path),

        "--pri_col", config["pri"],
        "--sub_col", config["sub"],
        "--oxy_col", config["oxy"],
        "--mode", config["mode"],
        "--expression", config["expression"],
        "--expression2", config["expression2"],
        "--out_dir", str(project_dir / "generated_images"),
    ]

    print("Running:", " ".join(cmd))
    print("Working Directory:", project_dir)

    subprocess.run(
        cmd,
        check=True,
        cwd=project_dir   # ✅ IMPORTANT
    )


# === UI ACTION ===
def run_pipeline():
    try:
        config = {
            "pri": pri_entry.get(),
            "sub": sub_entry.get(),
            "oxy": oxy_entry.get(),
            "mode": mode_var.get(),
            "expression": expr_entry.get(),
            "expression2": expr2_entry.get(),
        }

        # Clean output dir
        out_dir = Path(IMAGE_OUTPUT_DIR)
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True)

        # Run processing
        run_processing(config)

        # Create viewer
        import webbrowser
        project_dir = Path(__file__).parent
        dashboard_path = project_dir / "dashboard.html"
        webbrowser.open(f"file://{dashboard_path}")


        messagebox.showinfo("Done", "Processing complete!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# === GUI ===
root = tk.Tk()
root.title("Sensor Config + Image Viewer")

frame = ttk.Frame(root, padding=20)
frame.grid()

# Inputs
ttk.Label(frame, text="Primary Column:").grid(row=0, column=0)
pri_entry = ttk.Entry(frame)
pri_entry.insert(0, "1050led_910pd")
pri_entry.grid(row=0, column=1)

ttk.Label(frame, text="Subtract Column:").grid(row=1, column=0)
sub_entry = ttk.Entry(frame)
sub_entry.insert(0, "530led_480pd")
sub_entry.grid(row=1, column=1)

ttk.Label(frame, text="Oxygen Column:").grid(row=2, column=0)
oxy_entry = ttk.Entry(frame)
oxy_entry.insert(0, "660led_910pd")
oxy_entry.grid(row=2, column=1)


ttk.Label(frame, text="Signal Expression:").grid(row=3, column=0)
expr_entry = ttk.Entry(frame, width=20)
expr_entry.insert(0, "sub - pri")
expr_entry.grid(row=3, column=1)


# Second Expression
ttk.Label(frame, text="Second Expression:").grid(row=4, column=0)

expr2_entry = ttk.Entry(frame)
expr2_entry.insert(0, "")
expr2_entry.grid(row=4, column=1)



# Mode selection
mode_var = tk.StringVar(value="continuous")
ttk.Label(frame, text="Mode:").grid(row=5, column=0)

mode_combo = ttk.Combobox(
    frame,
    textvariable=mode_var,
    values=["continuous", "window"]
)
mode_combo.grid(row=5, column=1)

# Run button
run_button = ttk.Button(frame, text="Run Pipeline", command=run_pipeline)
run_button.grid(row=6, columnspan=2, pady=10)

root.mainloop()