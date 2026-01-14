import flet as ft
import sqlite3
import os

def main(page: ft.Page):
    # Configurações para garantir visibilidade no Android
    page.title = "MOZER SYSTEM 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0  # Usaremos SafeArea para o padding
    
    # --- BANCO DE DADOS EM LOCAL PERMITIDO NO ANDROID ---
    try:
        # Local oficial para dados do app no Flet/Android
        db_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        db_path = os.path.join(db_dir, "mozer_2026.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL)''')
        conn.commit()
    except Exception as e:
        print(f"Erro banco: {e}")

    # --- COMPONENTES ---
    txt_nome = ft.TextField(label="Nome do Produto", border_color="green")
    txt_preco = ft.TextField(label="Preço", keyboard_type=ft.KeyboardType.NUMBER)
    lista_produtos = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def salvar(e):
        if txt_nome.value:
            cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?,?)", 
                          (txt_nome.value, float(txt_preco.value or 0)))
            conn.commit()
            txt_nome.value = ""
            txt_preco.value = ""
            atualizar_lista()
            page.update()

    def atualizar_lista():
        lista_produtos.controls.clear()
        cursor.execute("SELECT nome, preco FROM produtos")
        for row in cursor.fetchall():
            lista_produtos.controls.append(ft.ListTile(title=ft.Text(row[0]), subtitle=ft.Text(f"R$ {row[1]}")))
        page.update()

    # --- LAYOUT SEGURO (Evita Tela Preta) ---
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column([
                    ft.Text("MOZER SYSTEM v2026", size=28, weight="bold", color="green"),
                    txt_nome,
                    txt_preco,
                    ft.ElevatedButton("CADASTRAR PRODUTO", on_click=salvar, bgcolor="green", color="white"),
                    ft.Divider(),
                    ft.Text("PRODUTOS EM ESTOQUE:", weight="bold"),
                    lista_produtos
                ], spacing=15),
                padding=20,
                expand=True
            )
        )
    )
    atualizar_lista()

if __name__ == "__main__":
    ft.app(target=main)
