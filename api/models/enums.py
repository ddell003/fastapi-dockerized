from enum import Enum


class UserType(Enum):
    basic = 'basic'
    investigator = 'investigator'
    sponsor = 'sponsor'


class UserContactType(Enum):
    email = 'email'
    fax = 'fax'
    phone = 'phone'


class AccomplishmentType(Enum):
    specialty = 'specialty'
    degree = 'degree'


class EthicType(Enum):
    central = 'central'
    local = 'local'


class PatientSource(Enum):
    emr = 'emr'
    chart_review = 'chart_review'
