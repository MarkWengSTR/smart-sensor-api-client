# -*- coding: utf-8 -*-
"""Use case 5: request historic measurement data of an asset - latest

This code prints out the latest measurements from all of your assets.

Example:
    $ python get_latest_measurements.py

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, debug: bool = False) -> bool:

    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    # Print organization
    print('Organization {}, {}'.format(client.organization_id, client.organization_name))
    print()

    # Get list of plants
    plants = client.get_plant_list()

    # Iterate the plant list and print all assets therein
    # for plant in plants:

    # for 1212 in twabb, 10395 in tahobali
    plant = list(filter(lambda p:p['plantID'] in [1212, 10395], plants))[0]
    print('Plant {}, {}:'.format(plant['plantID'], plant['plantName']))
    print('Assets:')

    # Get list of assets
    assets = client.get_asset_list(organization_id=client.organization_id, plant_id=plant['plantID'])
    if len(assets) == 0:
        # print('No assets in this plant')
        return {"msg": 'No assets in this plant'}
    else:
        asset_data = client.asset_get_asset_by_id(asset_id=assets[0]['assetID'])
        # print('Latest measurements of Asset {}, {}:'.format(asset['assetID'], asset['assetName']))

        if asset_data is None:
            # If there is an error, skip to the next asset
            # continue
            return {"msg": "no asset"}

        vib_temp_json = filter(lambda m: m['measurementTypeCode'] in ['OverallVibration', 'SkinTemp'], asset_data['measurements'])
        vib_temp_value = list(map(lambda j: j['measurementTypeName'].ljust(20) + ": " + j['measurementValue'] + "( {} )".format(j['healthStatus']['healthCode']), vib_temp_json))
        total_data = ["Asset".ljust(20) + ": " + "{}".format(asset_data['assetName'])] + vib_temp_value

        print(total_data)

        # for m in asset_data['measurements']:
        # # Iterate all the measurements available and print them
        # for m in asset_data['measurements']:

        #     # Print measurements that contain values
        #     if m['measurementValue'] is not None:
        #         value = [m['measurementTypeName'].ljust(37) + ':' + m['measurementValue'] + '(' + m['timeStamp'] + ')']
        #         print(value)
        #         values_list += value
        # for asset in assets:
        #     asset_data = client.asset_get_asset_by_id(asset_id=asset['assetID'])
        #     print('Latest measurements of Asset {}, {}:'.format(asset['assetID'], asset['assetName']))

        #     if asset_data is None:
        #         # If there is an error, skip to the next asset
        #         continue

        #     # Iterate all the measurements available and print them
        #     for m in asset_data['measurements']:

        #         # Print measurements that contain values
        #         if m['measurementValue'] is not None:
        #             value = [m['measurementTypeName'].ljust(37) + ':' + m['measurementValue'] + '(' + m['timeStamp'] + ')']
        #             print(value)
        #             values_list += value
        #     print()

    # print()

    return total_data


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shows the latest measurements of all the assets belonging to the users current organization.')
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(debug=args.debug)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
