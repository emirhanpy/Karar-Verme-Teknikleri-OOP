import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class BelirsizlikAltindaKararVerme():
    def __init__(self):
        """
            Belirsizlik Altında Karar Verme problemi için bir sınıf oluşturulur.

            Kullanıcıdan aşağıdaki bilgileri alarak sınıfı başlatır:
            - problem_turu (str): 'K' (kazanç) veya 'M' (maliyet) olarak belirtilen problem türü.
            - secenek_sayisi (int): Karar verilebilecek seçenek sayısı.
            - dogaldurum_sayisi (int): Doğal durumların sayısı.
            - hurwicz (float): Hurwicz ölçütü için α değeri.

            Sınıf özellikleri:
            - matris (list): Kullanıcının girdiği (secenek_sayisi * dogaldurum_sayisi) boyutunda karar matrisi.
            - np_matris (NumPy array): Karar matrisini NumPy array formatına dönüştürür.
            - secenekler (list): Kullanıcının girdiği seçenek başlıkları.
            - dogal_durumlar (list): Kullanıcının girdiği doğal durum başlıkları.
            - df (pd.DataFrame): Karar matrisini içeren bir Pandas DataFrame.
            - hesaplamalari_yap (method): Karar verme ölçütlerini hesaplayıp sonuçları yazdırır.
            """

        self.problem_turu = self.problem_secimi()
        self.secenek_sayisi, self.dogaldurum_sayisi = self.matris_boyut()
        self.hurwicz, self.hurwicz_olumsuz = self.hurwicz_degeri_al()
        self.matris = self.matris_olustur()
        self.np_matris = np.array(self.matris)
        self.secenekler = self.secenekler_gir()
        self.dogal_durumlar = self.dogal_durumlar_gir()
        self.df = pd.DataFrame(self.matris, index=self.secenekler, columns=self.dogal_durumlar)
        self.hesaplamalari_yazdir()

    def problem_secimi(self):
        """
            Kullanıcının problem türünü girmesini sağlar ve hata kontrolü yapar.

            Return:
            - problem_turu (str): Kullanıcının girdiği problem türünü temsil eden "K" (kazanç) veya "M" (maliyet) değeri.
            """
        while True:
            problem_turu = input("Eğer problem türünüz kazanç ise 'K', maliyet ise 'M' yazınız: ")

            if problem_turu.upper() not in ["K", "M"]:
                print("Hata: Geçersiz giriş. Lütfen 'K' veya 'M' girin.")
                continue
            else:
                break
        return problem_turu

    def matris_boyut(self):
        """
            Kullanıcının seçenek ve doğal durum sayılarını girmesini sağlar ve hata kontrolü yapar.

            Returns:
            - secenek_sayisi (int): Kullanıcının girdiği seçenek sayısını temsil eden pozitif tam sayı değeri.
            - dogaldurum_sayisi (int): Kullanıcının girdiği doğal durum sayısını temsil eden pozitif tam sayı değeri.
            """
        while True:
            try:
                secenek_sayisi = int(input("Kaç adet seçeneğiniz var? "))
                dogaldurum_sayisi = int(input("Kaç adet doğal durumunuz var? "))

                if secenek_sayisi <= 0 or dogaldurum_sayisi <= 0:
                    raise ValueError("Hata: İstenen değerler sıfırdan büyük olmalıdır.")

            except ValueError:
                print("Hatalı giriş. Lütfen pozitif tam sayı girin.")
                continue

            return secenek_sayisi, dogaldurum_sayisi

    def hurwicz_degeri_al(self):
        """
            Kullanıcının Hurwicz kriteri için α değerini girmesini sağlar ve hata kontrolü yapar.

            Returns:
            - hurwicz (float): Kullanıcının girdiği α değerini temsil eden bir ondalık sayı.
            - hurwicz_olumsuz (float): Hurwicz kriteri için α değerinin olumsuz durumunu temsil eden bir ondalık sayı.
            """
        while True:
            try:
                hurwicz = float(input("Hurwicz(α) değerini giriniz: "))

                if 0 <= hurwicz <= 1:
                    return hurwicz, 1 - hurwicz
                else:
                    print("Hata: Geçersiz giriş yaptınız. Lütfen 0 ile 1 arasında bir değer girin.")

            except ValueError:
                print("Hata: Geçersiz giriş yaptınız. Lütfen sayısal bir değer girin.")

    def matris_olustur(self):
        """
            Kullanıcıdan belirtilen boyuttaki bir karar matrisini girmesini sağlar ve hata kontrolü yapar.

            Return:
            - matris (list): Kullanıcının girdiği karar matrisini temsil eden bir liste.
            """
        while True:
            print(f"{self.secenek_sayisi}*{self.dogaldurum_sayisi} karar matrisinin elemanlarını boşluk bırakarak girin.")

            matris = []
            for i in range(self.secenek_sayisi):
                try:
                    satir = list(map(float, input(f'{i + 1}. satır: ').split()))

                    if len(satir) != self.dogaldurum_sayisi:
                        raise ValueError("Hata: Girilen satırın uzunluğu, matrisin doğal durum sayısı ile eşleşmiyor.")
                    matris.append(satir)

                except ValueError:
                    print("Hatalı giriş. Lütfen sayısal bir değer girin.")
                    break

            if len(matris) == self.secenek_sayisi:
                return matris

    def secenekler_gir(self):
        """
            Kullanıcıdan seçenek isimlerini alır ve hata kontrolü yapar.

            Return:
            secenekler (List) : Kullanıcının girdiği seçenek isimlerini içeren bir liste.
            """

        while True:
            secenekler = input(
                "Seçenekleri aralarında boşluk bırakarak, birleşik olacak şekilde giriniz: (ör: OyunYazılımı)").split()

            if len(secenekler) != self.secenek_sayisi:
                print("Hata: Girilen seçenek isimleri, matrisin seçenek sayısı ile eşleşmiyor!\n")
            else:
                return secenekler

    def dogal_durumlar_gir(self):
        """
            Kullanıcıdan doğal durum başlıklarını alır ve hata kontrolü yapar.

            Return:
            dogal_durumlar (List) : Kullanıcının girdiği doğal durum başlıklarını içeren bir liste.
            """

        while True:
            dogal_durumlar = input(
                "Doğal durumları aralarında boşluk bırakarak, birleşik olacak şekilde giriniz: (ör: DüşükTalep) ").split()

            if len(dogal_durumlar) != self.dogaldurum_sayisi:
                print("Hata: Girilen doğal durum başlıkları, matrisin doğal durum sayısı ile eşleşmiyor!\n")
            else:
                return dogal_durumlar

    def laplace_kriteri(self):
        """
            Laplace kriterine göre kazanç veya maliyet durumunu hesaplar.

            Returns:
            - laplace_index (str): Bulunan durumun indeksi.
            - laplace_toplam (float): Toplam değeri.
            """
        toplam_satir = self.np_matris.sum(axis=1)

        if self.problem_turu == 'K':
            laplace_deger = np.max(toplam_satir)
        else:
            laplace_deger = np.min(toplam_satir)

        laplace_sonuclar = []
        for i in range(len(toplam_satir)):
            if toplam_satir[i] == laplace_deger:
                laplace_sonuclar.append(i)
        laplace_index = ', '.join(self.df.index[laplace_sonuclar])

        return laplace_index, laplace_deger

    def firsat_kaybi(self):
        """
            Fırsat kaybını hesaplar ve çıktı için gereken bilgileri içeren üç ayrı değeri döndürür.

            Returns:
            - fk_df (pd.DataFrame): Fırsat kaybını içeren bir DataFrame.
            - firsat_kaybi (float): Fırsat kaybı değeri.
            - fk_index (str): Fırsat kaybının olduğu durumların indeksleri.
            """

        if self.problem_turu == 'K':
            fk_matris = abs(self.matris - np.max(self.matris, axis=0))
        else:
            fk_matris = abs(self.matris - np.min(self.matris, axis=0))

        fk_df = pd.DataFrame(fk_matris, index=self.secenekler, columns=self.dogal_durumlar)

        en_buyukler = np.max(fk_matris, axis=1)
        firsat_kaybi = np.min(en_buyukler)

        fk_sonuc = []
        for i in range(len(en_buyukler)):
            if np.max(fk_matris[i]) == firsat_kaybi:
                fk_sonuc.append(fk_df.index[i])
        fk_index = ', '.join(fk_sonuc)

        return fk_df, firsat_kaybi, fk_index

    def olcutleri_hesapla(self):
        """
            Belirtilen probleme göre iyimserlik, kötumserlik ve hurwicz değerlerini hesaplar,
            gerekli bilgileri içeren altı ayrı değeri döndürür.

            Returns:
            - iyimserlik_degeri (float): İyimserlik değeri.
            - kotumserlik_degeri (float): Kötümserlik değeri.
            - iyimserlik_index (str): İyimserlik durumunun indeksleri.
            - kotumserlik_index (str): Kötümserlik durumunun indeksleri.
            - hurwicz_degeri (float): Hurwicz kriterine göre değer.
            - hurwicz_index (str): Hurwicz kriterine göre durumun indeksi.
        """

        if self.problem_turu == 'K':

            en_buyukler = np.max(self.np_matris, axis=1)
            en_kucukler = np.min(self.np_matris, axis=1)

            iyimserlik_degeri = np.max(en_buyukler)
            kotumserlik_degeri = np.max(en_kucukler)

            iyimserlik_sonuc = []
            for i in range(len(en_buyukler)):
                if iyimserlik_degeri == np.max(self.matris[i]):
                    iyimserlik_sonuc.append(self.df.index[i])
            iyimserlik_index = ', '.join(iyimserlik_sonuc)

            kotumserlik_sonuc = []
            for i in range(len(en_kucukler)):
                if kotumserlik_degeri == np.min(self.matris[i]):
                    kotumserlik_sonuc.append(self.df.index[i])
            kotumserlik_index = ', '.join(kotumserlik_sonuc)

            hurwicz_degeri = self.hurwicz * en_buyukler + self.hurwicz_olumsuz * en_kucukler

            hurwicz_sonuc = []
            for i in range(len(hurwicz_degeri)):
                if hurwicz_degeri[i] == np.max(hurwicz_degeri):
                    hurwicz_sonuc.append(self.df.index[i])
            hurwicz_index = ', '.join(hurwicz_sonuc)

            hurwicz_degeri = max(hurwicz_degeri)

        else:

            en_buyukler = np.min(self.np_matris, axis=1)
            en_kucukler = np.max(self.np_matris, axis=1)

            iyimserlik_degeri = np.min(en_buyukler)
            kotumserlik_degeri = np.min(en_kucukler)

            iyimserlik_sonuc = []
            for i in range(len(en_buyukler)):
                if iyimserlik_degeri == np.min(self.np_matris[i]):
                    iyimserlik_sonuc.append(self.df.index[i])
            iyimserlik_index = ', '.join(iyimserlik_sonuc)

            kotumserlik_sonuc = []
            for i in range(len(en_kucukler)):
                if kotumserlik_degeri == np.max(self.np_matris[i]):
                    kotumserlik_sonuc.append(self.df.index[i])
            kotumserlik_index = ', '.join(kotumserlik_sonuc)

            hurwicz_degeri = self.hurwicz * en_buyukler + self.hurwicz_olumsuz * en_kucukler

            hurwicz_sonuc = []
            for i in range(len(hurwicz_degeri)):
                if hurwicz_degeri[i] == np.min(hurwicz_degeri):
                    hurwicz_sonuc.append(self.df.index[i])
            hurwicz_index = ', '.join(hurwicz_sonuc)

            hurwicz_degeri = min(hurwicz_degeri)

        return iyimserlik_degeri, kotumserlik_degeri, iyimserlik_index, kotumserlik_index, hurwicz_degeri, hurwicz_index


    def veri_gorsellestirme(self, iyimserlik_degeri, kotumserlik_degeri, laplace_degeri, hurwicz_degeri, firsat_kaybi):
        """
            Karar ölçütlerini görselleştirmek için bir sütun grafiği oluşturur.

            Parameters:
            - iyimserlik_degeri (float): İyimserlik değeri.
            - kotumserlik_degeri (float): Kötümserlik değeri.
            - laplace_degeri (float): Laplace kriterine göre değer.
            - hurwicz_degeri (float): Hurwicz kriterine göre değer.
            - firsat_kaybi (float): Fırsat kaybı değeri.

            Returns:
            None: Sütun grafiği ekranda gösterir.
            """

        olcutler = ['İyimserlik', 'Kötümserlik', 'Eş-Olasılık', 'Hurwicz', 'Pişmanlık']
        degerler = [iyimserlik_degeri, kotumserlik_degeri, laplace_degeri, hurwicz_degeri, firsat_kaybi]

        sns.set(style="darkgrid")
        plt.figure(figsize=(14, 8))
        sns.barplot(x=olcutler, y=degerler, palette="tab10")
        plt.title('Karar Ölçütlerinin Değerleri', fontsize=36)
        plt.xlabel('Karar Ölçütleri', fontsize=26)
        plt.ylabel('Değerler', fontsize=26)
        plt.tick_params(axis='x', labelsize=22)
        plt.tick_params(axis='y', labelsize=22)
        plt.show()


    def hesaplamalari_yazdir(self):
        """
            Hesaplamaların sonuçları ekrana yazdırılır ve veri görselleştirmesi yapar.
            """

        iyimserlik_degeri, kotumserlik_degeri, iyimserlik_index, kotumserlik_index, hurwicz_degeri, \
        hurwicz_index = self.olcutleri_hesapla()
        laplace_index, laplace_deger = self.laplace_kriteri()
        laplace_degeri = laplace_deger / self.np_matris.shape[1]
        fk_df, firsat_kaybi, fk_index = self.firsat_kaybi()

        print("\n\n\nKARAR MATRİSİ;")
        print(f'{self.df}\n')

        print(f"İyimserlik ölçütüne göre kararınız {iyimserlik_index} olmalıdır.")
        print(f"Değer: {iyimserlik_degeri}\n")

        print(f"Kötümserlik ölçütüne göre kararınız {kotumserlik_index} olmalıdır.")
        print(f"Değer: {kotumserlik_degeri}\n")

        print(f"Laplace kriterine göre kararınız {laplace_index} olmalıdır.")
        print(f"Değer: {laplace_degeri}\n")

        print(f"Hurwicz ölçütüne göre kararınız {hurwicz_index} olmalıdır.")
        print(f"Değer: {hurwicz_degeri}\n")

        print("FIRSAT KAYIPLARI MATRİSİ;")
        print(f'{fk_df}\n')

        print(f"Fırsat kaybı ölçütüne göre kararınız {fk_index} olmalıdır.")
        print(f"Değer: {firsat_kaybi}")

        self.veri_gorsellestirme(iyimserlik_degeri, kotumserlik_degeri, laplace_degeri, hurwicz_degeri, firsat_kaybi)


class RiskAltindaKararVerme():
    def __init__(self):
        """
            Risk Altında Karar Verme problemini çözmek için bir sınıf başlatır.

            Kullanıcıdan aşağıdaki bilgileri alarak sınıfı başlatır:
            - problem_turu (str): 'K' (kazanç) veya 'M' (maliyet) olarak belirtilen problem türü.
            - secenek_sayisi (int): Karar verilebilecek seçenek sayısı.
            - dogaldurum_sayisi (int): Doğal durumların sayısı.
            - matris (list): Kullanıcının girdiği (secenek_sayisi * dogaldurum_sayisi) boyutunda, bir karar matrisi.
            - np_matris (NumPy array): Karar matrisini NumPy array formatına dönüştürür.
            - secenekler (list): Kullanıcının girdiği seçenekler.
            - dogal_durumlar (list): Kullanıcının girdiği doğal durum başlıkları.
            - olasiliklar (list): Kullanıcının girdiği doğal durum olasılıkları.
            - df (pd.DataFrame): Karar matrisini içeren bir DataFrame.
            - hesaplamalar (method): Karar verme ölçütlerini ve beklenen değerleri hesaplayan bir method.
            """

        self.problem_turu = self.problem_secimi()
        self.secenek_sayisi, self.dogaldurum_sayisi = self.matris_boyut()
        self.matris = self.matris_olustur()
        self.np_matris = np.array(self.matris)
        self.secenekler = self.secenekler_gir()
        self.dogal_durumlar = self.dogal_durumlar_gir()
        self.olasiliklar = self.olasiliklar_gir()
        self.df = pd.DataFrame(self.matris, index=self.secenekler, columns=self.dogal_durumlar)
        self.hesaplamalar = self.hesaplamalari_yap()

    def problem_secimi(self):
        """
            Kullanıcının problem türünü girmesini sağlar ve hata kontrolü yapar.

            Return:
            - problem_turu (str): Kullanıcının girdiği problem türünü temsil eden "K" (kazanç) veya "M" (maliyet) değeri.
            """
        while True:
            problem_turu = input("Eğer problem türünüz kazanç ise 'K', maliyet ise 'M' yazınız: ")

            if problem_turu.upper() not in ["K", "M"]:
                print("Hata: Geçersiz giriş. Lütfen 'K' veya 'M' girin.")
                continue
            else:
                break
        return problem_turu

    def matris_boyut(self):
        """
            Kullanıcının seçenek ve doğal durum sayılarını girmesini sağlar ve hata kontrolü yapar.

            Returns:
            - secenek_sayisi (int): Kullanıcının girdiği seçenek sayısını temsil eden pozitif tam sayı değeri.
            - dogaldurum_sayisi (int): Kullanıcının girdiği doğal durum sayısını temsil eden pozitif tam sayı değeri.
            """
        while True:
            try:
                secenek_sayisi = int(input("Kaç adet seçeneğiniz var? "))
                dogaldurum_sayisi = int(input("Kaç adet doğal durumunuz var? "))

                if secenek_sayisi <= 0 or dogaldurum_sayisi <= 0:
                    raise ValueError("Hata: İstenen değerler sıfırdan büyük olmalıdır.")

            except ValueError:
                print("Hatalı giriş. Lütfen pozitif tam sayı girin.")
                continue

            return secenek_sayisi, dogaldurum_sayisi

    def matris_olustur(self):
        """
            Kullanıcıdan belirtilen boyuttaki bir karar matrisini girmesini sağlar ve hata kontrolü yapar.

            Return:
            - matris (list): Kullanıcının girdiği karar matrisini temsil eden bir liste.
            """
        while True:
            print(f"{self.secenek_sayisi}*{self.dogaldurum_sayisi} karar matrisinin elemanlarını boşluk bırakarak girin.")

            matris = []
            for i in range(self.secenek_sayisi):
                try:
                    satir = list(map(float, input(f'{i + 1}. satır: ').split()))

                    if len(satir) != self.dogaldurum_sayisi:
                        raise ValueError("Hata: Girilen satırın uzunluğu, matrisin doğal durum sayısı ile eşleşmiyor.")
                    matris.append(satir)

                except ValueError as h:
                    print(h)
                    print("Hatalı giriş. Lütfen tekrar deneyin.")
                    break

            if len(matris) == self.secenek_sayisi:
                return matris

    def secenekler_gir(self):
        """
            Kullanıcıdan seçenek isimlerini alır ve hata kontrolü yapar.

            Return:
            secenekler (List) : Kullanıcının girdiği seçenek isimlerini içeren bir liste.
            """

        while True:
            secenekler = input("Seçenekleri aralarında boşluk bırakarak giriniz: ").split()

            if len(secenekler) != self.secenek_sayisi:
                print("Hata: Girilen seçenek isimleri, matrisin seçenek sayısı ile eşleşmiyor!\n")
            else:
                return secenekler

    def dogal_durumlar_gir(self):
        """
            Kullanıcıdan doğal durum başlıklarını alır ve hata kontrolü yapar.

            Return:
            dogal_durumlar (List) : Kullanıcının girdiği doğal durum başlıklarını içeren bir liste.
            """

        while True:
            dogal_durumlar = input(
                "Doğal durumları aralarında boşluk bırakarak, birleşik olacak şekilde giriniz: (ör: DüşükTalep) ").split()

            if len(dogal_durumlar) != self.dogaldurum_sayisi:
                print("Hata: Girilen doğal durum başlıkları, matrisin doğal durum sayısı ile eşleşmiyor!\n")
            else:
                return dogal_durumlar

    def olasiliklar_gir(self):
        """
            Kullanıcıdan doğal durum olasılıklarını girmesini isteyen ve girilen değerleri kontrol eden bir fonksiyon.

            Return:
            - olasiliklar (list): Kullanıcının girdiği doğal durum olasılıklarını içeren bir liste.
            """

        while True:
            try:
                olasiliklar = list(map(float, input(f'Olasılıkları aralarında boşluk bırakarak giriniz: ').split()))

                if len(olasiliklar) != self.dogaldurum_sayisi:
                    raise ValueError("Hata: Girilen olasılık sayısı, matrisin doğal durum sayısı ile eşleşmiyor.")

                if any(olasilik < 0 or olasilik > 1 for olasilik in olasiliklar):
                    raise ValueError("Hata: Olasılıklar 0 ile 1 arasında olmalıdır.")

                if sum(olasiliklar) != 1:
                    raise ValueError("Hata: Girilen olasılıkların toplamı 1'e eşit olmalıdır.")

                return olasiliklar

            except ValueError:
                print("Hatalı giriş. Lütfen sayısal bir değer girin.")

    def veri_gorsellestirme(self):
        """
            Seçeneklerin beklenen değerlerini sütun grafiği ile görselleştirir ve beklenen değer noktalarını işaretler.

            Return:
            None: Sütun grafiğini ekranda gösterir.
            """
        plt.figure(figsize=(12, 6))
        sns.set(style='darkgrid')
        sns.lineplot(x=self.df.index, y=self.df['Beklenen Değerler'], marker='o', color='b')
        plt.xlabel('Seçenekler', fontsize=18)
        plt.ylabel('Beklenen Değerler', fontsize=18)
        plt.title('Seçeneklerin Beklenen Değerleri', fontsize=22)
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        plt.show()

    def karar_matrisi(self):
        """
            Beklenen değerleri hesaplar ve ölçütlere göre en uygun kararı belirler.

            Returns:
            bd_index (str): En uygun kararın indeksi
            bd (float) : Beklenen değeri içeren bir tuple.
            """

        sonuc = np.sum(self.np_matris * np.array(self.olasiliklar), axis=1)
        self.df['Beklenen Değerler'] = sonuc

        if self.problem_turu == 'K':
            bd = max(sonuc)
        else:
            bd = min(sonuc)

        eslesen_satirlar = self.df.index[self.df['Beklenen Değerler'] == bd].tolist()
        bd_index = ', '.join(eslesen_satirlar)

        return bd_index, bd

    def firsat_kaybi(self):
        """
            Fırsat kaybını hesaplar ve gerekli bilgileri içeren üç ayrı değeri döndürür.

            Returns:
            fk_df (pd.DataFrame): Fırsat kaybını içeren DataFrame.
            firsat_kaybi (float): Fırsat kaybı değeri
            bfk (NumPy.Array): Beklenen fırsat kaybı değerlerini içeren bir NumPy array.
            """

        if self.problem_turu == 'K':
            fk_matris = abs(self.matris - np.max(self.matris, axis=0))
        else:
            fk_matris = abs(self.matris - np.min(self.matris, axis=0))

        fk_df = pd.DataFrame(fk_matris, index=self.secenekler, columns=self.dogal_durumlar)

        en_buyukler = np.max(fk_matris, axis=1)
        firsat_kaybi = np.min(en_buyukler)

        fk_sonuc = []
        for i in range(len(en_buyukler)):
            if firsat_kaybi == np.max(fk_matris[i]):
                fk_sonuc.append(fk_df.index[i])
        fk_index = ', '.join(fk_sonuc)

        bfk = np.sum(fk_matris * np.array(self.olasiliklar), axis=1)
        fk_df['BFK'] = bfk

        return fk_df, firsat_kaybi, bfk

    def firsat_kaybi_gorsellestir(self):
        """
            Fırsat kaybı matrisini görselleştirir ve ekrana çizdirir.

            Return:
            None: Çizgi grafiğini ekranda gösterir.
            """

        fk_df, _, _ = self.firsat_kaybi()
        plt.figure(figsize=(12, 6))
        sns.set(style='darkgrid')
        sns.lineplot(x=fk_df.index, y=fk_df['BFK'], marker='o', color='r')
        plt.xlabel('Seçenekler', fontsize=18)
        plt.ylabel('Fırsat Kayıpları', fontsize=18)
        plt.title('Beklenen Değerlerin Fırsat Kaybı', fontsize=22)
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        plt.show()

    def olasilik_kriteri(self):
        """
            Olasılık kriterine göre  problem türü üzerinden en uygun doğal durumu belirler ve değerleri döndürür.

            Returns:
            - sut_deger (float): Olasılık kriterine göre seçilen doğal durumun değeri.
            - sut_index (str): Olasılık kriterine göre seçilen doğal durumun hangi sütuna ait olduğu.
            """

        max_olasilik = max(self.olasiliklar)
        max_index = self.olasiliklar.index(max_olasilik)

        if self.problem_turu == 'K':
            sut_deger = self.df[self.df.columns[max_index]].max()
            sut_index = self.df.columns[max_index]
        else:
            sut_deger = self.df[self.df.columns[max_index]].min()
            sut_index = self.df.columns[max_index]

        return sut_deger, sut_index

    def hesaplamalari_yap(self):
        """
            Beklenen değeri, karar matrisini, olasılık kriterini hesaplar ve görselleştirmeyi yapar.
            Son olarak sonuçları ekrana yazdırır.
            """

        bd_index, bd = self.karar_matrisi()
        sut_deger, sut_index = self.olasilik_kriteri()
        fk_df, firsat_kaybi, bfk = self.firsat_kaybi()
        print("\nKARAR MATRİSİ;")
        print(f'\n\n\n{self.df}')

        if self.problem_turu == 'K':
            self.df['Tam Bilgi ile BD'] = self.df['Beklenen Değerler'] + fk_df['BFK']
        else:
            self.df['Tam Bilgi ile BD'] = abs(self.df['Beklenen Değerler'] - fk_df['BFK'])

        tam_bilgi_degerleri = self.df['Tam Bilgi ile BD'].tolist()
        tam_bilgi_degeri = tam_bilgi_degerleri[0]


        print(f'\nBeklenen değere göre kararınız {bd_index} olmalıdır.\nDeğer:{bd}')
        print(f'\nTam bilgi ile BD: {tam_bilgi_degeri}')
        print(f'\nOlasılık kriterine göre seçilen doğal durum {sut_index} olmalıdır.\nDeğer: {sut_deger}')
        self.veri_gorsellestirme()

        print("\nFIRSAT KAYIPLARI MATRİSİ;")
        print(fk_df)
        self.firsat_kaybi_gorsellestir()
        print(f'\nTam bilgiye harcanması gereken maksimum tutar: {min(bfk)}')




# Kullanım için bir örnek
def main():
    problem = 0
    while True:
            problem_cesidi = input(
                "Karar verme probleminizdeki doğal durumların olasılıklarını biliyor musunuz ? (E/H) yazınız ")
            if problem_cesidi.upper() not in ["E", "H"]:
                print("Geçersiz giriş! Sadece 'E' veya 'H' giriniz.")
                continue
            else:
                break
    if problem_cesidi == 'H':
        problem = 0
    elif problem_cesidi == 'E':
        problem += 1

    if problem == 0:
        BelirsizlikAltindaKararVerme()
    else:
        RiskAltindaKararVerme()

if __name__ == "__main__":
    main()
