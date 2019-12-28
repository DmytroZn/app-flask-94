from flask import (
                    Flask,
                    render_template,
                    request
                    )
from models import models
import requests
import json
import webbrowser
import hashlib
import re
import datetime
import logging


app = Flask(__name__)


# @app.route('/a', methods=['POST', 'GET'])
# def admin_meth():
#     url = 'https://core.piastrix.com/bill/create'
#     headers = {'Content-type': 'application/json',  # Определение типа данных
#             'Accept': 'text/plain',
#             'Content-Encoding': 'utf-8'}
#     data = {"description": "Test Bill",
#             "payer_currency": 643,
#             "shop_amount": "23.15",
#             "shop_currency": 643,
#             "shop_id": "5",
#             "shop_order_id": 123456,
#             "sign": "091ee6f0bce195a508231ee0d62d7645bd0b38b63e22bde78046b277d6988045"} # Если по одному ключу находится несколько словарей, формируем список словарей
#     answer = requests.post(url, data=json.dumps(data), headers=headers)
#     print(answer)
#     print('44444444444444444444444444444444')
#     response = answer.json()
#     print(response)
# admin_meth()

logging.basicConfig(filename="log_app.log", level=logging.INFO)

logging.debug("This is a debug message")
# logging.info("Programm started")
logging.error("An error has happened!")

logging.info("Programm started")
log = logging.getLogger("ex")
@app.route('/', methods=['POST', 'GET'])
@app.route('/start')
def start():
    print('Start on Huroku 1')
    # currency = ['EUR', 'USD', 'RUB']
    currency_dict = {'EUR' : '978', 'USD' : '840', 'RUB': '643'}
    shop_id = '5'
    secretKey = 'SecretKey01'
    payway = 'payeer_rub'
    error = 'Используйте только цифры. Н-р 15.78'
    amount = ''
    payment_currency = ''
    description = ''
    print('Start on Huroku 2')
    if request.method == 'POST':
        amount = request.form.get('amount')
        
        if amount:
            rrr = '0256'
            result = re.split(r'\.', amount)
            len_of = len(result)
            if len_of == 2 or len_of == 1 :
                c_list = 0
                for i in result:
                    c_str = 0
                    for k in i:
                        if re.findall(r'[0-9]', k):
                            c_str += 1
                    if c_str == len(i):
                        c_list += 1
                if c_list == len(result):
                    pass
                else:
                    # error = 'Используйте только цифры. Н-р 15.78'
                    return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency, error=error)    
            else:
                # error = 'Используйте только цифры. Н-р 15.78'
                return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency, error=error)

             

        payment_currency = request.form.get('payment_currency')
        description = request.form.get('description')
        try:
            amount_float = float(amount) * 100
        except ValueError:
            log.exception("Error!")
            return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency)

        amount = amount_float / 100
        amount = f'{amount:.{2}f}'
        payment_currency1 = currency_dict[payment_currency]
    if payment_currency == 'EUR':
        print('Start on EUR')
        logging.info("Programm choice EUR")
        url = 'https://pay.piastrix.com/ru/pay'
        shop_order_id = '101'
        keys_sorted = ['amount', 'currency', 'shop_id', 'shop_order_id']
        sha = f'{amount}:{currency_dict[payment_currency]}:{shop_id}:{shop_order_id}{secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        # models.Payment(**{
        #     'currency' : payment_currency,
        #     'amount' : amount_float,
        #     'date_time' : datetime.datetime.now(),
        #     'description' : description,
        #     'identeficate' : f'{sign}_{datetime.datetime.now()}'
        # }).save()
        logging.info("Programm done with EUR")
        return render_template('index.html', 
                                url=url, payment_currency=payment_currency,
                                shop_id=shop_id, amount=amount, 
                                currency=payment_currency1, 
                                shop_order_id=shop_order_id, sign=sign)
    elif payment_currency == 'USD':
        logging.info("Programm choice USD")
        shop_order_id = '123456'  
        url = 'https://core.piastrix.com/bill/create'
        headers = {'Content-type': 'application/json', 
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'}
        s = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
        sha = f'{payment_currency1}:{amount}:{payment_currency1}:{shop_id}:{shop_order_id}{secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        data = {"payer_currency": payment_currency1,
                "shop_amount": amount,
                "shop_currency": payment_currency1,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
                "sign": sign}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        response = answer.json()
        url1 = response['data']['url'] 
        webbrowser.open(url1, new=1)
        webbrowser.get('chrome')
        # models.Payment(**{
        #     'currency' : payment_currency,
        #     'amount' : amount_float,
        #     'date_time' : datetime.datetime.now(),
        #     'description' : description,
        #     'identeficate' : f'{sign}_{datetime.datetime.now()}'
        # }).save()
        logging.info("Programm done with USD")
        return render_template('index.html', payment_currency=payment_currency, url1=url1)
    elif payment_currency == 'RUB':
        logging.info("Programm choice RUB")
        url = 'https://core.piastrix.com/invoice/create'
        shop_order_id = "123456"
        headers = {'Content-type': 'application/json',  
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'}
        s = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id', 'sign']
        sha = f'{amount}:{payment_currency1}:{payway}:{shop_id}:{shop_order_id}{secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        data = {
            "amount": amount,
            "currency": payment_currency1,
            "payway": payway,
            "shop_id": shop_id,
            "shop_order_id": shop_order_id,
            "sign": sign} 
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        response = answer.json()
        url = response['data']['url']
        method = response['data']['method']
        id_ident = response['data']['id']
        lang = response['data']['data']['lang']
        m_curorderid = response['data']['data']['m_curorderid']
        m_historyid = response['data']['data']['m_historyid']
        m_historytm = response['data']['data']['m_historytm']
        referer = response['data']['data']['referer']

        # models.Payment(**{
        #     'currency' : payment_currency,
        #     'amount' : amount_float,
        #     'date_time' : datetime.datetime.now(),
        #     'description' : description,
        #     'identeficate' : f'{sign}_{datetime.datetime.now()}'
        # }).save()
        logging.info("Programm done with RUB")
        return render_template('index.html', 
                            payment_currency=payment_currency, 
                            url=url, lang=lang, m_curorderid=m_curorderid,
                            m_historyid=m_historyid, m_historytm=m_historytm,
                            referer=referer)

        # webbrowser.open(url1, new=2)
       
    
    return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency)




if __name__ == '__main__':
    app.run(port=5000, debug=True)