from python_dhl.dhl import service
from python_dhl.dhl.resources import *

service = service.DHLService('Juntos', 'w6jDMkWsZI', '803921577')
service.test_mode = True
sender = address.DHLCompany(
            company_name='GitHub',
            person_name='Git Hub',
            street_lines='275 Brannan Street',
            city='San Francisco',
            postal_code='94107',
            country_code='US',
            phone='11111111',
            email='git@github.com'
            )

receiver = address.DHLPerson(
            person_name='Jon Doe',
            street_lines='276 Brannan Street',
            city='San Francisco',
            postal_code='94107',
            country_code='US',
            phone='11111111',
            email='jon@github.com'
            )

packages = [
    package.DHLPackage(
        weight=0.15,
        width=10,
        length=10,
        height=10,
        price=100,
        description='Good product'
    ),
    package.DHLPackage(
        weight=0.15,
        width=10,
        length=10,
        height=10,
        price=100,
        description='The best product'
    )
]

shipment = shipment.DHLShipment(sender, receiver, packages)
print(shipment)
# rate_response = service.rate_request(shipment)
# print(rate_response.services)