######################################## GOOGLE API ###########################
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1D0zmwKAo3UvKdtU2WXrOrzMqMGu3BVl3iABf7xw3HbY'
SAMPLE_RANGE_NAME = 'BMW-OIL!A4:O'

######################################## CORE #################################
NOACK_THRESHOLD = 6.8 # NOACK
LL_ONE_COUNTRIES = ['BA', 'MD']
LL_FOUR_COUNTRIES = ['CN', 'KR', 'JP', 'RU', 'NZ', 'TK']
AFRICA_APPROVALS = ['BMWLL01']
EUROPE_APPROVALS = ['BMWLL01', 'BMWLL04']
ASIA_APPROVALS = ['BMWLL01']
OCEANIA_APPROVALS = ['BMWLL01']
NORTH_AMERICA_APPROVALS = ['BMWLL04', 'BMWLL01']
SOUTH_AMERICA_APPROVALS = ['BMWLL01']
OIL_CONS_L_ONE = 0.7
OIL_CONS_L_TWO = 1.5
ENGINES = {'1':'M40', '2':'M42', '3':'M43', '4':'M43', '5':'N40', '6':'N42', '7':'N43', '8':'N46', '9':'M50', '10':'S50', '11':'M52', '12':'M54', '13':'S54', '14':'N52', '15':'N53' , '16':'M60', '17':'M62', '18':'N62', '19':'S62', '20':'S65', '21':'S85', '22':'M70', '23':'S70', '24':'M73', '25':'N73', '26':'M10', '27':'S14'  }
