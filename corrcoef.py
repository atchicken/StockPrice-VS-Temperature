import argparse
import csv
import datetime as dt
import math
import matplotlib.pyplot as plt
import numpy as np



def main():
    """
    corrcoef.py's main

    Note:
        2021/11/28: Create New
    """
    
    args = Parse()

    # データ取得
    print("Get Data...")
    dataList = ReadFiles(args)

    # 相関係数計算
    allAveCoef, allMaxCoef, allMinCoef = CalcCorrCoef(dataList, "all")
    springAveCoef, springMaxCoef, springMinCoef = CalcCorrCoef(dataList, "spring")
    summerAveCoef, summerMaxCoef, summerMinCoef = CalcCorrCoef(dataList, "summer")
    authomAveCoef, authomMaxCoef, authomMinCoef = CalcCorrCoef(dataList, "authom")
    winterAveCoef, winterMaxCoef, winterMinCoef = CalcCorrCoef(dataList, "winter")

    print("[ALL] ave: {} max: {} min: {}".format(allAveCoef, allMaxCoef, allMinCoef))
    print("[SPRING] ave: {} max: {} min: {}".format(springAveCoef, springMaxCoef, springMinCoef))
    print("[SUMMER] ave: {} max: {} min: {}".format(summerAveCoef, summerMaxCoef, summerMinCoef))
    print("[AUTHOM] ave: {} max: {} min: {}".format(authomAveCoef, authomMaxCoef, authomMinCoef))
    print("[WINTER] ave: {} max: {} min: {}".format(winterAveCoef, winterMaxCoef, winterMinCoef))
    
    # グラフ作成
    drawGraph(dataList, args.graphPath)
    
    return


def ReadFiles(args):
    """
    Read Stock Price and Temperature File and Get Required Data

    Args:
        args (argparse): Commandline Arguments
    """

    # データ：日時・平均気温・最高気温・最低気温・終値
    dataList = []

    tf = open(args.tempPath, "r")
    tempReader = csv.reader(tf, delimiter=",")
    #next(tempReader)

    # 株価データ読み込み
    sf = open(args.stockPath, "r")
    stockReader = csv.reader(sf, delimiter=",")

    # 読み飛ばし
    next(stockReader)
        
    for tdata in tempReader:
        tdate = dt.datetime.strptime(tdata[0], "%Y/%m/%d")

        sf = open(args.stockPath, "r")
        stockReader = csv.reader(sf, delimiter=",")
        next(stockReader)
        
        # 同じ日時のデータを格納
        for sdata in stockReader:
            sdate = dt.datetime.strptime(sdata[0], "%Y-%m-%d")
            if tdate == sdate:
                data = {"date": tdate, "aveTemp": float(tdata[1]), "maxTemp":
                        float(tdata[4]), "minTemp": float(tdata[7]),
                        "closeStock": float(sdata[4])}
                dataList.append(data)
                break
            
    return dataList


def CalcCorrCoef(dataList, season):
    """
    Calculate the Correlation Coefficient for Each Season

    Args:
        dataList (list): List of Temperature and Stock Price Data
        season    (str): "spring" or "summer" or "authom" or "winter"

    Returns:
        aveCoef (float): Correlation Coefficient of Average Temperature vs. Closing Price
        maxCoef (float): Correlation Coefficient of Maximum Temperature vs. Closing Price
        minCoef (float): Correlation Coefficient of Minimum Temperature vs. Closing Price
    """
    
    if season == "spring":
        startMonth, endMonth = 3, 5
    elif season == "summer":
        startMonth, endMonth = 6, 8
    elif season == "authom":
        startMonth, endMonth = 9, 11
    elif season == "winter":
        startMonth, endMonth = 12, 2
    else:
        # All Season
        startMonth, endMonth = 1, 12

    # 該当する季節のデータを取り出し
    aveTempList = []
    maxTempList = []
    minTempList = []
    closeStockList = []
    for data in dataList:
        if (season != "winter" and startMonth <= data["date"].month <= endMonth) or \
           (season == "winter" and (data["date"].month == startMonth or \
                                    0 < data["date"].month <= endMonth)):
            aveTempList.append(data["aveTemp"])
            maxTempList.append(data["maxTemp"])
            minTempList.append(data["minTemp"])
            closeStockList.append(data["closeStock"])

    # 相関係数計算
    aveCoef = np.corrcoef(aveTempList, closeStockList)
    maxCoef = np.corrcoef(maxTempList, closeStockList)
    minCoef = np.corrcoef(minTempList, closeStockList)
    
    return round(aveCoef[0][1], 3), round(maxCoef[0][1], 3), round(minCoef[0][1], 3)


def drawGraph(dataList, graphPath):
    """
    Create TimeSeries Graph of Temperature and Stock Price
    
    Args:
        dataList (list): List of Temperature and StockPrice Data
        graphPath (str): Save Graph File Path
    """
    
    # 各情報を分離
    dateList = []
    aveTempList = []
    maxTempList = []
    minTempList = []
    stockList = []
    for data in dataList:
        dateList.append(data["date"])
        aveTempList.append(data["aveTemp"])
        maxTempList.append(data["maxTemp"])
        minTempList.append(data["minTemp"])
        stockList.append(data["closeStock"])

    # グラフ定義
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.get_xticklabels()
    ax2 = ax.twinx()

    # プロット
    ax.plot(dateList, aveTempList, linewidth="0.3", color="orange", label="Average Temperature")
    ax.plot(dateList, maxTempList, linewidth="0.3", color="red", label="High Temperature")
    ax.plot(dateList, minTempList, linewidth="0.3", color="blue", label="Low Temperature")
    ax2.plot(dateList, stockList, linewidth="1.0", color="green", label="Stock Price")

    # 軸ラベル・タイトル設定
    ax.set_xlim([dateList[0] + dt.timedelta(days=-5),
                 dateList[-1] + dt.timedelta(days=5)])
    ax.set_ylim([0, 40])
    ax2.set_ylim([math.floor(min(stockList) / 1000) * 1000,
                  math.ceil(max(stockList) / 1000) * 1000])
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Temperature[degC]", fontsize=10)
    ax2.set_ylabel("Price[yen]", fontsize=10)
    plt.grid(True)
    plt.title("Itoen(2593)StockPrice vs. Temperature")

    # 凡例・表示・保存
    leg = ax.legend(bbox_to_anchor=(0, 1), loc="upper left", borderaxespad=1, fontsize=8)
    for line in leg.get_lines():
        line.set_linewidth(1.5)
    ax2.legend(bbox_to_anchor=(0.023, 0.835), loc="upper left", borderaxespad=0, fontsize=8)
    plt.show()
    fig.savefig(graphPath)

    return


def Parse():
    """
    Get Commandline Arguments

    Returns:
        args (argparse): Commandline Arguments
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-sp", "--stockPath", type=str, default="./itoen.csv")
    parser.add_argument("-tp", "--tempPath", type=str, default="./temperature.csv")
    parser.add_argument("-gp", "--graphPath", type=str, default="./graph.png")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
