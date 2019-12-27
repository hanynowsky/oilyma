from country_list import countries_for_language
import pycountry_convert as pc

class Utilz:

    def __init__(self, debug=False):
        self.debug = debug

    def get_countries(self):
        """ List of Countries. Dictionary.
        """
        countries = dict(countries_for_language('en'))
        return countries
        # countries['ES']


    def country_to_continent(self, country_name):
        """  Returns Continent for a givien Country
        """
        country_name = country_name.lower().capitalize()
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name



#toto = Utilz()
#print(toto.country_to_continent('azerbaijan'))
