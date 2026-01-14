import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "MOZER SYSTEM v2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # --- BANCO DE DADOS (Igual ao seu) ---
    conn = sqlite3.connect('mozer_master_2026.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo TEXT UNIQUE, nome TEXT, 
         custo_compra REAL, preco_un REAL, preco_cx REAL, divisor INTEGER)''')
    conn.commit()

    # --- COMPONENTES DE INTERFACE ---
    txt_nome = ft.TextField(label="Nome do Produto")
    txt_custo = ft.TextField(label="Custo Compra", keyboard_type=ft.KeyboardType.NUMBER)
    txt_preco_un = ft.TextField(label="Preço Unidade", keyboard_type=ft.KeyboardType.NUMBER)
    
    lista_produtos = ft.Column()

    def salvar_produto(e):
        try:
            cursor.execute("INSERT INTO produtos (nome, custo_compra, preco_un) VALUES (?,?,?)", 
                          (txt_nome.value, float(txt_custo.value), float(txt_preco_un.value)))
            conn.commit()
            txt_nome.value = ""
            txt_custo.value = ""
            txt_preco_un.value = ""
            atualizar_lista()
            page.show_snack_bar(ft.SnackBar(ft.Text("Produto Salvo!")))
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Erro: {ex}")))

    def atualizar_lista():
        lista_produtos.controls.clear()
        cursor.execute("SELECT nome, preco_un FROM produtos")
        for row in cursor.fetchall():
            lista_produtos.controls.append(ft.ListTile(title=ft.Text(row[0]), subtitle=ft.Text(f"R$ {row[1]}")))
        page.update()

    # --- LAYOUT EM ABAS (Mobile Style) ---
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="CADASTRO", content=ft.Column([
                txt_nome, txt_custo, txt_preco_un,
                ft.ElevatedButton("CADASTRAR", on_click=salvar_produto, bgcolor="green", color="white")
            ])),
            ft.Tab(text="ESTOQUE", content=lista_produtos),
            ft.Tab(text="VENDAS", content=ft.Text("Terminal de Vendas Mobile")),
        ],
        expand=1
    )

    page.add(tabs)
    atualizar_lista()

ft.app(target=main)