import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import PI


def serialize_pi(record):
    return {
        'id': record.id,
        'name': record.name,
        'phone': record.phone,
        'relationship': record.relationship,
        'building': record.building,
        'unit': record.unit,
        'room': record.room,
        'propertyType': record.property_type,
    }


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def pi_collection(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        records = PI.objects.all().order_by('-id')
        if phone:
            records = records.filter(phone=phone)
        return JsonResponse({'results': [serialize_pi(record) for record in records]})

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': '请求体必须是 JSON'}, status=400)

    required_fields = {
        'name': '姓名',
        'phone': '手机号',
        'relationship': '身份关系',
        'building': '楼栋',
        'unit': '单元',
        'room': '房号',
        'propertyType': '房屋属性',
    }

    missing = [
        label for key, label in required_fields.items()
        if not str(payload.get(key, '')).strip()
    ]
    if missing:
        return JsonResponse({'error': f'缺少字段：{"、".join(missing)}'}, status=400)

    phone = str(payload['phone']).strip()
    if not phone.isdigit() or len(phone) != 11:
        return JsonResponse({'error': '手机号必须是 11 位数字'}, status=400)

    record = PI.objects.filter(phone=phone).first()
    if record is None:
        record = PI(phone=phone)

    record.name = str(payload['name']).strip()
    record.relationship = str(payload['relationship']).strip()
    record.building = str(payload['building']).strip()
    record.unit = str(payload['unit']).strip()
    record.room = str(payload['room']).strip()
    record.property_type = str(payload['propertyType']).strip()
    record.save()

    return JsonResponse({'result': serialize_pi(record)}, status=201)
