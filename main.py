import streamlit as st
import pandas as pd
from datetime import date

# Inicializar o estado da sessão para dataframes
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Veículo", "KM Inicial", 
                                                "Data de Cadastro", 
                                                "Combustível", 
                                                "Capacidade do Tanque (L)"])

if 'df_abastecimentos' not in st.session_state:
    st.session_state.df_abastecimentos = pd.DataFrame(columns=["Veículo", 
                                                               "KM Atual",
                                                               "Quantidade Litros", 
                                                               "Preço por Litro", 
                                                               "Tipo de Combustível", 
                                                               "Data do Abastecimento",
                                                               "Consumo (km/L)"])

# Função para formatar moeda
def format_currency(value):
    return f"R${value:.2f}"

# Função para registrar um novo veículo
def cadastrar_veiculo():
    nome_veiculo = st.text_input("Nome do Veículo:")
    km_inicial = st.number_input("KM Inicial:", min_value=0.0, step=0.1)
    data_cadastro = st.date_input("Data de Cadastro:")
    combustivel = st.selectbox("Combustível:", ["Gasolina", "Etanol", "Gas"])
    capacidade_tanque = st.number_input("Capacidade do Tanque (L):", min_value=0.0, step=0.1)
    
    if st.button("Cadastrar Veículo"):
        new_row = pd.DataFrame({
            "Veículo": [nome_veiculo],
            "KM Inicial": [km_inicial],
            "Data de Cadastro": [data_cadastro],
            "Combustível": [combustivel],
            "Capacidade do Tanque (L)": [capacidade_tanque]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success("Veículo cadastrado com sucesso!")

# Função para editar dados do veículo
def editar_veiculo():
    if not st.session_state.df.empty:
        veiculo_para_editar = st.selectbox("Selecione o veículo para editar:", st.session_state.df["Veículo"].unique())
        if veiculo_para_editar:
            idx = st.session_state.df.index[st.session_state.df["Veículo"] == veiculo_para_editar].tolist()[0]
            
            novo_nome = st.text_input("Nome do Veículo:", value=st.session_state.df.loc[idx, "Veículo"])
            novo_km = st.number_input("KM Inicial:", value=float(st.session_state.df.loc[idx, "KM Inicial"]), min_value=0.0, step=0.1)
            nova_data = st.date_input("Data de Cadastro:", value=pd.to_datetime(st.session_state.df.loc[idx, "Data de Cadastro"]).date())
            novo_combustivel = st.selectbox("Combustível:", ["Gasolina", "Etanol", "Gas"], index=["Gasolina", "Etanol", "Gas"].index(st.session_state.df.loc[idx, "Combustível"]))
            nova_capacidade = st.number_input("Capacidade do Tanque (L):", value=float(st.session_state.df.loc[idx, "Capacidade do Tanque (L)"]), min_value=0.0, step=0.1)
            
            if st.button("Atualizar Veículo"):
                st.session_state.df.loc[idx] = [novo_nome, novo_km, nova_data, novo_combustivel, nova_capacidade]
                st.success("Veículo atualizado com sucesso!")
    else:
        st.info("Nenhum veículo cadastrado para editar.")

# Função para registrar um novo abastecimento
def cadastrar_abastecimento():
    if not st.session_state.df.empty:
        veiculo = st.selectbox("Selecione um veículo:", st.session_state.df["Veículo"].unique())
        km_atual = st.number_input("KM Atual:", min_value=0.0, step=0.1)
        quantidade_litros = st.number_input("Quantidade Litros:", min_value=0.0, step=0.1)
        preco_por_litro = st.number_input("Preço por Litro:", min_value=0.0, step=0.01)
        tipo_combustivel = st.selectbox("Tipo de Combustível:", ["Gasolina", "Etanol", "Gas"])
        data_abastecimento = st.date_input("Data do Abastecimento:", value=date.today())
        
        if st.button("Cadastrar Abastecimento"):
            km_inicial = st.session_state.df[st.session_state.df["Veículo"] == veiculo]["KM Inicial"].values[0]
            consumo = (km_atual - km_inicial) / quantidade_litros if quantidade_litros > 0 else 0
            
            new_row = pd.DataFrame({
                "Veículo": [veiculo],
                "KM Atual": [km_atual],
                "Quantidade Litros": [quantidade_litros],
                "Preço por Litro": [preco_por_litro],
                "Tipo de Combustível": [tipo_combustivel],
                "Data do Abastecimento": [data_abastecimento],
                "Consumo (km/L)": [consumo]
            })
            st.session_state.df_abastecimentos = pd.concat([st.session_state.df_abastecimentos, new_row], ignore_index=True)
            
            # Atualizar KM Inicial no dataframe de veículos
            idx = st.session_state.df.index[st.session_state.df["Veículo"] == veiculo].tolist()[0]
            st.session_state.df.loc[idx, "KM Inicial"] = km_atual
            
            st.success("Abastecimento cadastrado com sucesso!")
    else:
        st.warning("Cadastre um veículo primeiro.")

# Função para editar dados de abastecimento
def editar_abastecimento():
    if not st.session_state.df_abastecimentos.empty:
        veiculo_para_editar = st.selectbox("Selecione o veículo:", st.session_state.df_abastecimentos["Veículo"].unique())
        if veiculo_para_editar:
            abastecimentos_veiculo = st.session_state.df_abastecimentos[st.session_state.df_abastecimentos["Veículo"] == veiculo_para_editar]
            abastecimento_para_editar = st.selectbox("Selecione o abastecimento para editar:", 
                                                     abastecimentos_veiculo.apply(lambda row: f"{row['Data do Abastecimento']} - {row['Quantidade Litros']}L de {row['Tipo de Combustível']}", axis=1))
            
            if abastecimento_para_editar:
                idx = abastecimentos_veiculo.index[abastecimentos_veiculo.apply(lambda row: f"{row['Data do Abastecimento']} - {row['Quantidade Litros']}L de {row['Tipo de Combustível']}", axis=1) == abastecimento_para_editar].tolist()[0]
                
                novo_km_atual = st.number_input("KM Atual:", value=float(st.session_state.df_abastecimentos.loc[idx, "KM Atual"]), min_value=0.0, step=0.1)
                nova_quantidade = st.number_input("Quantidade Litros:", value=float(st.session_state.df_abastecimentos.loc[idx, "Quantidade Litros"]), min_value=0.0, step=0.1)
                novo_preco = st.number_input("Preço por Litro:", value=float(st.session_state.df_abastecimentos.loc[idx, "Preço por Litro"]), min_value=0.0, step=0.01)
                novo_tipo = st.selectbox("Tipo de Combustível:", ["Gasolina", "Etanol", "Gas"], index=["Gasolina", "Etanol", "Gas"].index(st.session_state.df_abastecimentos.loc[idx, "Tipo de Combustível"]))
                nova_data = st.date_input("Data do Abastecimento:", value=pd.to_datetime(st.session_state.df_abastecimentos.loc[idx, "Data do Abastecimento"]).date())
                
                if st.button("Atualizar Abastecimento"):
                    km_inicial = st.session_state.df[st.session_state.df["Veículo"] == veiculo_para_editar]["KM Inicial"].values[0]
                    novo_consumo = (novo_km_atual - km_inicial) / nova_quantidade if nova_quantidade > 0 else 0
                    
                    st.session_state.df_abastecimentos.loc[idx] = [veiculo_para_editar, novo_km_atual, nova_quantidade, novo_preco, novo_tipo, nova_data, novo_consumo]
                    
                    # Atualizar KM Inicial no dataframe de veículos
                    idx_veiculo = st.session_state.df.index[st.session_state.df["Veículo"] == veiculo_para_editar].tolist()[0]
                    st.session_state.df.loc[idx_veiculo, "KM Inicial"] = novo_km_atual
                    
                    st.success("Abastecimento atualizado com sucesso!")
    else:
        st.info("Nenhum abastecimento cadastrado para editar.")

# Função para exibir veículos
def exibir_veiculos():
    if not st.session_state.df.empty:
        st.write(st.session_state.df)
    else:
        st.info("Nenhum veículo cadastrado.")

# Função para exibir abastecimentos
def exibir_abastecimentos():
    if not st.session_state.df_abastecimentos.empty:
        df_display = st.session_state.df_abastecimentos.copy()
        df_display["Preço por Litro"] = df_display["Preço por Litro"].apply(format_currency)
        df_display["Quantidade Litros"] = df_display["Quantidade Litros"].apply(lambda x: f"{x:.1f}L")
        df_display["Consumo (km/L)"] = df_display["Consumo (km/L)"].apply(lambda x: f"{x:.2f}km/L")
        st.write(df_display)
    else:
        st.info("Nenhum abastecimento cadastrado.")

# Função para exibir despesas totais por veículo
def exibir_gastos_totais_veiculo():
    if not st.session_state.df_abastecimentos.empty:
        gastos_totais = st.session_state.df_abastecimentos.groupby("Veículo").apply(lambda x: (x["Quantidade Litros"] * x["Preço por Litro"]).sum())
        gastos_totais = gastos_totais.apply(format_currency)
        st.write(gastos_totais)
    else:
        st.info("Nenhum dado de abastecimento disponível.")

# Função para exibir despesas totais por tipo de combustível
def exibir_gastos_totais_combustivel():
    if not st.session_state.df_abastecimentos.empty:
        gastos_totais_combustivel = st.session_state.df_abastecimentos.groupby("Tipo de Combustível").apply(lambda x: (x["Quantidade Litros"] * x["Preço por Litro"]).sum())
        gastos_totais_combustivel = gastos_totais_combustivel.apply(format_currency)
        st.write(gastos_totais_combustivel)
    else:
        st.info("Nenhum dado de abastecimento disponível.")

# Função para exibir despesas totais por período de tempo
def exibir_gastos_totais_periodo():
    if not st.session_state.df_abastecimentos.empty:
        df_temp = st.session_state.df_abastecimentos.copy()
        df_temp['Data do Abastecimento'] = pd.to_datetime(df_temp['Data do Abastecimento'])
        gastos_totais_periodo = df_temp.groupby(df_temp['Data do Abastecimento'].dt.to_period('M')).apply(lambda x: (x["Quantidade Litros"] * x["Preço por Litro"]).sum())
        gastos_totais_periodo = gastos_totais_periodo.apply(format_currency)
        st.write(gastos_totais_periodo)
    else:
        st.info("Nenhum dado de abastecimento disponível.")

# Função para exibir o consumo médio por veículo
def exibir_consumo_medio_veiculo():
    if not st.session_state.df_abastecimentos.empty:
        consumo_medio = st.session_state.df_abastecimentos.groupby("Veículo")["Consumo (km/L)"].mean()
        consumo_medio = consumo_medio.apply(lambda x: f"{x:.2f}km/L")
        st.write(consumo_medio)
    else:
        st.info("Nenhum dado de abastecimento disponível.")

# Criar a aplicação Streamlit
st.title("Gerenciamento de Consumo de Combustível")

# Barra lateral para navegação
menu = st.sidebar.selectbox("Menu", ["Cadastrar Veículo", "Editar Veículo", "Cadastrar Abastecimento", "Editar Abastecimento", "Visualizar Dados", "Relatórios"])

if menu == "Cadastrar Veículo":
    st.header("Cadastrar Veículo")
    cadastrar_veiculo()

elif menu == "Editar Veículo":
    st.header("Editar Veículo")
    editar_veiculo()

elif menu == "Cadastrar Abastecimento":
    st.header("Cadastrar Abastecimento")
    cadastrar_abastecimento()

elif menu == "Editar Abastecimento":
    st.header("Editar Abastecimento")
    editar_abastecimento()

elif menu == "Visualizar Dados":
    st.header("Veículos Cadastrados")
    exibir_veiculos()
    st.header("Abastecimentos Cadastrados")
    exibir_abastecimentos()
    
elif menu == "Relatórios":
    st.header("Consumo Km/L")
    exibir_consumo_medio_veiculo()
    st.header("Gasto em R$")
    exibir_gastos_totais_periodo()
    st.header("Gasto por veículo")
    exibir_gastos_totais_veiculo()
    st.header("Gasto por combustível")
    exibir_gastos_totais_combustivel()
    st.header("Gasto total")
    exibir_gastos_totais_periodo()


# Salvar os dados
if st.sidebar.button("Salvar Dados"):
    st.session_state.df.to_csv("consumo_combustivel.csv", index=False)
    st.session_state.df_abastecimentos.to_csv("abastecimentos.csv", index=False)
    st.sidebar.success("Dados salvos com sucesso!")