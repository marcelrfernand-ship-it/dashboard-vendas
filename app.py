import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Executivo de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para dark mode
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e293b 0%, #581c87 50%, #1e293b 100%);
    }
    .stMetric {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(139, 92, 246, 0.3);
    }
    .stMetric label {
        color: #d1d5db !important;
        font-weight: bold;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: white;
        font-size: 36px;
        font-weight: 900;
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stSelectbox label, .stMultiSelect label {
        color: #d1d5db !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ⚠️ ALTERE ESTA SENHA!
SENHA_ADMIN = "admin123"

# Inicializar session state
if 'dados' not in st.session_state:
    st.session_state.dados = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = Smart@0102

# Sidebar - Login Admin
with st.sidebar:
    st.markdown("### 🔐 Área do Administrador")
    
    if not st.session_state.is_admin:
        senha_input = st.text_input("Senha Admin", type="password")
        if st.button("🔓 Entrar como Admin"):
            if senha_input == SENHA_ADMIN:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta!")
    else:
        st.success("✅ Logado como Admin")
        
        uploaded_file = st.file_uploader("📁 Upload Excel", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                
                if df.columns[0].startswith('Unnamed'):
                    df = pd.read_excel(uploaded_file, skiprows=1)
                if df.columns[0].startswith('Unnamed'):
                    df = pd.read_excel(uploaded_file, skiprows=2)
                
                st.session_state.dados = df
                st.success(f"✅ {len(df)} registros carregados!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {e}")
        
        if st.button("🚪 Sair"):
            st.session_state.is_admin = False
            st.rerun()

if st.session_state.dados is None:
    st.markdown("""
    <div style='text-align: center; padding: 100px;'>
        <h1 style='color: white; font-size: 48px;'>📊 Dashboard Executivo de Vendas</h1>
        <p style='color: #d1d5db; font-size: 20px; margin-top: 20px;'>
            Nenhum dado disponível ainda.
        </p>
        <p style='color: #9ca3af; font-size: 16px;'>
            👈 Use a área admin na barra lateral para fazer upload do arquivo Excel
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = st.session_state.dados.copy()

st.markdown("""
<div style='background: linear-gradient(90deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%); 
            padding: 30px; border-radius: 20px; margin-bottom: 30px;'>
    <h1 style='color: white; margin: 0;'>Dashboard Executivo de Vendas</h1>
    <p style='color: rgba(255,255,255,0.8); margin: 10px 0 0 0;'>
        Análise Estratégica • Outubro 2025
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Filtros Inteligentes")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    vendedores = ['Todos'] + sorted(df['VENDEDOR'].dropna().unique().tolist())
    filtro_vendedor = st.multiselect('Vendedor', vendedores, default=['Todos'])

with col2:
    tipos = ['Todos'] + sorted(df['TIPO TRANSAÇÃO'].dropna().unique().tolist())
    filtro_tipo = st.multiselect('Tipo', tipos, default=['Todos'])

with col3:
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    meses_disponiveis = ['Todos'] + [m for m in meses if m in df['MES'].values]
    filtro_mes = st.multiselect('Mês', meses_disponiveis, default=['Todos'])

with col4:
    estados = ['Todos'] + sorted(df['ESTADO'].dropna().unique().tolist())
    filtro_estado = st.multiselect('Estado', estados, default=['Todos'])

with col5:
    fabricantes = ['Todos'] + sorted(df['FABRICANTE'].dropna().unique().tolist())
    filtro_fabricante = st.multiselect('Fabricante', fabricantes, default=['Todos'])

with col6:
    clientes = ['Todos'] + sorted(df['CLIENTE AJUSTADO'].dropna().unique().tolist())
    filtro_cliente = st.multiselect('Cliente', clientes[:100], default=['Todos'])

df_filtrado = df.copy()

if 'Todos' not in filtro_vendedor and len(filtro_vendedor) > 0:
    df_filtrado = df_filtrado[df_filtrado['VENDEDOR'].isin(filtro_vendedor)]
if 'Todos' not in filtro_tipo and len(filtro_tipo) > 0:
    df_filtrado = df_filtrado[df_filtrado['TIPO TRANSAÇÃO'].isin(filtro_tipo)]
if 'Todos' not in filtro_mes and len(filtro_mes) > 0:
    df_filtrado = df_filtrado[df_filtrado['MES'].isin(filtro_mes)]
if 'Todos' not in filtro_estado and len(filtro_estado) > 0:
    df_filtrado = df_filtrado[df_filtrado['ESTADO'].isin(filtro_estado)]
if 'Todos' not in filtro_fabricante and len(filtro_fabricante) > 0:
    df_filtrado = df_filtrado[df_filtrado['FABRICANTE'].isin(filtro_fabricante)]
if 'Todos' not in filtro_cliente and len(filtro_cliente) > 0:
    df_filtrado = df_filtrado[df_filtrado['CLIENTE AJUSTADO'].isin(filtro_cliente)]

st.info(f"📊 Exibindo {len(df_filtrado)} de {len(df)} registros")

st.markdown("### 📈 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total_vendas = df_filtrado['TOTAL VP'].sum()
total_margem = df_filtrado['VALOR MARGEM CONTRIBUICAO'].sum()
margem_perc = (total_margem / total_vendas * 100) if total_vendas > 0 else 0
ticket_medio = df_filtrado['TOTAL VP'].mean()
clientes_unicos = df_filtrado['COD CLIENTE'].nunique()

with col1:
    st.metric("💰 Faturamento Total", f"R$ {total_vendas:,.0f}", 
              f"{len(df_filtrado)} transações")
with col2:
    st.metric("📊 Margem", f"R$ {total_margem:,.0f}", 
              f"{margem_perc:.1f}%")
with col3:
    st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.0f}")
with col4:
    st.metric("👥 Clientes Únicos", f"{clientes_unicos}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📅 Evolução Mensal")
    vendas_mes = df_filtrado.groupby('MES').agg({
        'TOTAL VP': 'sum',
        'VALOR MARGEM CONTRIBUICAO': 'sum'
    }).reset_index()
    
    ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    vendas_mes['ordem'] = vendas_mes['MES'].apply(lambda x: ordem_meses.index(x) if x in ordem_meses else 99)
    vendas_mes = vendas_mes.sort_values('ordem')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vendas_mes['MES'], y=vendas_mes['TOTAL VP']/1000,
                            name='Faturamento', fill='tozeroy', line=dict(color='#8b5cf6')))
    fig.add_trace(go.Scatter(x=vendas_mes['MES'], y=vendas_mes['VALOR MARGEM CONTRIBUICAO']/1000,
                            name='Margem', fill='tozeroy', line=dict(color='#ec4899')))
    fig.update_layout(height=400, template='plotly_dark', 
                     yaxis_title='R$ (milhares)', showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top 5 Vendedores")
    top_vendedores = df_filtrado.groupby('VENDEDOR')['TOTAL VP'].sum().sort_values(ascending=True).tail(5)
    
    fig = go.Figure(go.Bar(
        x=top_vendedores.values,
        y=top_vendedores.index,
        orientation='h',
        marker=dict(color='#8b5cf6')
    ))
    fig.update_layout(height=400, template='plotly_dark',
                     xaxis_title='Faturamento (R$)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🎯 Top 30 Clientes")

top_clientes = df_filtrado.groupby('CLIENTE AJUSTADO').agg({
    'TOTAL VP': 'sum',
    'VALOR MARGEM CONTRIBUICAO': 'sum',
    'COD CLIENTE': 'count',
    'ESTADO': 'first',
    'VENDEDOR': 'first'
}).reset_index()

top_clientes.columns = ['Cliente', 'Total', 'Margem', 'Qtd Vendas', 'Estado', 'Vendedor']
top_clientes['% Margem'] = (top_clientes['Margem'] / top_clientes['Total'] * 100).round(1)
top_clientes['Ticket Médio'] = (top_clientes['Total'] / top_clientes['Qtd Vendas']).round(0)
top_clientes = top_clientes.sort_values('Total', ascending=False).head(30)
top_clientes.insert(0, '#', range(1, len(top_clientes) + 1))

top_clientes['Total'] = top_clientes['Total'].apply(lambda x: f"R$ {x:,.0f}")
top_clientes['Margem'] = top_clientes['Margem'].apply(lambda x: f"R$ {x:,.0f}")
top_clientes['Ticket Médio'] = top_clientes['Ticket Médio'].apply(lambda x: f"R$ {x:,.0f}")

st.dataframe(top_clientes, use_container_width=True, height=600)

st.markdown("---")
st.markdown("### 👨‍💼 Detalhamento por Vendedor")

vendedores_detalhado = df_filtrado.groupby('VENDEDOR').agg({
    'TOTAL VP': 'sum',
    'VALOR MARGEM CONTRIBUICAO': 'sum',
    'COD CLIENTE': ['count', 'nunique']
}).reset_index()

vendedores_detalhado.columns = ['Vendedor', 'Total', 'Margem', 'Qtd Vendas', 'Clientes']
vendedores_detalhado['% Margem'] = (vendedores_detalhado['Margem'] / vendedores_detalhado['Total'] * 100).round(1)
vendedores_detalhado['Ticket Médio'] = (vendedores_detalhado['Total'] / vendedores_detalhado['Qtd Vendas']).round(0)
vendedores_detalhado = vendedores_detalhado.sort_values('Total', ascending=False).head(10)

vendedores_detalhado['Total'] = vendedores_detalhado['Total'].apply(lambda x: f"R$ {x:,.0f}")
vendedores_detalhado['Margem'] = vendedores_detalhado['Margem'].apply(lambda x: f"R$ {x:,.0f}")
vendedores_detalhado['Ticket Médio'] = vendedores_detalhado['Ticket Médio'].apply(lambda x: f"R$ {x:,.0f}")

st.dataframe(vendedores_detalhado, use_container_width=True, height=400)
