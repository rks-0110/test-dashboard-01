# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__) # cria o aplicativo do flask (sempre que usar o dash necessário fazer isso)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#arq = sys.argv[1] # Não é possível passar parametros de linha de comnado (aparentemente)
with open('parametro.txt', 'r') as file:
    arq = file.read().strip()
#df = pd.read_excel("Vendas.xlsx")
df = pd.read_excel(arq)

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group") # criando o gráfico aqui
opc = list(df['ID Loja'].unique())
opc.append('Todas as Lojas')

# layout do dash
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o Faturamento de Todos os Produtos separados por Loja'),
    # usando itens de html (itens puramente visuais / fixas / não relacionadas ao gráfico)
    html.Div(children=''' 
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),

    #html.Div(id='texto'),
    dcc.Dropdown(opc, value='Todas as Lojas', id='lista_lojas'),
    # usando itens de dashboard (itens dinâmicos / interage com um gráfico)
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])

@app.callback(
    #Output('texto', 'children'),
    Output('grafico_quantidade_vendas', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja']==value, :] # .loc[coluna, linha] (: representa todos)
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    #return f'You have selected {value}'
    return fig

"""
<html>
    <body>
        <div>
            <h1></h1>
            <div>
                <'dashboard'></'dashboard'>
            </div>
        </div>
    </body>
</html>
"""

# coloca no ar o site
if __name__ == '__main__':
    app.run(debug=True)
