from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media"
BUILD = MEDIA / "public_preview_build"
OUT = MEDIA / "keeperhub-execution-receipt-public-preview.mp4"
CONTACT = MEDIA / "keeperhub-execution-receipt-public-preview-contact-sheet.jpg"
DEMO_JSON = ROOT / "examples" / "demo_output_mock.json"

W, H, FPS = 1920, 1080, 30
BG = (9, 14, 24)
PANEL = (20, 29, 43)
PANEL_2 = (15, 23, 35)
LINE = (52, 68, 94)
TEXT = (238, 244, 250)
MUTED = (150, 164, 184)
GREEN = (44, 211, 142)
BLUE = (71, 154, 255)
AMBER = (245, 174, 57)
RED = (248, 82, 82)
PURPLE = (156, 124, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def mono(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except OSError:
        return font(size)


F_KICKER = font(24, True)
F_TITLE = font(76, True)
F_H1 = font(55, True)
F_H2 = font(38, True)
F_BODY = font(31)
F_SMALL = font(23)
F_TINY = font(19)
F_MONO = mono(24)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1, c2, t: float):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            probe = f"{line} {word}"
            if draw.textbbox((0, 0), probe, font=fnt)[2] <= max_width:
                line = probe
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill=TEXT, width=900, gap=10):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def text_in_box(draw, box, text, fnt, fill=TEXT, pad=34, gap=10):
    return text_block(
        draw,
        (box[0] + pad, box[1] + pad),
        text,
        fnt,
        fill,
        max(1, box[2] - box[0] - pad * 2),
        gap,
    )


def footer(draw, caption: str):
    draw.rectangle((0, H - 92, W, H), fill=(8, 12, 20))
    draw.text((86, H - 62), caption, font=F_SMALL, fill=TEXT)
    draw.text((1420, H - 62), "KEEPERHUB READ RUN / WRITE TX PENDING", font=F_TINY, fill=AMBER)


def header(draw, title: str, t: float):
    draw.rectangle((0, 0, W, 10), fill=mix(BLUE, GREEN, t))
    draw.text((86, 46), "KeeperHub Execution Receipt Kit", font=F_KICKER, fill=MUTED)
    draw.text((86, 86), title, font=F_H1, fill=TEXT)


def load_receipts():
    data = json.loads(DEMO_JSON.read_text(encoding="utf-8-sig"))
    return {r["scenario"]: r for r in data["receipts"]}


def code_panel(draw, box, lines):
    rounded(draw, box, PANEL_2, outline=LINE, radius=16)
    x, y = box[0] + 28, box[1] + 26
    for text, color in lines:
        draw.text((x, y), text, font=F_MONO, fill=color)
        y += 36


def scene_hook(img, draw, p, receipts):
    glow = int(60 + 70 * ease(p))
    draw.ellipse((1230, -240, 2150, 650), fill=(8, glow, 74))
    draw.ellipse((-320, 700, 620, 1580), fill=(23, 40, 82))
    draw.text((100, 155), "Can an agent", font=F_TITLE, fill=TEXT)
    draw.text((100, 250), "prove what it did", font=F_TITLE, fill=GREEN)
    draw.text((100, 345), "before and after KeeperHub?", font=F_TITLE, fill=TEXT)
    text_block(draw, (108, 500), "A public-preview demo for policy-gated execution receipts around AI agents delegating onchain actions to KeeperHub.", F_BODY, MUTED, 1060)
    status_box = (106, 700, 1180, 850)
    rounded(draw, status_box, PANEL, outline=AMBER, radius=18)
    text_in_box(draw, status_box, "Current status: KeeperHub MCP connected + read workflow run captured. Write tx pending.", F_BODY, AMBER, pad=40, gap=8)
    footer(draw, "This preview is honest by design: real read run, no fake transaction hash.")


def scene_evidence_first(img, draw, p, receipts):
    header(draw, "Evidence first", p)
    cards = [
        ("PUBLIC REPO", "github.com/kei99-web3/keeperhub-execution-receipt-kit", GREEN),
        ("TESTS", "keeperhub_execution_receipt_agent.test.js passed", BLUE),
        ("READ RUN", "wrun_01KWRFQK1EQG92MERS9N49G5W6 captured", PURPLE),
        ("WRITE TX", "pending user-attended testnet transaction", AMBER),
    ]
    for i, (label, value, color) in enumerate(cards):
        x = 115 + (i % 2) * 860
        y = 245 + (i // 2) * 245
        a = ease(max(0, min(1, p * 1.4 - i * 0.16)))
        rounded(draw, (x, int(y + 25 * (1 - a)), x + 760, int(y + 175 + 25 * (1 - a))), PANEL, outline=color, width=3, radius=18)
        draw.text((x + 30, int(y + 38 + 25 * (1 - a))), label, font=F_KICKER, fill=color)
        text_block(draw, (x + 30, int(y + 82 + 25 * (1 - a))), value, F_BODY, TEXT, 660)
    footer(draw, "Casper lesson applied: show proof and limits before the architecture.")


def scene_flow(img, draw, p, receipts):
    header(draw, "From intent to receipt", p)
    labels = [
        ("Agent intent", BLUE),
        ("Policy gate", GREEN),
        ("KeeperHub request", AMBER),
        ("Evidence receipt", PURPLE),
    ]
    y = 450
    for i, (label, color) in enumerate(labels):
        x = 115 + i * 440
        progress = ease(max(0, min(1, p * 1.8 - i * 0.22)))
        rounded(draw, (x, y, x + 315, y + 140), PANEL, outline=color, width=3, radius=18)
        draw.text((x + 28, y + 32), str(i + 1), font=F_H2, fill=color)
        text_block(draw, (x + 82, y + 36), label, F_BODY, TEXT, 210)
        if i < 3:
            line_end = x + 332 + int(82 * progress)
            draw.line((x + 320, y + 70, line_end, y + 70), fill=MUTED, width=5)
            if progress > 0.8:
                draw.polygon([(x + 415, y + 70), (x + 397, y + 58), (x + 397, y + 82)], fill=MUTED)
    text_block(draw, (130, 705), "KeeperHub handles execution. The kit records the policy and evidence around the delegation point.", F_BODY, MUTED, 1520)
    footer(draw, "The design goal is auditability, not replacing KeeperHub.")


def scene_approved(img, draw, p, receipts):
    header(draw, "Approved path", p)
    r = receipts["in_policy_yield_rebalance"]
    code_panel(draw, (105, 225, 1010, 740), [
        ("intent: supply 18 USDC", TEXT),
        ("chain: base-sepolia", BLUE),
        ("destination: keeperhub-aave-v3-usdc-vault", TEXT),
        ("confidence: 8420 bps", GREEN),
        ("simulation: ok", GREEN),
        ("status: approved_for_prepared_execution", GREEN),
        (f"requestHash: {r['keeperHubRequestHash'][:34]}...", AMBER),
    ])
    text_block(draw, (1100, 250), "When every hard check passes, the kit prepares a KeeperHub-ready request and a deterministic receipt.", F_BODY, TEXT, 650)
    rounded(draw, (1095, 530, 1765, 700), PANEL, outline=AMBER, radius=16)
    text_block(draw, (1130, 562), "txHash is still null here. That is intentional until a write transaction is completed.", F_BODY, AMBER, 590)
    footer(draw, "No fabricated evidence: tx hash remains null until a write run returns one.")


def scene_fail_closed(img, draw, p, receipts):
    header(draw, "Unsafe requests fail closed", p)
    failures = [
        ("OVER CAP", "180 USDC exceeds 25 USDC max", RED),
        ("WRONG DESTINATION", "unknown router is not approved", RED),
        ("LOW CONFIDENCE", "6100 bps below 7600 bps minimum", AMBER),
    ]
    for i, (label, body, color) in enumerate(failures):
        x = 120 + i * 575
        y = 305
        a = ease(max(0, min(1, p * 1.5 - i * 0.18)))
        rounded(draw, (x, int(y + 35 * (1 - a)), x + 455, int(y + 315 + 35 * (1 - a))), PANEL, outline=color, width=3, radius=18)
        draw.text((x + 32, int(y + 38 + 35 * (1 - a))), label, font=F_H2, fill=color)
        text_block(draw, (x + 32, int(y + 108 + 35 * (1 - a))), body, F_BODY, TEXT, 360)
        draw.text((x + 32, int(y + 240 + 35 * (1 - a))), "No KeeperHub request emitted", font=F_SMALL, fill=MUTED)
    footer(draw, "Blocked receipts are part of the evidence, not a side note.")


def scene_repo(img, draw, p, receipts):
    header(draw, "Public repo package", p)
    text_block(draw, (120, 235), "The public repository is sanitized: code, tests, mock example, receipt schema, policy gate docs, integration runbook, and this video.", F_BODY, TEXT, 760)
    code_panel(draw, (1010, 215, 1775, 735), [
        ("README.md", GREEN),
        ("src/keeperhub_execution_receipt_agent.js", TEXT),
        ("test/keeperhub_execution_receipt_agent.test.js", TEXT),
        ("docs/receipt_schema.md", TEXT),
        ("docs/policy_gate.md", TEXT),
        ("docs/keeperhub_integration_runbook.md", TEXT),
        ("examples/keeperhub_read_execution_evidence.json", GREEN),
        ("media/public-preview.mp4", AMBER),
    ])
    proof_box = (120, 690, 880, 835)
    rounded(draw, proof_box, PANEL, outline=GREEN, radius=16)
    text_in_box(draw, proof_box, "No secrets. No wallet data. No fake transaction evidence.", F_BODY, GREEN, pad=38, gap=8)
    footer(draw, "Repo URL is already public and ready for DoraHacks draft fields.")


def scene_keeperhub_pending(img, draw, p, receipts):
    header(draw, "KeeperHub integration status", p)
    steps = [
        ("MCP endpoint", "Connected: https://app.keeperhub.com/mcp", GREEN),
        ("Read workflow", "Run id captured: wrun_01KWRFQK1EQG92MERS9N49G5W6", PURPLE),
        ("Write tx", "Still pending user-attended testnet signing", AMBER),
        ("Evidence", "Read receipt now, tx hash after write run", BLUE),
    ]
    for i, (title, body, color) in enumerate(steps):
        y = 230 + i * 150
        rounded(draw, (130, y, 1765, y + 96), PANEL, outline=color, width=2, radius=16)
        draw.text((170, y + 25), f"{i + 1}. {title}", font=F_H2, fill=color)
        draw.text((650, y + 31), body, font=F_BODY, fill=TEXT)
    footer(draw, "Read workflow proof is captured. Transaction-hash proof remains separate.")


def scene_submission(img, draw, p, receipts):
    header(draw, "DoraHacks fields now vs after tx", p)
    left = (115, 240, 875, 780)
    right = (1035, 240, 1795, 780)
    rounded(draw, left, PANEL, outline=AMBER, radius=18)
    rounded(draw, right, PANEL, outline=GREEN, radius=18)
    draw.text((left[0] + 34, left[1] + 34), "NOW", font=F_H2, fill=AMBER)
    text_block(draw, (left[0] + 34, left[1] + 95), "Repo, video, and KeeperHub read run are ready. Transaction link is pending. Wording must distinguish read proof from write tx proof.", F_BODY, TEXT, 650)
    draw.text((right[0] + 34, right[1] + 34), "AFTER TESTNET RUN", font=F_H2, fill=GREEN)
    text_block(draw, (right[0] + 34, right[1] + 95), "Update README, receipt JSON, video, and DoraHacks fields with the real transaction hash after a write run.", F_BODY, TEXT, 650)
    footer(draw, "Public today with read proof, final tx proof after one write transaction.")


def scene_close(img, draw, p, receipts):
    draw.text((110, 170), "Execution is the claim.", font=F_TITLE, fill=TEXT)
    draw.text((110, 265), "The receipt is the proof.", font=F_TITLE, fill=GREEN)
    text_block(draw, (118, 425), "This public preview now includes one real KeeperHub read workflow run and its safety boundary. The final winning version should add one write transaction hash.", F_BODY, MUTED, 1180)
    rounded(draw, (118, 690, 1520, 825), PANEL, outline=AMBER, radius=18)
    draw.text((158, 735), "Public preview ready. Read run captured; write tx pending.", font=F_H2, fill=AMBER)
    footer(draw, "Next: run one user-attended testnet write transaction for tx hash proof.")


SCENES = [
    (scene_hook, 10),
    (scene_evidence_first, 12),
    (scene_flow, 11),
    (scene_approved, 12),
    (scene_fail_closed, 12),
    (scene_repo, 12),
    (scene_keeperhub_pending, 12),
    (scene_submission, 12),
    (scene_close, 10),
]


def draw_frame(scene_fn, p, receipts):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    scene_fn(img, draw, p, receipts)
    return img


def render():
    MEDIA.mkdir(exist_ok=True)
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()
    receipts = load_receipts()
    frames_dir = BUILD / "frames"
    frames_dir.mkdir()
    frame_idx = 0
    contact_paths = []

    for scene_i, (scene_fn, duration) in enumerate(SCENES):
        total = duration * FPS
        mid_path = None
        for local in range(total):
            p = local / max(1, total - 1)
            img = draw_frame(scene_fn, p, receipts)
            if local < 10 and scene_i > 0:
                overlay = Image.new("RGB", (W, H), BG)
                alpha = local / 10
                img = Image.blend(overlay, img, alpha)
            path = frames_dir / f"frame_{frame_idx:05d}.jpg"
            img.save(path, quality=92)
            if local == total // 2:
                mid_path = path
            frame_idx += 1
        if mid_path:
            contact_paths.append(mid_path)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%05d.jpg"),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-shortest",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k",
        str(OUT),
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    save_contact_sheet(contact_paths)
    print(OUT)
    print(CONTACT)


def save_contact_sheet(paths):
    cols = 3
    thumb_w, thumb_h = 480, 270
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * 318), (242, 245, 249))
    d = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        img = Image.open(path).resize((thumb_w, thumb_h))
        x = (i % cols) * thumb_w
        y = (i // cols) * 318
        sheet.paste(img, (x, y))
        d.text((x + 12, y + 278), f"Scene {i + 1}", font=F_SMALL, fill=(30, 41, 59))
    sheet.save(CONTACT, quality=92)


if __name__ == "__main__":
    render()
