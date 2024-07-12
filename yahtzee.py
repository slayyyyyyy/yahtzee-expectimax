from random import randint, random
import itertools

def roll():
    return [randint(1, 6) for _ in range(5)]

def valideaza_input(prompt, raspuns_valid):
    raspuns = input(prompt).strip().lower()
    while raspuns not in raspuns_valid:
        print("INPUT INCORECT\n")
        raspuns = input(prompt).strip().lower()
    return raspuns

def swap(lista_zaruri):
    while True:
        swap_zaruri = input("Cu ce zaruri vrei să mai dai o dată? (1-5) ").replace(",", "").replace(" ", "")
        if all(d.isdigit() and 1 <= int(d) <= 5 for d in swap_zaruri):
            break
        print("INPUT INCORECT")
    swap_zar = [int(d) - 1 for d in swap_zaruri]
    for index in swap_zar:
        lista_zaruri[index] = randint(1, 6)
    return lista_zaruri, swap_zar

def tip_roll(lista_zaruri):
    valori_zaruri = {x: lista_zaruri.count(x) for x in set(lista_zaruri)}
    valori_unice_zaruri = sorted(set(lista_zaruri))
    rezultat = {
        "THREE OF A KIND": 3 in valori_zaruri.values() and len(valori_zaruri) > 2,
        "SMALL STRAIGHT": any(
            valori_unice_zaruri[i:i + 4] in [list(range(x, x + 4)) for x in range(1, 4)] for i in range(len(valori_unice_zaruri) - 3)
        )
    }
    return rezultat

# consideram toate combinatiile UNICE prin
combinatii = []
for a1 in range(1, 7):
        for a2 in range(a1, 7):
            for a3 in range(a2, 7):
                for a4 in range(a3, 7):
                    for a5 in range(a4, 7):
                        combinatii.append([a1, a2, a3, a4, a5])

#print(combinatii)
#print(len(combinatii))

fullhouse = [[1, 1, 1, 1, 1], [1, 1, 1, 2, 2], [1,1,1,3,3], [1,1,1,4,4], [1,1,1,5,5],
             [1,1,1,6,6], [2,2,2,2,2], [2,2,2,3,3], [2,2,2,4,4], [2,2,2,5,5], [2,2,2,6,6],
             [3,3,3,3,3], [3,3,3,4,4], [3,3,3,5,5], [3,3,3,6,6], [4,4,4,4,4], [4,4,4,5,5],
             [4,4,4,6,6], [5,5,5,5,5], [5,5,5,6,6], [6,6,6,6,6]]
smallstraight = [[1,1,2,3,4], [1,2,2,3,4], [1,2,3,3,4], [1,2,3,4,4], [1,2,3,4,5],
                 [1,2,3,4,6], [2,2,3,4,5], [2,3,3,4,5], [2,3,4,4,5], [2,3,4,5,5],
                 [2,3,4,5,6], [1,3,4,5,6], [3,3,4,5,6], [3,4,4,5,6], [3,4,5,5,6], [3,4,5,6,6]]


def euristica_simpla():
    score = 0
    roll_1 = roll()
    roll_1.sort()

    if roll_1 in fullhouse:
        score = 25
    elif roll_1 in smallstraight:
        score = 30
    else:
        roll_2 = roll()
        roll_2.sort()

        if roll_2 in fullhouse:
            score = 25
        elif roll_2 in smallstraight:
            score = 30
        else:
            roll_3 = roll()
            roll_3.sort()

            if roll_3 in fullhouse:
                score = 25
            elif roll_3 in smallstraight:
                score = 30
    roll2_1 = roll()
    roll2_1.sort()
    if score == 25:
        if roll2_1 in smallstraight:
            score = 55
        else:
            roll2_2 = roll()
            roll2_2.sort()
            if roll2_2 in smallstraight:
                score = 55
            else:
                roll2_3 = roll()
                roll2_3.sort()
                if roll2_3 in smallstraight:
                    score = 55
    elif score == 30:
        if roll2_1 in fullhouse:
            score = 55
        else:
            roll2_2 = roll()
            roll2_2.sort()
            if roll2_2 in fullhouse:
                score = 55
            else:
                roll2_3 = roll()
                roll2_3.sort()
                if roll2_3 in fullhouse:
                    score = 55
    else:
        if roll2_1 in fullhouse:
            score = 25
        elif roll2_1 in smallstraight:
            score = 30
        else:
            roll2_2 = roll()
            roll2_2.sort()
            if roll2_2 in fullhouse:
                score = 25
            elif roll2_2 in smallstraight:
                score = 30
            else:
                roll2_3 = roll()
                roll2_3.sort()
                if roll2_3 in fullhouse:
                    score = 25
                elif roll2_3 in smallstraight:
                    score = 30
    return score

class Nod:
    def __init__(self, _info, _parinte = None, _h = 0):
        self.info = _info
        self.parinte = _parinte
        self.h = _h
        self.succesori = []

    def drumRadacina(self):
        nod = self
        drum = []
        while nod:
            drum.insert(0, nod)
            nod = nod.parinte
        return drum

class Arbore:
    def __init__(self, _start, _scopuri):
        self.start = _start
        self.scopuri = _scopuri

    def scop(self, informatieNod):
        return informatieNod in self.scopuri

    def succesori(self, nod):
        info = nod.info
        for i in range(1,6):
            info_nou = info[:]
            reroll = random.sample (range(5), i)
            for j in reroll:
                info_nou[j] = random.randint(1,6)
            nod_nou = Nod(info_nou, nod.h + 1)
            nod.succesori.append(nod_nou)

def euristica_medie():
    return

s = 0
for i in range(1000000):
     c = euristica_simpla()
     s = s+c
print(s/1000000)

def mutare_ai(zaruri_initiale):
    suma_actuala = 0
    scor_max = -1

    class Nod(object):
        def __init__(self, info):
            self.info = info
            self.succesori = []
            self.scor = 0

        def adauga_succesor(self, obj):
            self.succesori.append(obj)

    def zaruri_optime(zaruri_posibile):
        zaruri = []
        for i in zaruri_posibile:
            zaruri.append(zaruri_initiale.index(i))
        return zaruri[0], zaruri[1]

    def calculeaza_scor(a, b, c, d, e):
        if a == b == c or a == b == d or a == b == e or a == c == d or a == c == e or a == d == e or \
        b == c == d or b == c == e or c == d == e:  #pentru three of a kind
            return sum((a, b, c, d, e))
        else:
            return 30 #pentru small straight

    arunca_doar = []
    [arunca_doar.append([i]) for i in zaruri_initiale]
    [arunca_doar.append(list(i)) for i in list(itertools.combinations(zaruri_initiale, 2))]
    [arunca_doar.append(list(i)) for i in list(itertools.combinations(zaruri_initiale, 3))]
    [arunca_doar.append(list(i)) for i in list(itertools.combinations(zaruri_initiale, 4))]
    [arunca_doar.append(list(i)) for i in list(itertools.combinations(zaruri_initiale, 5))]

    radacina = Nod(zaruri_initiale)
    for i in arunca_doar:
        succesor = Nod(i)
        radacina.adauga_succesor(succesor)

    for succesor in radacina.succesori:
        if len(succesor.info) == 1:
            if zaruri_initiale.index(succesor.info[0]) == 0:
                for i in range(1, 7):
                    suma_actuala += ((1/6) * calculeaza_scor(i, zaruri_initiale[1], zaruri_initiale[2]))
                succesor.scor = suma_actuala
                suma_actuala = 0
            elif zaruri_initiale.index(succesor.info[0]) == 1:
                for i in range(1, 7):
                    suma_actuala += ((1/6) * calculeaza_scor(zaruri_initiale[0], i, zaruri_initiale[2]))
                succesor.scor = suma_actuala
                suma_actuala = 0
            else:
                for i in range(1, 7):
                    suma_actuala += ((1/6) * calculeaza_scor(zaruri_initiale[0], zaruri_initiale[1], i))
                succesor.scor = suma_actuala
                suma_actuala = 0
        elif len(succesor.info) == 2:
            index_1, index_2 = zaruri_optime(succesor.info)
            if index_1 == 0 and index_2 == 1:
                for i in range(1, 7):
                    for j in range(1, 7):
                        suma_actuala += ((1/36) * calculeaza_scor(i, j, zaruri_initiale[2]))
                succesor.scor = suma_actuala
                suma_actuala = 0
            elif index_1 == 0 and index_2 == 2:
                for i in range(1, 7):
                    for j in range(1, 7):
                        suma_actuala += ((1/36) * calculeaza_scor(i, zaruri_initiale[1], j))
                succesor.scor = suma_actuala
                suma_actuala = 0
            else:
                for i in range(1, 7):
                    for j in range(1, 7):
                        suma_actuala += ((1/36) * calculeaza_scor(zaruri_initiale[0], i, j))
                succesor.scor = suma_actuala
                suma_actuala = 0
        else:
            for i in range(1, 7):
                for j in range(1, 7):
                    for k in range(1, 7):
                        suma_actuala += ((1/216) * calculeaza_scor(i, j, k))
            succesor.scor = suma_actuala
            suma_actuala = 0

    fara_reroll = Nod('fara_reroll')
    radacina.adauga_succesor(fara_reroll)
    radacina.succesori[7].scor = calculeaza_scor(zaruri_initiale[0], zaruri_initiale[1], zaruri_initiale[2])

    for succesor in radacina.succesori:
        if succesor.scor > scor_max:
            scor_max = succesor.scor
            zar = succesor

    if zar.info == 'fara_reroll':
        print(f"AI decide să nu dea cu zarul.")
        return tip_roll(zaruri_initiale)
    else:
        if len(zar.info) == 1:
            index = zaruri_initiale.index(zar.info[0])
            zaruri_initiale[index] = randint(1, 6)
            print(f"AI decide să dea cu zarul {index + 1}. Noul zar: {zaruri_initiale}")
        elif len(zar.info) == 2:
            index_1, index_2 = zaruri_optime(zar.info)
            zaruri_initiale[index_1] = randint(1, 6)
            zaruri_initiale[index_2] = randint(1, 6)
            print(f"AI decide să dea cu zarurile {index_1 + 1} și {index_2 + 1}. Noile zaruri: {zaruri_initiale}")
        else:
            for i in range(3):
                zaruri_initiale[i] = randint(1, 6)
            print(f"AI decide să dea cu toate zarurile. Noile zaruri: {zaruri_initiale}")
        return tip_roll(zaruri_initiale)

def joc_single(jucator=True):
    if jucator:
        roll1 = roll()
        print(f"Rândul tău:")
        print(f"Ai dat cu zarurile: {roll1}")
        prompt = valideaza_input("Vrei să schimbi vreun zar? (y pentru HITME, n pentru HOLD): ", ["y", "n"])

        if prompt == "y":
            roll2, swap_zaruri = swap(roll1)
            print(f"Se schimbă zaruri: {swap_zaruri}")
            print(f"Ai dat cu zarurile: {roll2}")
            prompt2 = valideaza_input("Vrei să schimbi vreun zar? (y pentru HITME, n pentru HOLD): ", ["y", "n"])
            if prompt2 == "y":
                roll3, swap_zaruri = swap(roll2)
                print(f"Se schimbă zaruri: {swap_zaruri}")
                print(f"Ai dat cu zarurile: {roll3}")
                return tip_roll(roll3)
            return tip_roll(roll2)
        return tip_roll(roll1)
    else:
        zaruri_initiale = roll()
        print(f"Rândul AI-ului:")
        print(f"AI a dat cu zarurile: {zaruri_initiale}")
        return mutare_ai(zaruri_initiale)

def main():
    stats = {
        "YAHTZEE": 0,
        "FULL HOUSE": 0,
        "SMALL STRAIGHT": 0,
        "LARGE STRAIGHT": 0,
        "FOUR OF A KIND": 0,
        "THREE OF A KIND": 0
    }
    nr_joc = 0
    scor_jucator = 0
    scor_ai = 0

    while valideaza_input("Vrei să joci? (y pentru DA, n pentru NU): ", ["y", "n"]) == "y":
        nr_joc += 1
        print(f"JOCUL {nr_joc}")

        rezultat_jucator = joc_single(jucator=True)
        for key, value in rezultat_jucator.items():
            if value:
                stats[key] += 1
                print(f"Tu: {key}")
        scor_jucator += sum(rezultat_jucator.values())

        rezultat_ai = joc_single(jucator=False)
        for key, value in rezultat_ai.items():
            if value:
                stats[key] += 1
                print(f"AI: {key}")
        scor_ai += sum(rezultat_ai.values())

        print(f"SFÂRȘITUL JOCULUI {nr_joc}")

    print("\n" + "-" * 80)
    print(f"{'STATS':>43}")
    for key, value in stats.items():
        procent = (value / nr_joc) * 100 if nr_joc else 0
        print(f"{key.capitalize() + 's' if value != 1 else key.capitalize()}: {value} ({procent:.2f}%)")


    if scor_jucator > scor_ai:
        print("Ai câștigat jocul! Bravo!")
    elif scor_ai > scor_jucator:
        print("AI a câștigat jocul!")
    else:
        print("Egalitate! Jocul s-a încheiat fără un câștigător clar.")

if __name__ == "__main__":
    main()
