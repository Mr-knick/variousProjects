import matplotlib.pyplot as plt
import math

def amountAfterNumYears(initial, deposit, years, rate):
    accumulatedTotal = pert(initial, rate, 5)
    while(years >= 1):
        accumulatedTotal += pert(deposit, rate, years)
        years -= 1

    return accumulatedTotal


def pert(initalAmount, rate, years):
    return initalAmount * math.pow((1 + rate/12), 12 * years)

if __name__ == '__main__':
    # 10 is a good first year
    firstYearToCalc = 7
    # 25 is good last year
    maxYearToCalc = 18
    thisYear = 24.7
    rangeOfyears = list(range(firstYearToCalc, maxYearToCalc))

    # bInterest = .0000
    # cInterests = .0000
    # avgInterest = (bInterest + cInterests) / 2

    # rate = .0000
    # rate = avgInterest
    rate = .0000
    rateLow = rate * .80
    rateHigh = rate * 1.20

    yearlyInvestment = 0000
    yearlyInvestmentLow = yearlyInvestment - 10_000
    yearlyInvestmentHigh = yearlyInvestment + 10_000

    initalAmount = 0000

    TG_rateM_inM = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateM_inM.append(amountAfterNumYears(initalAmount, yearlyInvestment, i, rate))
        i += 1

    TG_rateL_inM = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateL_inM.append(amountAfterNumYears(initalAmount, yearlyInvestment, i, rateLow))
        i += 1

    TG_rateH_inM = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateH_inM.append(amountAfterNumYears(initalAmount, yearlyInvestment, i, rateHigh))
        i += 1
########################################################################################################################
    TG_rateM_inH = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateM_inH.append(amountAfterNumYears(initalAmount, yearlyInvestmentHigh, i, rate))
        i += 1

    TG_rateL_inH = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateL_inH.append(amountAfterNumYears(initalAmount, yearlyInvestmentHigh, i, rateLow))
        i += 1

    TG_rateH_inH = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateH_inH.append(amountAfterNumYears(initalAmount, yearlyInvestmentHigh, i, rateHigh))
        i += 1

########################################################################################################################

    TG_rateM_inL = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateM_inL.append(amountAfterNumYears(initalAmount, yearlyInvestmentLow, i, rate))
        i += 1

    TG_rateL_inL = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateL_inL.append(amountAfterNumYears(initalAmount, yearlyInvestmentLow, i, rateLow))
        i += 1

    TG_rateH_inL = []
    i = firstYearToCalc
    while(i < maxYearToCalc):
        TG_rateH_inL.append(amountAfterNumYears(initalAmount, yearlyInvestmentLow, i, rateHigh))
        i += 1
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateM_inL, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rate * 100:,.2f}% and Yearly Add \${yearlyInvestmentLow:,d}", color="cornflowerblue")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateM_inM, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rate*100:,.2f}% and Yearly Add \${yearlyInvestment:,d}", color="blue")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateM_inH, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rate * 100:,.2f}% and Yearly Add \${yearlyInvestmentHigh:,d}", color="navy")

    plt.plot([x + thisYear for x in rangeOfyears], TG_rateL_inL, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateLow * 100:,.2f}% and Yearly Add \${yearlyInvestmentLow:,d}", color="lime")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateL_inM, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateLow * 100:,.2f}% and Yearly Add \${yearlyInvestment:,d}", color="limegreen")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateL_inH, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateLow * 100:,.2f}% and Yearly Add \${yearlyInvestmentHigh:,d}", color="seagreen")

    plt.plot([x + thisYear for x in rangeOfyears], TG_rateH_inL, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateHigh * 100:,.2f}% and Yearly Add \${yearlyInvestmentLow:,d}", color="salmon")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateH_inM, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateHigh * 100:,.2f}% and Yearly Add \${yearlyInvestment:,d}", color="red")
    plt.plot([x + thisYear for x in rangeOfyears], TG_rateH_inH, '-d', label=f"Initial Amount \${initalAmount:,.0f} Interest {rateHigh * 100:,.2f}% and Yearly Add \${yearlyInvestmentHigh:,d}", color="brown")

    # retirement goal amount
    # plt.axhline(y=3200000, color='red')
    # plt.axhline(y=1_000_000, color='red')
    plt.axhline(y=3_200_000, color='red')
    plt.legend()
    plt.title('Amount by year')
    plt.xlabel('Year')
    plt.ylabel('Total')
    plt.show()


