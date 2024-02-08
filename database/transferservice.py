from database.models import UserCard, Transfer

from datetime import datetime

from database import get_db


def validate_card(card_number, db):

    exact_card = db.query(UserCard).filter_by(card_number=card_number).first()

    return exact_card


def create_transaction_db(card_from, card_to, amount):
    db = next(get_db())

    check_card_from = validate_card(card_from, db)
    check_card_to = validate_card(card_to, db)

    if check_card_from and check_card_to:
        if check_card_from.balance >= amount:
            check_card_from.balance -= amount

            check_card_to.balance += amount

            new_transaction = Transfer(card_from_id=check_card_from.card_id, card_to_id=check_card_to.card_id, amount=amount, transaction_date=datetime.now())

            db.add(new_transaction)
            db.commit()

            return 'Перевод успешно выполнен'
        else:
            return 'Недостаточно средств на балансе'

    else:
        return f'Одна из карт не существует {check_card_from}, {check_card_to}'


def get_history_transactions(card_from_id):
    db = next(get_db())

    card_transaction = db.query(Transfer).filter_by(card_from_id=card_from_id).all()

    if card_transaction:
        return card_transaction
    else:
        return f'У этого пользователь нету истории'


def cancel_transaction_db(card_from, card_to, amount, transfer_id):
    db = next(get_db())

    check_card_from = validate_card(card_from, db)
    check_card_to = validate_card(card_to, db)

    if check_card_from and check_card_to:
        transaction_to_cancel = db.query(Transfer).filter_by(transfer_id=transfer_id).first()
        if transaction_to_cancel:
            check_card_from.balance += amount
            check_card_to.balance -= amount
            transaction_to_cancel.status = False
            db.delete(transaction_to_cancel)
            db.commit()
            return 'Перевод отменен'
        else:
            return 'Указанный перевод не существует'
    else:
        return f'Одна из карт не существует {check_card_from}, {check_card_to}'




