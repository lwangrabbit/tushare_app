#coding=utf-8

import tushare as ts
import datetime
import xlwt


def get_zz500_ok():

    all_result = []
    df = ts.get_zz500s()
    for index in range(50):
        code = df[index: index + 1].get('code').values[0]
        name = df[index: index + 1].get('name').values[0]
        avg_20_json = get_avg_20(code, datetime.datetime.now())

        print code + ":" + name

        result = {
            "code": code,
            "name": name,
            "close": avg_20_json['close'],
            "avg_20": avg_20_json['avg20'],
            "last_trade_date": avg_20_json['last_trade_date'],
            "util_date": avg_20_json['util_date']
        }
        all_result.append(result)
    return all_result


def filter_zz500(zz500_result):
    my_result = []
    for result in zz500_result:
        #当天收盘价大于20日均线的上证股票
        if result['close'] > result['avg_20'] and  not str(result['code']).startswith('3'):
            my_result.append(result)
    return my_result


def get_avg_20(code, until_date):

    end_date = until_date
    delta = datetime.timedelta(days=30)
    start_date = end_date - delta

    ts_start = start_date.strftime('%Y-%m-%d')
    ts_end = end_date.strftime('%Y-%m-%d')
    df = ts.bar(code = code, start_date=ts_start, end_date=ts_end, ma=[20])

    if df.size < 1:
        avg20 = 0
        last_trade_date = ''
        close = 0
    else:
        my_df = df.head(1)
        avg20 = str(df.get('MA20').values[0])
        last_trade_date = str(df.index.values[0])
        close = str(my_df.get('close').values[0])
    ret = {
        "code": code,
        "util_date": until_date.strftime('%Y-%m-%d'),
        "last_trade_date": last_trade_date,
        "close": close,
        "avg20": avg20
    }
    return ret


def write_result_to_csv(result):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('result')

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'
    style.font = font

    ws.write(0, 0, 'code')
    ws.write(0, 1, 'name')
    ws.write(0, 2, 'avg_20')
    ws.write(0, 3, 'close')
    ws.write(0, 4, 'last_trade_date')
    ws.write(0, 5, 'util_date')

    index = 1
    for res in result:
        ws.write(index, 0, res['code'])
        ws.write(index, 1, res['name'], style)
        ws.write(index, 2, str(res['avg_20']))
        ws.write(index, 3, str(res['close']))
        ws.write(index, 4, res['last_trade_date'])
        ws.write(index, 5, res['util_date'])
        index = index + 1
    wb.save('result.csv')


zz500_result = get_zz500_ok()
my_avg20_result = filter_zz500(zz500_result)
print my_avg20_result
write_result_to_csv(my_avg20_result)


