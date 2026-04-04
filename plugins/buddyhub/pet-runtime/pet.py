#!/usr/bin/env python3
"""Claude Code Desktop Pet - A pixel cat that reacts to Claude's state.

Usage:
    python3 ~/.claude/pet/pet.py

Requires: pip install Pillow
"""

import json
import os
import sys
import time
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageTk

# Add script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from sprites import PALETTE, PIXEL_SIZE, SPRITES

STATE_FILE = Path.home() / ".claude" / "pet" / "state.json"
PROJECTS_DIR = Path.home() / ".claude" / "projects"
FRAME_DELAY = 300
STATE_POLL = 500
IDENTITY_POLL = 10000
IDLE_TIMEOUT = 30
SPRITE_SIZE = 16
CANVAS_SIZE = SPRITE_SIZE * PIXEL_SIZE  # 64px
PADDING = 12
WINDOW_SIZE = CANVAS_SIZE + PADDING * 2  # 88px
BG_COLOR = "#1e1e2e"
LABEL_COLOR = "#cdd6f4"
BUBBLE_BG = "#313244"
BUBBLE_TEXT = "#f5e0dc"
SPECIES_ACCENTS = {
    "blob": "#f38ba8",
}

STATE_LABELS = {
    "idle": "zzZ",
    "waking": "hello!",
    "listening": "listening",
    "thinking": "thinking...",
    "coffee": "coffee",
    "coding": "coding!",
    "debugging": "debugging",
    "reading": "reading",
    "studying": "studying",
    "running": "running...",
    "browsing": "browsing",
    "researching": "researching",
    "waiting": "meow?",
    "exploring": "exploring",
    "error": "!!!",
    "done": "done~",
    "celebrating": "yay!",
    "sleeping": "nap time",
    "clicked": "!",
    "dragged": "~>_<~",
    "petted": "<3",
}

STATE_BUBBLES = {
    "idle": "resting quietly",
    "waking": "hello there",
    "listening": "listening closely",
    "thinking": "thinking...",
    "coffee": "coffee break",
    "coding": "making changes",
    "debugging": "debugging",
    "reading": "reading",
    "studying": "studying code",
    "running": "running",
    "browsing": "browsing",
    "researching": "researching",
    "waiting": "waiting on you",
    "exploring": "exploring",
    "error": "something's wrong",
    "done": "done!",
    "celebrating": "nice work!",
    "sleeping": "nap time",
}


class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Claude Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg=BG_COLOR)
        self.root.attributes("-alpha", 0.93)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - WINDOW_SIZE - 30
        y = sh - WINDOW_SIZE - 60
        total_h = WINDOW_SIZE + 64  # bubble + status + identity labels
        self.root.geometry(f"{WINDOW_SIZE}x{total_h}+{x}+{y}")

        # Main frame
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.bubble_label = tk.Label(
            self.frame,
            text="resting quietly",
            fg=BUBBLE_TEXT,
            bg=BUBBLE_BG,
            font=("Menlo", 9),
            padx=8,
            pady=3,
        )
        self.bubble_label.pack(pady=(PADDING - 6, 2))

        self.canvas = tk.Canvas(
            self.frame, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.pack(pady=(0, 2))

        self.label = tk.Label(
            self.frame, text="zzZ", fg=LABEL_COLOR, bg=BG_COLOR,
            font=("Menlo", 10)
        )
        self.label.pack()

        self.identity_label = tk.Label(
            self.frame, text="", fg=LABEL_COLOR, bg=BG_COLOR,
            font=("Menlo", 9)
        )
        self.identity_label.pack(pady=(0, 4))

        # State
        self.state = "idle"
        self.activity = ""
        self.buddy_name = "Buddy"
        self.buddy_species = ""
        self.frame_idx = 0
        self.last_event_time = time.time()
        self.current_image = None
        self.interaction_state = None
        self.interaction_until = 0
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        self.bubble_text = "resting quietly"

        # Bind mouse events on all widgets
        for w in (self.canvas, self.label, self.identity_label, self.bubble_label, self.frame):
            w.bind("<Enter>", self.on_hover)
            w.bind("<Button-1>", self.on_click)
            w.bind("<B1-Motion>", self.on_drag)
            w.bind("<ButtonRelease-1>", self.on_drop)
            w.bind("<Double-Button-1>", self.on_double_click)
            w.bind("<Button-2>", self.on_right_click)
            w.bind("<Control-Button-1>", self.on_right_click)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="About Claude Pet", command=self.show_about)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.root.quit)

        self.refresh_identity()
        self.animate()
        self.poll_state()
        self.poll_identity()

    def render_frame(self, sprite_data, active_state):
        img = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (30, 30, 46, 255))
        pixels = img.load()
        for row_i, row in enumerate(sprite_data):
            for col_i, ch in enumerate(row):
                color = PALETTE.get(ch)
                if color is None:
                    continue
                for dy in range(PIXEL_SIZE):
                    for dx in range(PIXEL_SIZE):
                        px = col_i * PIXEL_SIZE + dx
                        py = row_i * PIXEL_SIZE + dy
                        if px < CANVAS_SIZE and py < CANVAS_SIZE:
                            pixels[px, py] = (*color, 255)
        self.decorate_frame(img, active_state)
        return ImageTk.PhotoImage(img)

    def decorate_frame(self, img, active_state):
        draw = ImageDraw.Draw(img, "RGBA")
        accent = self.hex_to_rgba(self.get_species_accent(), 210)
        if self.buddy_species == "blob":
            self.draw_blob_orb(draw, 7, CANVAS_SIZE - 10, 5, accent)
            self.draw_blob_orb(draw, CANVAS_SIZE - 10, CANVAS_SIZE - 14, 4, accent)
            self.draw_blob_orb(draw, CANVAS_SIZE - 16, 8, 3, self.hex_to_rgba(self.get_species_accent(), 160))
        self.draw_state_badge(draw, active_state)

    def draw_blob_orb(self, draw, x, y, radius, color):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
        draw.ellipse((x - radius + 2, y - radius + 2, x - radius + 4, y - radius + 4), fill=(255, 255, 255, 90))

    def draw_state_badge(self, draw, active_state):
        badge = self.badge_for_state(active_state)
        if not badge:
            return
        accent = self.hex_to_rgba(self.get_species_accent(), 255)
        x0, y0, x1, y1 = CANVAS_SIZE - 20, 4, CANVAS_SIZE - 4, 18
        draw.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=(49, 50, 68, 230), outline=accent, width=1)
        draw.text((x0 + 5, y0 + 2), badge, fill=(245, 224, 220, 255))

    def badge_for_state(self, active_state):
        badges = {
            "idle": "Z",
            "sleeping": "Z",
            "waking": "!",
            "listening": "?",
            "thinking": ".",
            "coffee": "C",
            "coding": ">",
            "debugging": "!",
            "reading": "B",
            "studying": "B",
            "researching": "B",
            "running": ">",
            "browsing": "B",
            "waiting": "?",
            "exploring": "*",
            "error": "X",
            "done": "+",
            "celebrating": "+",
        }
        return badges.get(active_state, "")

    def hex_to_rgba(self, color_hex, alpha):
        color_hex = color_hex.lstrip("#")
        return (
            int(color_hex[0:2], 16),
            int(color_hex[2:4], 16),
            int(color_hex[4:6], 16),
            alpha,
        )

    def get_active_state(self):
        if self.interaction_state and time.time() < self.interaction_until:
            return self.interaction_state
        self.interaction_state = None
        return self.state

    def animate(self):
        active = self.get_active_state()
        frames = SPRITES.get(active, SPRITES["idle"])
        if not frames:
            frames = SPRITES["idle"]
        self.frame_idx = self.frame_idx % len(frames)
        self.current_image = self.render_frame(frames[self.frame_idx], active)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
        label = self.activity if active == self.state and self.activity else STATE_LABELS.get(active, "")
        if len(label) > 12:
            label = label[:11] + "..."
        self.label.config(text=label)
        bubble = self.get_bubble_text(active)
        self.bubble_label.config(text=bubble, fg=BUBBLE_TEXT, bg=BUBBLE_BG)
        identity = self.buddy_name
        if self.buddy_species:
            identity = f"{identity} · {self.buddy_species}"
        self.identity_label.config(text=identity, fg=self.get_species_accent())
        self.frame_idx += 1
        self.root.after(FRAME_DELAY, self.animate)

    def poll_state(self):
        try:
            if STATE_FILE.exists():
                data = json.loads(STATE_FILE.read_text())
                new_state = data.get("state", "idle")
                if new_state != self.state:
                    self.state = new_state
                    self.frame_idx = 0
                self.activity = data.get("activity", "")
                self.last_event_time = data.get("timestamp", time.time())
        except (json.JSONDecodeError, OSError):
            pass
        if time.time() - self.last_event_time > IDLE_TIMEOUT:
            if self.state != "idle":
                self.state = "idle"
                self.activity = ""
                self.frame_idx = 0
        self.root.after(STATE_POLL, self.poll_state)

    def refresh_identity(self):
        latest_ts = ""
        latest_name = self.buddy_name
        latest_species = self.buddy_species
        try:
            files = sorted(
                PROJECTS_DIR.rglob("*.jsonl"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[:20]
        except OSError:
            files = []

        for path in files:
            try:
                for line in path.read_text().splitlines():
                    if '"companion_intro"' not in line:
                        continue
                    payload = json.loads(line)
                    attachment = payload.get("attachment", {})
                    if attachment.get("type") != "companion_intro":
                        continue
                    ts = payload.get("timestamp", "")
                    if ts >= latest_ts:
                        latest_ts = ts
                        latest_name = attachment.get("name") or latest_name
                        latest_species = attachment.get("species") or latest_species
            except (OSError, json.JSONDecodeError):
                continue

        self.buddy_name = latest_name or "Buddy"
        self.buddy_species = latest_species
        self.root.title(f"Claude Pet - {self.buddy_name}")

    def get_species_accent(self):
        return SPECIES_ACCENTS.get(self.buddy_species, LABEL_COLOR)

    def get_bubble_text(self, active_state):
        if active_state == self.state and self.activity:
            bubble = self.activity
        else:
            bubble = STATE_BUBBLES.get(active_state, STATE_LABELS.get(active_state, ""))
        if len(bubble) > 20:
            bubble = bubble[:19] + "..."
        return bubble

    def poll_identity(self):
        self.refresh_identity()
        self.root.after(IDENTITY_POLL, self.poll_identity)

    # ── Mouse interactions ──

    def set_temp_state(self, state, duration=1.5):
        self.interaction_state = state
        self.interaction_until = time.time() + duration
        self.frame_idx = 0

    def on_hover(self, event):
        if not self.drag_data["dragging"]:
            self.set_temp_state("waiting", 2.0)

    def on_click(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.set_temp_state("clicked", 0.8)
        os.system("afplay /System/Library/Sounds/Pop.aiff &")

    def on_double_click(self, event):
        self.set_temp_state("petted", 2.0)

    def on_drag(self, event):
        self.drag_data["dragging"] = True
        self.interaction_state = "dragged"
        self.interaction_until = time.time() + 10
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")

    def on_drop(self, event):
        if self.drag_data["dragging"]:
            self.drag_data["dragging"] = False
            self.set_temp_state("clicked", 0.5)

    def on_right_click(self, event):
        self.menu.post(event.x_root, event.y_root)

    def show_about(self):
        import tkinter.messagebox as mb
        species = f"\nSpecies: {self.buddy_species}" if self.buddy_species else ""
        mb.showinfo(
            "Claude Pet",
            f"Claude Code Desktop Pet\nBuddy: {self.buddy_name}{species}\nYour coding companion cat!",
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    pet = DesktopPet()
    pet.run()
