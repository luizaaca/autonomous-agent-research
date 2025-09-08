A extração de resultado deve seguir algumas convenções:
Deve textualizar o json, para tanto, use dicionarios para fazer a traduçao

Em um caso como esse:

```json
"choices": [
            {"text": "Se você é um Policial (Police Officer)", "goto": 9, "set-occupation": "Police Officer"},
]
```

Deve textualizar o json em:

```json
"<any text>: se você é um Policial (Police Officer) vá para página 9 e atribua occupation Police Officer"
```

No caso a seguir,

```json
"choices": [{"goto": 7, "effects": [{"action": "heal_damage", "amount": 4}]}],
```

textualize em:

```json
"<any text>: vá para a página 7 e receba efeito \"heal_damage\" com valor 4"
```

No dicionario ficaria
"goto": "vá para a página"
"effects": "receba efeito"
"amount": "com valor"

No seguinte caso

```json
"choices": [
            {
                "opposed_roll": "Fighting",
                "opponent_skill": {"full": 40, "half": 20},
                "outcomes": {
                    "win": {"goto": 8},
                    "lose": {
                        "goto": 12,
                        "effects": [{"action": "take_damage", "amount": 2}],
                    },
                    "draw": {"goto": 28},
                },
            }
        ],
```

textualize o item 0 em:

```json
"<any text>: rolar dados contra (Fighting; Opponent 40/20;). Results in: lose, vá para a pagina 12 e receba efeito \"take_damage\" com valor 2"
```

No dicionário:

"opposed_roll": "rolar dados contra (Fighting;)."
"opponent_skill": "(Opponent 40/20;)" <--- append inside the "()" above
"outcomes": "Results in: {win/lose/draw}" <--- this value must be the result of the roll
"goto": "vá para a pagina"
"effects": "receba efeito"
"amount": "com valor"

No caso a seguir, se escolher 1:

```json
"choices": [
            {
                "conditional_on": "occupation",
                "paths": {
                    "Police Officer": {
                        "text": "Identifique-se como Policial",
                        "goto": 19,
                    }
                }
            },
            {"text": "Lançar feitiço Impello", "goto": 26},
            {"text": "Lançar feitiço Scindere", "goto": 69},
            {"text": "Enfrentar o agressor fisicamente", "goto": 4},
        ],
```

deve resultar em
```json
"<any text>: condicao Police Officer: Identifique-se como Policial; vá para a pagina 19"
```
No dicionário
"conditional_on": "condicao"
"goto": "vá para a pagina"

Nesse aqui, opçao 2:
```json
"choices": [
            {
                "text": "Se decidiu aprender Impello",
                "effects": [{"action": "gain_skill", "skill": "Impello"}],
                "goto": 21,
            },
            {
                "text": "Se decidiu aprender Scindere",
                "effects": [{"action": "gain_skill", "skill": "Scindere"}],
                "goto": 30,
            },
```
Deve resultar em: 
```json
"<any text>: Se decidiu aprender Scindere, receba efeito ganhar habilidade Scindere; vá para a pagina 30"
```
No dicionário
"effects": "receba efeito"
"goto": "vá para a pagina"
"gain_skill" : "ganhar habilidade"


Nesse caso:
```json
"choices": [
            {
                "roll": "DEX",
                "results": {
                    "5": {
                        "goto": 34,
                        "effects": [{"action": "take_damage", "amount": 2}],
                    },
                    "4": {
                        "goto": 34,
                        "effects": [{"action": "take_damage", "amount": 2}],
                    },
                    "3": {
                        "goto": 34,
                        "effects": [{"action": "take_damage", "amount": 2}],
                    },
                    "2": {
                        "goto": 78,
                        "effects": [{"action": "take_damage", "amount": 3}],
                    },
                    "1": {
                        "goto": 78,
                        "effects": [{"action": "take_damage", "amount": 3}],
                    },
                },
            }
```

Resultaria assim nas opções disponiveis:

```json
"<any text>: rolar DEX; rolagem critica, vá para a pagina 34 e receba efeito \"take_damage\" com valor 2; rolagem <level da rolagem 4>, vá para a pagina 34 e receba efeito \"take_damage\" com valor 2; rolagem <level da rolagem 3>, vá para a pagina 78 e receba efeito \"take_damage\" com valor 3; rol..."

```
e assim no log e historico

```json
"<any text>: rolar DEX; rolagem <level da rolagem 4>, vá para a pagina 34 e receba efeito \"take_damage\" com valor 2;"

```

Esse formato de string deve aparecer tanto nas opções disponiveis no cockpit, quanto no log e no histórico. Note, porém, que nas opções disponiveis deve constar todos os resultados possiveis como outcomes.

Se encontrar outro caso fora desses formatos, me pergunte como proceder e eu atualizarei esse arquivo.

Sempre confirme o entendimento antes de prosseguir!
 