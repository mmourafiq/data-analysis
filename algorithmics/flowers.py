def flowers():
    nbr_fl, nbr_fr = [int(x) for x in raw_input().split()]
    prices = [float(x) for x in raw_input().split()]
    prices.sort()
    amount = 0
    x = 0
    while nbr_fl:
        if nbr_fl <= nbr_fr:
            amount += sum([(1 + x) * c for c in prices[:nbr_fl]])
            nbr_fl = 0
        else:
            amount += sum([(1 + x) * c for c in prices[nbr_fl - nbr_fr:nbr_fl]])
            nbr_fl -= nbr_fr
            x += 1
    amount_flat = int(amount)
    amount_float = amount % 1
    if amount_float != 0:
        print amount
    else:
        print amount_flat


flowers()
