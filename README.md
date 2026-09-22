# 🍔 Sistema de Vendas para Hamburgueria em Console (Python)

Um sistema interativo via terminal/console desenvolvido em Python para gerenciamento de pedidos e autenticação de usuários em uma hamburgueria.

---

## 📌 Sumário
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Credenciais Padrão](#-credenciais-padrão)

---

## ✨ Funcionalidades

### 🔐 Autenticação e Usuários
* **Cadastro de Usuários:** Permite cadastrar novos clientes com verificação de e-mail duplicado e validação de confirmação de senha.
* **Senha Oculta:** Máscara de senha no terminal utilizando caracteres `*` para maior segurança visual.
* **Login de Usuários:** Autenticação por e-mail e senha cadastrados.

### 📜 Cardápio e Carrinho
* **Navegação por Categoria:** Exibição clara e formatada de hambúrgueres e bebidas com preços em formato local (`R$ 0,00`).
* **Adição de Itens:** Inclusão flexível de produtos no carrinho por código e quantidade.
* **Gestão do Carrinho:** Visualização dos itens selecionados com subtotais individuais e valor total acumulado.

### 💳 Checkout e Pedido
* **Formas de Pagamento:** Suporte para Dinheiro, Pix, Cartão de Débito e Cartão de Crédito.
* **Resumo e Emissão de Comprovante:** Exibição do resumo completo da compra com nome do cliente, forma de pagamento, total e data/hora exata da transação.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.x](https://www.python.org/):** Linguagem principal do projeto.
* **`msvcrt` (Biblioteca Padrão do Windows):** Utilizada para a captura de teclas em tempo real para ocultar a digitação da senha.
* **`datetime` (Biblioteca Padrão):** Utilizada para registrar a data e hora do encerramento do pedido.

---

## ⚠️ Pré-requisitos

* **Sistema Operacional:** Windows *(A biblioteca `msvcrt` é nativa apenas para sistemas operacionais Windows)*.
* **Python:** Versão 3.6 ou superior instalada.

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório ou baixe os arquivos:**
   ```bash
   