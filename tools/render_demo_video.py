from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media"
BUILD = MEDIA / "demo_build"
OUT = MEDIA / "keeperhub-execution-receipt-demo-draft.mp4"
CONTACT = MEDIA / "keeperhub-execution-receipt-demo-draft-contact-sheet.jpg"
DEMO_JSON = ROOT / "examples" / "demo_output_mock.json"

W, H = 1920, 1080
BG = (12, 18, 28)
PANEL = (24, 33, 47)
PANEL_2 = (18, 25, 36)
TEXT = (237, 242, 247)
MUTED = (156, 170, 190)
GREEN = (39, 201, 128)
BLUE = (72, 149, 239)
AMBER = (245, 158, 11)
RED = (239, 68, 68)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_TITLE = font(74, True)
F_H1 = font(54, True)
F_H2 = font(36, True)
F_BODY = font(31)
F_SMALL = font(24)
F_CODE = font(25)
F_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 25)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            probe = f"{line} {word}"
            if draw.textbbox((0, 0), probe, font=fnt)[2] <= width:
                line = probe
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_block(draw, xy, text, fnt, fill=TEXT, width=780, line_gap=12):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def code_block(draw, box, lines):
    rounded(draw, box, PANEL_2, outline=(48, 63, 86), radius=14)
    x, y = box[0] + 28, box[1] + 24
    for line, color in lines:
        draw.text((x, y), line, font=F_MONO, fill=color)
        y += 38


def load_receipts():
    data = json.loads(DEMO_JSON.read_text(encoding="utf-8-sig"))
    return {r["scenario"]: r for r in data["receipts"]}


def base(title: str, kicker: str = "KeeperHub Execution Receipt Kit"):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 9), fill=GREEN)
    draw.text((88, 58), kicker, font=F_SMALL, fill=MUTED)
    draw.text((88, 100), title, font=F_H1, fill=TEXT)
    return img, draw


def slide_title():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, H), fill=BG)
    draw.ellipse((1350, -180, 2150, 620), fill=(20, 69, 76))
    draw.ellipse((-260, 650, 560, 1470), fill=(35, 51, 88))
    draw.text((110, 170), "KeeperHub", font=F_TITLE, fill=GREEN)
    draw.text((110, 260), "Execution Receipt Kit", font=F_TITLE, fill=TEXT)
    text_block(draw, (116, 390), "Policy-gated receipts for AI agents preparing onchain execution through KeeperHub.", F_BODY, MUTED, 980)
    rounded(draw, (116, 620, 980, 820), PANEL, outline=(48, 63, 86), radius=22)
    text_block(draw, (155, 665), "Status today: local prototype, mock evidence only. The final submission needs one approved KeeperHub run and tx hash.", F_BODY, TEXT, 760)
    draw.text((116, 925), "Draft demo generated locally. No wallet, login, or transaction was used.", font=F_SMALL, fill=MUTED)
    return img


def slide_problem():
    img, draw = base("The missing layer: proof around execution")
    text_block(draw, (95, 210), "Agent hackathons often show reasoning. KeeperHub Agents Onchain rewards the harder thing: real execution with evidence.", F_BODY, TEXT, 760)
    items = [
        ("intent", "What did the agent decide?"),
        ("policy", "Why was it allowed or blocked?"),
        ("request", "What KeeperHub workflow would run?"),
        ("evidence", "Which tx, run id, outcome, and audit trail came back?")
    ]
    x = 980
    for i, (label, body) in enumerate(items):
        y = 205 + i * 160
        rounded(draw, (x, y, 1760, y + 105), PANEL, outline=(48, 63, 86), radius=16)
        draw.text((x + 28, y + 18), label.upper(), font=F_SMALL, fill=GREEN if i < 3 else AMBER)
        draw.text((x + 28, y + 52), body, font=F_BODY, fill=TEXT)
    return img


def slide_architecture():
    img, draw = base("Receipt flow")
    stages = [
        ("1", "Agent intent", BLUE),
        ("2", "Policy gate", GREEN),
        ("3", "KeeperHub request", AMBER),
        ("4", "Execution evidence", TEXT),
    ]
    y = 360
    for idx, (num, label, color) in enumerate(stages):
        x = 120 + idx * 450
        rounded(draw, (x, y, x + 330, y + 150), PANEL, outline=color, width=3, radius=18)
        draw.text((x + 28, y + 30), num, font=F_H2, fill=color)
        draw.text((x + 85, y + 40), label, font=F_BODY, fill=TEXT)
        if idx < len(stages) - 1:
            draw.line((x + 340, y + 75, x + 430, y + 75), fill=MUTED, width=5)
            draw.polygon([(x + 430, y + 75), (x + 410, y + 62), (x + 410, y + 88)], fill=MUTED)
    text_block(draw, (135, 625), "The kit does not replace KeeperHub. It records the policy and audit trail around the moment an agent delegates an onchain action.", F_BODY, MUTED, 1520)
    return img


def slide_success(receipts):
    r = receipts["in_policy_yield_rebalance"]
    img, draw = base("Approved path: prepared execution")
    code_block(draw, (95, 225, 1000, 760), [
        ("intent: supply 18 USDC", TEXT),
        ("chain: base-sepolia", BLUE),
        ("destination: keeperhub-aave-v3-usdc-vault", TEXT),
        ("confidence: 8420 bps", GREEN),
        ("simulation: ok", GREEN),
        ("status: approved_for_prepared_execution", GREEN),
        (f"requestHash: {r['keeperHubRequestHash'][:26]}...", AMBER),
    ])
    text_block(draw, (1100, 250), "When every hard check passes, the kit emits a KeeperHub-ready request and a deterministic receipt.", F_BODY, TEXT, 620)
    text_block(draw, (1100, 500), "Current evidence is still mock-only. After approval, this is where the real KeeperHub run id and tx hash will be attached.", F_BODY, MUTED, 620)
    return img


def slide_blocks(receipts):
    img, draw = base("Unsafe requests fail closed")
    failures = [
        ("Over cap", "180 USDC > 25 USDC max", RED),
        ("Wrong destination", "unknown router is not approved", RED),
        ("Low confidence", "6100 bps < 7600 bps min", AMBER),
    ]
    for i, (title, body, color) in enumerate(failures):
        x = 120 + i * 580
        rounded(draw, (x, 270, x + 470, 620), PANEL, outline=color, width=3, radius=20)
        draw.text((x + 32, 315), title, font=F_H2, fill=color)
        text_block(draw, (x + 32, 385), body, F_BODY, TEXT, 380)
        draw.text((x + 32, 535), "No KeeperHub request emitted", font=F_SMALL, fill=MUTED)
    text_block(draw, (130, 760), "Fail-closed behavior is part of the product: blocked receipts are evidence too.", F_BODY, TEXT, 1480)
    return img


def slide_schema():
    img, draw = base("Receipt schema")
    code_block(draw, (110, 225, 1810, 820), [
        ('schema: "keeperhub.execution_receipt.v0"', TEXT),
        ("intentHash: sha256:...", BLUE),
        ("policyHash: sha256:...", BLUE),
        ("keeperHubRequestHash: sha256:...", AMBER),
        ("executionEvidence.current: local_mock_only", MUTED),
        ("executionEvidence.txHash: null", RED),
        ("nextRequired: attach real KeeperHub run id and tx hash", GREEN),
    ])
    return img


def slide_repo():
    img, draw = base("Public repo candidate")
    text_block(draw, (120, 230), "The public repository contains only sanitized prototype files: code, tests, examples, receipt schema, policy gate docs, and the KeeperHub integration runbook.", F_BODY, TEXT, 760)
    code_block(draw, (980, 225, 1775, 710), [
        ("README.md", GREEN),
        ("src/keeperhub_execution_receipt_agent.js", TEXT),
        ("test/keeperhub_execution_receipt_agent.test.js", TEXT),
        ("docs/receipt_schema.md", TEXT),
        ("docs/policy_gate.md", TEXT),
        ("docs/keeperhub_integration_runbook.md", TEXT),
        ("examples/demo_output_mock.json", TEXT),
    ])
    draw.text((120, 805), "No secrets. No wallet data. No fake transaction evidence.", font=F_BODY, fill=AMBER)
    return img


def slide_next():
    img, draw = base("Final proof path")
    steps = [
        ("User-assisted OAuth", "KeeperHub login happens in the user's browser."),
        ("One testnet run", "Execute exactly one low-risk transaction through KeeperHub."),
        ("Attach evidence", "workflow/run id, tx hash, chain, timestamp, outcome, audit URL."),
        ("Submit", "Repo, video, tx link, and honest limitations go into DoraHacks.")
    ]
    for i, (title, body) in enumerate(steps):
        y = 235 + i * 165
        rounded(draw, (160, y, 1760, y + 105), PANEL, outline=(48, 63, 86), radius=16)
        draw.text((200, y + 24), f"{i + 1}. {title}", font=F_H2, fill=GREEN if i != 1 else AMBER)
        draw.text((610, y + 32), body, font=F_BODY, fill=TEXT)
    return img


def slide_close():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.text((120, 180), "Execution is the claim.", font=F_TITLE, fill=TEXT)
    draw.text((120, 280), "The receipt is the proof.", font=F_TITLE, fill=GREEN)
    text_block(draw, (130, 440), "Current draft: KeeperHub-ready local prototype. Final target: one approved KeeperHub testnet run with real transaction evidence.", F_BODY, MUTED, 1200)
    rounded(draw, (130, 700, 1510, 830), PANEL, outline=AMBER, radius=18)
    draw.text((170, 742), "No real tx yet. Do not submit this draft as final proof.", font=F_H2, fill=AMBER)
    return img


def save_contact_sheet(paths: list[Path]):
    thumbs = []
    for path in paths:
        img = Image.open(path).resize((480, 270))
        thumbs.append(img)
    sheet = Image.new("RGB", (960, math.ceil(len(thumbs) / 2) * 310), (245, 247, 250))
    d = ImageDraw.Draw(sheet)
    for i, thumb in enumerate(thumbs):
        x = (i % 2) * 480
        y = (i // 2) * 310
        sheet.paste(thumb, (x, y))
        d.text((x + 12, y + 276), f"Slide {i + 1}", font=F_SMALL, fill=(30, 41, 59))
    sheet.save(CONTACT, quality=90)


def main():
    MEDIA.mkdir(exist_ok=True)
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()

    receipts = load_receipts()
    slides = [
        (slide_title(), 7),
        (slide_problem(), 8),
        (slide_architecture(), 8),
        (slide_success(receipts), 9),
        (slide_blocks(receipts), 9),
        (slide_schema(), 8),
        (slide_repo(), 8),
        (slide_next(), 9),
        (slide_close(), 7),
    ]

    paths = []
    for i, (img, _duration) in enumerate(slides, 1):
        path = BUILD / f"slide_{i:02d}.png"
        img.save(path)
        paths.append(path)
    save_contact_sheet(paths)

    concat = BUILD / "slides.txt"
    with concat.open("w", encoding="utf-8") as f:
        for path, (_img, duration) in zip(paths, slides):
            f.write(f"file '{path.as_posix()}'\n")
            f.write(f"duration {duration}\n")
        f.write(f"file '{paths[-1].as_posix()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-shortest",
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k",
        str(OUT),
    ]
    subprocess.run(cmd, check=True)
    print(OUT)
    print(CONTACT)


if __name__ == "__main__":
    main()
