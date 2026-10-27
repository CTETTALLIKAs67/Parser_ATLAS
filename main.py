from parser import Parser_ATLAS

def main():
    city = ['Гродно', 'Витебск']
    for i in city:
        parser = Parser_ATLAS(
            'https://atlasbus.by/',
            'Минск',
            i
        )
        parser.openBus()


if __name__ == "__main__":
    main()