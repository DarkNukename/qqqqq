grammar = {
    'Terms': {
        "a": "IDENT",
        "+": "ADD",
        "*": "MUL",
        "(": "LP",
        ")": "RP"
    },

    'nonterms': ['E', 'T', 'F'],

    "productions": [
    {"E": [
        {
            "symbols": [
                {
                    "type": "nonterm",
                    "name": "E"
                },
                {
                    "type": "term",
                    "name": "ADD"
                },
                {
                    "type": "nonterm",
                    "name": "T"
                },
                
            ]
        },
        {
            "symbols": [
                {
                    "type": "nonterm",
                    "name": "T"
                }
            ]
        }  
    ]},

    {"T": [
        {
            "symbols": [
                {
                    "type": "nonterm",
                    "name": "T"
                },
                {
                    "type": "term",
                    "name": "MUL"
                },
                {
                    "type": "nonterm",
                    "name": "F"
                },
                
            ]
        },
        {
            "symbols": [
                {
                    "type": "nonterm",
                    "name": "F"
                }
            ]
        }
    ]},

    {"F": [
        {
            "symbols": [
                {
                    # "type": "term",
                    # "name": "IDENT"
                    "type": "nonterm",
                    "name": "T"
                }   
            ]
        },
        {
            "symbols": [
                {
                    "type": "term",
                    "name": "LP"
                },
                {
                    "type": "nonterm",
                    "name": "E"
                },
                    {
                    "type": "nonterm",
                    "name": "RP"
                }
            ]
        }
    ]}
    ],

    "start": "E"
    }


import copy
import os
os.system('clear')




class BaseGrammarMethods():
    def __init__(self):
        self.mega_costyl = False

    # Возвращает список продукций указанного нонтерма
    def get_nonterm_productions(self, nonterm):
        for nonterm_position in grammar['productions']:
            if nonterm_position.get(nonterm):
                return nonterm_position[nonterm]

    # Возвращает позицию указанного нонтерма в грамматике
    def get_nonterm_position(self, nonterm):
        for position in range(0, len(grammar['nonterms'])):
            if grammar['nonterms'][position] == nonterm:
                return position

    # Возвращает нонтерм, соответствующий указанной позиции
    def get_nonterm_by_position(self, position):
        return grammar['nonterms'][position]

    # Возвращает тип символа
    def get_symbol_type(self, symbol):
        if symbol in grammar['nonterms']:
            return 'nonterm'
        else:
            return 'term' 

    # Добавляет новый нонтерм
    def add_new_nonterm(self, name, productions, position):
        grammar['nonterms'].insert(position, name)
        grammar['productions'].insert(position, {name: productions})
    
    # Перезаписывает продукции указанного нонтерма
    def update_nonterm_productions(self, nonterm, new_productions):
        for current_nonterm in grammar['productions']:
            if current_nonterm.get(nonterm):
                current_nonterm[nonterm] = []
                for production in new_productions:
                    current_nonterm[nonterm].append(production)
                
                
    
    # Возвращает символ по номеру из указанной продукции
    def get_production_symbol(self, production, position):
        return production['symbols'][position]['name']

class KillLeftRecursion(BaseGrammarMethods):
    
    # Проверяет наличие непосредственной левой рекурсии в указанных продукциях или одной продукции если is_one = True
    def check_left_recursion(self, productions, current_nonterm_position, is_one = False):
        if is_one == True:
            left_symbol = self.get_production_symbol(productions, 0)
            if self.get_symbol_type(left_symbol) == 'nonterm':
                if self.get_nonterm_position(left_symbol) == current_nonterm_position:
                    return True
            return False
        
        
        for production in productions:
            left_symbol = self.get_production_symbol(production, 0)
            if self.get_symbol_type(left_symbol) == 'nonterm':
                if self.get_nonterm_position(left_symbol) == current_nonterm_position:
                    return True
        return False
    
    def kill_left_recursion(self, productions, current_nonterm_position, last_symbol):
        import copy
        if self.check_left_recursion(productions, current_nonterm_position):
            print("\nУстраняем непосредственную рекурсию")
            a = []
            # a_num = 0
            b = []
            # b_num = 0

            update_term_productions = []
            new_term_name = self.get_nonterm_by_position(current_nonterm_position) + "!"
            new_term = []
            t = self.get_nonterm_by_position(current_nonterm_position)

            if t == last_symbol:
                self.mega_costyl = True

            print(f"Продукции: {productions}\n")
            for production in productions:

                if len(production['symbols']) == 1 and production['symbols'][0]['name'] == t:
                    continue

                print(f"Текущая продукция: {production}")
                if self.check_left_recursion(production, current_nonterm_position, is_one=True):
                    print(f"Обнаружена левая рекурсия\n")
                    formed_production = copy.deepcopy(production)
                    formed_production['symbols'].pop(0)
                    a.append(formed_production)
                    production_ = copy.deepcopy(formed_production)
                    production_['symbols'].append({"type": "nonterm", "name": new_term_name})
                    new_term.append(production_)
                   
                   
                else:
                    print(f"Левая рекурсия не обнаружена\n")
                    b.append(production)
                    production_ = copy.deepcopy(production)
                    production_['symbols'].append({"type": "nonterm", "name": new_term_name})
                    update_term_productions.append(production_)
                    
            
            for b_productions in b:
                update_term_productions.append(b_productions)

            for a_productions in a:
                new_term.append(a_productions)

            for n in range(0, len(new_term)):
                if len(new_term[n]['symbols']) == 1 and new_term[n]['symbols'][0]['name'] == new_term_name:
                    new_term.pop(n)
            
            for n in range(0, len(update_term_productions)):
                if len(update_term_productions[n]['symbols']) == 1 and update_term_productions[n]['symbols'][0]['name'] == t:
                    update_term_productions.pop(n)

            print(f'\nСоздан новый терм: {new_term_name}')
            print(f'Продукции нового терма: {new_term}')
            
            print(f'\nОбновлены продукции терма {t}')
            print(f'Продукции терма {t}: {update_term_productions}')


            self.update_nonterm_productions(self.get_nonterm_by_position(current_nonterm_position), update_term_productions)
            self.add_new_nonterm(new_term_name, new_term, current_nonterm_position + 1)

    def kill_indirect_recursion(self):

        last_symbol = self.get_nonterm_by_position(len(grammar['nonterms']) - 1)
        
        current_position = 0
        end_position = len(grammar['nonterms'])

        while current_position < end_position :
            
            if self.mega_costyl == True:
                break

            print("-" * 100)
            current_nonterm = self.get_nonterm_by_position(current_position)
            current_productions = self.get_nonterm_productions(current_nonterm)

            print(f"Текущий нонтерм: {current_nonterm}")
            print(f"Позиция текущего нонтерма: {current_position}")
            print(f"Продукции текущего нонтерма\n {current_productions}\n")
            new_productions = []
            warning = True
            while warning == True:

                warning = False
                new_productions = []
                for current_production in current_productions:

                    print(f"Текущая продукция: {current_production}")
                    left_symbol = self.get_production_symbol(current_production, 0)
                    left_synbol_position = self.get_nonterm_position(left_symbol)
                    left_symbol_type = self.get_symbol_type(left_symbol)
                    print(f'Левый символ: {left_symbol}')
                    print(f'Позиция левого символа: {left_synbol_position}')

                    if left_symbol_type == "nonterm" and left_synbol_position < current_position:
                        print("\nВозможна косвенная рекурсия")
                        warning = True
                        left_symbol_productions = self.get_nonterm_productions(left_symbol)
                        print(f'Продукции левого символа: {left_symbol_productions}')
                        print("+" * 100)
                        for left_symbol_production in left_symbol_productions:
                            print(f'текущая продукция левого символа: {left_symbol_production}')

                            new = copy.deepcopy(left_symbol_production)

                            for current_production_symbol in range(1, len(current_production['symbols'])):
                                new['symbols'] = (current_production['symbols'][current_production_symbol])

                            new_productions.append(new)
                    
                    else:
                        new_productions.append(current_production)
                    
                current_productions = copy.deepcopy(new_productions)

            self.kill_left_recursion(current_productions, current_position, last_symbol)
            end_position = len(grammar['nonterms'])
            current_position += 1 
        


test = [{'symbols': [{'type': 'nonterm', 'name': 'T'}, {'type': 'term', 'name': 'MUL'}, {'type': 'nonterm', 'name': 'F'}]}, {'symbols': [{'type': 'nonterm', 'name': 'F'}]}]   
a = KillLeftRecursion()
a.kill_indirect_recursion()
print(grammar['productions'])
