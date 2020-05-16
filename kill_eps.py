grammar = {
    "nonterms": ['S', 'A', 'B', 'C', 'D', 'E'],
    'terms': ['a', 'b', 'c', 'e'],
    'productions': [
        {
            'S':[
                {
                    "symbols":[
                        {
                            'name': 'A',
                            'type': 'nonterm'
                        }
                    ]
                },

                {
                     "symbols":[
                        {
                            'name': 'B',
                            'type': 'nonterm'
                        }
                    ]
                }
            ]  
        },
        {
            'A':[
                 {
                    "symbols":[
                        {
                            'name': 'C',
                            'type': 'nonterm'
                        },
                        ##########################
                        {
                            'name': 'D',
                            'type': 'nonterm'
                        },
                        {
                            'name': 'E',
                            'type': 'nonterm'
                        }
                    ]
                },

                {
                     "symbols":[
                        {
                            'name': 'D',
                            'type': 'nonterm'
                        }
                    ]
                }
            ]
        },
        {
            'B':[
                 {
                    "symbols":[
                        {
                            'name': 'D',
                            'type': 'nonterm'
                        }
                    ]
                },

                {
                     "symbols":[
                        {
                            'name': 'E',
                            'type': 'nonterm'
                        }
                    ]
                }
            ]
        },
        {
            'C':[
                 {
                    "symbols":[
                        {
                            'name': 'S',
                            'type': 'nonterm'
                        }
                    ]
                },
                {
                     "symbols":[
                        {
                            'name': 'a',
                            'type': 'term'
                        }
                    ]
                },
                {
                     "symbols":[
                        {
                            'name': 'e',
                            'type': 'term'
                        }
                    ]
                }
            ]
        },
        {
            'D':[
                {
                    "symbols":[
                        {
                            'name': 'S',
                            'type': 'nonterm'
                        }
                    ]
                },
                {
                     "symbols":[
                        {
                            'name': 'b',
                            'type': 'term'
                        }
                    ]
                },

            ]
        },
        {
            'E':[
                {
                    "symbols":[
                        {
                            'name': 'S',
                            'type': 'nonterm'
                        }
                    ]
                },
                {
                     "symbols":[
                        {
                            'name': 'c',
                            'type': 'term'
                        }
                    ]
                },
                {
                     "symbols":[
                        {
                            'name': 'e',
                            'type': 'term'
                        }
                    ]
                }  
            ]
        }
    ]
}

import copy
class BaseGrammarMethods():

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

class KillEps(BaseGrammarMethods):
    
    def __init__(self):
        self.eps_prods_list = []
        self.serarch_productions_with_eps()
        self.create_new_prods_without_eps()
        
    def serarch_productions_with_eps(self):
        
        for current_position in range(0, len(grammar['productions'])):
            current_nonterm = self.get_nonterm_by_position(current_position)
            current_productions = self.get_nonterm_productions(current_nonterm)
            is_eps = False
            for production in current_productions:
                
                if is_eps == True:
                    break

                for symbol in production['symbols']:
                    if symbol['name'] == 'e':
                        self.eps_prods_list.append(current_nonterm)
                        is_eps == True
                        break
        
        for current_position in range(0, len(grammar['productions'])):
            current_nonterm = self.get_nonterm_by_position(current_position)
            current_productions = self.get_nonterm_productions(current_nonterm)
            is_indirect_eps = True
            for production in current_productions:
                
                if is_indirect_eps == False:
                    break

                for symbol in production['symbols']:
                    if symbol['name'] not in self.eps_prods_list:
                        is_indirect_eps = False
                        break

            if is_indirect_eps == True:
                self.eps_prods_list.append(current_nonterm)

        # print(self.eps_prods_list)
    
    def _combinator(self, variable_prod, current, end, curent_list, main_list):
        productions = self.get_nonterm_productions(variable_prod[current])
        for production in productions:
            if len(curent_list) < current + 1:
                curent_list.append(production['symbols'])
            else:
                curent_list[current] = production['symbols']

            if current < end:
                self._combinator(variable_prod, current + 1, end, curent_list, main_list)
            else:
                main_list.append(copy.deepcopy(curent_list))
                

        if current == end:
            curent_list = []

    def productions_combinator(self, prod_symbols_list):
        expression = []
        variable_prod = []
        result_production = []

        main_list = []
        current_list = []
        for symbol in  prod_symbols_list:
            if symbol['name'] not in self.eps_prods_list:
                expression.append(symbol['name'])
            else:
                expression.append('!' + symbol['name'])
                variable_prod.append(symbol['name'])

        end = len(variable_prod) - 1
        self._combinator(variable_prod, 0, end, current_list, main_list)
        
        n = 0
        for variables in main_list:
            num = 0
            result_production.append([])
            for position in range(0, len(expression)):
                
                if "!" in expression[position]:
    
                    if variables[num][0]['name'] == 'e':
                        num += 1
                        continue
                    
                    result_production[n].append(variables[num][0])
                    num += 1
                else:
                    symbol_type = self.get_symbol_type(expression[position])
                    result_production[n].append({'name': expression[position], 'type': symbol_type})
            
            if len(result_production[n]) == 0:
                result_production.pop(n)
            else:
                n += 1
        
        return result_production

    def delete_repetitions(self, production):
        new_prod = []
        for i in production:
            for j in production:
                if i != j:
                    new_prod.append(i)
        return new_prod

    def create_new_prods_without_eps(self):
        for current_position in range(0, len(grammar['productions'])):
            current_nonterm = self.get_nonterm_by_position(current_position)
            current_productions = self.get_nonterm_productions(current_nonterm)
            have_eps_nonterms = False
            new_productions = []
            

            for production in current_productions:
                prod_symbols_list = []
                for symbol in production['symbols']:
                    prod_symbols_list.append(symbol)
                    if symbol['name'] in self.eps_prods_list:
                        have_eps_nonterms = True

                if have_eps_nonterms == True:
                    update_productions = self.productions_combinator(prod_symbols_list)
                    for poduction in update_productions:
                        new_productions.append({'symbols': poduction})
                    have_eps_nonterms = False
                else:
                    new_productions.append({'symbols': prod_symbols_list})
            
            self.update_nonterm_productions(current_nonterm, new_productions)



        for current_position in range(0, len(grammar['productions'])):
            current_nonterm = self.get_nonterm_by_position(current_position)
            current_productions = self.get_nonterm_productions(current_nonterm)
            new = []
            if current_nonterm in self.eps_prods_list:
                for production in current_productions:
                    is_e = False
                    for symbol in production['symbols']:
                        if symbol['name'] == 'e':
                            is_e = True
                    if is_e == False:
                        new.append(production)

                self.update_nonterm_productions(current_nonterm, new)

        for i in grammar['productions']:
            print(i)


    



a = KillEps()