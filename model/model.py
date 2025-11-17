import copy

from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        consumi=[]
        a=ConsumoDAO.get_consumi(1)
        b=ConsumoDAO.get_consumi(2)
        media=0
        i=0
        for c in a:
            if c.data.month==mese:
                media=c.kwh+media
                i=i+1
        media=media/i
        consumi.append(("Impianto A",media))
        media = 0
        i=0
        for c in b:
            if c.data.month==mese:
                media=c.kwh+media
                i=i+1
        media=media/i
        consumi.append(("Impianto B",media))
        return consumi

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno > 7:
            if  self.__costo_ottimo == -1 or self.__costo_ottimo > int(costo_corrente):
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = copy.deepcopy(sequenza_parziale)
            #print(sequenza_parziale)
            #print(self.__costo_ottimo)
            #print(self.__sequenza_ottima)
        else:
            for j in range(1,3):
                old_ultimo = ultimo_impianto
                old_costo = costo_corrente
                if ultimo_impianto == None or ultimo_impianto== j:
                    u=0
                else:
                    u=5
                sequenza_parziale.append(j)
                ultimo_impianto = j
                costo_corrente += consumi_settimana.get(j)[giorno-1]+u
                self.__ricorsione(sequenza_parziale,giorno+1,ultimo_impianto,costo_corrente,consumi_settimana)
                sequenza_parziale.pop()
                ultimo_impianto = old_ultimo
                costo_corrente = old_costo

            """
            a=0
            b=0
            if ultimo_impianto==1:
                b=5
            elif ultimo_impianto==2:
                a=5
            #print(consumi_settimana.get(1)[giorno-1])
            #print(a,b)
            if (consumi_settimana.get(1)[giorno-1]+a)<(consumi_settimana.get(2)[giorno-1]+b):

                sequenza_parziale.append(1)
                ultimo_impianto=1
                costo_corrente=costo_corrente+consumi_settimana.get(1)[giorno-1]+a
            else:
                sequenza_parziale.append(2)
                ultimo_impianto=2
                costo_corrente=costo_corrente+consumi_settimana.get(2)[giorno-1]+b
            #print(costo_corrente)
            print(sequenza_parziale)
            self.__ricorsione(sequenza_parziale,giorno+1,ultimo_impianto,costo_corrente,consumi_settimana)
            """


    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        a = ConsumoDAO.get_consumi(1)
        b = ConsumoDAO.get_consumi(2)
        somma = []
        for c in a:
            if c.data.month == mese:
                if c.data.day<=7:
                    somma.append(c.kwh)
        somma_b = []
        for c in b:
            if c.data.month == mese:
                if c.data.day<=7:
                    somma_b.append(c.kwh)
        consumi={1:somma, 2:somma_b}
        #print(consumi)
        return consumi


