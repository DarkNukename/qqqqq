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
                #  {
                #     "symbols":[
                #         {
                #             'name': 'S',
                #             'type': 'nonterm'
                #         }
                #     ]
                # },
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
                # {
                #     "symbols":[
                #         {
                #             'name': 'S',
                #             'type': 'nonterm'
                #         }
                #     ]
                # },
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
                # {
                #     "symbols":[
                #         {
                #             'name': 'S',
                #             'type': 'nonterm'
                #         }
                #     ]
                # },
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


class MyTask(BaseGrammarMethods):

    def main(self):
        useless_symbols = []

        # Шаг 1
        for current_nonterm_position in range(0, len(grammar['nonterms'])):
            current_nonterm = self.get_nonterm_by_position(current_nonterm_position)
            current_productions = self.get_nonterm_productions(current_nonterm)
            all_terms = True
            for production in current_productions:
                for symbol in production['symbols']:
                    if self.get_symbol_type(symbol['name']) == 'nonterm':
                        all_terms = False
                        break
            
            if all_terms == True:
                useless_symbols.append(current_nonterm)


        # Шаг 2 и 3
        old_useless_symbols = useless_symbols
        new_useless_symbols = []
        is_first = True
        while new_useless_symbols != old_useless_symbols:

            if is_first == True:
                new_useless_symbols = copy.deepcopy(old_useless_symbols)
                is_first = False
            else:
                old_useless_symbols = copy.deepcopy(new_useless_symbols)


            for current_nonterm_position in range(0, len(grammar['nonterms'])):
                current_nonterm = self.get_nonterm_by_position(current_nonterm_position)
                current_productions = self.get_nonterm_productions(current_nonterm)
                all_terms = True
                for production in current_productions:
                    for symbol in production['symbols']:
                        if self.get_symbol_type(symbol['name']) not in old_useless_symbols:
                            all_terms = False
                            break

                if all_terms == True:
                    new_useless_symbols.append(current_nonterm)

        new_prods = []   
        for nonterm_prod in grammar['productions']:
            nonterm = list(nonterm_prod.keys())[0]
            if nonterm in new_useless_symbols:
                continue
            else:
                new_prods.append(nonterm)


        grammar['productions'] = []
        grammar['productions'] = copy.deepcopy(new_prods)

        print(grammar['productions'])
   


a = MyTask()
a.main()



