# Öğretmen USB Kilidi – Kurulum

Bu program akıllı tahtayı otomatik kilitler. Tahtaya **öğretmen USB'si** takılınca kilit açılır, USB çıkarılınca tahta tekrar kilitlenir.

## 1. Önce USB'yi hazırlayın (yönetici bilgisayarında)

1. `admin_generator.py` dosyasını açın.
2. Öğretmenin adını yazın.
3. "İmzalı USB dosyasını kaydet" düğmesine basın.
4. Oluşan `teacher-key.json` dosyasını USB'nin köküne (klasör içine değil) kopyalayın.

> `admin_generator.py` yalnızca yönetici bilgisayarında kalsın. Tahtalara *kopyalamayın*.

## 2. Tahtaya kurulum

Tahtaya yalnızca `board_verifier.py` dosyasını kopyalamanız yeterli. Başka dosya gerekmez.

**Kurulumdan önce öğretmen USB'sini yanınızda bulundurun.**

### Pardus / Linux

1. `board_verifier.py` dosyasını herhangi bir yere kopyalayın.
2. İlk seferliğine dosyayı çalıştırın. (Daha sonra program kendiliğinden çalışır)
4. İlk kurulumda parola sorarsa tahtanın yönetici parolasını girin.
5. Tahtayı yeniden başlatın. Bundan sonra her açılışta kilit kendiliğinden gelir.

### Windows

1. [python.org](https://www.python.org/downloads/) adresinden Python'u kurun. Kurarken "Add Python to PATH" kutusunu işaretleyin.
2. Bilgisayarda *Komut İstemi*'ni açıp şunu yazın:

   ```
   pip install cryptography
   ```

3. `board_verifier.py` dosyasına çift tıklayın. "İzin vermek istiyor musunuz?" sorusuna *Evet* deyin.
4. Tahtayı yeniden başlatın.

## 3. Kullanım

- Kilit ekranı geldiğinde öğretmen USB'sini takın, kilit açılır.
- USB'yi çıkarınca tahta tekrar kilitlenir.

## 4. Sorun olursa

- **USB takıldı ama açılmıyor:** `teacher-key.json` dosyası USB'nin en dışında mı, adı doğru mu bakın. Dosya başka bir yönetici anahtarıyla üretilmişse çalışmaz.

## 5. Programı kaldırmak

- **Pardus:** Terminalde `sudo python3 /opt/etap-usb-kilidi/board_verifier.py --remove`
- **Windows:** Dosyayı kurduğunuz dizindeki terminalde `sudo python board_verifier.py --remove`(Windows ayarlarında "sudo" etkinleştirilmiş olmalı)
(Komutlar çalıştırıldıktan sonra cihazı yeniden başlatın.)