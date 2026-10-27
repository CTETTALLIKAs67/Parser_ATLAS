from parser import Parser_ATLAS

def main():
    city = ['Гродно', 'Витебск']
    for i in city:
        parser_1 = Parser_ATLAS(
            'https://atlasbus.by/',
            'Минск',
            i
        )
        parser_1.collecting_info()

        parser_2 = Parser_ATLAS(
            'https://atlasbus.by/',
            i,
            'Минск'
        )
        parser_2.collecting_info()


if __name__ == "__main__":
    main()