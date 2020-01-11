from flask import (
                    Flask,
                    render_template,
                    request
                    )

import logging
import hashlib
import json
import requests
import random
import re

log = logging.getLogger("ex")

class CheckAmount:
    
    def __init__(self, amount, currency_dict, error, payment_currency):
        self._amount = amount
        self._currency_dict = currency_dict
        self._error = error
        self._payment_currency = payment_currency
    
    def check(self):
        shop_id = '5'
        secretKey = 'SecretKey01'
        currency_dict = {'EUR' : '978', 'USD' : '840', 'RUB': '643'}
        result = re.split(r'\.', self._amount)
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
                try:
                    amount_float = float(self._amount) * 100
                except ValueError:
                    log.exception("Error!")
                    return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency)

                self._amount = amount_float / 100
                self._amount = f'{self._amount:.{2}f}'
                self._payment_currency = request.form.get('payment_currency')
                self._description = request.form.get('description')
                payment_currency1 = currency_dict[self._payment_currency]
                if self._payment_currency == 'EUR':
                    return PaymentCurrency(self._amount, self._currency_dict, self._payment_currency, shop_id, secretKey, payment_currency1).eur()  
                elif self._payment_currency == 'USD':
                    return PaymentCurrency(self._amount, self._currency_dict, self._payment_currency, shop_id, secretKey, payment_currency1).usd() 
                elif self._payment_currency == 'RUB':
                    return PaymentCurrency(self._amount, self._currency_dict, self._payment_currency, shop_id, secretKey, payment_currency1).rub() 
            else:
                return render_template('index.html', currency_dict=self._currency_dict, error=self._error)             
        else:
            return render_template('index.html', currency_dict=self._currency_dict, error=self._error)  

class PaymentCurrency:

    def __init__(self, amount, currency_dict, payment_currency, shop_id, secretKey, payment_currency1):
        self._amount = amount
        self._currency_dict = currency_dict
        self._payment_currency = payment_currency
        self._shop_id = shop_id
        self._secretKey = secretKey
        self._payment_currency1 = payment_currency1

    def eur(self):
        logging.info("Programm choice EUR")
        url = 'https://pay.piastrix.com/ru/pay'
        shop_order_id = '101'
        keys_sorted = ['amount', 'currency', 'shop_id', 'shop_order_id']
        sha = f'{self._amount}:{self._currency_dict[self._payment_currency]}:{self._shop_id}:{shop_order_id}{self._secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        print('ggoooooof')
        logging.info("Programm done with EUR")
        return render_template('index.html', 
                                url=url, payment_currency=self._payment_currency,
                                shop_id=self._shop_id, amount=self._amount, 
                                currency=self._payment_currency1, 
                                shop_order_id=shop_order_id, sign=sign)
    
    def usd(self):
        logging.info("Programm choice USD")
        shop_order_id = '123456'  
        url = 'https://core.piastrix.com/bill/create'
        headers = {'Content-type': 'application/json', 
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'}
        s = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
        sha = f'{self._payment_currency1}:{self._amount}:{self._payment_currency1}:{self._shop_id}:{shop_order_id}{self._secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        data = {"payer_currency": self._payment_currency1,
                "shop_amount": self._amount,
                "shop_currency": self._payment_currency1,
                "shop_id": self._shop_id,
                "shop_order_id": shop_order_id,
                "sign": sign}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        response = answer.json()
        url1 = response['data']['url'] 
        logging.info("Programm done with USD")
        return render_template('index.html', payment_currency=self._payment_currency, url1=url1)
    
    def rub(self):
        logging.info("Programm choice RUB")
        url = 'https://core.piastrix.com/invoice/create'
        shop_order_id = "123456"
        payway = 'payeer_rub'
        headers = {'Content-type': 'application/json',  
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'}
        s = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id', 'sign']
        sha = f'{self._amount}:{self._payment_currency1}:{payway}:{self._shop_id}:{shop_order_id}{self._secretKey}'
        sign = hashlib.sha256(f'{sha}'.encode()).hexdigest()
        data = {
            "amount": self._amount,
            "currency": self._payment_currency1,
            "payway": payway,
            "shop_id": self._shop_id,
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
            
        logging.info("Programm done with RUB")
        return render_template('index.html', 
                            payment_currency=self._payment_currency, 
                            url=url, lang=lang, m_curorderid=m_curorderid,
                            m_historyid=m_historyid, m_historytm=m_historytm,
                            referer=referer)

