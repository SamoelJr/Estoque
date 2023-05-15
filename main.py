#eu
import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
''')

#chatgpt
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
''')

conn.commit()

#eu
print("Opções para a aplicação. Ps: Digitar no terminal opção desejada. Ex: cadastrar_produto()")
print("cadastrar_produto(); consultar_estoque_usuario(); fazer_pedido()")


def cadastrar_produto():
  nome = input('Digite o nome do produto: ')
  quantidade = int(input('Digite a quantidade inicial do produto: '))

  cursor.execute('INSERT INTO produtos (nome, quantidade) VALUES (?, ?)',
                 (nome, quantidade))
  conn.commit()
  print('Produto cadastrado com sucesso!')


#chatgpt
def estoque(nome):
  # Verifica se o produto existe no banco de dados
  cursor.execute('SELECT * FROM produtos WHERE nome = ?', (nome, ))
  resultado = cursor.fetchone()

  if resultado is None:
    print(f'Produto {nome} não foi encontrado')
    return None

  # Busca a quantidade do produto no banco de dados
  cursor.execute('SELECT quantidade FROM produtos WHERE nome = ?', (nome, ))
  resultado = cursor.fetchone()

  #Eu
  quantidade = resultado[0]
  
  if quantidade <= 5:
    print(f'ATENÇÃO: A quantidade do produto {nome} está baixa ({quantidade} unidades no estoque)'
    )

  if quantidade == 0:
    print(f'ATENÇÃO: O produto {nome} está em falta no estoque')

  print(f'O produto {nome} tem {quantidade} unidades em estoque')
  return quantidade

def consultar_estoque_usuario():
  nome = input('Digite o nome do produto que deseja consultar: ')
  estoque(nome)


def fazer_pedido():
  nome = input('Digite o nome do produto que deseja comprar: ')
  quantidade = int(input('Digite a quantidade que deseja comprar: '))

  cursor.execute('SELECT quantidade FROM produtos WHERE nome = ?', (nome, ))
  resultado = cursor.fetchone()

  if resultado is None:
    print(f'Produto {nome} não foi encontrado')
    return

  estoque_disponivel = resultado[0]
  if estoque_disponivel < quantidade:
    print(
      f'Não há estoque suficiente do produto {nome} .'
    )
    return

  #chatgpt
  # Atualiza a quantidade em estoque do produto
  nova_quantidade = estoque_disponivel - quantidade
  cursor.execute('UPDATE produtos SET quantidade = ? WHERE nome = ?',
                 (nova_quantidade, nome))
  conn.commit()

  #eu
  cursor.execute('SELECT id FROM produtos WHERE nome = ?', (nome, ))
  produto_id = cursor.fetchone()[0]
  cursor.execute('INSERT INTO pedidos (produto_id, quantidade) VALUES (?, ?)',
                 (produto_id, quantidade))
  conn.commit()

  print(
    f'Pedido de {quantidade} unidades do produto {nome} feito!'
  )