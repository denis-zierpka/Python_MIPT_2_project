from datetime import datetime
from http import HTTPStatus
from threading import Thread
from typing import Any

from flask import Flask

from app.database_interaction import (
    CustomError,
    add_new_currency,
    add_new_user,
    count_of_crypto,
    exchange_currency,
    get_all_currencies,
    get_money_info,
    get_user_history,
    user_currency_status,
)
from app.init_database import init_database, update_rate
from app.local_info import Info, time_of_last_operation

flask_app = Flask(__name__)


@flask_app.before_first_request
def start_work() -> None:
    init_database()
    th = Thread(target=update_rate, daemon=True)
    th.start()


@flask_app.route('/', methods=['post', 'get'])
def home_page() -> Any:
    return Info.welcome_message, HTTPStatus.OK


@flask_app.route('/register/<string:name>', methods=['post', 'get'])
def register(name: str) -> Any:
    try:
        result = add_new_user(name)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/<int:user_id>/money', methods=['post', 'get'])
def money_info(user_id: int) -> Any:
    try:
        result = get_money_info(user_id)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/info/<string:currency_name>', methods=['post', 'get'])
def currency_info(currency_name: str) -> Any:
    try:
        result = count_of_crypto(currency_name)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/<int:user_id>/list', methods=['post', 'get'])
def list_user_status(user_id: int) -> Any:
    try:
        result = user_currency_status(user_id)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route(
    '/<int:user_id>/buy/<string:currency_name>/<string:count>',
    methods=['post', 'get'],
)
def buy(user_id: int, currency_name: str, count: str) -> Any:
    try:
        result = exchange_currency(user_id, currency_name, count, 'buy')
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route(
    '/<int:user_id>/sell/<string:name>/<string:count>',
    methods=['post', 'get'],
)
def sell(user_id: int, name: str, count: str) -> Any:
    try:
        result = exchange_currency(user_id, name, count, 'sell')
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/<int:user_id>/history', methods=['post', 'get'])
def history(user_id: int) -> Any:
    try:
        result = get_user_history(user_id)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/newcurrency/<string:name>/<string:price>', methods=['post', 'get'])
def new_currency(name: str, price: str) -> Any:
    try:
        result = add_new_currency(name, price)
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST


@flask_app.route('/help', methods=['post', 'get'])
def all_currencies() -> Any:
    try:
        result = get_all_currencies()
        return result, HTTPStatus.OK
    except CustomError as ex:
        return ex.message, HTTPStatus.BAD_REQUEST
