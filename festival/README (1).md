# Gestão de Concertos e Estilos Musicais

(para visualizar o README renderizado, utilize `Ctrl + Shift + V`)


## 1. Modelação de estilos musicais

Este festival tem bandas de diferentes estilos musicais: punk, rock, electronic e pop.

Exemplos:
- Alessi Rose → pop
- Florence + The Machine → rock, pop
- Buraka Som Sistema → electronic
- Palaye Royale → punk, rock

Deverá:
- Alterar a modelação da aplicação para permitir associar um ou mais estilos a cada banda.
- migrar as alterações para a base de dados.
- no admin, criar estilos, e associar a cada estilo um conjunto de bandas, segundo critério livre
---

## 2. Página de estilos

Criar uma nova página que:

- liste os estilos musicais;
- para cada estilo, liste as bandas associadas a cada estilo.

Exemplo:

### Rock
- Florence + The Machine
- Palaye Royale

### Pop
- Alessi Rose
- Florence + The Machine

---

## 3. Menu de navegação

Integrar no menu principal um link para a nova página de estilos.


---

## 4. Informação adicional nas bandas

Nas paginas estilos, dias e palcos, incluir os respetivos estilos musicais depois do nome da banda.

Exemplo:
- Florence + The Machine (rock pop)
- Buraka Som Sistema (electronic)
- Palaye Royale (punk rock)
---

## 5. Edição dos palcos

Na página dos placos exite um botão de editar capacidade que não tem a sua funcionalidade implementada. Crie o form, view, template e url necessários para permitir editar a capacidade de um palco.

---

## 6. Alterações na edição de concertos

Alterar a funcionalidade de edição de um concerto para permitir:
- alterar o palco;
- alterar o dia.
