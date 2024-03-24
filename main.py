import random
import os
from rich import print
from rich.padding import Padding
from rich.table import Table
from rich.text import Text


def tam_sayi_al(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Geçersiz giriş! Lütfen bir tamsayı girin.")


renkler = ["#eb281a", "#1ad2eb", "#c11aeb", "#1aeb3d"]


class Savasci:
    def __init__(
        self,
        kaynak,
        can,
        hasar,
        gercekHasarMi,
        menzil,
        harf,
        x,
        y,
        map_boyut,
        renk="white",
        sira=1,
        saldiri_sirasi=1,
    ):
        self.kaynak = kaynak
        self.can = can
        self.hasar = hasar
        self.gercekHasarMi = gercekHasarMi
        self.menzil = menzil
        self.harf = harf
        self.x = x
        self.y = y
        self.komsular = self.komsulari_hesapla(x, y, map_boyut)
        self.sira = sira
        self.saldiri_sirasi = saldiri_sirasi
        self.renk = renk
        self.canli = False

    def komsulari_hesapla(self, x, y, map_boyut):
        komsular = [
            [x - 1, y - 1],
            [x, y - 1],
            [x + 1, y - 1],
            [x - 1, y],
            [x + 1, y],
            [x - 1, y + 1],
            [x, y + 1],
            [x + 1, y + 1],
        ]

        for i, (nx, ny) in enumerate(komsular):
            if (
                int(nx) < 0
                or int(nx) >= int(map_boyut)
                or int(ny) < 0
                or int(ny) >= int(map_boyut)
            ):
                komsular[i] = None

        return komsular

    def isim(self):
        return self.harf + str(self.sira)

    def menzildeki_dusmanlar(self, map):
        (yatay, dikey, capraz) = self.menzil

        yataydakiler = self.yataydaki_dusmanlar(map, yatay)
        dikeydekiler = self.dikeydeki_dusmanlar(map, dikey)
        caprazdakiler = self.caprazdaki_dusmanlar(map, capraz)

        dusmanlar = yataydakiler + dikeydekiler + caprazdakiler

        i = len(dusmanlar) - 1

        while i >= 0:
            if dusmanlar[i].renk == self.renk:
                del dusmanlar[i]
            i -= 1

        return dusmanlar

    def yataydaki_dusmanlar(self, map, uzaklik):
        yataydakiler = []

        for i in range(1, uzaklik + 1):
            if self.x - i >= 0:
                sol = map.matris[self.y][self.x - i]

                if self.dusman_mi(sol):
                    yataydakiler.append(sol)

            if self.x + i < map.map_boyut:
                sag = map.matris[self.y][self.x + i]

                if self.dusman_mi(sag):
                    yataydakiler.append(sag)

        return yataydakiler

    def dikeydeki_dusmanlar(self, map, uzaklik):
        dikeydekiler = []

        for i in range(1, uzaklik + 1):
            if self.y - i >= 0:
                ust = map.matris[self.y - i][self.x]

                if self.dusman_mi(ust):
                    dikeydekiler.append(ust)

            if self.y + i < map.map_boyut:
                alt = map.matris[self.y + i][self.x]

                if self.dusman_mi(alt):
                    dikeydekiler.append(alt)

        return dikeydekiler

    def caprazdaki_dusmanlar(self, map, uzaklik):
        caprazdakiler = []

        for i in range(1, uzaklik + 1):
            if self.y - i >= 0 and self.x - i >= 0:
                sol_ust = map.matris[self.y - i][self.x - i]

                if self.dusman_mi(sol_ust):
                    caprazdakiler.append(sol_ust)

            if self.y - i >= 0 and self.x + i < map.map_boyut:
                sag_ust = map.matris[self.y - i][self.x + i]

                if self.dusman_mi(sag_ust):
                    caprazdakiler.append(sag_ust)

            if self.x - i >= 0 and self.y + i < map.map_boyut:
                sol_alt = map.matris[self.y + i][self.x - i]

                if self.dusman_mi(sol_alt):
                    caprazdakiler.append(sol_alt)

            if self.x + i < map.map_boyut and self.y + i < map.map_boyut:
                sag_alt = map.matris[self.y + i][self.x + i]

                if self.dusman_mi(sag_alt):
                    caprazdakiler.append(sag_alt)

        return caprazdakiler

    def dusman_mi(self, kare):
        if kare != 0:
            return True

        return False

    def saldir(self, dusman):
        if self.gercekHasarMi:
            dusman.can -= self.hasar
        else:
            dusman.can -= dusman.can * self.hasar / 100

        print(Text(f"{self.isim()}({self.can})", style=self.renk), end="")
        print(" x ", end="")
        print(Text(f"{dusman.isim()}({dusman.can})", style=dusman.renk))

        return dusman.can


class Muhafiz(Savasci):
    def __init__(self, x, y, map_boyut, renk, sira=1, saldiri_sirasi=1):
        super().__init__(
            10,
            80,
            20,
            True,
            (1, 1, 1),
            "M",
            x,
            y,
            map_boyut,
            renk,
            sira,
            saldiri_sirasi,
        )


class Okcu(Savasci):
    def __init__(self, x, y, map_boyut, renk, sira=1, saldiri_sirasi=1):
        super().__init__(
            20,
            30,
            60,
            False,
            (2, 2, 2),
            "O",
            x,
            y,
            map_boyut,
            renk,
            sira,
            saldiri_sirasi,
        )


class Saglikci(Savasci):
    def __init__(self, x, y, map_boyut, renk, sira=1, saldiri_sirasi=1):
        super().__init__(
            10,
            100,
            50,
            False,
            (2, 2, 2),
            "S",
            x,
            y,
            map_boyut,
            renk,
            sira,
            saldiri_sirasi,
        )

    def menzildeki_dusmanlar(self, map):
        (yatay, dikey, capraz) = self.menzil

        yataydakiler = self.yataydaki_dusmanlar(map, yatay)
        dikeydekiler = self.dikeydeki_dusmanlar(map, dikey)
        caprazdakiler = self.caprazdaki_dusmanlar(map, capraz)

        dusmanlar = yataydakiler + dikeydekiler + caprazdakiler

        i = len(dusmanlar) - 1

        while i >= 0:
            if dusmanlar[i].renk != self.renk:
                del dusmanlar[i]
            i -= 1

        return dusmanlar

    def saldir(self, dusman):
        dusman.can += dusman.can * self.hasar / 100

        return dusman.can


class Topcu(Savasci):
    def __init__(self, x, y, map_boyut, renk, sira=1, saldiri_sirasi=1):
        super().__init__(
            50,
            30,
            100,
            False,
            (2, 2, 0),
            "T",
            x,
            y,
            map_boyut,
            renk,
            sira,
            saldiri_sirasi,
        )


class Atli(Savasci):
    def __init__(self, x, y, map_boyut, renk, sira=1, saldiri_sirasi=1):
        super().__init__(
            30,
            40,
            30,
            True,
            (0, 0, 3),
            "A",
            x,
            y,
            map_boyut,
            renk,
            sira,
            saldiri_sirasi,
        )


class Map:
    def __init__(self, map_boyut, oyuncular):
        self.matris = []
        self.oyuncular = oyuncular
        self.map_boyut = map_boyut
        self.savasci_sayisi = 0
        self.muhafiz_sayisi = 0
        self.okcu_sayisi = 0
        self.topcu_sayisi = 0
        self.atli_sayisi = 0
        self.saglikci_sayisi = 0

        for i in range(map_boyut):
            x = []
            for j in range(map_boyut):
                x.append(0)
            self.matris.append(x)

        self.render()

    def render(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        cells = []
        komsular = {}

        for oyuncu in self.oyuncular:
            komsular[oyuncu.renk] = []

        for y in range(self.map_boyut):
            row = []
            for x in range(self.map_boyut):
                block = self.matris[y][x]
                if block == 0:
                    row.append(Padding(".", (0, 1)))
                else:
                    komsular[block.renk] += block.komsular
                    # print(block.komsular)
                    row.append(Text(str(block.isim()), style=block.renk))

            cells.append(row)

        for oyuncu in self.oyuncular:
            for komsu in komsular[oyuncu.renk]:
                if komsu:
                    if self.matris[komsu[1]][komsu[0]] == 0:
                        cells[komsu[1]][komsu[0]] = Padding(
                            Text("*", style=oyuncu.renk), (0, 1)
                        )

        table = Table(show_header=False, show_lines=True)

        for row in cells:
            table.add_row(*row)

        print(Padding((table), (0, 4)))

        table_kaynak = Table(show_lines=True)
        table_kaynak.add_column("Oyuncu")
        table_kaynak.add_column("Kaynak")
        for oyuncu in self.oyuncular:
            row = [Text(oyuncu.isim(), style=oyuncu.renk), str(oyuncu.kaynak)]
            table_kaynak.add_row(*row)

        print(Padding(table_kaynak, (0, 4)))

    def savasci_koy(self, x, y, oyuncu, tur):
        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.savasci_sayisi += 1

        savasci = Muhafiz(
            x,
            y,
            self.map_boyut,
            oyuncu.renk,
            oyuncu.muhafiz_sayisi,
            self.savasci_sayisi,
        )

        """
        0: Muhafız
        1: Okçu
        2: Topçu
        3: Atlı
        4: Sağlıkçı
        """

        if tur == 0:
            self.muhafiz_sayisi += 1
        elif tur == 1:
            savasci = Okcu(
                x,
                y,
                self.map_boyut,
                oyuncu.renk,
                oyuncu.okcu_sayisi,
                self.savasci_sayisi,
            )
            self.okcu_sayisi += 1
        elif tur == 2:
            savasci = Topcu(
                x,
                y,
                self.map_boyut,
                oyuncu.renk,
                oyuncu.topcu_sayisi,
                self.savasci_sayisi,
            )
            self.topcu_sayisi += 1
        elif tur == 3:
            savasci = Atli(
                x,
                y,
                self.map_boyut,
                oyuncu.renk,
                oyuncu.atli_sayisi,
                self.savasci_sayisi,
            )
            self.atli_sayisi += 1
        elif tur == 4:
            savasci = Saglikci(
                x,
                y,
                self.map_boyut,
                oyuncu.renk,
                oyuncu.saglikci_sayisi,
                self.savasci_sayisi,
            )
            self.saglikci_sayisi += 1

        if self.matris[y][x] != 0:
            oyuncu.kaynak += (self.matris[y][x].kaynak * 80) / 100

        self.matris[y][x] = savasci
        oyuncu.savascilar.append(savasci)
        oyuncu.savasci_sayisi += 1

        self.render()
        oyuncu.komsular()
        return savasci

    def muhafiz_koy(self, x, y, oyuncu):
        return self.savasci_koy(x, y, oyuncu, 0)

    def okcu_koy(self, x, y, oyuncu):
        return self.savasci_koy(x, y, oyuncu, 1)

    def topcu_koy(self, x, y, oyuncu):
        return self.savasci_koy(x, y, oyuncu, 2)

    def atli_koy(self, x, y, oyuncu):
        return self.savasci_koy(x, y, oyuncu, 3)

    def saglikci_koy(self, x, y, oyuncu):
        return self.savasci_koy(x, y, oyuncu, 4)

    def savasci_sil(self, savasci, tur):
        self.matris[savasci.y][savasci.x] = 0
        self.savasci_sayisi -= 1

        if tur == 0:
            self.muhafiz_sayisi -= 1
        elif tur == 1:
            self.okcu_sayisi -= 1
        elif tur == 2:
            self.topcu_sayisi -= 1
        elif tur == 3:
            self.atli_sayisi -= 1
        elif tur == 4:
            self.saglikci_sayisi -= 1


class Oyuncu:
    def __init__(self, id, renk):
        self.kaynak = 200
        self.id = id
        self.renk = renk
        self.savascilar = []
        self.savasci_sayisi = 0
        self.muhafiz_sayisi = 0
        self.okcu_sayisi = 0
        self.topcu_sayisi = 0
        self.atli_sayisi = 0
        self.saglikci_sayisi = 0
        self.pas_sayisi = 0

    def komsular(self):
        komsular = []
        for savasci in self.savascilar:
            komsular += savasci.komsular

        komsular_filtre = []
        [
            komsular_filtre.append(komsu)
            for komsu in komsular
            if komsu not in komsular_filtre
        ]

        return komsular_filtre

    def isim(self):
        return "P" + str(self.id)

    def savasci_sil(self, savasci, tur):
        self.savascilar.remove(savasci)
        self.savasci_sayisi -= 1

        if tur == 0:
            self.muhafiz_sayisi -= 1
        elif tur == 1:
            self.okcu_sayisi -= 1
        elif tur == 2:
            self.topcu_sayisi -= 1
        elif tur == 3:
            self.atli_sayisi -= 1
        elif tur == 4:
            self.saglikci_sayisi -= 1

        return self.savasci_sayisi


class Game:
    def __init__(self):
        print("Lords of the Polywarphism oyuna hoşgeldiniz.")
        oyuncu_sayisi = tam_sayi_al(
            "Oyunu kaç gerçek oyuncunun oynayacağını giriniz (1-4): "
        )
        print("Oyuna başlamak için bu maplerden birini seçin: ")
        print("1. 16x16 ")
        print("2. 24x24 ")
        print("3. 32x32 ")
        print("4. Kendi boyutumu ayarlamak istiyorum. (8x8-32x32 arası olmalıdır.)")
        tercih = tam_sayi_al("Oynamak istediğiniz mapi seçiniz: ")
        boyut = 8
        if tercih == 1:
            boyut = 16
        elif tercih == 2:
            boyut = 24
        elif tercih == 3:
            boyut = 32
        else:
            boyut = tam_sayi_al("Oynamak istediğiniz map boyutunu giriniz: ")
            if boyut < 8:
                boyut = 8
            elif boyut > 32:
                boyut = 32

        self.map_boyut = boyut
        self.oyuncu_sayisi = oyuncu_sayisi
        self.oyuncular = [Oyuncu(x + 1, renkler[x]) for x in range(oyuncu_sayisi)]
        self.savascilar = []
        self.map = Map(boyut, self.oyuncular)
        self.sira = 1

        for oyuncu in self.oyuncular:
            while True:
                x = random.choice([0, self.map_boyut - 1])
                y = random.choice([0, self.map_boyut - 1])
                if self.map.matris[y][x] == 0:
                    self.savasci_koy(
                        x,
                        y,
                        1,
                        oyuncu,
                        True,
                    )
                    break

        while self.sira <= oyuncu_sayisi:
            self.oyna(self.sira - 1)
            self.sira += 1
            if self.sira > oyuncu_sayisi:
                self.saldirilari_gerceklestir()
                self.sira = 1
                for oyuncu in self.oyuncular:
                    blok_sayisi = self.map_boyut * self.map_boyut
                    if oyuncu.savasci_sayisi >= blok_sayisi * 60 / 100:
                        print(f"Oyunu {oyuncu.isim()} oyuncusu kazandı.")
                        break

                if self.oyuncu_sayisi == 1:
                    print(
                        f"Oyunu {self.oyuncular[0].isim()} oyuncusu tek kişi kaldığı için kazandı."
                    )
                    break

    def pas_gec(self, oyuncu):
        pas_gec = input("Savaşçı üretmek istiyor musunuz? (e/h) ").upper() == "E"

        if pas_gec:
            oyuncu.pas_sayisi = 0
        else:
            oyuncu.pas_sayisi += 1

        return pas_gec

    def savascilari_sirala(self, savasci):
        return savasci.saldiri_sirasi

    def cana_gore_sirala(self, savasci):
        return savasci.can

    def kaynaga_gore_sirala(self, savasci):
        return savasci.kaynak

    def saldirilari_gerceklestir(self):
        siralanmis_savascilar = sorted(self.savascilar, key=self.savascilari_sirala)

        for savasci in siralanmis_savascilar:
            # print(savasci.isim(), savasci.renk,  savasci.saldiri_sirasi)
            dusmanlar = savasci.menzildeki_dusmanlar(self.map)
            if isinstance(savasci, Muhafiz):
                self.saldir(savasci, dusmanlar)

            elif isinstance(savasci, Okcu):
                siralanmis_dusmanlar = sorted(
                    dusmanlar, key=self.cana_gore_sirala, reverse=True
                )[:3]
                self.saldir(savasci, siralanmis_dusmanlar)

            elif isinstance(savasci, Topcu):
                siralanmis_dusmanlar = sorted(
                    dusmanlar, key=self.cana_gore_sirala, reverse=True
                )[:1]
                self.saldir(savasci, siralanmis_dusmanlar)

            elif isinstance(savasci, Atli):
                siralanmis_dusmanlar = sorted(
                    dusmanlar, key=self.kaynaga_gore_sirala, reverse=True
                )[:2]
                self.saldir(savasci, siralanmis_dusmanlar)

            elif isinstance(savasci, Saglikci):
                siralanmis_dusmanlar = sorted(dusmanlar, key=self.cana_gore_sirala)[:3]
                self.saldir(savasci, siralanmis_dusmanlar)

        self.map.render()

    def saldir(self, savasci, dusmanlar):
        for dusman in dusmanlar:
            kalan_can = savasci.saldir(dusman)
            if kalan_can <= 0:
                self.savasci_sil(dusman)

    def savasci_sil(self, savasci):
        tur = 0
        if isinstance(savasci, Muhafiz):
            tur = 0
        elif isinstance(savasci, Okcu):
            tur = 1
        elif isinstance(savasci, Topcu):
            tur = 2
        elif isinstance(savasci, Atli):
            tur = 3
        elif isinstance(savasci, Saglikci):
            tur = 4

        self.map.savasci_sil(savasci, tur)
        self.savascilar.remove(savasci)

        for oyuncu in self.oyuncular:
            if oyuncu.renk == savasci.renk:
                kalan_savasci = oyuncu.savasci_sil(savasci, tur)
                if kalan_savasci == 0:
                    self.oyuncular.remove(oyuncu)
                    self.oyuncu_sayisi -= 1

    def oyna(self, id):
        oyuncu = self.oyuncular[id]
        print(Text(f"Oyun sırası: {oyuncu.isim()}", style=oyuncu.renk))
        sayac = 0

        while sayac < 2:
            print(Text("[X] ", style=oyuncu.renk), end="")
            pas_gec = self.pas_gec(oyuncu)

            if pas_gec:
                print("1. Muhafız")
                print("2. Okçu")
                print("3. Topçu")
                print("4. Atlı")
                print("5. Sağlıkçı")
                print(Text("[X] ", style=oyuncu.renk), end="")
                savasci_turu = tam_sayi_al(
                    "Koymak istediğiniz savaşçı türünü giriniz: "
                )
                while True:
                    x = tam_sayi_al("X koordinatını giriniz: ")
                    y = tam_sayi_al("Y koordinatını giriniz: ")
                    komsular = oyuncu.komsular()
                    if [x, y] in komsular:
                        if (
                            self.map.matris[y][x] == 0
                            or self.map.matris[y][x].renk == oyuncu.renk
                        ):
                            self.savasci_koy(x, y, savasci_turu, oyuncu, False)
                            break
                        else:
                            print("Koordinatta rakip asker var!")
                    else:
                        print("Uygun koordinat giriniz!")
                        print(komsular)
            else:
                break

            sayac += 1
            oyuncu.kaynak += 10 + oyuncu.savasci_sayisi
            self.map.render()

    def savasci_koy(self, x, y, savasci_turu, oyuncu, baslangic=False):
        if baslangic:
            oyuncu.muhafiz_sayisi += 1
            self.savascilar.append(self.map.muhafiz_koy(x, y, oyuncu))
        else:
            savasci = None
            if savasci_turu == 1:
                savasci = self.muhafiz_koy(x, y, oyuncu)
            elif savasci_turu == 2:
                savasci = self.okcu_koy(x, y, oyuncu)
            elif savasci_turu == 3:
                savasci = self.topcu_koy(x, y, oyuncu)
            elif savasci_turu == 4:
                savasci = self.atli_koy(x, y, oyuncu)
            elif savasci_turu == 5:
                savasci = self.saglikci_koy(x, y, oyuncu)

            self.savascilar.append(savasci)

            return savasci

    def muhafiz_koy(self, x, y, oyuncu):
        oyuncu.muhafiz_sayisi += 1
        muhafiz = self.map.muhafiz_koy(x, y, oyuncu)
        oyuncu.kaynak -= muhafiz.kaynak
        self.map.render()
        return muhafiz

    def okcu_koy(self, x, y, oyuncu):
        oyuncu.okcu_sayisi += 1
        okcu = self.map.okcu_koy(x, y, oyuncu)
        oyuncu.kaynak -= okcu.kaynak
        self.map.render()
        return okcu

    def topcu_koy(self, x, y, oyuncu):
        oyuncu.topcu_sayisi += 1
        topcu = self.map.topcu_koy(x, y, oyuncu)
        oyuncu.kaynak -= topcu.kaynak
        self.map.render()
        return topcu

    def atli_koy(self, x, y, oyuncu):
        oyuncu.atli_sayisi += 1
        atli = self.map.atli_koy(x, y, oyuncu)
        oyuncu.kaynak -= atli.kaynak
        self.map.render()
        return atli

    def saglikci_koy(self, x, y, oyuncu):
        oyuncu.saglikci_sayisi += 1
        saglikci = self.map.saglikci_koy(x, y, oyuncu)
        oyuncu.kaynak -= saglikci.kaynak
        self.map.render()
        return saglikci


if __name__ == "__main__":
    oyun = Game()
    """        
                            ### TODO ###
    #################################################################
    # * Hasar alma X                                                #
    # * Kaynak azaltma X                                            #
    # * Her tur kaynak kazanımı X                                   #
    # * Oyun bitirme koşulu X                                       #
    # * Var olan askerin üzerine koyma X                            #
    # * Sırayla saldırma X                                          #
    # * Herkes yerleştirdikten sonra saldırma X                     #
    # * Yapay zeka                                                  #
    # * Tek oyuncu kaldıysa oyunu bitir X                           #
    # * Rakip düşmanın üzerine asker konamaz X                      #
    # * Oyuncu öldükten sonra oyundan çıkar ve askerlerini sil. X   #
    #################################################################

    """
