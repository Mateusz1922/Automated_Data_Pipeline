import argparse

class CliInterface:
    def parse_arguments(self):
        # initialize a parser
        parser = argparse.ArgumentParser(
            description="NBP Data Pipeline - Professional Currency Analytics Tool",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter # shows default values in --help
            )

        # add arguments
        parser.add_argument('--currencies', type=str, default='USD, EUR, CHF, GBP', help='Comma-separated list of currency codes') # TODO: add list of choices
        parser.add_argument('--days', type=int, default=7, help='Number of days for trend analysis and charts') 
        parser.add_argument('--check-gold', action='store_true', help='Flag to fetch and store current gold price')
        parser.add_argument('--threshold', type=float, default=0.2, help='Anomaly detection threshold')

        # returned parsed args
        return parser.parse_args()