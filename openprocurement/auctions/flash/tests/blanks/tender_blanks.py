# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta

from openprocurement.api.utils import get_now
from openprocurement.api.constants import SANDBOX_MODE

from openprocurement.auctions.flash.models import Auction
from openprocurement.auctions.flash.tests.base import test_auction_data, test_organization
from openprocurement.api.tests.base import JSON_RENDERER_ERROR

# AuctionTest


def create_role(self):
    fields = set([
        'awardCriteriaDetails', 'awardCriteriaDetails_en', 'awardCriteriaDetails_ru',
        'description', 'description_en', 'description_ru',
        'eligibilityCriteria', 'eligibilityCriteria_en', 'eligibilityCriteria_ru',
        'enquiryPeriod', 'features', 'guarantee', 'hasEnquiries', 'items', 'lots', 'minimalStep', 'mode',
        'procurementMethodRationale', 'procurementMethodRationale_en', 'procurementMethodRationale_ru',
        'procurementMethodType', 'procuringEntity',
        'submissionMethodDetails', 'submissionMethodDetails_en', 'submissionMethodDetails_ru',
        'tenderPeriod', 'title', 'title_en', 'title_ru', 'value',
    ])
    if SANDBOX_MODE:
        fields.add('procurementMethodDetails')
    self.assertEqual(set(Auction._fields) - Auction._options.roles['create'].fields, fields)


def edit_role(self):
    fields = set([
        'awardCriteriaDetails', 'awardCriteriaDetails_en', 'awardCriteriaDetails_ru',
        'description', 'description_en', 'description_ru',
        'eligibilityCriteria', 'eligibilityCriteria_en', 'eligibilityCriteria_ru',
        'enquiryPeriod', 'features', 'guarantee', 'hasEnquiries', 'items', 'minimalStep',
        'procurementMethodRationale', 'procurementMethodRationale_en', 'procurementMethodRationale_ru',
        'procuringEntity',
        'submissionMethodDetails', 'submissionMethodDetails_en', 'submissionMethodDetails_ru',
        'tenderPeriod', 'title', 'title_en', 'title_ru', 'value',
    ])
    if SANDBOX_MODE:
        fields.add('procurementMethodDetails')
    self.assertEqual(set(Auction._fields) - Auction._options.roles['edit_active.enquiries'].fields, fields)

# AuctionResourceTest


def create_auction_invalid(self):
    request_path = '/auctions'
    response = self.app.post(request_path, 'data', status=415)
    self.assertEqual(response.status, '415 Unsupported Media Type')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description':
            u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
    ])

    response = self.app.post(
        request_path, 'data', content_type='application/json', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        JSON_RENDERER_ERROR
    ])

    response = self.app.post_json(request_path, 'data', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'not_data': {}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': []}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    # response = self.app.post_json(request_path, {'data': {'procurementMethodType': 'invalid_value'}}, status=415)
    # self.assertEqual(response.status, '415 Unsupported Media Type')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': u'Not implemented', u'location': u'data', u'name': u'procurementMethodType'}
    # ])

    response = self.app.post_json(request_path, {'data': {
                                  'invalid_field': 'invalid_value'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Rogue field', u'location':
            u'body', u'name': u'invalid_field'}
    ])

    response = self.app.post_json(request_path, {'data': {'value': 'invalid_value'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [
            u'Please use a mapping for this field or Value instance instead of unicode.'], u'location': u'body', u'name': u'value'}
    ])

    response = self.app.post_json(request_path, {'data': {'procurementMethod': 'invalid_value'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertIn({u'description': [u"Value must be one of ['open', 'selective', 'limited']."], u'location': u'body', u'name': u'procurementMethod'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'tenderPeriod'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'minimalStep'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'items'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'enquiryPeriod'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'value'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'items'}, response.json['errors'])

    response = self.app.post_json(request_path, {'data': {'enquiryPeriod': {'endDate': 'invalid_value'}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'endDate': [u"Could not parse invalid_value. Should be ISO8601."]}, u'location': u'body', u'name': u'enquiryPeriod'}
    ])

    response = self.app.post_json(request_path, {'data': {'enquiryPeriod': {'endDate': '9999-12-31T23:59:59.999999'}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'endDate': [u'date value out of range']}, u'location': u'body', u'name': u'enquiryPeriod'}
    ])

    data = test_auction_data['tenderPeriod']
    test_auction_data['tenderPeriod'] = {'startDate': '2014-10-31T00:00:00', 'endDate': '2014-10-01T00:00:00'}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data['tenderPeriod'] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'startDate': [u'period should begin before its end']}, u'location': u'body', u'name': u'tenderPeriod'}
    ])

    data = test_auction_data['tenderPeriod']
    test_auction_data['tenderPeriod'] = {'startDate': '2014-10-31T00:00:00', 'endDate': '2015-10-01T00:00:00'}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data['tenderPeriod'] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'period should begin after enquiryPeriod'], u'location': u'body', u'name': u'tenderPeriod'}
    ])

    now = get_now()
    test_auction_data['awardPeriod'] = {'startDate': now.isoformat(), 'endDate': now.isoformat()}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    del test_auction_data['awardPeriod']
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'period should begin after tenderPeriod'], u'location': u'body', u'name': u'awardPeriod'}
    ])

    test_auction_data['auctionPeriod'] = {'startDate': (now + timedelta(days=15)).isoformat(), 'endDate': (now + timedelta(days=15)).isoformat()}
    test_auction_data['awardPeriod'] = {'startDate': (now + timedelta(days=14)).isoformat(), 'endDate': (now + timedelta(days=14)).isoformat()}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    del test_auction_data['auctionPeriod']
    del test_auction_data['awardPeriod']
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'period should begin after auctionPeriod'], u'location': u'body', u'name': u'awardPeriod'}
    ])

    data = test_auction_data['minimalStep']
    test_auction_data['minimalStep'] = {'amount': '1000.0'}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data['minimalStep'] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'value should be less than value of auction'], u'location': u'body', u'name': u'minimalStep'}
    ])

    data = test_auction_data['minimalStep']
    test_auction_data['minimalStep'] = {'amount': '100.0', 'valueAddedTaxIncluded': False}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data['minimalStep'] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'valueAddedTaxIncluded should be identical to valueAddedTaxIncluded of value of auction'], u'location': u'body', u'name': u'minimalStep'}
    ])

    data = test_auction_data['minimalStep']
    test_auction_data['minimalStep'] = {'amount': '100.0', 'currency': "USD"}
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data['minimalStep'] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'currency should be identical to currency of value of auction'], u'location': u'body', u'name': u'minimalStep'}
    ])

    data = test_auction_data["items"][0]["additionalClassifications"][0]["scheme"]
    test_auction_data["items"][0]["additionalClassifications"][0]["scheme"] = 'Не ДКПП'
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data["items"][0]["additionalClassifications"][0]["scheme"] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [{u'additionalClassifications': [u"One of additional classifications should be one of [ДКПП, NONE, ДК003, ДК015, ДК018]."]}], u'location': u'body', u'name': u'items'}
    ])

    data = test_organization["contactPoint"]["telephone"]
    del test_organization["contactPoint"]["telephone"]
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_organization["contactPoint"]["telephone"] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'contactPoint': {u'email': [u'telephone or email should be present']}}, u'location': u'body', u'name': u'procuringEntity'}
    ])

    data = test_auction_data["items"][0].copy()
    classification = data['classification'].copy()
    classification["id"] = u'66113000-5'
    data['classification'] = classification
    test_auction_data["items"] = [test_auction_data["items"][0], data]
    response = self.app.post_json(request_path, {'data': test_auction_data}, status=422)
    test_auction_data["items"] = test_auction_data["items"][:1]
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'CAV group of items be identical'], u'location': u'body', u'name': u'items'}
    ])


def create_auction_generated(self):
    data = test_auction_data.copy()
    #del data['awardPeriod']
    data.update({'id': 'hash', 'doc_id': 'hash2', 'auctionID': 'hash3'})
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    if 'procurementMethodDetails' in auction:
        auction.pop('procurementMethodDetails')
    self.assertEqual(set(auction), set([u'procurementMethodType', u'id', u'date', u'dateModified', u'auctionID', u'status', u'enquiryPeriod',
                                       u'tenderPeriod', u'minimalStep', u'items', u'value', u'procuringEntity', u'next_check',
                                       u'procurementMethod', u'awardCriteria', u'submissionMethod', u'title', u'owner']))
    self.assertNotEqual(data['id'], auction['id'])
    self.assertNotEqual(data['doc_id'], auction['id'])
    self.assertNotEqual(data['auctionID'], auction['auctionID'])


def create_auction(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/auctions', {"data": test_auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertEqual(set(auction) - set(test_auction_data), set(
        [u'id', u'dateModified', u'auctionID', u'date', u'status', u'procurementMethod', u'awardCriteria', u'submissionMethod', u'next_check', u'owner']))
    self.assertIn(auction['id'], response.headers['Location'])

    response = self.app.get('/auctions/{}'.format(auction['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(set(response.json['data']), set(auction))
    self.assertEqual(response.json['data'], auction)

    response = self.app.post_json('/auctions?opt_jsonp=callback', {"data": test_auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/javascript')
    self.assertIn('callback({"', response.body)

    response = self.app.post_json('/auctions?opt_pretty=1', {"data": test_auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)

    response = self.app.post_json('/auctions', {"data": test_auction_data, "options": {"pretty": True}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)

    auction_data = deepcopy(test_auction_data)
    auction_data['guarantee'] = {"amount": 100500, "currency": "USD"}
    response = self.app.post_json('/auctions', {'data': auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    data = response.json['data']
    self.assertIn('guarantee', data)
    self.assertEqual(data['guarantee']['amount'], 100500)
    self.assertEqual(data['guarantee']['currency'], "USD")


def patch_auction(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/auctions', {'data': test_auction_data})
    self.assertEqual(response.status, '201 Created')
    auction = response.json['data']
    owner_token = response.json['access']['token']
    dateModified = auction.pop('dateModified')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {'data': {'status': 'cancelled'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['status'], 'cancelled')

    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'status': 'cancelled'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['status'], 'cancelled')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {'data': {'procuringEntity': {'kind': 'defense'}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('kind', response.json['data']['procuringEntity'])

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'tenderPeriod': {'startDate': None}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('startDate', response.json['data']['tenderPeriod'])

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'tenderPeriod': {'startDate': auction['enquiryPeriod']['endDate']}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('startDate', response.json['data']['tenderPeriod'])

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'procurementMethodRationale': 'Open'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction = response.json['data']
    new_dateModified = new_auction.pop('dateModified')
    auction['procurementMethodRationale'] = 'Open'
    self.assertEqual(auction, new_auction)
    self.assertNotEqual(dateModified, new_dateModified)

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'dateModified': new_dateModified}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction2 = response.json['data']
    new_dateModified2 = new_auction2.pop('dateModified')
    self.assertEqual(new_auction, new_auction2)
    self.assertEqual(new_dateModified, new_dateModified2)

    revisions = self.db.get(auction['id']).get('revisions')
    self.assertEqual(revisions[-1][u'changes'][0]['op'], u'remove')
    self.assertEqual(revisions[-1][u'changes'][0]['path'], u'/procurementMethodRationale')

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'items': [test_auction_data['items'][0]]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'items': [{}, test_auction_data['items'][0]]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    item0 = response.json['data']['items'][0]
    item1 = response.json['data']['items'][1]
    self.assertNotEqual(item0.pop('id'), item1.pop('id'))
    self.assertEqual(item0, item1)

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'items': [{}]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['items']), 1)

    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'items': [{"classification": {
        "scheme": u"CAV",
        "id": u"70123000-9",
        "description": u"Нерухомість"
    }}]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'items': [{"additionalClassifications": auction['items'][0]["additionalClassifications"]}]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'enquiryPeriod': {'endDate': new_dateModified2}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction = response.json['data']
    self.assertIn('startDate', new_auction['enquiryPeriod'])

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {"data": {"guarantee": {"amount": 12, "valueAddedTaxIncluded": True}}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'][0], {u'description': {u'valueAddedTaxIncluded': u'Rogue field'}, u'location': u'body', u'name': u'guarantee'})

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {"data": {"guarantee": {"amount": 12}}})
    self.assertEqual(response.status, '200 OK')
    self.assertIn('guarantee', response.json['data'])
    self.assertEqual(response.json['data']['guarantee']['amount'], 12)
    self.assertEqual(response.json['data']['guarantee']['currency'], 'UAH')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {"data": {"guarantee": {"currency": "USD"}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['guarantee']['currency'], 'USD')


    #response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'status': 'active.auction'}})
    #self.assertEqual(response.status, '200 OK')

    #response = self.app.get('/auctions/{}'.format(auction['id']))
    #self.assertEqual(response.status, '200 OK')
    #self.assertEqual(response.content_type, 'application/json')
    #self.assertIn('auctionUrl', response.json['data'])

    auction_data = self.db.get(auction['id'])
    auction_data['status'] = 'complete'
    self.db.save(auction_data)

    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'status': 'active.auction'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update auction in current (complete) status")


def dateModified_auction(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/auctions', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    auction = response.json['data']
    dateModified = auction['dateModified']

    response = self.app.get('/auctions/{}'.format(auction['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['dateModified'], dateModified)

    response = self.app.patch_json('/auctions/{}'.format(
        auction['id']), {'data': {'procurementMethodRationale': 'Open'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['dateModified'], dateModified)
    auction = response.json['data']
    dateModified = auction['dateModified']

    response = self.app.get('/auctions/{}'.format(auction['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], auction)
    self.assertEqual(response.json['data']['dateModified'], dateModified)


def guarantee(self):
    response = self.app.post_json('/auctions', {'data': test_auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertNotIn('guarantee', response.json['data'])
    auction = response.json['data']
    response = self.app.patch_json('/auctions/{}'.format(auction['id']),
                                   {'data': {'guarantee': {"amount": 55}}})
    self.assertEqual(response.status, '200 OK')
    self.assertIn('guarantee', response.json['data'])
    self.assertEqual(response.json['data']['guarantee']['amount'], 55)
    self.assertEqual(response.json['data']['guarantee']['currency'], 'UAH')

    response = self.app.patch_json('/auctions/{}'.format(auction['id']),
                                   {'data': {'guarantee': {"amount": 100500, "currency": "USD"}}})
    self.assertEqual(response.status, '200 OK')
    self.assertIn('guarantee', response.json['data'])
    self.assertEqual(response.json['data']['guarantee']['amount'], 100500)
    self.assertEqual(response.json['data']['guarantee']['currency'], 'USD')

    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'guarantee': None}})
    self.assertEqual(response.status, '200 OK')
    self.assertIn('guarantee', response.json['data'])
    self.assertEqual(response.json['data']['guarantee']['amount'], 100500)
    self.assertEqual(response.json['data']['guarantee']['currency'], 'USD')

    data = deepcopy(test_auction_data)
    data['guarantee'] = {"amount": 100, "currency": "USD"}
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertIn('guarantee', response.json['data'])
    self.assertEqual(response.json['data']['guarantee']['amount'], 100)
    self.assertEqual(response.json['data']['guarantee']['currency'], 'USD')

# AuctionProcessTest


def one_valid_bid_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    response = self.app.post_json('/auctions',
                                  {"data": test_auction_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    # switch to active.tendering
    response = self.set_status('active.tendering', {"auctionPeriod": {"startDate": (get_now() + timedelta(days=10)).isoformat()}})
    self.assertIn("auctionPeriod", response.json['data'])
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                  {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
    # switch to active.qualification
    self.set_status('active.auction', {'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"id": auction_id}})
    self.assertNotIn('auctionPeriod', response.json['data'])
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    award_date = [i['date'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # set award as active
    response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token), {"data": {"status": "active"}})
    self.assertNotEqual(response.json['data']['date'], award_date)

    # get contract id
    response = self.app.get('/auctions/{}'.format(auction_id))
    contract_id = response.json['data']['contracts'][-1]['id']
    # after stand slill period
    self.app.authorization = ('Basic', ('chronograph', ''))
    self.set_status('complete', {'status': 'active.awarded'})
    # time travel
    auction = self.db.get(auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)
    # sign contract
    self.app.authorization = ('Basic', ('broker', ''))
    self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token), {"data": {"status": "active"}})
    # check status
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'complete')


def one_invalid_bid_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    response = self.app.post_json('/auctions',
                                  {"data": test_auction_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    # switch to active.tendering
    self.set_status('active.tendering')
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                  {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
    # switch to active.qualification
    self.set_status('active.auction', {"auctionPeriod": {"startDate": None}, 'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"id": auction_id}})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # set award as unsuccessful
    response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
                                   {"data": {"status": "unsuccessful"}})
    # time travel
    auction = self.db.get(auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)
    # set auction status after stand slill period
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"id": auction_id}})
    # check status
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'unsuccessful')


def first_bid_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    response = self.app.post_json('/auctions',
                                  {"data": test_auction_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    # switch to active.tendering
    self.set_status('active.tendering')
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                  {'data': {'tenderers': [test_organization], "value": {"amount": 450}}})
    bid_id = response.json['data']['id']
    bid_token = response.json['access']['token']
    # create second bid
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                  {'data': {'tenderers': [test_organization], "value": {"amount": 475}}})
    # switch to active.auction
    self.set_status('active.auction')

    # get auction info
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}/auction'.format(auction_id))
    auction_bids_data = response.json['data']['bids']
    # posting auction urls
    response = self.app.patch_json('/auctions/{}/auction'.format(auction_id),
                                   {
                                       'data': {
                                           'auctionUrl': 'https://auction.auction.url',
                                           'bids': [
                                               {
                                                   'id': i['id'],
                                                   'participationUrl': 'https://auction.auction.url/for_bid/{}'.format(i['id'])
                                               }
                                               for i in auction_bids_data
                                           ]
                                       }
    })
    # view bid participationUrl
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bid_id, bid_token))
    self.assertEqual(response.json['data']['participationUrl'], 'https://auction.auction.url/for_bid/{}'.format(bid_id))

    # posting auction results
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.post_json('/auctions/{}/auction'.format(auction_id),
                                  {'data': {'bids': auction_bids_data}})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # set award as unsuccessful
    response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
                                   {"data": {"status": "unsuccessful"}})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award2_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    self.assertNotEqual(award_id, award2_id)
    # create first award complaint
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(auction_id, award_id, bid_token),
                                  {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization, 'status': 'claim'}})
    complaint_id = response.json['data']['id']
    complaint_owner_token = response.json['access']['token']
    # create first award complaint #2
    response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(auction_id, award_id, bid_token),
                                  {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': test_organization}})
    # answering claim
    self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(auction_id, award_id, complaint_id, owner_token), {"data": {
        "status": "answered",
        "resolutionType": "resolved",
        "resolution": "resolution text " * 2
    }})
    # satisfying resolution
    self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(auction_id, award_id, complaint_id, complaint_owner_token), {"data": {
        "satisfied": True,
        "status": "resolved"
    }})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # set award as active
    self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token), {"data": {"status": "active"}})
    # get contract id
    response = self.app.get('/auctions/{}'.format(auction_id))
    contract_id = response.json['data']['contracts'][-1]['id']
    # create auction contract document for test
    response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(auction_id, contract_id, owner_token), upload_files=[('file', 'name.doc', 'content')], status=201)
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    # after stand slill period
    self.app.authorization = ('Basic', ('chronograph', ''))
    self.set_status('complete', {'status': 'active.awarded'})
    # time travel
    auction = self.db.get(auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)
    # sign contract
    self.app.authorization = ('Basic', ('broker', ''))
    self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token), {"data": {"status": "active"}})
    # check status
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'complete')

    response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(auction_id, contract_id, owner_token), upload_files=[('file', 'name.doc', 'content')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(auction_id, contract_id, doc_id, owner_token), {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) auction status")

    response = self.app.put('/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(auction_id, contract_id, doc_id, owner_token), upload_files=[('file', 'name.doc', 'content3')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) auction status")
