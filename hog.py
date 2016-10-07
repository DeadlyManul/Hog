"""Игра в «Свинью»"""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # Цель игры в «Свинью» -- набрать 100 очков.

######################
# Часть 1: Симулятор #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Бросает DICE(кость) NUM_ROLLS(количество бросков) раз. Возвращает либо сумму результатов,
    либо 1, если хоть раз выпала 1 (обжора). Делает ровно NUM_ROLLS вызовов функции DICE.

    num_rolls:  Число бросков кости, которые нужно сделать; больше либо равно 1.
    dice:       Функция без аргументов, возвращает результат отдельного броска.
    """
    # Эти проверки гарантируют, что num_rolls является положительным целым.
    assert type(num_rolls) == int, 'num_rolls должна быть целой (int).'
    assert num_rolls > 0, 'должен быть хотя бы один бросок кости.'
    a, sum, fat = 0, 0, False
    while a < num_rolls:
        b = dice()
        if b == 1:
            fat = True
        else:
            sum += b

        a += 1

    return (fat and 1) or sum

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Симуляция хода с NUM_ROLLS бросками, бросков может не быть (Халявный бекон).

    num_rolls:       Число бросков кости, которые нужно сделать.
    opponent_score:  Количество очков противника.
    dice:            Функция без аргументов, возвращает результат отдельного броска.
    """
    assert type(num_rolls) == int, 'num_rolls должна быть целой (int).'
    assert num_rolls >= 0, 'Число бросков не может быть отрицательным'
    assert num_rolls <= 10, 'Нельзя бросить кость более 10 раз'
    assert opponent_score < 100, 'Игра должна закончится'
    if num_rolls == 0:
        return int(max(str(opponent_score))) + 1
    elif num_rolls > 0:
        return roll_dice(num_rolls, dice)

def select_dice(score, opponent_score):
    """Возвращает шестигранную кость если сумма SCORE и OPPONENT_SCORE 
    не кратна 7, в этом случае возвращает четырехгранную кость (Дикий кабан).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def is_prime(n):
    """Возвращает True, если N простое число, иначе возвращает False. 
    1 не является простым числом!

    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(4)
    False
    >>> is_prime(11)
    True
    """
    assert type(n) == int, 'n должна быть целой (int).'
    assert n >= 0, 'n должна быть неотрицательной.'
    if n <= 1:
        return False
    i = 2
    while i < n:
        if n % i == 0:
            return False
        i += 1
    return True

def next_prime(x):
    found = False
    while not found:
        x = x + 1
        if is_prime(x):
            found = True
            return x

def other(who):
    """Возвращает индекс противника, допустимые значения WHO: 0 и 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.
    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.
    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    while score0 < goal and score1 < goal:
        dice = select_dice(score0,score1)
        if who == 0:
            num_rolls = strategy0(score0, score1)
            this_score = take_turn(num_rolls,score1,dice)
            score0 = score0 + this_score
        elif who == 1:
            num_rolls = strategy1(score1, score0)
            this_score = take_turn(num_rolls, score0, dice)
            score1 = score1 + this_score    

        if is_prime(score1 + score0) == True:
            if score1 > score0:
                score1 = score1 + this_score
            elif score1 < score0:
                score0 = score0 + this_score
        who = other(who)

    return score0, score1  # You may want to change this line.


######################
# Часть 2: Стратегии #
######################

def always_roll(n):
    """Возвращает стратегию, по которой всегда надо бросать N костей.

    Стратегия -- это функция, которая принимает два аргумента: количество очков
    текущего игрока и количество очков противника и возвращает число бросков костей
    для текущего хода игрока.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Эксперименты

def make_averaged(fn, num_samples=1000):
    """Возвращает функцию, которая возвращает average_value (среднее значение)
     по NUM_SAMPLES вызовам функции FN.

    Для реализации потребуется использовать синтаксис *args --
    возможность, рассмотренную в описании шестой задачи.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    В последнем примере рассматривается усреднение двух различных сценариев.
    - В первый ход результаты бросков 3 и 1, результат: 1 очко.
    - Во второй ход результаты бросков 5 и 6, результат: 11 очков.
    - И так 500 раз

    Таким образом среднее значение по 1000 ходам равно 6.0.
    """
    def ret(*args):
        i, sum = 0, 0
        while i < num_samples:
            sum, i = sum + fn(*args), i + 1
        return sum / num_samples

    return ret

def max_scoring_num_rolls(dice=six_sided):
    """Возвращает число бросков (от 1 до 10), которое приведет в среднем к максимальному
    количеству очков за ход. Функция многократно вызывает roll_dice с заданной костью (DICE).
    Предполагаем, что кость (DICE) всегда выдает положительные результаты.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    maxx, ret, number_of_dice = 0, 0,10
    while number_of_dice > 0:
        avg = make_averaged(roll_dice)(number_of_dice, dice)
        maxx = max(maxx, avg)

        if avg >= maxx:
            ret = number_of_dice

        number_of_dice -= 1

    return ret

def winner(strategy0, strategy1):
    """Возвращает 0 если  strategy0 выигрывает против strategy1, иначе 1."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Возвращает долю побед (от 0 до 1) стратегии (STRATEGY) против
    другой стратегии (BASELINE)."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Усреднение результатов

def run_experiments():
    """Запускает набор экспериментов со стратегией и выводит информацию
    о результатах."""
    if True: # Измени на False, когда закончишь делать max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Оптимальное количество бросков для шестигранной кости:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Оптимальное количество бросков для четырехгранной кости:', four_sided_max)

    if False: # Измени на True для теста always_roll(8)
        print('Доля побед для always_roll(8):', average_win_rate(always_roll(8)))

    if False: # Измени на True для теста bacon_strategy
        print('Доля побед для bacon_strategy:', average_win_rate(bacon_strategy))

    if False: # Измени на True для теста prime_strategy
        print('Доля побед для prime_strategy:', average_win_rate(prime_strategy))

    if False: # Измени на True для теста final_strategy
        print('Доля побед для final_strategy:', average_win_rate(final_strategy))

    "*** Можешь добавить дополнительные эксперименты, если хочешь ***"

# Стратегии

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """Эта стратегия возвращает 0, если можно получить по крайней мере
    MARGIN очков, в противном случае возвращает NUM_ROLLS.
    """
    free_p = 1 + max([int(i) for i in str(opponent_score)][-2::])

    if is_prime(free_p):
        free_p = next_prime(free_p)

    if free_p >= margin:
        return 0
    else:
        return num_rolls

def prime_strategy(score, opponent_score, margin=8, num_rolls=5):
    """Эта стратегия This strategy rolls 0 dice when it results in a beneficial boost and
    rolls NUM_ROLLS if rolling 0 dice gives the opponent a boost. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    "*** ТВОЙ КОД ЗДЕСЬ ***"
    free_bacon = int(max(str(opponent_score)))+1
    if is_prime(free_bacon+score+opponent_score):
        if score + free_bacon > opponent_score:
            return 0
        elif score + free_bacon < opponent_score:
            return num_rolls
    else:
        if free_bacon >= margin:
            return 0
        else:
            return num_rolls

def final_strategy(score, opponent_score):
    """Напиши краткое описание твоей финальной стратегии.

    *** ТВОЕ ОПИСАНИЕ ЗДЕСЬ ***
    """
    "*** ТВОЙ КОД ЗДЕСЬ ***"
    free_bacon = int(max(str(opponent_score)))+1 #assign the score you would get if you choose to roll 0 dice
    opp_bacon = int(max(str(score)))+1 #oppponent's free bacon 
    margin = 8
    num_rolls = 5

    if free_bacon + score >= 100:
        return 0
    else:  
        if opponent_score < 33: #Opening
            if score >= opponent_score:
                margin = margin - ((score-opponent_score)//9) #decrease margin to a lower number if you are far ahead. If it is close margin = 8
            elif (score + 15) < opponent_score:
                margin = 8 #if I am trailing by more than 15 in the opening, don't utilize free bacon unless it adds 8,9 or 10
                num_rolls = 6
            if (free_bacon + score + opponent_score)%7 == 0 and free_bacon >= 6: # Force my opponent to roll 4 sided dice by utilizing free bacon
                return 0 
            if (1 + score + opponent_score)%7 == 0: #if pigging out results in my oppponent having to roll 4 sided dice, take a bigger risk
                num_rolls = num_rolls + 1
            if (score + opponent_score)%7 == 0: #When I have to roll a 4 sided dice, I decrease the amount of dice I want to roll
                num_rolls = num_rolls -2
                if num_rolls <= 0:
                    num_rolls = 1
                    margin = 4
            
        
        elif opponent_score <= 66 and opponent_score >= 33: #MiddleGame
            if score >= opponent_score:
                margin = margin - ((score-opponent_score)//11) #decrease margin to a lower number if you are far ahead. If it is close margin = 8
            elif (score +10) <= opponent_score:
                margin = 8 #if I am trailing by 10 or less, only use free bacon if it gives you 10 9 or 8 points
            if (free_bacon + score + opponent_score)%7 == 0 and free_bacon >= 6: # Force my opponent to roll 4 sided dice by utilizing free bacon
                return 0 
            if (1 + score + opponent_score)%7 == 0: #if pigging out results in my oppponent having to roll 4 sided dice, take a bigger risk
                num_rolls = num_rolls + 1
            if (score + opponent_score)%7 == 0: #When I have to roll a 4 sided dice, I decrease the amount of dice I want to roll
                num_rolls = num_rolls -2
                if num_rolls <= 0:
                    num_rolls = 1
                    margin = 4
            

        else: #EndGame
            if score >= opponent_score:
                margin = margin - ((score-opponent_score)//10) #decrease margin to a lower number if you are far ahead. If it is close margin = 8
                num_rolls = num_rolls - ((score-opponent_score)//10) 
                if num_rolls <= 0:
                    num_rolls = 1
                if (free_bacon + score + opponent_score)%7 == 0 and free_bacon >= 6:
                    return 0 
                if (score + opponent_score)%7 == 0:
                    num_rolls = num_rolls -2
                    if num_rolls <= 0:
                        num_rolls = 1
                        margin = 4
            elif (score +10) <= opponent_score:
                margin = 10 #if I am trailing by 10 or less, only use free bacon if it gives you 10 points
                if opponent_score + opp_bacon >= 100: #opponent will win on next turn if I don't win now
                    margin = 11 #don't use free bacon in this case
                    if score < 67:
                        num_rolls = 8 #desperation- try to get 33 or more by rolling 8 dice
                    elif score < 74:
                        num_rolls = 7
                    else:
                        num_rolls = 6
            else: #if I am trailing by less than 10 
                if opponent_score + opp_bacon >= 100: #opponent will win on next turn if I don't win now
                    margin = 11 #don't use free bacon in this case
                elif opponent_score >= 80:
                    if (free_bacon + score + opponent_score)%7 == 0 and free_bacon >= 6: # Force my opponent to roll 4 sided dice by utilizing free bacon
                        return 0 
                    if (score + opponent_score)%7 == 0: #When I have to roll a 4 sided dice, I decrease the amount of dice I want to roll
                        num_rolls = num_rolls -2
                        if num_rolls <= 0:
                            num_rolls = 1
                            margin = 4



        return prime_strategy(score, opponent_score,margin,num_rolls)


##############################
# Интерфейс командной строки #
##############################

# Учти: Функции в этой секции не должны меняться. Здесь используются возможности 
#       Python выходящие за материал курса.


@main
def run(*args):
    """Считывает аргументы командной строки и вызывает соответствующие
    функции.

    Эта функция использует возможности Python выходящие за пределы курса.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Игра в «Свинью»")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Запускает эксперименты со стратегиями')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()