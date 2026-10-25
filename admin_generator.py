"""Yönetici bilgisayarı: imzalama anahtarı oluşturur ve öğretmen USB anahtarı üretir."""
import base64
import json
import tkinter as tk
import uuid
from datetime import datetime, timezone
from pathlib import Path
from tkinter import filedialog, messagebox

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

PRIVATE_KEY_PEM = b"""-----BEGIN PRIVATE KEY-----MC4CAQAwBQYDK2VwBCIEIEl2z+sCKney0Ui570c3GT1jHlgkIY8HqAxoT49CTrVl-----END PRIVATE KEY-----"""

def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def load_private_key():
    key = serialization.load_pem_private_key(PRIVATE_KEY_PEM, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("Yönetici özel anahtarı Ed25519 biçiminde değil.")
    return key

def make_teacher_file(name):
    normalized_name = " ".join(name.split())
    if not normalized_name:
        raise ValueError("Öğretmen adını girin.")
    key = load_private_key()

    payload = {
        "schema_version": 1,
        "teacher_name": normalized_name,
        "key_id": str(uuid.uuid4()),
        "issued_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    return {"payload": payload, "signature": base64.b64encode(key.sign(canonical_payload(payload))).decode("ascii")}

class AdminApp:
    def __init__(self, root):
        self.root = root
        root.title("Yönetici • Öğretmen USB Anahtarı")
        root.geometry("540x330")
        root.configure(bg="#f4f6f8")
        tk.Label(root, text="Öğretmen anahtarı üret", font=("Segoe UI", 18, "bold"), bg="#f4f6f8", fg="#183153").pack(anchor="w", padx=26, pady=(22, 5))
        tk.Label(root, text="Bu uygulamayı yalnızca güvenilir yönetici bilgisayarında kullanın.", font=("Segoe UI", 10), bg="#f4f6f8", fg="#4b5563").pack(anchor="w", padx=26, pady=(0, 14))
        self.status = tk.StringVar(value=self.key_status())
        tk.Label(root, textvariable=self.status, bg="#f4f6f8", fg="#185b35", font=("Segoe UI", 9), wraplength=480).pack(anchor="w", padx=26, pady=(0, 12))
        self.key_button = tk.Button(root, text="Özel anahtarı kontrol et", command=self.create_keys)
        self.key_button.pack(anchor="w", padx=26, pady=(0, 16))
        if self.status.get().startswith("İmzalama anahtarı program içinde hazır"):
            self.key_button.configure(state="disabled")
        tk.Label(root, text="Öğretmen adı", bg="#f4f6f8", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=26)
        self.name = tk.Entry(root, font=("Segoe UI", 12), relief="solid", bd=1)
        self.name.pack(fill="x", padx=26, pady=(5, 14), ipady=7)
        tk.Button(root, text="İmzalı USB dosyasını kaydet…", command=self.issue, bg="#1769aa", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=12, pady=9).pack(anchor="e", padx=26)
        tk.Label(root, text="Özel imzalama anahtarı bu yönetici programının içindedir; programı panoya kopyalamayın.", bg="#f4f6f8", fg="#7a3e00", wraplength=480, font=("Segoe UI", 9)).pack(anchor="w", padx=26, pady=15)

    def key_status(self):
        try:
            load_private_key()
        except (TypeError, ValueError) as exc:
            return f"İmzalama anahtarı geçersiz: {exc}"
        return "İmzalama anahtarı program içinde hazır."

    def create_keys(self):
        try:
            load_private_key()
        except (TypeError, ValueError) as exc:
            messagebox.showerror("Anahtar geçersiz", str(exc), parent=self.root)
            return
        self.status.set(self.key_status())
        self.key_button.configure(state="disabled")
        messagebox.showinfo("Anahtar hazır", "Özel imzalama anahtarı bu yönetici programının içindedir. Bu programı panoya kopyalamayın.", parent=self.root)

    def issue(self):
        try:
            document = make_teacher_file(self.name.get())
        except (OSError, ValueError) as exc:
            messagebox.showerror("Dosya oluşturulamadı", str(exc), parent=self.root)
            return
        path = filedialog.asksaveasfilename(title="USB öğretmen dosyasını kaydet", defaultextension=".json", initialfile="teacher-key.json", filetypes=[("Öğretmen anahtarı", "*.json")])
        if not path:
            return
        try:
            Path(path).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Kaydedilemedi", str(exc), parent=self.root)
            return
        messagebox.showinfo("Tamamlandı", "İmzalı öğretmen dosyası kaydedildi. Bunu USB'ye kopyalayın. Dosyanın kopyalanması imzayla engellenmez.", parent=self.root)

if __name__ == "__main__":
    window = tk.Tk()
    AdminApp(window)
    window.mainloop()
