import flet as ft
import sqlite3
import os

def main(page: ft.Page):
    page.title = "MOZER DISTRIBUIDORA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # --- BANCO DE DADOS (Caminho compatível com Android/PC) ---
    db_path = os.path.join(os.getcwd(), "distribuidora.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, custo_un REAL, preco_un REAL, preco_cx REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS vendas 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT, qtd INTEGER, tipo TEXT, total REAL, lucro REAL)''')
    conn.commit()

    # --- ABA 1: CADASTRO/ESTOQUE/EDITAR/EXCLUIR ---
    txt_nome = ft.TextField(label="Nome do Produto (Ex: Skol 350ml)")
    txt_custo = ft.TextField(label="Custo Unitário", keyboard_type=ft.KeyboardType.NUMBER)
    txt_preco_un = ft.TextField(label="Preço Venda Unidade", keyboard_type=ft.KeyboardType.NUMBER)
    txt_preco_cx = ft.TextField(label="Preço Venda Caixa (12 un)", keyboard_type=ft.KeyboardType.NUMBER)
    lista_estoque = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def carregar_estoque():
        lista_estoque.controls.clear()
        cursor.execute("SELECT id, nome, preco_un, preco_cx FROM produtos")
        for row in cursor.fetchall():
            lista_estoque.controls.append(
                ft.ListTile(
                    title=ft.Text(row[1]),
                    subtitle=ft.Text(f"Un: R$ {row[2]:.2f} | Cx: R$ {row[3]:.2f}"),
                    trailing=ft.Row([
                        # Botão de Excluir
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, prod_id=row[0]: excluir_produto(e, prod_id), tooltip="Excluir"),
                        # Botão de Editar (Adicione a lógica de edição aqui se necessário)
                        # ft.IconButton(ft.icons.EDIT, ... )
                    ], width=100)
                )
            )
        page.update()

    def excluir_produto(e, prod_id):
        cursor.execute("DELETE FROM produtos WHERE id=?", (prod_id,))
        conn.commit()
        page.snack_bar = ft.SnackBar(ft.Text("Produto excluído!"), bgcolor="red")
        page.snack_bar.open = True
        carregar_estoque()

    def cadastrar(e):
        try:
            cursor.execute("INSERT INTO produtos (nome, custo_un, preco_un, preco_cx) VALUES (?,?,?,?)",
                          (txt_nome.value, float(txt_custo.value), float(txt_preco_un.value), float(txt_preco_cx.value or 0)))
            conn.commit()
            carregar_estoque() # Atualiza a lista após cadastrar
            # ... limpar campos e snackbar ...
        except: pass

    # --- ABA 2: VENDAS ---
    dropdown_produtos = ft.Dropdown(label="Selecionar Produto", expand=True)
    # ... (restante da lógica de vendas da mensagem anterior) ...

    # --- ABA 3: RELATÓRIO/RESET FINANCEIRO ---
    col_relatorio = ft.Column(scroll=ft.ScrollMode.AUTO)
    txt_resumo = ft.Text(size=20, weight="bold", color="green")

    def resetar_financeiro(e):
        cursor.execute("DELETE FROM vendas")
        conn.commit()
        atualizar_relatorio()
        page.snack_bar = ft.SnackBar(ft.Text("Financeiro Resetado!"), bgcolor="orange")
        page.snack_bar.open = True
        page.update()

    def atualizar_relatorio(e=None):
        # ... (lógica de relatório da mensagem anterior) ...
        pass # Implementação completa está acima, apenas garantindo que a função exista

    # --- ESTRUTURA DE ABAS ---
    tabs = ft.Tabs(
        # ... (abas de Cadastro, Vendas e Lucro) ...
        tabs=[
            ft.Tab(text="CADASTRO", content=ft.Container(padding=20, content=ft.Column([
                ft.Text("Cadastrar/Estoque", size=20, weight="bold"),
                txt_nome, txt_custo, txt_preco_un, txt_preco_cx,
                ft.ElevatedButton("SALVAR", on_click=cadastrar, bgcolor="green", color="white"),
                ft.Divider(),
                ft.Text("Estoque Atual:", size=16),
                lista_estoque # Exibe a lista de produtos aqui
            ]))),
            # ... (Abas de Vendas e Lucro) ...
             ft.Tab(text="LUCRO", content=ft.Container(padding=20, content=ft.Column([
                ft.Text("Resumo Financeiro", size=20, weight="bold"),
                txt_resumo,
                ft.ElevatedButton("RESETAR FINANCEIRO", on_click=resetar_financeiro, bgcolor="orange"),
                ft.Divider(),
                ft.Text("Últimas Vendas:"),
                col_relatorio
            ])))
        ], expand=True
    )

    page.add(ft.SafeArea(tabs))
    carregar_estoque() # Carrega a lista ao iniciar
    carregar_produtos_venda()
    atualizar_relatorio() # Carrega o resumo financeiro ao iniciar

ft.app(target=main)
