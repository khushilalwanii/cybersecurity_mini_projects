# phishing_detector_gui.py
import re
import tkinter as tk
from tkinter import ttk, scrolledtext
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "login", "secure", "account", "update", "verify", "signin", "bank", "confirm"
]

def score_url(url):
    score = 0
    reasons = []
    if not re.match(r'^[a-zA-Z]+://', url):
        url = "http://" + url
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()
    full = url.lower()

    if '@' in full:
        score += 2
        reasons.append("Contains '@' symbol")
    if '-' in netloc:
        score += 1
        reasons.append("Hyphen in domain")
    if parsed.scheme != "https":
        score += 1
        reasons.append("Not using HTTPS")
    if len(netloc) > 30:
        score += 1
        reasons.append("Domain unusually long")
    if re.search(r'^\d+\.\d+\.\d+\.\d+$', netloc.split(':')[0]):
        score += 2
        reasons.append("IP address used instead of domain")
    if len(netloc.split('.')) >= 5:
        score += 1
        reasons.append("Many subdomains")
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in netloc or kw in path:
            score += 1
            reasons.append(f"Contains suspicious keyword '{kw}'")
            break
    if 'xn--' in netloc:
        score += 1
        reasons.append("Contains punycode (xn--)")
    return score, reasons

def verdict_from_score(score):
    if score == 0:
        return "Legit ✅"
    elif 1 <= score <= 2:
        return "Suspicious ⚠️"
    else:
        return "Likely Phishing 🚨"

def on_check():
    url = url_entry.get().strip()
    if not url:
        result_label.config(text="Please enter a URL.")
        reason_box.delete("1.0", tk.END)
        return
    score, reasons = score_url(url)
    verdict = verdict_from_score(score)
    result_label.config(text=f"Result: {verdict} (score={score})")
    reason_box.delete("1.0", tk.END)
    if reasons:
        reason_box.insert(tk.END, "\n".join(reasons))
    else:
        reason_box.insert(tk.END, "No suspicious patterns detected.")

# GUI layout
root = tk.Tk()
root.title("Phishing URL Detector — Simple")
root.geometry("600x300")
root.resizable(False, False)

frame = ttk.Frame(root, padding=12)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Enter URL:").grid(row=0, column=0, sticky="w")
url_entry = ttk.Entry(frame, width=60)
url_entry.grid(row=0, column=1, padx=6, pady=6)

check_btn = ttk.Button(frame, text="Check", command=on_check)
check_btn.grid(row=0, column=2, padx=6)

result_label = ttk.Label(frame, text="Result: ")
result_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 4))

ttk.Label(frame, text="Reasons:").grid(row=2, column=0, sticky="nw")
reason_box = scrolledtext.ScrolledText(frame, width=70, height=8, wrap=tk.WORD)
reason_box.grid(row=2, column=1, columnspan=2, pady=6)

root.mainloop()
