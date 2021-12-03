# StockPrice-VS-Temperature
Calculate the Correlation Coefficient between Itoen's Stock Price and Temperature at Tokyo

## How to Use
・Download Stock Price Data

See [pandas_datareader Repository](https://github.com/atchicken/pandas_datareader)

・Download Temperature Data

Download from [JMA's Website](https://www.data.jma.go.jp/risk/obsdl/index.php)

・Execute the Following Source Code after the Above is Completed
```bash:bash
python corrcoef.py -sp {Stock Price Data Path} -tp {Temperature Data Path} ¥
-gp {Create Graph Path}
```

## Detailed Explanation(Japanese)
・[Blog](https://atchicken.com/itoen_vs_temp/)

## Graph Depicting Data Using matplotlib
![image](https://user-images.githubusercontent.com/93382642/143731788-1bc71f5b-d534-41f6-9db7-ea3266346eae.png)
