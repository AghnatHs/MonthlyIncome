def threeDigit(num):
    """
        numbering format   
        ex: 154675 = 154.675
        ex: 2454367 = 2.454.367
        ex: 2445325.12 = 2.445.325,12
    """
    num=str(num).split(".")

    if len(num) == 2:
        afterComma = "," + num[1]
    else:
        afterComma=""

    num = list(num[0])
    num.reverse()
    num = [num[i:i+3] for i in range(0, len(num), 3)]
    new_num = ""

    for i in range(0,len(num)):
        num[i].reverse()
    num.reverse()

    for i in range(0,len(num)):
        new_num = new_num + "." + "".join(num[i])
    new_num = list(new_num)
    new_num.pop(0)
    new_num = "".join(new_num)
    new_num = new_num + afterComma

    return new_num