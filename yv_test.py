import logging, requests

HOST                = 'http://yvng.yadvashem.org/yvngNamesService.asmx/'
BUILD_QUERY         = HOST + 'buildQuery'
GET_PERSON_COUNT    = HOST + 'GetListCount'
GET_PERSON_LIST     = HOST + 'GetPersonList'
UNIQUE_ID           = '675675'

def build_query(session, first_name='', last_name='', place=''):
    d = dict(
        langApi             = 'HEB',
        isAdvancedSearch    = False,
        advancedValues      = [],
        clearFilter         = True,
        firstName           = first_name,
        lastName            = last_name,
        place               = place,
        newSearch           = True,
        uniqueId            = UNIQUE_ID,
    )
    
    res = session.post(BUILD_QUERY, json=d)
    return res.json()['d']
    
def get_person_count(session):
    d = dict(
        langApi   = 'HEB',
        useFilter = False,
        uniqueId  = UNIQUE_ID,
    )
    
    res = session.post(GET_PERSON_COUNT, json=d)
    print res
    print res.content
    return int(res.json()['d'])

def get_person_list(session, person_row=0):
    d = dict(
        langApi   = 'HEB',
        uniqueId  = UNIQUE_ID,
        orderBy   = 'LAST_NAME',
        orderType = 'asc',
        rowNum    = person_row,
    )

    res = session.post(GET_PERSON_LIST, json=d)
    return res.json()['d']

def main():
    s = requests.session()
    if not build_query(s, place='poland'):
        logging.log(logging.FATAL, 'build query failed')
        return
    count = get_person_count(s)
    logging.log(logging.FATAL, 'count: {}'.format(count))
    l = get_person_list(s, person_row=count/1000)
    logging.log(logging.FATAL, 'list len: {}, row: {}, person: {}'.format(len(l), count/1000, l[0]))
    
if __name__ == '__main__':
    main()