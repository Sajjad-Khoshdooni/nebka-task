import logging
import requests
from celery import shared_task

from fund.models import Fund

logger = logging.getLogger(__name__)


@shared_task
def populate_funds():
    url = 'https://fund.fipiran.ir/api/v1/fund/fundcompare'
    resp = requests.get(url=url)

    if resp.ok:
        for fund in resp.json().get('items', []):
            Fund.objects.update_or_create(
                reg_no=fund['regNo'],
                defaults={
                    'name': fund['name'],
                    'net_asset': fund['netAsset'],
                    'cancel_nav': fund['cancelNav'],
                    'annual_efficiency': fund['annualEfficiency']
                }
            )
    else:
        logger.warning('populate funds detail failed due to fipiran bad response', extra={
            'status': resp.status_code,
            'content': resp.content
        })


@shared_task
def populate_funds_detail():
    for fund in Fund.objects.all():
        set_funds_detail.delay(fund.reg_no)


@shared_task(queue='fund')
def set_funds_detail(reg_no):
    url = f'https://fund.fipiran.ir/api/v1/fund/getfund?regno={reg_no}'
    resp = requests.get(url=url)
    if resp.ok:
        data = resp.json().get('item', {})
        Fund.objects.filter(reg_no=reg_no).update(
            investment_manager=data.get('investmentManager'),
            ins_inv_no=data.get('insInvNo'),
            ret_inv_no=data.get('retInvNo'),
        )

    else:
        logger.warning('populate funds detail failed due to fipiran bad response', extra={
            'status': resp.status_code,
            'content': resp.content
        })
