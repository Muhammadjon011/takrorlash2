# ============================================================
#   SHAHAR SIMULYATSIYASI — 10 ta sinf
# ============================================================

from abc import ABC, abstractmethod
import random


# ============================================================
# 1. INSON (asosiy abstrakt sinf)
# ============================================================
class Inson(ABC):
    def __init__(self, ism: str, yosh: int):
        self.ism = ism
        self.yosh = yosh
        self._pul = 0.0

    @property
    def pul(self):
        return self._pul

    def pul_ishlash(self, miqdor: float):
        self._pul += miqdor
        print(f"{self.ism} ${miqdor:.0f} ishladi. Balans: ${self._pul:.0f}")

    def pul_sarflash(self, miqdor: float) -> bool:
        if self._pul >= miqdor:
            self._pul -= miqdor
            return True
        print(f"{self.ism}da yetarli pul yo'q!")
        return False

    @abstractmethod
    def ish_qilish(self):
        pass

    def __str__(self):
        return f"{self.ism} ({self.yosh} yosh)"


# ============================================================
# 2. ISHCHI
# ============================================================
class Ishchi(Inson):
    def __init__(self, ism: str, yosh: int, kasb: str, oylik: float):
        super().__init__(ism, yosh)
        self.kasb = kasb
        self.oylik = oylik

    def ish_qilish(self):
        self.pul_ishlash(self.oylik / 30)
        print(f"{self.ism} {self.kasb} sifatida ishladi.")

    def oylik_olish(self):
        self.pul_ishlash(self.oylik)
        print(f"{self.ism} oylik oldi: ${self.oylik:.0f}")


# ============================================================
# 3. TALABA
# ============================================================
class Talaba(Inson):
    def __init__(self, ism: str, yosh: int, universitet: str):
        super().__init__(ism, yosh)
        self.universitet = universitet
        self.baholar: list[int] = []
        self._stipendiya = 200.0

    def ish_qilish(self):
        baho = random.randint(60, 100)
        self.baholar.append(baho)
        print(f"{self.ism} dars o'qidi. Baho: {baho}")
        if baho >= 85:
            self.pul_ishlash(self._stipendiya)

    def ortacha_baho(self) -> float:
        return sum(self.baholar) / len(self.baholar) if self.baholar else 0

    def __str__(self):
        return f"{self.ism} — {self.universitet} talabasi"


# ============================================================
# 4. DOKTOR (Ishchidan meros)
# ============================================================
class Doktor(Ishchi):
    def __init__(self, ism: str, yosh: int, mutaxassislik: str):
        super().__init__(ism, yosh, "Doktor", oylik=3000)
        self.mutaxassislik = mutaxassislik
        self._bemorlar_soni = 0

    def bemor_qabul(self, bemor: Inson):
        narx = random.randint(50, 200)
        print(f"\nDr.{self.ism} → {bemor.ism}ni qabul qildi [{self.mutaxassislik}]")
        if bemor.pul_sarflash(narx):
            self.pul_ishlash(narx)
            print(f"Davolanish muvaffaqiyatli! Narx: ${narx}")
        else:
            print("Bemor to'lay olmadi, bepul davolandi.")
        self._bemorlar_soni += 1

    def ish_qilish(self):
        print(f"Dr.{self.ism} kasalxonada navbatchilik qildi.")
        self.pul_ishlash(self.oylik / 30)


# ============================================================
# 5. BINO (abstrakt)
# ============================================================
class Bino(ABC):
    def __init__(self, nomi: str, manzil: str):
        self.nomi = nomi
        self.manzil = manzil
        self._ochiq = True

    def ochish(self):
        self._ochiq = True
        print(f"{self.nomi} ochildi.")

    def yopish(self):
        self._ochiq = False
        print(f"{self.nomi} yopildi.")

    @abstractmethod
    def xizmat_korsatish(self, mijoz: Inson):
        pass

    def __str__(self):
        return f"{self.nomi} ({self.manzil}) — {'ochiq' if self._ochiq else 'yopiq'}"


# ============================================================
# 6. DO'KON
# ============================================================
class Dokon(Bino):
    def __init__(self, nomi: str, manzil: str):
        super().__init__(nomi, manzil)
        self.mahsulotlar: dict[str, float] = {}
        self._daromad = 0.0

    def mahsulot_qoshish(self, nomi: str, narx: float):
        self.mahsulotlar[nomi] = narx
        print(f"  '{nomi}' qo'shildi — ${narx:.2f}")

    def xizmat_korsatish(self, mijoz: Inson):
        if not self._ochiq:
            print(f"{self.nomi} yopiq!")
            return
        if not self.mahsulotlar:
            print("Do'kon bo'sh!")
            return
        nomi, narx = random.choice(list(self.mahsulotlar.items()))
        print(f"\n{mijoz.ism} → {self.nomi}ga kirdi. Tanladi: {nomi} (${narx:.2f})")
        if mijoz.pul_sarflash(narx):
            self._daromad += narx
            print(f"Xarid muvaffaqiyatli!")

    def daromad(self):
        print(f"{self.nomi} jami daromadi: ${self._daromad:.2f}")


# ============================================================
# 7. BANK
# ============================================================
class Bank(Bino):
    def __init__(self, nomi: str, manzil: str):
        super().__init__(nomi, manzil)
        self._hisoblar: dict[str, float] = {}

    def hisob_ochish(self, inson: Inson, boshlangich: float = 0):
        self._hisoblar[inson.ism] = boshlangich
        print(f"{inson.ism} uchun hisob ochildi. Balans: ${boshlangich:.0f}")

    def depozit(self, inson: Inson, miqdor: float):
        if inson.ism not in self._hisoblar:
            self.hisob_ochish(inson)
        if inson.pul_sarflash(miqdor):
            self._hisoblar[inson.ism] += miqdor
            print(f"{inson.ism} ${miqdor:.0f} joylashtirdi. Bank balans: ${self._hisoblar[inson.ism]:.0f}")

    def kredit_berish(self, inson: Inson, miqdor: float):
        print(f"{inson.ism}ga ${miqdor:.0f} kredit berildi.")
        inson.pul_ishlash(miqdor)
        self._hisoblar[inson.ism] = self._hisoblar.get(inson.ism, 0) - miqdor

    def xizmat_korsatish(self, mijoz: Inson):
        print(f"{mijoz.ism} bankka keldi.")
        balans = self._hisoblar.get(mijoz.ism, None)
        if balans is not None:
            print(f"Bank balansi: ${balans:.0f}")
        else:
            self.hisob_ochish(mijoz)


# ============================================================
# 8. MAKTAB
# ============================================================
class Maktab(Bino):
    def __init__(self, nomi: str, manzil: str):
        super().__init__(nomi, manzil)
        self.oqituvchilar: list[Ishchi] = []
        self.oquvchilar: list[Inson] = []

    def oqituvchi_qoshish(self, oqituvchi: Ishchi):
        self.oqituvchilar.append(oqituvchi)
        print(f"O'qituvchi {oqituvchi.ism} → {self.nomi}ga qo'shildi.")

    def xizmat_korsatish(self, mijoz: Inson):
        self.oquvchilar.append(mijoz)
        baho = random.randint(70, 100)
        print(f"{mijoz.ism} maktabga keldi → dars oldi. Baho: {baho}/100")

    def yillik_tadbir(self):
        print(f"\n{self.nomi} yillik tadbiri!")
        print(f"  O'quvchilar : {len(self.oquvchilar)}")
        print(f"  O'qituvchilar: {len(self.oqituvchilar)}")


# ============================================================
# 9. TRANSPORT (abstrakt) + AVTOBUS + TAKSI
# ============================================================
class Transport(ABC):
    def __init__(self, nomi: str, sigim: int, narx_km: float):
        self.nomi = nomi
        self.sigim = sigim
        self.narx_km = narx_km
        self._yolovchilar: list[Inson] = []

    def minish(self, inson: Inson):
        if len(self._yolovchilar) >= self.sigim:
            print(f"{self.nomi} to'liq!")
            return
        self._yolovchilar.append(inson)
        print(f"{inson.ism} {self.nomi}ga mindi.")

    def tushish(self, inson: Inson):
        if inson in self._yolovchilar:
            self._yolovchilar.remove(inson)
            print(f"{inson.ism} {self.nomi}dan tushdi.")

    @abstractmethod
    def harakat_qilish(self, km: float):
        pass


class Avtobus(Transport):
    def __init__(self, raqam: str):
        super().__init__(f"{raqam}-avtobus", sigim=40, narx_km=0.5)

    def harakat_qilish(self, km: float):
        narx = km * self.narx_km
        print(f"{self.nomi} {km} km yurdi. Har yo'lovchi: ${narx:.1f}")
        for y in self._yolovchilar:
            y.pul_sarflash(narx)


class Taksi(Transport):
    def __init__(self, haydovchi: Ishchi):
        super().__init__("Taksi", sigim=4, narx_km=2.0)
        self.haydovchi = haydovchi

    def harakat_qilish(self, km: float):
        narx = km * self.narx_km
        print(f"Taksi {km} km yurdi. Narx: ${narx:.1f}")
        for y in self._yolovchilar:
            if y.pul_sarflash(narx):
                self.haydovchi.pul_ishlash(narx * 0.8)


# ============================================================
# 10. SHAHAR (hamma sinflarni birlashtiradi)
# ============================================================
class Shahar:
    def __init__(self, nomi: str):
        self.nomi = nomi
        self.aholisi: list[Inson] = []
        self.binolar: list[Bino] = []
        self.transportlar: list[Transport] = []
        self._kun = 1

    def aholi_qoshish(self, *insonlar):
        for i in insonlar:
            self.aholisi.append(i)
            print(f"{i.ism} → {self.nomi} shahriga ko'chib keldi.")

    def bino_qoshish(self, *binolar):
        for b in binolar:
            self.binolar.append(b)
            print(f"Bino qo'shildi: {b.nomi}")

    def transport_qoshish(self, *transportlar):
        for t in transportlar:
            self.transportlar.append(t)
            print(f"Transport qo'shildi: {t.nomi}")

    def kun_otkazish(self):
        print(f"\n{'='*45}")
        print(f"  {self.nomi} — {self._kun}-kun")
        print(f"{'='*45}")
        for inson in self.aholisi:
            inson.ish_qilish()
        self._kun += 1

    def statistika(self):
        print(f"\n{'='*45}")
        print(f"  {self.nomi} shahri statistikasi")
        print(f"{'='*45}")
        print(f"  Aholi       : {len(self.aholisi)} kishi")
        print(f"  Binolar     : {len(self.binolar)} ta")
        print(f"  Transportlar: {len(self.transportlar)} ta")
        print(f"  Joriy kun   : {self._kun}")
        print(f"\n  Fuqarolar holati:")
        for i in self.aholisi:
            print(f"    • {i} — ${i.pul:.0f}")


# ============================================================
# ISHLATISH
# ============================================================
if __name__ == "__main__":

    # --- Insonlar ---
    ali     = Ishchi("Ali",     30, "Muhandis",    2500)
    malika  = Talaba("Malika",  21, "TATU")
    bobur   = Doktor("Bobur",   45, "Kardiolog")
    zulfiya = Ishchi("Zulfiya", 35, "O'qituvchi",  1800)
    jasur   = Ishchi("Jasur",   28, "Haydovchi",   1500)

    # Boshlang'ich pullar
    ali._pul    = 800
    malika._pul = 300
    bobur._pul  = 1500
    zulfiya._pul = 600
    jasur._pul  = 400

    # --- Binolar ---
    print("\n--- BINOLAR OCHILMOQDA ---")
    supermarket  = Dokon("Korzinka",     "Mustaqillik 10")
    supermarket.mahsulot_qoshish("Non",     1.5)
    supermarket.mahsulot_qoshish("Sut",     2.0)
    supermarket.mahsulot_qoshish("Noutbuk", 800.0)
    supermarket.mahsulot_qoshish("Kiyim",   50.0)

    ipoteka_bank = Bank("Ipoteka Bank",  "Amir Temur 5")
    maktab_1     = Maktab("1-maktab",   "Chilonzor")
    maktab_1.oqituvchi_qoshish(zulfiya)

    # --- Transportlar ---
    print("\n--- TRANSPORTLAR ---")
    avtobus_45  = Avtobus("45")
    jasur_taksi = Taksi(jasur)

    # --- Shahar ---
    print("\n--- SHAHAR TUZILMOQDA ---")
    toshkent = Shahar("Toshkent")
    toshkent.aholi_qoshish(ali, malika, bobur, zulfiya, jasur)
    toshkent.bino_qoshish(supermarket, ipoteka_bank, maktab_1)
    toshkent.transport_qoshish(avtobus_45, jasur_taksi)

    # --- 3 kun simulyatsiya ---
    for _ in range(3):
        toshkent.kun_otkazish()

    # --- Xizmatlar ---
    print("\n--- DO'KON ---")
    supermarket.xizmat_korsatish(ali)
    supermarket.xizmat_korsatish(malika)
    supermarket.xizmat_korsatish(bobur)

    print("\n--- BANK ---")
    ipoteka_bank.hisob_ochish(ali, 500)
    ipoteka_bank.depozit(ali, 200)
    ipoteka_bank.kredit_berish(malika, 500)
    ipoteka_bank.xizmat_korsatish(bobur)

    print("\n--- KASALXONA ---")
    bobur.bemor_qabul(ali)
    bobur.bemor_qabul(malika)

    print("\n--- MAKTAB ---")
    maktab_1.xizmat_korsatish(malika)
    maktab_1.xizmat_korsatish(ali)
    maktab_1.yillik_tadbir()

    print("\n--- TRANSPORT ---")
    avtobus_45.minish(ali)
    avtobus_45.minish(malika)
    avtobus_45.harakat_qilish(10)
    avtobus_45.tushish(ali)

    jasur_taksi.minish(bobur)
    jasur_taksi.harakat_qilish(5)

    # --- Yakuniy statistika ---
    toshkent.statistika()
    supermarket.daromad()