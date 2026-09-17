import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime
import json
import os
import urllib.request
import io

# ============================================================
# Chapa Quente Hamburguers
# Interface: 900x600
# ============================================================

LARGURA = 900
ALTURA = 600

COR_FUNDO = "#101010"
COR_CARD = "#1b1b1b"
COR_CARD_2 = "#252525"
COR_VERMELHO = "#e63946"
COR_VERMELHO_ESCURO = "#b92330"
COR_BRANCO = "#ffffff"
COR_CINZA = "#aaaaaa"
COR_VERDE = "#2ecc71"

ARQUIVO_PEDIDOS = "pedidos.json"
PASTA_IMAGENS = "imagens"

os.makedirs(PASTA_IMAGENS, exist_ok=True)

CARDAPIO = {
    "X-Burger": {
        "preco": 15.00,
        "descricao": "Pao, carne, queijo e molho especial",
        "imagem": "xburger.jpg",
        "emoji": "🍔"
    },
    "X-Salada": {
        "preco": 18.00,
        "descricao": "Carne, queijo, alface e tomate",
        "imagem": "xsalada.jpg",
        "emoji": "🥬"
    },
    "X-Bacon": {
        "preco": 22.00,
        "descricao": "Carne, queijo, bacon e molho",
        "imagem": "xbacon.jpg",
        "emoji": "🥓"
    },
    "X-Tudo": {
        "preco": 28.00,
        "descricao": "Carne, queijo, bacon, salada e ovo",
        "imagem": "xtudo.jpg",
        "emoji": "🍔"
    },
    "Batata Frita": {
        "preco": 12.00,
        "descricao": "Batata frita crocante",
        "imagem": "batata.jpg",
        "emoji": "🍟"
    },
    "Refrigerante": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "refrigerante.jpg",
        "emoji": "🥤"
    },
    "Suco": {
        "preco": 8.00,
        "descricao": "Suco natural",
        "imagem": "suco.jpg",
        "emoji": "🧃"
    },
    "Agua": {
        "preco": 4.00,
        "descricao": "Agua mineral 500ml",
        "imagem": "agua.jpg",
        "emoji": "💧"
    },

    "X-Frango": {
        "preco": 20.00,
        "descricao": "Frango grelhado, queijo e molho especial",
        "imagem": "xfrango.jpg",
        "emoji": "🍔"
    },
    "X-Cheddar": {
        "preco": 23.00,
        "descricao": "Carne, cheddar cremoso e molho especial",
        "imagem": "xcheddar.jpg",
        "emoji": "🍔"
    },
    "X-Duplo": {
        "preco": 30.00,
        "descricao": "Duas carnes, queijo, bacon e molho",
        "imagem": "xduplo.jpg",
        "emoji": "🍔"
    },
    "X-Barbecue": {
        "preco": 26.00,
        "descricao": "Carne, queijo, bacon e molho barbecue",
        "imagem": "xbarbecue.jpg",
        "emoji": "🍔"
    },
    "Coca-Cola": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "coca.jpg",
        "emoji": "🥤"
    },
    "Guarana": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "guarana.jpg",
        "emoji": "🥤"
    },
    "Fanta Laranja": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "fanta.jpg",
        "emoji": "🥤"
    },
    "Sprite": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "sprite.jpg",
        "emoji": "🥤"
    },
    "Pepsi": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "pepsi.jpg",
        "emoji": "🥤"
    },
    "Suco de Laranja": {
        "preco": 9.00,
        "descricao": "Suco natural de laranja",
        "imagem": "suco_laranja.jpg",
        "emoji": "🧃"
    },
    "Suco de Maracuja": {
        "preco": 9.00,
        "descricao": "Suco natural de maracuja",
        "imagem": "suco_maracuja.jpg",
        "emoji": "🧃"
    },
    "Suco de Morango": {
        "preco": 10.00,
        "descricao": "Suco natural de morango",
        "imagem": "suco_morango.jpg",
        "emoji": "🧃"
    },
    "Suco de Limao": {
        "preco": 8.00,
        "descricao": "Suco natural de limao",
        "imagem": "suco_limao.jpg",
        "emoji": "🧃"
    },
}

carrinho = []
imagens = {}


# ============================================================
# UTILITARIOS
# ============================================================

def formatar_real(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def criar_imagem_fallback(nome, emoji):
    caminho = os.path.join(PASTA_IMAGENS, nome)

    if os.path.exists(caminho):
        return

    imagem = Image.new("RGB", (400, 220), "#292929")
    desenho = ImageDraw.Draw(imagem)

    desenho.rounded_rectangle(
        (5, 5, 395, 215),
        radius=25,
        fill="#202020"
    )

    desenho.ellipse(
        (100, 10, 300, 210),
        fill="#333333"
    )

    try:
        fonte = ImageFont.truetype("seguiemj.ttf", 90)
    except Exception:
        fonte = ImageFont.load_default()

    desenho.text(
        (200, 110),
        emoji,
        anchor="mm",
        font=fonte
    )

    imagem.save(caminho, "JPEG", quality=90)


def baixar_fotos():
    # Fotos sao baixadas somente se ainda nao existirem.
    urls = {
        "xburger.jpg":
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80",
        "xsalada.jpg":
            "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",
        "xbacon.jpg":
            "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600&q=80",
        "xtudo.jpg":
            "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=600&q=80",
        "batata.jpg":
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80",
        "refrigerante.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "suco.jpg":
            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
        "agua.jpg":
            "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&q=80",

        "xfrango.jpg":
            "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=600&q=80",
        "xcheddar.jpg":
            "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=600&q=80",
        "xduplo.jpg":
            "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600&q=80",
        "xbarbecue.jpg":
            "https://images.unsplash.com/photo-1550317138-10000687a72b?w=600&q=80",
        "coca.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "guarana.jpg":
            "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",
        "fanta.jpg":
            "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
        "sprite.jpg":
            "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",
        "pepsi.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "suco_laranja.jpg":
            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
        "suco_maracuja.jpg":
            "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80",
        "suco_morango.jpg":
            "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80",
        "suco_limao.jpg":
            "https://images.unsplash.com/photo-1523677011781-c91d1bbe2f3f?w=600&q=80"
    }

    for produto, dados in CARDAPIO.items():
        caminho = os.path.join(PASTA_IMAGENS, dados["imagem"])

        if os.path.exists(caminho):
            continue

        try:
            requisicao = urllib.request.Request(
                urls[dados["imagem"]],
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(requisicao, timeout=3) as resposta:
                dados_imagem = resposta.read()

            imagem = Image.open(io.BytesIO(dados_imagem))
            imagem.convert("RGB").save(caminho, "JPEG", quality=90)

        except Exception:
            criar_imagem_fallback(
                dados["imagem"],
                dados["emoji"]
            )


def carregar_imagem(caminho, tamanho=(180, 90)):
    try:
        imagem = Image.open(caminho)
        imagem = imagem.resize(
            tamanho,
            Image.Resampling.LANCZOS
        )
        return ImageTk.PhotoImage(imagem)
    except Exception:
        imagem = Image.new("RGB", tamanho, "#333333")
        desenho = ImageDraw.Draw(imagem)
        desenho.text(
            (tamanho[0] // 2, tamanho[1] // 2),
            "🍔",
            anchor="mm"
        )
        return ImageTk.PhotoImage(imagem)


def calcular_valores():
    subtotal = sum(
        item["preco"] * item["quantidade"]
        for item in carrinho
    )

    desconto = subtotal * 0.10 if subtotal >= 50 else 0
    total = subtotal - desconto

    return subtotal, desconto, total


# ============================================================
# CARRINHO
# ============================================================

def adicionar_produto(produto):
    for item in carrinho:
        if item["produto"] == produto:
            item["quantidade"] += 1
            atualizar_carrinho()
            return

    carrinho.append({
        "produto": produto,
        "preco": CARDAPIO[produto]["preco"],
        "quantidade": 1
    })

    atualizar_carrinho()


def remover_item():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione um item para remover."
        )
        return

    indice = tabela.index(selecionado[0])

    if 0 <= indice < len(carrinho):
        if carrinho[indice]["quantidade"] > 1:
            carrinho[indice]["quantidade"] -= 1
        else:
            carrinho.pop(indice)

    atualizar_carrinho()


def atualizar_carrinho():
    for item in tabela.get_children():
        tabela.delete(item)

    for item in carrinho:
        total_item = item["preco"] * item["quantidade"]

        tabela.insert(
            "",
            tk.END,
            values=(
                item["produto"],
                item["quantidade"],
                formatar_real(total_item)
            )
        )

    subtotal, desconto, total = calcular_valores()

    subtotal_label.config(
        text=f"Subtotal: {formatar_real(subtotal)}"
    )

    desconto_label.config(
        text=f"Desconto: {formatar_real(desconto)}"
    )

    total_label.config(
        text=f"TOTAL: {formatar_real(total)}"
    )


# ============================================================
# FINALIZACAO / CHECKOUT
# ============================================================

def abrir_checkout():
    if not carrinho:
        messagebox.showwarning(
            "Carrinho vazio",
            "Adicione produtos antes de finalizar a compra."
        )
        return

    checkout = tk.Toplevel(janela)
    checkout.title("Finalizar compra")
    checkout.geometry("430x540")
    checkout.resizable(False, False)
    checkout.configure(bg=COR_CARD)
    checkout.transient(janela)
    checkout.grab_set()

    tk.Label(
        checkout,
        text="✓ FINALIZAR COMPRA",
        font=("Arial", 19, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(pady=(18, 3))

    tk.Label(
        checkout,
        text="Preencha os dados para concluir o pedido",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(pady=(0, 12))

    formulario = tk.Frame(checkout, bg=COR_CARD)
    formulario.pack(fill="x", padx=25)

    # Nome
    tk.Label(
        formulario,
        text="Nome do cliente *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_nome = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_nome.pack(fill="x", pady=(3, 9), ipady=6)

    # Endereco
    tk.Label(
        formulario,
        text="Endereço / Rua *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_endereco = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_endereco.pack(fill="x", pady=(3, 9), ipady=6)

    # Tipo de residencia
    tk.Label(
        formulario,
        text="Tipo de residência",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    tipo_var = tk.StringVar(value="Casa")

    combo_tipo = ttk.Combobox(
        formulario,
        textvariable=tipo_var,
        values=["Casa", "Apartamento", "Outro"],
        state="readonly"
    )
    combo_tipo.pack(fill="x", pady=(3, 9), ipady=4)

    # Numero da casa
    tk.Label(
        formulario,
        text="Número da casa *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_numero = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_numero.pack(fill="x", pady=(3, 9), ipady=6)

    # Forma de pagamento
    tk.Label(
        formulario,
        text="Forma de pagamento *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    pagamento_var = tk.StringVar(value="PIX")

    combo_pagamento = ttk.Combobox(
        formulario,
        textvariable=pagamento_var,
        values=[
            "PIX",
            "Dinheiro",
            "Cartão de Débito",
            "Cartão de Crédito"
        ],
        state="readonly"
    )
    combo_pagamento.pack(fill="x", pady=(3, 10), ipady=4)

    subtotal, desconto, total = calcular_valores()

    resumo = tk.Frame(
        checkout,
        bg="#111111"
    )
    resumo.pack(
        fill="x",
        padx=25,
        pady=(2, 10)
    )

    tk.Label(
        resumo,
        text=f"Total da compra: {formatar_real(total)}",
        font=("Arial", 12, "bold"),
        bg="#111111",
        fg=COR_VERDE
    ).pack(pady=9)

    def confirmar_compra():
        nome = entrada_nome.get().strip()
        endereco = entrada_endereco.get().strip()
        numero_casa = entrada_numero.get().strip()
        tipo_residencia = tipo_var.get()
        pagamento = pagamento_var.get()

        if not nome:
            messagebox.showwarning(
                "Dados incompletos",
                "Digite o nome do cliente.",
                parent=checkout
            )
            entrada_nome.focus()
            return

        if not endereco:
            messagebox.showwarning(
                "Dados incompletos",
                "Digite o endereço / rua.",
                parent=checkout
            )
            entrada_endereco.focus()
            return

        if not numero_casa:
            messagebox.showwarning(
                "Dados incompletos",
                "Digite o número da casa.",
                parent=checkout
            )
            entrada_numero.focus()
            return

        if not pagamento:
            messagebox.showwarning(
                "Dados incompletos",
                "Escolha uma forma de pagamento.",
                parent=checkout
            )
            return

        finalizar_pedido(
            nome,
            endereco,
            tipo_residencia,
            numero_casa,
            pagamento,
            checkout
        )

    tk.Button(
        checkout,
        text="✓ CONFIRMAR E FINALIZAR",
        command=confirmar_compra,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        activeforeground=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 11, "bold")
    ).pack(
        fill="x",
        padx=25,
        ipady=9
    )

    entrada_nome.focus()


def finalizar_pedido(
    nome,
    endereco,
    tipo_residencia,
    numero_casa,
    pagamento,
    checkout
):
    subtotal, desconto, total = calcular_valores()

    agora = datetime.now()
    numero = agora.strftime("%Y%m%d%H%M%S")

    pedido = {
        "numero": numero,
        "cliente": nome,
        "endereco": endereco,
        "tipo_residencia": tipo_residencia,
        "numero_casa": numero_casa,
        "data": agora.strftime("%d/%m/%Y"),
        "hora": agora.strftime("%H:%M:%S"),
        "status": "Recebido",
        "pagamento": pagamento,
        "itens": [item.copy() for item in carrinho],
        "subtotal": subtotal,
        "desconto": desconto,
        "total": total
    }

    salvar_pedido(pedido)

    checkout.destroy()

    mostrar_recibo(pedido)

    limpar_pedido()


def salvar_pedido(pedido):
    pedidos = []

    if os.path.exists(ARQUIVO_PEDIDOS):
        try:
            with open(
                ARQUIVO_PEDIDOS,
                "r",
                encoding="utf-8"
            ) as arquivo:
                pedidos = json.load(arquivo)
        except (json.JSONDecodeError, FileNotFoundError):
            pedidos = []

    pedidos.append(pedido)

    with open(
        ARQUIVO_PEDIDOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            pedidos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def mostrar_recibo(pedido):
    janela_recibo = tk.Toplevel(janela)
    janela_recibo.title("Pedido finalizado")
    janela_recibo.geometry("450x570")
    janela_recibo.resizable(False, False)
    janela_recibo.configure(bg=COR_CARD)

    tk.Label(
        janela_recibo,
        text="🍔 PEDIDO CONFIRMADO",
        font=("Arial", 18, "bold"),
        bg=COR_CARD,
        fg=COR_VERMELHO
    ).pack(pady=(15, 5))

    texto = tk.Text(
        janela_recibo,
        bg="#111111",
        fg=COR_BRANCO,
        font=("Consolas", 9),
        relief="flat",
        padx=12,
        pady=12
    )
    texto.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=12
    )

    recibo = (
        "====================================\n"
        "       HAMBURGUERIA AUTOMATIZADA\n"
        "====================================\n\n"
        f"PEDIDO Nº: {pedido['numero']}\n"
        f"Cliente: {pedido['cliente']}\n"
        f"Data: {pedido['data']}  {pedido['hora']}\n\n"
        "ENDEREÇO DE ENTREGA\n"
        "------------------------------------\n"
        f"Endereço: {pedido['endereco']}\n"
        f"Tipo: {pedido['tipo_residencia']}\n"
        f"Número: {pedido['numero_casa']}\n\n"
        "ITENS DO PEDIDO\n"
        "------------------------------------\n"
    )

    for item in pedido["itens"]:
        valor_item = item["preco"] * item["quantidade"]
        recibo += (
            f"{item['quantidade']}x {item['produto']}\n"
            f"    {formatar_real(valor_item)}\n"
        )

    recibo += (
        "\n------------------------------------\n"
        f"Subtotal: {formatar_real(pedido['subtotal'])}\n"
        f"Desconto: {formatar_real(pedido['desconto'])}\n"
        f"TOTAL: {formatar_real(pedido['total'])}\n\n"
        f"Pagamento: {pedido['pagamento']}\n"
        f"Status: {pedido['status']}\n\n"
        "Obrigado pela preferência! ❤️\n"
        "====================================\n"
    )

    texto.insert("1.0", recibo)
    texto.config(state="disabled")

    tk.Button(
        janela_recibo,
        text="FECHAR",
        command=janela_recibo.destroy,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=18,
        pady=(0, 18),
        ipady=8
    )


def limpar_pedido():
    carrinho.clear()
    atualizar_carrinho()


# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

baixar_fotos()

janela = tk.Tk()
janela.title("Chapa Quente Hmaburguers")
janela.geometry(f"{LARGURA}x{ALTURA}")
janela.resizable(False, False)
janela.configure(bg=COR_FUNDO)

# Cabecalho
topo = tk.Frame(
    janela,
    bg="#0b0b0b",
    height=65
)
topo.pack(fill="x")
topo.pack_propagate(False)

tk.Label(
    topo,
    text="🍔 Chapa Quente",
    font=("Arial", 20, "bold"),
    bg="#0b0b0b",
    fg=COR_BRANCO
).pack(side="left", padx=20)

tk.Label(
    topo,
    text="Hamburguers",
    font=("Arial", 10, "bold"),
    bg="#0b0b0b",
    fg=COR_VERMELHO
).pack(side="left")

relogio = tk.Label(
    topo,
    text="",
    font=("Arial", 9),
    bg="#0b0b0b",
    fg=COR_CINZA
)
relogio.pack(side="right", padx=20)


def atualizar_relogio():
    relogio.config(
        text=datetime.now().strftime(
            "%d/%m/%Y  •  %H:%M:%S"
        )
    )
    janela.after(1000, atualizar_relogio)


# Corpo
principal = tk.Frame(
    janela,
    bg=COR_FUNDO
)
principal.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ============================================================
# CARDAPIO
# ============================================================

esquerda = tk.Frame(
    principal,
    bg=COR_FUNDO,
    width=570
)
esquerda.pack(
    side="left",
    fill="both",
    expand=True
)

tk.Label(
    esquerda,
    text="🍔 Cardápio",
    font=("Arial", 17, "bold"),
    bg=COR_FUNDO,
    fg=COR_BRANCO
).pack(anchor="w", pady=(0, 5))

canvas = tk.Canvas(
    esquerda,
    bg=COR_FUNDO,
    highlightthickness=0
)

scrollbar_produtos = ttk.Scrollbar(
    esquerda,
    orient="vertical",
    command=canvas.yview
)

area_produtos = tk.Frame(
    canvas,
    bg=COR_FUNDO
)

area_produtos.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=area_produtos,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar_produtos.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar_produtos.pack(
    side="right",
    fill="y"
)

for indice, (produto, dados) in enumerate(CARDAPIO.items()):
    linha = indice // 2
    coluna = indice % 2

    card = tk.Frame(
        area_produtos,
        bg=COR_CARD,
        width=260,
        height=175
    )
    card.grid(
        row=linha,
        column=coluna,
        padx=5,
        pady=5
    )
    card.grid_propagate(False)

    caminho = os.path.join(
        PASTA_IMAGENS,
        dados["imagem"]
    )

    imagem = carregar_imagem(
        caminho,
        (235, 78)
    )
    imagens[produto] = imagem

    tk.Label(
        card,
        image=imagem,
        bg=COR_CARD
    ).pack(pady=(6, 3))

    tk.Label(
        card,
        text=produto,
        font=("Arial", 11, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack()

    rodape = tk.Frame(
        card,
        bg=COR_CARD
    )
    rodape.pack(
        fill="x",
        padx=10,
        pady=4
    )

    tk.Label(
        rodape,
        text=formatar_real(dados["preco"]),
        font=("Arial", 11, "bold"),
        bg=COR_CARD,
        fg=COR_VERMELHO
    ).pack(side="left")

    tk.Button(
        rodape,
        text="+ ADICIONAR",
        command=lambda p=produto: adicionar_produto(p),
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 8, "bold")
    ).pack(side="right")


# ============================================================
# PEDIDO
# ============================================================

direita = tk.Frame(
    principal,
    bg=COR_CARD,
    width=295
)
direita.pack(
    side="right",
    fill="y",
    padx=(10, 0)
)
direita.pack_propagate(False)

tk.Label(
    direita,
    text="🛒 Seu Pedido",
    font=("Arial", 17, "bold"),
    bg=COR_CARD,
    fg=COR_BRANCO
).pack(
    anchor="w",
    padx=15,
    pady=(15, 8)
)

colunas = (
    "Produto",
    "Qtd",
    "Total"
)

tabela = ttk.Treeview(
    direita,
    columns=colunas,
    show="headings",
    height=8
)

tabela.heading("Produto", text="Produto")
tabela.heading("Qtd", text="Qtd")
tabela.heading("Total", text="Total")

tabela.column("Produto", width=125)
tabela.column("Qtd", width=35, anchor="center")
tabela.column("Total", width=70, anchor="e")

tabela.pack(
    fill="x",
    padx=15
)

tk.Button(
    direita,
    text="🗑 Remover item",
    command=remover_item,
    bg="#333333",
    fg=COR_BRANCO,
    activebackground="#444444",
    relief="flat",
    cursor="hand2",
    font=("Arial", 8, "bold")
).pack(
    fill="x",
    padx=15,
    pady=6,
    ipady=5
)

tk.Frame(
    direita,
    bg="#333333",
    height=1
).pack(
    fill="x",
    padx=15,
    pady=3
)

subtotal_label = tk.Label(
    direita,
    text="Subtotal: R$ 0,00",
    font=("Arial", 9),
    bg=COR_CARD,
    fg=COR_CINZA
)
subtotal_label.pack(
    anchor="w",
    padx=15,
    pady=2
)

desconto_label = tk.Label(
    direita,
    text="Desconto: R$ 0,00",
    font=("Arial", 9),
    bg=COR_CARD,
    fg=COR_CINZA
)
desconto_label.pack(
    anchor="w",
    padx=15,
    pady=2
)

total_label = tk.Label(
    direita,
    text="TOTAL: R$ 0,00",
    font=("Arial", 14, "bold"),
    bg=COR_CARD,
    fg=COR_VERMELHO
)
total_label.pack(
    anchor="w",
    padx=15,
    pady=(4, 8)
)

tk.Label(
    direita,
    text="Na próxima tela você informa:\n"
         "nome, endereço, casa e pagamento.",
    font=("Arial", 8),
    justify="left",
    bg=COR_CARD,
    fg=COR_CINZA
).pack(
    anchor="w",
    padx=15,
    pady=(0, 8)
)

tk.Button(
    direita,
    text="✓ FINALIZAR COMPRA",
    command=abrir_checkout,
    bg=COR_VERMELHO,
    fg=COR_BRANCO,
    activebackground=COR_VERMELHO_ESCURO,
    activeforeground=COR_BRANCO,
    relief="flat",
    cursor="hand2",
    font=("Arial", 10, "bold")
).pack(
    fill="x",
    padx=15,
    ipady=9
)

tk.Button(
    direita,
    text="＋ NOVO PEDIDO",
    command=limpar_pedido,
    bg="#333333",
    fg=COR_BRANCO,
    activebackground="#444444",
    relief="flat",
    cursor="hand2",
    font=("Arial", 9, "bold")
).pack(
    fill="x",
    padx=15,
    pady=7,
    ipady=6
)

atualizar_carrinho()
atualizar_relogio()

janela.mainloop()
