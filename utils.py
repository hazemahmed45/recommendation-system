import os
import numpy as np
import time
import pycountry
from collections import OrderedDict

columns_order = ['date', 'customer_id', 'employee_index', 'country_residence', 'gender', 'age', 'date_joined', 'new_customer', 'seniority', 'is_first', 'last_date', 'customer_type',
                 'relation_type', 'is_residence', 'is_foregine', 'is_spouse', 'channel', 'is_deceased', 'address_type', 'province_code', 'province_name', 'is_active', 'gross', 'segment']
columns_order_spanish = ['fecha_dato', 'ncodpers', 'ind_empleado', 'pais_residencia', 'sexo', 'age', 'fecha_alta', 'ind_nuevo', 'antiguedad', 'indrel', 'ult_fec_cli_1t', 'indrel_1mes',
                         'tiprel_1mes', 'indresi', 'indext', 'conyuemp', 'canal_entrada', 'indfall', 'tipodom', 'cod_prov', 'nomprov', 'ind_actividad_cliente', 'renta', 'segmento']

DEFUALT_VALUE = -99
DEFULT_STRING = 'NA'


class Debugger:
    def __init__(self) -> None:
        return


class Logger:
    def __init__(self) -> None:
        return


class Timer:
    def __init__(self, timedClass) -> None:
        self.timedClass = timedClass
        return

    def __call__(self, *args):
        print(args[0])
        nowTime = time.time()
        self.timedClass(args[0])
        endTime = time.time()
        print(endTime-nowTime)
        return


def prepare_dict_from_request(request_values) -> OrderedDict:
    age_value = request_values.get('age')
    seniority_value = request_values.get('seniority')
    gender_value = request_values.get('gender')
    gross_value = request_values.get('gross')
    country_residence_value = request_values.get('country_residence')
    relation_type_value = request_values.get('relation_type')
    is_active_value = request_values.get('is_active')
    segment_value = request_values.get('segment')
    region_value = request_values.get('region')
    customer_id_value = request_values.get('customer_id')

    request_dict = {
        'age': str(age_value),
        'seniority': str(seniority_value),
        'gender': DEFULT_STRING if gender_value == None else 'V' if gender_value.lower() == 'male' else 'H',
        'country_residence': prepare_customer_country_residence(country_residence_value),
        'relation_type': prepare_customer_relation_type(relation_type_value),
        'is_active': prepare_customer_is_active(is_active_value),
        'segment': prepare_customer_segment(segment_value),
        'gross': str(gross_value),
        'customer_id': str(customer_id_value),
    }
    orderedDict = OrderedDict()
    for col, col_s in zip(columns_order, columns_order_spanish):
        if('ind_actividad_cliente' == col_s):
            print(col, col_s)
        if(col in request_dict.keys()):

            orderedDict[col_s] = request_dict[col]
        else:
            orderedDict[col_s] = DEFULT_STRING
    return orderedDict


def prepare_customer_segment(segment):
    if(segment.lower() == 'student'):
        return '03 - UNIVERSITARIO'
    elif(segment.lower() == 'individual'):
        return '02 - PARTICULARES'
    elif(segment.lower() == 'vip'):
        return '01 - TOP'
    return DEFUALT_VALUE


def prepare_customer_is_active(is_active):
    if(is_active.lower() == 'active'):
        return '1'
    elif(is_active.lower() == 'inactive'):
        return '0'
    return DEFULT_STRING


def prepare_customer_country_residence(country_residence):
    for country in pycountry.countries:
        if(country_residence in country.name):
            return country.alpha_2
    return DEFULT_STRING


def prepare_customer_relation_type(relation_type):
    if(relation_type.lower() == 'active'):
        return 'A'
    elif(relation_type.lower() == 'inactive'):
        return 'I'
    elif(relation_type.lower() == 'former customer'):
        return 'P'
    elif(relation_type.lower() == 'potential'):
        return 'R'
    elif(relation_type.lower() == 'former co-owner'):
        return 'N'
    return DEFULT_STRING
