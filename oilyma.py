from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from configuration import *
import utilz

class Oilyma:

    def __init__(self, debug=False):
        self.debug = debug
        self.creds = None
        self.error_name = None

    def authentika(self):
        """ Authenticate to Google Sheet API
            - returns: google api client discovery build
        """
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

            service = build('sheets', 'v4', credentials=self.creds)
            return service
        except Exception as ex:
            print('No authentication established', ex)
            self.error_name = ex
            return None

    def get_values(self):
        """  Return values from spreadsheet
        """
        try:
            # Call the Sheets API
            service = self.authentika()
            if not isinstance(service, Resource) or service is None:
                return None
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])
            return values
        except Exception as ex:
            print('Error while fetching values', ex)
            self.error_name = ex
            return None

    def forge_data(self):
        """ Forge Data onto a list
        """
        dicto = []
        values = self.get_values()
        if values is None:
            return None
        if not values:
            print('No data found.')
            return []
        else:
            for row in values:
                if row[13] in [None, '', '?']: row[13] = '11.0'
                for xay in [4, 5, 13]:
                    if row[xay].isnumeric():
                        row[xay] = float(row[xay])
                data = {'oid':row[0], 'label':row[1], 'grade':row[2], 'approval':row[3], 'visc_100':row[4], 'visc_40':row[5], 'dync_5w':row[6], 'mrv':row[7], 'vol_mass':row[8], 'flash_point':row[9], 'pour_point':row[10], 'vi':row[11], 'hths':row[12], 'noack':row[13], 'tbn':row[14]}                
                dicto.append(data)
        return dicto


    def j_data(self):
        """ Usage of the Google Sheets API.
        Prints values from a spreadsheet.
        """
        try:
            data = self.forge_data()
            if data is None:
                return None
            obj = json.dumps(data, indent=4, sort_keys=True)
            return obj
            if self.debug:
                print(obj)
        except Exception as ex:
            print('Error getting results', ex)
            self.error_name = ex
            return json.dumps([], indent=4, sort_keys=True)

    def j_fdata(self, grades=[], approvals=[]):
        """ returns filtered data
            - grades (List of strings) = List of grades
            - approvals (List of Strings) = List of approvals
        """
        result = []
        jee_data = self.j_data()
        if jee_data is None:
            return None
        jdata = json.loads(jee_data)
        if approvals == ['']: approvals = []
        if grades == ['']: grades = []
        for elem in jdata:
            if ((elem['approval'].strip().replace(' ', '') in approvals or approvals == []) and (elem['grade'].strip().replace(' ', '') in grades or grades == [])):
                result.append(elem)
        return json.dumps(result, indent=4, sort_keys=True)

    def get_country_approvals(self, approvals=['BMWLL01', 'BMWLL04'], country=None):
        """ Returns default approvals per country
        """
        if country:
            if country in LL_FOUR_COUNTRIES:
                approvals =  ['BMWLL01', 'BMWLL04']
            if country in LL_ONE_COUNTRIES:
                approvals =  ['BMWLL01']
            if approvals == ['']: approvals = ['BMWLL01', 'BMWLL04']
        return approvals

    def get_continent_approvals(self, continent='Europe'):
        """ Returns default approvals per continent
        """
        approvals = ['BMWLL01', 'BMWLL04']
        if continent:
            if continent in ['Africa']:
                approvals =  AFRICA_APPROVALS
            if continent in ['Europe']:
                approvals =  EUROPE_APPROVALS
            if continent in ['North America']:
                approvals =  NORTH_AMERICA_APPROVALS
            if continent in ['South America']:
                approvals =  SOUTH_AMERICA_APPROVALS
            if continent in ['Asia']:
                approvals = ASIA_APPROVALS
            if continent in ['Oceania']:
                approvals =  ['BMWLL01']
        return approvals

    def j_sdata(self, auto=0, ocons=0, mileage=100000, country='ES', grades=[], approvals=[]):
        """ returns selection of oils based on search criteria
            - ocons (FLOAT) = Oil consumption per 2000 Kms in liters.
            - mileage (INTEGER) = Mileage in Kilometers.
            - country (STRING) = Country where the car is being driven
        """
        do_append = True
        mileage_rank = 0
        ocons_level = 0
        if int(mileage) > 100000:
            mileage_rank = 1 
        if int(mileage) > 150000:
            mileage_rank = 2 
        if int(mileage) > 200000:
            mileage_rank = 3 
        
        if float(ocons) > OIL_CONS_L_ONE:
            ocons_level = 1
        if float(ocons) >= OIL_CONS_L_TWO:
            ocons_level = 2
        
        result =  []
        if int(auto) == 1:
            tools = utilz.Utilz()
            countries = tools.get_countries()
            patry = countries[country]
            continent = tools.country_to_continent(patry)
            approvals = self.get_continent_approvals(continent=continent)
            approvals = self.get_country_approvals(approvals=approvals, country=country)
            if ocons_level == 2 or mileage_rank == 3:
                grades = ['5W40', '0W40']
        fdata = self.j_fdata(grades=grades, approvals=approvals)
        if fdata is None:
            return None, self.error_name
        for elem in json.loads(fdata):
            elem['mileage'] = 'standard'
            elem['selected'] = False
            #if elem['noack'] in ['', '?']: elem['noack'] = 11.0
            if elem['vi'] in ['?', '']: elem['vi'] = 160
            if elem['flash_point'] in ['?', '']: elem['flash_point'] = 230
            # TODO move hard-coded thresholds to configuration
            if float(elem['noack']) <= NOACK_THRESHOLD:
                elem['selected'] = True
            if ocons_level == 1:
                if float(elem['vi']) >= 170 and float(elem['visc_100']) >= 12 and float(elem['flash_point']) >= 230:
                    elem['selected'] = True
            if ocons_level == 2:
                if float(elem['vi']) >= 170 and float(elem['visc_100']) >= 14 and float(elem['flash_point']) >= 230:
                    elem['selected'] = True
            if mileage_rank == 1:
                if float(elem['vi']) >= 160:
                    if float(elem['visc_100']) >= 11.7:
                        if float(elem['flash_point']) >= 230:
                            elem['mileage'] = 'medium'
            if mileage_rank == 2:
                if float(elem['vi']) >= 170 and float(elem['visc_100']) >= 12 and float(elem['flash_point']) >= 230:
                    elem['mileage'] = 'high'
            if mileage_rank == 3:
                if float(elem['vi']) >= 175 and float(elem['visc_100']) >= 14 and float(elem['flash_point']) >= 230:
                    elem['mileage'] = 'high'
            if do_append:
                result.append(elem)
        
        
        return json.dumps(result, indent=4, sort_keys=True), self.error_name

########################################## TEST ###############################
#toto = Oilyma()
#print(toto.j_sdata())
