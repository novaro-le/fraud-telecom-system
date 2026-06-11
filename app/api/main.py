from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import joblib

from database.database import engine, SessionLocal, Base
from database.models import Transaction


# ====================================================
# INITIALISATION SQLITE
# ====================================================
Base.metadata.create_all(bind=engine)


# ====================================================
# APPLICATION FASTAPI
# ====================================================
app = FastAPI(
    title="Fraud Detection API",
    version="1.0.0",
    description="API de détection de fraude télécom"
)


# ====================================================
# CONFIGURATION
# ====================================================
MODEL_PATH = Path("/app/model/fraud_model.pkl")

FRAUD_THRESHOLD = 0.20


# ====================================================
# CHARGEMENT DU MODELE
# ====================================================
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Modèle introuvable : {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

EXPECTED_COLUMNS = (
    model.get_booster().feature_names
    if hasattr(model, "get_booster")
    else None
)


# ====================================================
# SCHEMA ENTREE
# ====================================================
class TransactionInput(BaseModel):
    step: int

    type_TRANSFER: int
    type_CASH_OUT: int
    type_PAYMENT: int
    type_DEBIT: int

    amount: float

    oldbalanceOrg: float
    newbalanceOrig: float

    oldbalanceDest: float
    newbalanceDest: float


# ====================================================
# FEATURE ENGINEERING
# ====================================================
def feature_engineering(df):

    df["balance_diff"] = (
        df["oldbalanceOrg"]
        - df["newbalanceOrig"]
    )

    df["error_balance"] = (
        df["newbalanceOrig"]
        + df["amount"]
        - df["oldbalanceOrg"]
    )

    return df


# ====================================================
# PREPARATION DES DONNEES
# ====================================================
def prepare_data(transaction):

    df = pd.DataFrame(
        [transaction.model_dump()]
    )

    df = feature_engineering(df)

    if EXPECTED_COLUMNS:
        df = df.reindex(
            columns=EXPECTED_COLUMNS,
            fill_value=0
        )

    return df


# ====================================================
# ROUTES DE BASE
# ====================================================
@app.get("/")
def home():

    return {
        "message": "Fraud Detection API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.get("/model-info")
def model_info():

    return {
        "model": type(model).__name__,
        "threshold": FRAUD_THRESHOLD,
        "features": EXPECTED_COLUMNS
    }


# ====================================================
# HISTORIQUE SQLITE
# ====================================================
@app.get("/history")
def get_history():

    db = SessionLocal()

    try:

        transactions = db.query(Transaction).all()

        return [
            {
                "id": t.id,
                "amount": t.amount,
                "oldbalanceOrg": t.oldbalanceOrg,
                "newbalanceOrig": t.newbalanceOrig,
                "is_fraud": t.is_fraud,
                "fraud_probability": t.fraud_probability,
                "transaction_type": t.transaction_type,
                "created_at": t.created_at
            }
            for t in transactions
        ]

    finally:
        db.close()



@app.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        total_transactions = db.query(
            Transaction
        ).count()

        total_frauds = db.query(
            Transaction
        ).filter(
            Transaction.is_fraud == 1
        ).count()

        fraud_rate = (
            (total_frauds / total_transactions) * 100
            if total_transactions > 0
            else 0
        )

        avg_probability = db.query(
            Transaction
        ).with_entities(
            Transaction.fraud_probability
        ).all()

        if avg_probability:

            avg_probability = sum(
                p[0] for p in avg_probability
            ) / len(avg_probability)

        else:

            avg_probability = 0

        return {
            "total_transactions": total_transactions,
            "total_frauds": total_frauds,
            "fraud_rate": round(fraud_rate, 2),
            "avg_fraud_probability": round(
                avg_probability,
                4
            )
        }

    finally:

        db.close()

# ====================================================
# PREDICTION
# ====================================================
@app.post("/predict")
def predict(transaction: TransactionInput):

    db = SessionLocal()

    try:

        df = prepare_data(transaction)

        probability = float(
            model.predict_proba(df)[0][1]
        )

        prediction = int(
            probability >= FRAUD_THRESHOLD
        )

        transaction_type = (
            "TRANSFER" if transaction.type_TRANSFER else
            "CASH_OUT" if transaction.type_CASH_OUT else
            "PAYMENT" if transaction.type_PAYMENT else
            "DEBIT"
        )

        record = Transaction(
            amount=transaction.amount,
            oldbalanceOrg=transaction.oldbalanceOrg,
            newbalanceOrig=transaction.newbalanceOrig,
            is_fraud=prediction,
            fraud_probability=probability,
            transaction_type=transaction_type
        )

        db.add(record)
        db.commit()

        return {
            "isFraud": prediction,
            "fraud_probability": round(probability, 6),
            "threshold": FRAUD_THRESHOLD
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()