import yfinance
import getpass
from arthikaapi.security.user_handler import get_current_user
from loguru import logger
from fastapi import APIRouter, Depends
from arthikaapi.models.users import User
from database import SessionLocal
from arthikaapi.models.stocks import Stocks
from arthikaapi.schemas.stocks import StockCreate
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/arthika", tags=["Shares Information"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stocks")
def get_shares(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stocks = db.query(Stocks).filter(
        Stocks.user_id == current_user.id
    ).all()

    return stocks

@router.post("/{name}/stock")
def add_share(name: str, 
              stock: StockCreate, 
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    purchase_total = stock.quantity * stock.purchase_value
    present_total = stock.quantity * stock.present_value
    difference = present_total - purchase_total

    # Get user id
    #breakpoint()
    #cur_user = getpass.getuser()
    #user_id = db.query(User).filter(User.username == cur_user)
    
    logger.info(f"Adding stock: {name} for the user: {current_user}")

    db_stock = Stocks(name=stock.name,
                      quantity=stock.quantity,
                      purchase_value=stock.purchase_value,
                      present_value=stock.present_value,
                      purchase_total=purchase_total,
                      present_total=present_total,
                      difference=difference,
                      user_id=current_user.id)
    db.add(db_stock)
    db.commit()
    db.refresh