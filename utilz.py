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
        cname = ''
        if len(country_name.split(' ')) > 1: # Handle when name is composite
            for element in country_name.split(' '):
                cname = cname + element.capitalize() + ' '
            country_name = cname.strip()
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name

    def kw_to_hp(self, kw=1):
        """  Kilowatts to Horse Power
        """
        hp = float(kw) * 1.35962 
        return hp

    def pw_ratio(self, power=None, weight=None, cylinder=None):
        """  Computes Power to weight ratio.
            - weight: in kilograms
            - power: in horse power
            - Cylinder: in in cc3
            -- Threshold for Torque is 100nm per 1 Liter of Cylinder
            -- An ideal power to weight ratio = 1.0
        """
        pwr, target_torque = 0.0, 0.0
        for val in [power, weight, cylinder]:
            if val is None:
                return 0.0, 0.0
        
        pwr = (float(power) / (float(weight) * 2.205) ) * 10
        target_torque = float(cylinder) * 100
        return round(pwr, 2), round(target_torque, 2)

    def fuel_cons(self, mileage, cost, up, cons):
        """ Calculates Expected mileage by fuel consumption.
        """
        if True:
            if cost is None or cost == '':
                try:
                    f_tank = round(float( (float(cons) * float(mileage)) / 100 ), 2)
                    exp_mileage = round( ((f_tank * 100) / float(cons)), 2)
                    t_cons = round( ((f_tank * 100) / float(mileage)), 2)
                    exp_cost = float(float(up) * f_tank) 
                    return f_tank, exp_mileage, t_cons, exp_cost
                except Exception as ex:
                    print('TRIP COST UTILITY Failed', ex)
                    return 0.0, 0.0, 0.0, 0.0
            else:
                try:
                    f_tank = round(float(float(cost) / float(up)), 2)
                    exp_mileage = round( ((f_tank * 100) / float(cons)), 2)
                    t_cons = round( ((f_tank * 100) / float(mileage)), 2)
                    return f_tank, exp_mileage, t_cons
                except Exception as ex:
                    print('FUEL CONSUMPTION UTILITY Failed', ex)
                    return 0.0, 0.0, 0.0

#toto = Utilz()
#print(toto.fuel_cons(99.1, 100, 11.08, 7.9))


#print(toto.country_to_continent('United Kingdom'))
#pwr, tt = toto.pw_ratio(power='115', weight='1375', cylinder='1.8')
#print(pwr, tt)
