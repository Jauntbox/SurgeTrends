from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import config as cfg

#Set API keys from configuration file
server_token = cfg.server_token

session = Session(server_token=server_token)

# California Academy of Sciences
START_LAT = 37.770
START_LNG = -122.466

# Pier 39
END_LAT = 37.791
END_LNG = -122.405

client = UberRidesClient(session)
response = client.get_products(37.77, -122.41)
products = response.json.get('products')
product_id = products[0].get('product_id')

print "products"
print products
print ""
print "product_id:"
print product_id

#oauth2credential = OAuth2Credential(
#        client_id=credentials.get('client_id'),
#        access_token=credentials.get('access_token'),
#        expires_in_seconds=credentials.get('expires_in_seconds'),
#        scopes=credentials.get('scopes'),
#        grant_type=credentials.get('grant_type'),
#        redirect_url=credentials.get('redirect_url'),
#        client_secret=credentials.get('client_secret'),
#        refresh_token=credentials.get('refresh_token'),
#    )

#session = Session(oauth2credential=oauth2credential)
#return UberRidesClient(session, sandbox_mode=True)

#estimate = api_client.estimate_ride(product_id,37.77,-122.41,37.73,-122.41)
#print estimate