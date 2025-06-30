from models import CustomerDB, OrderDB, ProductDB
from sqlalchemy.orm import joinedload
from auth.security import hash_password
from logs.logger import setup_logger

logger = setup_logger()

def create_user(db, data):
    new_user = CustomerDB(
        username=data.get("username"),
        password=hash_password(data.get("password")),
        role=data.get("role", "user"),
        firstname=data.get("firstName"),
        lastname=data.get("lastName"),
        street_number=data["address"].get("streetNumber"),
        street=data["address"].get("street"),
        postalcode=data["address"].get("postalCode"),
        city=data["address"].get("city"),
        company_name=data.get("companyName")
    )
    db.add(new_user)
    db.commit()
    logger.debug(f"[✓] Utilisateur {new_user.id} créé.")

def update_user(db, user_id, data):
    user = db.query(CustomerDB).filter(CustomerDB.id == user_id).first()
    if not user:
        logger.debug(f"[!] Utilisateur {user_id} non trouvé pour mise à jour.")
        return

    if "username" in data:
        user.username = data["username"]
    if "password" in data:
        user.password = hash_password(data["password"])
    if "role" in data:
        user.role = data["role"]
    if "firstName" in data:
        user.firstname = data["firstName"]
    if "lastName" in data:
        user.lastname = data["lastName"]
    if "address" in data:
        addr = data["address"]
        if "streetNumber" in addr:
            user.street_number = addr["streetNumber"]
        if "street" in addr:
            user.street = addr["street"]
        if "postalCode" in addr:
            user.postalcode = addr["postalCode"]
        if "city" in addr:
            user.city = addr["city"]
    if "companyName" in data:
        user.company_name = data["companyName"]

    db.commit()
    logger.debug(f"[✓] Utilisateur {user_id} mis à jour.")

def delete_user(db, user_id):
    user = db.query(CustomerDB).filter(CustomerDB.id == user_id).first()
    if not user:
        logger.debug(f"[!] Utilisateur {user_id} non trouvé pour suppression.")
        return

    db.delete(user)
    db.commit()
    logger.debug(f"[✓] Utilisateur {user_id} supprimé.")

def create_order(db, order_id, data):
    new_order = OrderDB(id=order_id, customer_id=data["customer_id"])
    db.add(new_order)

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        new_order.products = products

    db.commit()
    logger.debug(f"[✓] Commande {order_id} créée.")

def update_order(db, order_id, data):
    order = db.query(OrderDB).options(joinedload(OrderDB.products)).filter(OrderDB.id == order_id).first()
    if not order:
        logger.debug(f"[!] Commande {order_id} non trouvée pour mise à jour.")
        return

    if "customer_id" in data:
        order.customer_id = data["customer_id"]

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        order.products = products

    db.commit()
    logger.debug(f"[✓] Commande {order_id} mise à jour.")

def delete_order(db, order_id):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        logger.debug(f"[!] Commande {order_id} non trouvée pour suppression.")
        return

    db.delete(order)
    db.commit()
    logger.debug(f"[✓] Commande {order_id} supprimée.")