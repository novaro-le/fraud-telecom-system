import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# ==================================
# CONFIG
# ==================================
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ==================================
# CSS
# ==================================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
}

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #0f172a,
        #1e293b
    );
}

.stButton > button{
    width:100%;
    background:linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    font-weight:bold;
}

.kpi-card{
    background:rgba(255,255,255,0.12);
    padding:20px;
    border-radius:20px;
    text-align:center;
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.15);
    box-shadow:0 8px 25px rgba(0,0,0,0.3);
    transition:0.3s;
}

.kpi-card:hover{
    transform:translateY(-5px);
}


.kpi-title{
    color:#cbd5e1;
    font-size:16px;
}

.kpi-value{
    color:white;
    font-size:30px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# HEADER
# ==================================
st.markdown(
    "<div class='main-title'>🛡️ Fraud Detection System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Détection intelligente de fraude télécom avec Machine Learning</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ==================================
# API
# ==================================
API_PREDICT = "http://api:8000/predict"
API_HISTORY = "http://api:8000/history"

# ==================================
# FONCTIONS
# ==================================
def predict_fraud(transaction):

    try:

        response = requests.post(
            API_PREDICT,
            json=transaction,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(f"Erreur API : {e}")

        return {
            "isFraud": 0,
            "fraud_probability": 0.0
        }


def load_history():

    try:

        response = requests.get(
            API_HISTORY,
            timeout=10
        )

        response.raise_for_status()

        return pd.DataFrame(
            response.json()
        )

    except Exception as e:

        st.error(f"Erreur historique : {e}")

        return pd.DataFrame()

# ==================================
# SIDEBAR
# ==================================
st.sidebar.title("⚙️ Simulation")

step = st.sidebar.number_input(
    "Step",
    min_value=1,
    value=1
)

transaction_type = st.sidebar.selectbox(
    "Type",
    [
        "TRANSFER",
        "CASH_OUT",
        "PAYMENT",
        "DEBIT"
    ]
)

amount = st.sidebar.number_input(
    "Montant",
    min_value=0.0,
    value=1000.0
)

oldbalanceOrg = st.sidebar.number_input(
    "Solde source avant",
    min_value=0.0,
    value=5000.0
)

newbalanceOrig = st.sidebar.number_input(
    "Solde source après",
    min_value=0.0,
    value=4000.0
)

oldbalanceDest = st.sidebar.number_input(
    "Solde destination avant",
    min_value=0.0,
    value=2000.0
)

newbalanceDest = st.sidebar.number_input(
    "Solde destination après",
    min_value=0.0,
    value=3000.0
)

simulate = st.sidebar.button(
    " Simuler"
)

refresh = st.sidebar.button(
    " Actualiser"
)
if refresh:
    st.rerun()
# ==================================
# PREDICTION
# ==================================
if simulate:

    transaction = {
        "step": step,
        "type_TRANSFER": int(transaction_type == "TRANSFER"),
        "type_CASH_OUT": int(transaction_type == "CASH_OUT"),
        "type_PAYMENT": int(transaction_type == "PAYMENT"),
        "type_DEBIT": int(transaction_type == "DEBIT"),
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    result = predict_fraud(transaction)

    risk = result["fraud_probability"]

    st.subheader("Résultat de l'analyse")

    st.progress(min(float(risk), 1.0))

    st.metric(
        "Probabilité de fraude",
        f"{risk:.2%}"
             )

    if result["isFraud"] == 1:

        st.error(
            f"🚨 FRAUDE DETECTÉE\n\nProbabilité : {risk:.2%}"
        )

    else:

        st.success(
            f" Transaction normale\n\nProbabilité : {risk:.2%}"
        )

# ==================================
# HISTORIQUE SQLITE
# ==================================
history_db = load_history()

if not history_db.empty:

    history_db = history_db.sort_values(
        by="created_at",
        ascending=False
    )

    history_db["created_at"] = pd.to_datetime(
        history_db["created_at"]
    )

    history_db["created_at"] = (
        history_db["created_at"]
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

# ==================================
# KPI
# ==================================
if not history_db.empty:

    total_transactions = len(history_db)

    total_frauds = int(
        history_db["is_fraud"].sum()
    )

    avg_prob = float(
        history_db["fraud_probability"].mean()
    )

    fraud_rate = (
        total_frauds /
        total_transactions
    ) * 100
    
    total_amount = float(
        history_db["amount"].sum()
    )
    fraud_amount = history_db.loc[
    history_db["is_fraud"] == 1,
    "amount"
    ].sum()

else:

    total_transactions = 0
    total_frauds = 0
    avg_prob = 0
    fraud_rate = 0
    total_amount = 0
    fraud_amount = 0

st.subheader(" Indicateurs Clés")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Transactions</div>
        <div class="kpi-value">{total_transactions}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Fraudes</div>
        <div class="kpi-value">{total_frauds}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Risque Moyen</div>
        <div class="kpi-value">{avg_prob:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Taux Fraude</div>
        <div class="kpi-value">{fraud_rate:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Montant Total</div>
        <div class="kpi-value">{total_amount:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🚨 Montant Frauduleux</div>
        <div class="kpi-value">{fraud_amount:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


st.markdown("---")
st.subheader(" Niveau de Risque Global")
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_prob * 100,
    title={"text": "Risque Moyen (%)"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#06b6d4"},
        "steps": [
            {"range": [0, 30], "color": "#22c55e"},
            {"range": [30, 70], "color": "#f59e0b"},
            {"range": [70, 100], "color": "#ef4444"}
        ]
    }
))

st.plotly_chart(
    gauge,
    use_container_width=True
)
#
# ==================================
# TABLEAU
# ==================================

st.subheader("Historique SQLite")

if not history_db.empty:

    def color_fraud(row):
        if row["is_fraud"] == 1:
            return ["background-color:#7f1d1d;color:white"] * len(row)
        else:
            return ["background-color:#052e16;color:white"] * len(row)

    st.dataframe(
        history_db.style.apply(color_fraud, axis=1),
        use_container_width=True
    )

else:
    st.warning("Aucune transaction enregistrée.")




# ==================================
# TOP 10 RISQUES
# ==================================

st.subheader(" Top 10 Transactions les Plus Risquées")

if not history_db.empty:

    top_risk = (
        history_db
        .sort_values(
            by="fraud_probability",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_risk.style.background_gradient(
            subset=["fraud_probability"],
            cmap="Reds"
        ),
        use_container_width=True
    )

else:

    st.info(
        "Aucune transaction disponible."
    )


# ==================================
# FRAUDES PAR TYPE
# ==================================


st.subheader(" Répartition des Fraudes par Type")

required_col = "transaction_type"

if history_db.empty:
    st.warning("Aucune donnée disponible.")
elif required_col not in history_db.columns:
    st.error(f"Colonne manquante : {required_col}")
else:
    st.bar_chart(history_db.groupby(required_col).size())

fraud_by_type = (
    history_db.groupby(
        "transaction_type"
    )["is_fraud"]
    .sum()
    .reset_index()
)

fig_type = px.bar(
    fraud_by_type,
    x="transaction_type",
    y="is_fraud",
    color="transaction_type",
    title="Nombre de Fraudes par Type de Transaction"
)

st.plotly_chart(
    fig_type,
    use_container_width=True
)
# ==================================
# VISUALISATIONS
# ==================================
if not history_db.empty:

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.pie(
            history_db,
            names="is_fraud",
            hole=0.70,
            color="is_fraud",
            title="Fraude vs Normal",
            color_discrete_map={
                0: "#22c55e",
                1: "#ef4444"
    }
)
        

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2 = px.histogram(
            history_db,
            x="amount",
            color="is_fraud",
            nbins=20,
            title="Distribution des Montants",
            color_discrete_map={
            0:"#3b82f6",
            1:"#ef4444"
    }
)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    fig3 = px.line(
        history_db,
        x="created_at",
        y="fraud_probability",
        color="transaction_type",
        markers=True,
        title="Evolution du risque"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )
    
    fig4 = px.scatter(
        history_db,
        x="created_at",
        y="amount",
        size="fraud_probability",
        color="is_fraud",
        hover_data=[
        "transaction_type"
    ],
        title="Evolution des Transactions"
)

    st.plotly_chart(
        fig4,
        use_container_width=True
)