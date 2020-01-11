from flask import (
                    Flask,
                    render_template,
                    request
                    )
import tem_render 
import hashlib
import re
import logging

app = Flask(__name__)

logging.basicConfig(filename="log_app.log", level=logging.INFO)
logging.debug("This is a debug message")
logging.error("An error has happened!")
logging.info("Programm started")
log = logging.getLogger("ex")


@app.route('/', methods=['POST', 'GET'])
@app.route('/start')
def start():
    print('Start on Huroku 1')
    currency_dict = {'EUR' : '978', 'USD' : '840', 'RUB': '643'}
    error = 'Используйте только цифры. Н-р 15.78'
    amount = ''
    payment_currency = ''
    description = ''
    print('Start on Huroku 2')
    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount:
            return tem_render.CheckAmount(amount, currency_dict, error, payment_currency).check()

    return render_template('index.html', currency_dict=currency_dict, payment_currency=payment_currency)




if __name__ == '__main__':
    app.run(port=5000, debug=True)