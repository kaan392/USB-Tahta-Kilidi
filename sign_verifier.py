"""USB'deki öğretmen anahtarının imzasını doğrular."""
import base64
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

APP_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PEM = b'-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAUp714gaysEk5DcM2y2dJ97tGABmeEyuP3LHJ1G9917I=\n-----END PUBLIC KEY-----\n'  # Yönetici anahtarı
REQUIRED_FIELDS = {"schema_version", "teacher_name", "key_id", "issued_at"}


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify_file(key_file):
    document = json.loads(Path(key_file).read_text(encoding="utf-8"))
    payload = document["payload"]
    signature = base64.b64decode(document["signature"], validate=True)
    if not isinstance(payload, dict) or set(payload) != REQUIRED_FIELDS:
        raise ValueError("Dosyanın içeriği beklenen biçimde değil.")
    if payload["schema_version"] != 1:
        raise ValueError("Desteklenmeyen dosya sürümü.")
    if not all(isinstance(payload[key], str) and payload[key].strip() for key in ("teacher_name", "key_id", "issued_at")):
        raise ValueError("Dosyadaki bilgiler geçersiz.")
    if PUBLIC_KEY_PEM is None:
        raise ValueError("Bu doğrulayıcıya yönetici açık anahtarı yüklenmemiş.")
    public_key = serialization.load_pem_public_key(PUBLIC_KEY_PEM)
    if not isinstance(public_key, Ed25519PublicKey):
        raise ValueError("Pano açık anahtarı Ed25519 biçiminde değil.")
    public_key.verify(signature, canonical_payload(payload))
    return payload


class BoardApp:
    def __init__(self, root):
        self.root = root
        root.title("Öğretmen USB Anahtarı Doğrulama")
        root.geometry("520x260")
        root.configure(bg="#f4f6f8")
        tk.Label(root, text="Öğretmen dosyasını doğrula", font=("Segoe UI", 18, "bold"), bg="#f4f6f8", fg="#183153").pack(anchor="w", padx=28, pady=(24, 8))
        tk.Label(root, text="USB'deki teacher-key.json dosyasını seçin.", font=("Segoe UI", 10), bg="#f4f6f8", fg="#4b5563").pack(anchor="w", padx=28, pady=(0, 18))
        tk.Button(root, text="USB dosyasını seç ve doğrula…", command=self.select_file, bg="#1769aa", fg="white", relief="flat", font=("Segoe UI", 11, "bold"), padx=14, pady=11).pack(anchor="w", padx=28)
        self.result = tk.StringVar(value="Hazır")
        tk.Label(root, textvariable=self.result, bg="#f4f6f8", fg="#374151", font=("Segoe UI", 11), wraplength=460, justify="left").pack(anchor="w", padx=28, pady=20)
        tk.Label(root, text="Bu prototip yalnızca doğrulama yapar; oturumu kilitlemez ve USB'yi izlemeye almaz.", bg="#f4f6f8", fg="#6b7280", wraplength=460, font=("Segoe UI", 9)).pack(anchor="w", padx=28)

    def select_file(self):
        path = filedialog.askopenfilename(title="USB'deki imzalı öğretmen dosyasını seç", filetypes=[("JSON anahtar dosyası", "*.json"), ("Tüm dosyalar", "*.*")])
        if not path:
            return
        try:
            payload = verify_file(path)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, InvalidSignature) as exc:
            self.result.set("DOĞRULANAMADI")
            messagebox.showerror("Geçersiz öğretmen dosyası", f"İmza doğrulanamadı.\n\n{exc}", parent=self.root)
            return
        message = f"İMZA GEÇERLİ\nÖğretmen: {payload['teacher_name']}\nKimlik: {payload['key_id']}"
        self.result.set(message)
        messagebox.showinfo("Doğrulama başarılı", message + "\n\nİmza dosyanın kopyalanmasını engellemez.", parent=self.root)


if __name__ == "__main__":
    window = tk.Tk()
    BoardApp(window)
    window.mainloop()
