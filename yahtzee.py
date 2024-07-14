from random import randint, random
from collections import Counter
import itertools
import random

def roll(n):
    return [randint(1, 6) for _ in range(n)]


# consideram toate combinatiile UNICE prin generarea valorilor zarurilor in ordine crescatoare
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
             [1,1,1,6,6], [1, 1, 2, 2, 2], [1, 1, 3, 3, 3], [1, 1, 4, 4, 4], [1, 1, 5, 5,5],
             [1, 1, 6, 6,6], [2,2,2,2,2], [2,2,2,3,3], [2,2,2,4,4], [2,2,2,5,5], [2,2,2,6,6],
             [2, 2, 3, 3, 3], [2, 2, 4, 4, 4], [2, 2, 5, 5, 5], [2, 2, 6, 6, 6],
             [3,3,3,3,3], [3,3,3,4,4], [3,3,3,5,5], [3,3,3,6,6], [3, 3, 4, 4, 4], [3, 3, 5, 5,5],
             [3, 3, 6, 6,6], [4,4,4,4,4], [4,4,4,5,5],
             [4,4,4,6,6], [4, 4, 5, 5, 5], [4, 4, 6, 6, 6], [5,5,5,5,5], [5,5,5,6,6],
             [5, 5, 6, 6, 6], [6,6,6,6,6]]
smallstraight = [[1,1,2,3,4], [1,2,2,3,4], [1,2,3,3,4], [1,2,3,4,4], [1,2,3,4,5],
                 [1,2,3,4,6], [2,2,3,4,5], [2,3,3,4,5], [2,3,4,4,5], [2,3,4,5,5],
                 [2,3,4,5,6], [1,3,4,5,6], [3,3,4,5,6], [3,4,4,5,6], [3,4,5,5,6], [3,4,5,6,6]]


def euristica_simpla():
    score = 0
    roll_1 = roll(5)
    roll_1.sort()

    if roll_1 in fullhouse:
        score = 25
    elif roll_1 in smallstraight:
        score = 30
    else:
        roll_2 = roll(5)
        roll_2.sort()

        if roll_2 in fullhouse:
            score = 25
        elif roll_2 in smallstraight:
            score = 30
        else:
            roll_3 = roll(5)
            roll_3.sort()

            if roll_3 in fullhouse:
                score = 25
            elif roll_3 in smallstraight:
                score = 30
    roll2_1 = roll(5)
    roll2_1.sort()
    if score == 25:
        if roll2_1 in smallstraight:
            score = 55
        else:
            roll2_2 = roll(5)
            roll2_2.sort()
            if roll2_2 in smallstraight:
                score = 55
            else:
                roll2_3 = roll(5)
                roll2_3.sort()
                if roll2_3 in smallstraight:
                    score = 55
    elif score == 30:
        if roll2_1 in fullhouse:
            score = 55
        else:
            roll2_2 = roll(5)
            roll2_2.sort()
            if roll2_2 in fullhouse:
                score = 55
            else:
                roll2_3 = roll(5)
                roll2_3.sort()
                if roll2_3 in fullhouse:
                    score = 55
    else:
        if roll2_1 in fullhouse:
            score = 25
        elif roll2_1 in smallstraight:
            score = 30
        else:
            roll2_2 = roll(5)
            roll2_2.sort()
            if roll2_2 in fullhouse:
                score = 25
            elif roll2_2 in smallstraight:
                score = 30
            else:
                roll2_3 = roll(5)
                roll2_3.sort()
                if roll2_3 in fullhouse:
                    score = 25
                elif roll2_3 in smallstraight:
                    score = 30
    return score

def distanta_combinatie(zaruri, combinatii):
    counter_zaruri = Counter(zaruri)
    distante = []
    for comb in combinatii:
        counter_comb = Counter(comb)
        # calculam diferenta dintre counters
        diferenta = counter_comb - counter_zaruri
        # adaugam suma valorilor (nr de elemente care lipsesc)
        distante.append(sum(diferenta.values()))
    return min(distante)

def euristica_medie():
    scor = 0
    def runda(scor):
        roll_1 = roll(5)
        distanta_smallstraight = distanta_combinatie(roll_1, smallstraight)
        distanta_fullhouse = distanta_combinatie(roll_1, fullhouse)

        if distanta_fullhouse == 0:
            return roll_1

        if distanta_smallstraight == 0:
            return roll_1

        if scor == 0:
            if distanta_smallstraight < distanta_fullhouse:
                #target= "small straight"
                combinatie_potentiala = smallstraight
            else:
                #target = "full house"
                combinatie_potentiala = fullhouse
        elif scor == 25:
            combinatie_potentiala = smallstraight
        elif scor == 30:
            combinatie_potentiala = fullhouse

        distante = [sum((Counter(comb) - Counter(roll_1)).values()) for comb in combinatie_potentiala]
        index_distanta_minima = distante.index(min(distante))
        zaruri_pastrate = list((Counter(combinatie_potentiala[index_distanta_minima]) & Counter(roll_1)).elements())

        nr_zaruri_reroll = 5 - len(zaruri_pastrate)
        reroll = roll(nr_zaruri_reroll)
        roll_nou = list(zaruri_pastrate) + reroll

        distanta_smallstraight = distanta_combinatie(roll_nou, smallstraight)
        distanta_fullhouse = distanta_combinatie(roll_nou, fullhouse)

        if distanta_fullhouse == 0:
            return roll_nou

        if distanta_smallstraight == 0:
            return roll_nou

        if scor == 0:
            if distanta_smallstraight < distanta_fullhouse:
                # target= "small straight"
                combinatie_potentiala = smallstraight
            else:
                # target = "full house"
                combinatie_potentiala = fullhouse
        elif scor == 25:
            combinatie_potentiala = smallstraight
        elif scor == 30:
            combinatie_potentiala = fullhouse

        distante = [sum((Counter(comb) - Counter(roll_nou)).values()) for comb in combinatie_potentiala]
        index_distanta_minima = distante.index(min(distante))
        zaruri_pastrate = list((Counter(combinatie_potentiala[index_distanta_minima]) & Counter(roll_nou)).elements())

        nr_zaruri_reroll = 5 - len(zaruri_pastrate)
        reroll = roll(nr_zaruri_reroll)
        roll_final = list(zaruri_pastrate) + reroll

        return roll_final

    runda1_roll = runda(scor)

    if sorted(runda1_roll) in [sorted(x) for x in smallstraight]:
        scor = 30
    elif sorted(runda1_roll) in [sorted(x) for x in fullhouse]:
        scor = 25
    else:
        scor = 0

    runda2_roll = runda(scor)

    if sorted(runda2_roll) in [sorted(x) for x in smallstraight] and scor == 25 :
        scor = scor + 30
    elif sorted(runda2_roll) in [sorted(x) for x in fullhouse] and scor == 30:
        scor = scor + 25
    else:
        scor = scor

    return scor

def euristica_grea():
    scor_final = 0
    scor = 0
    for i in range (1,3):
        best_scoruri = []
        actiunile_posibile = list(itertools.product([True, False], repeat=5))

        def calculeaza_scor(zaruri,scor):
            if sorted(zaruri) in smallstraight and scor == 0:
                return 30
            elif sorted(zaruri) in smallstraight and scor == 25:
                return 55
            elif sorted(zaruri) in fullhouse and scor == 0:
                return 25
            elif sorted(zaruri) in fullhouse and scor == 30:
                return 55
            else:
                return 0

        def fa_actiune(zaruri, actiune):
            return [zar if pastrat else random.randint(1, 6) for zar, pastrat in zip(zaruri, actiune)]

        for comb in combinatii:
            scor_max = 0
            best_secventa = None

            for actiune2 in actiunile_posibile:
                comb2 = fa_actiune(comb, actiune2)

                for actiune3 in actiunile_posibile:
                    for j in range(10):
                        comb_finala = fa_actiune(comb2, actiune3)
                        scor = calculeaza_scor(comb_finala,scor)

                        if scor > scor_max:
                            scor_max = scor
                            best_secventa = (actiune2, actiune3)

            best_scoruri.append((comb, scor_max, best_secventa))

        # Find the overall best action sequence
        zaruri_initiale = roll(5)
        if best_secventa:
            zaruri_primul_roll = fa_actiune(zaruri_initiale, best_secventa[0])
            zaruri_finale = fa_actiune(zaruri_primul_roll, best_secventa[1])
            scor_final = scor_final + calculeaza_scor(zaruri_finale, 0)

    return scor_final

def main():
    s1 = 0
    s2 = 0
    s3 = 0
    for i in range(10):
        c1 = euristica_simpla()
        s1 = s1 + c1
        c2 = euristica_medie()
        s2 = s2 + c2
        c3 = euristica_grea()
        s3 = s3 + c3
    print(s1 / 10, s2 / 10, s3/10)

main()