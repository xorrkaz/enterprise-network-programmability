APIC_EM_HOST = '198.18.129.100'
APIC_EM_USR = 'admin'
APIC_EM_PWD = 'C1sco12345'
APIC_EM_API = 'https://{}/api/v1'.format(APIC_EM_HOST)

CSR_HOST = '198.18.133.212'
CSR_USERNAME = 'admin'
CSR_PASSWORD = 'C1sco12345'


RESTCONF_ROOT = 'https://{}/restconf'.format(CSR_HOST)
RESTCONF_HEADERS = {
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json'
}
