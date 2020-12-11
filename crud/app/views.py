import json
import datetime
import os
import pandas as pd
from django.views import View
from app.models import CrudExample
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpResponse


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def validate_request(params, required_fields=[]):
    """校验字段"""
    missing_fields = set(required_fields) - set(params.keys())
    if missing_fields:
        raise Exception('缺失必要字段: {}'.format(', '.join(missing_fields)))
    return True

def cleanse_content(search_content):
    """清洗搜索内容并分段"""
    parts = search_content.strip().replace('\n', ',').replace('，', ',').split(',')
    parts = [x for x in parts if x]
    return parts

def obj2dict(obj):
    """对象转换成字典
    auto_now 及 auto_now_add 在model_to_dict转换时会被忽略, 需要手动处理
    """
    temp = model_to_dict(obj)
    time_fields = [field.name for field in obj.__class__._meta.get_fields() if 'auto_now' in field.__dict__ or 'auto_now_add' in field.__dict__]
    for one in time_fields:
        if isinstance(getattr(obj, one), datetime.datetime):
            temp[one] = getattr(obj, one).strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(getattr(obj, one), datetime.date):
            temp[one] = getattr(obj, one).strftime('%Y-%m-%d')
    return temp

class CrudView(View):

    def get(self, request):
        result = {'state': 'err', 'data': [], 'message': ''}
        params = request.GET
        print('GET请求参数:', params)

        if 'action' not in params:
            message = '缺少必要参数: action'
            return HttpResponse(json.dumps({'state': 'err', 'message': message}))

        # 搜索
        if params['action'] == 'GetData':
            page_size = int(params.get('pageSize', 10))
            page_num = int(params.get('pageNum', 1))

            q = Q()

            # 删除前后空格
            search = json.loads(params['search'])
            field1 = search.get('field1', '').strip()
            field2 = search.get('field2', '').strip()
            field3 = search.get('field3', '').strip()

            # 精确搜索
            if field1:
                q &= Q(field1=field1)

            # 多个值模糊搜索
            if field2:
                field2_parts = cleanse_content(field2)
                temp_q = Q()
                for one in field2_parts:
                    temp_q |= Q(field2__icontains=one)
                q &= temp_q

            if field3:
                q &= Q(field3__icontains=field3)

            pag = Paginator(CrudExample.objects.filter(q), page_size)
            data = []
            for one in pag.get_page(page_num):
                data.append(obj2dict(one))
            result['allCount'] = pag.count
            result['data'] = data
            result['state'] = 'success'

        # 导出
        if params['action'] == 'DownloadFile':
            df = pd.DataFrame(CrudExample.objects.filter().values())
            filename = 'export_file_{}.csv'.format(datetime.datetime.now().strftime("%Y%m%d%X"))
            df.to_csv(filename, index=False, encoding="utf_8_sig")
            with open(filename, 'rb') as file:
                response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename={}".format(filename)
            response['Access-Control-Expose-Headers'] = "FileName"
            response['FileName'] = json.dumps(filename)
            os.remove(filename)
            return response

        # 下载模板
        if params['action'] == 'DownloadTemplate':
            example_filename = 'CRUD上传模板.xlsx'
            with open(example_filename, 'rb') as file:
                response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename={}".format(example_filename)
            response['Access-Control-Expose-Headers'] = "FileName"
            response['FileName'] = json.dumps(example_filename)
            return response

        return HttpResponse(json.dumps(result, cls=ComplexEncoder))

    def post(self, request):
        result = {'state': 'err', 'data': [], 'message': ''}
        params = request.POST
        if not params:
            params = json.loads(request.body)
        if 'action' not in params:
            message = '缺少必要参数: action'
            return HttpResponse(json.dumps({'state': 'err', 'message': message}))

        print('POST请求参数:', params)

        try:
            # 上传文件
            if params['action'] == 'Upload':
                filename = 'upload_file_{}.xlsx'.format(datetime.datetime.now().strftime("%Y%m%d%X"))
                for _, upload_content in request.FILES.items():
                    with open(filename, 'wb') as file:
                        for chunk in upload_content:
                            file.write(chunk)
                # 写入文件
                df = pd.read_excel(filename)

                # 清除前后空格
                df = df.applymap(lambda x: x.strip())

                # 重命名各列
                df = df.rename(columns={'字段1': 'field1', '字段2': 'field2', '字段3': 'field3'})
                allow_fields = [x.name for x in CrudExample._meta.get_fields() if x.name not in ['id']]
                create_arr = []

                # 批量创建
                for one in df.to_dict('records'):
                    create_arr.append(CrudExample(**one))
                CrudExample.objects.bulk_create(create_arr)
                result['state'] = 'success'

            elif params['action'] == 'Create':
                create_form = {}
                allow_fields = [x.name for x in CrudExample._meta.get_fields() if x.name not in ['id']]
                for key, value in params['form'].items():
                    if key in allow_fields and value:
                        create_form[key] = value.strip()
                CrudExample.objects.create(**create_form)
                result['state'] = 'success'

            # 更改
            elif params['action'] == 'Update':
                validate_request(params, required_fields=['form'])
                CrudExample.objects.filter(id=params['id']).update(
                    field1=params['form']['field1'],
                    field2=params['form']['field2'],
                    field3=params['form']['field3'])
                result['state'] = 'success'

            # 删除
            elif params['action'] == 'Delete':
                validate_request(params, required_fields=['ids'])
                CrudExample.objects.filter(id__in=params['ids']).delete()
                result['state'] = 'success'

            else:
                result['message'] = 'action参数无效'

            return HttpResponse(json.dumps(result, cls=ComplexEncoder))
        except Exception as err:
            import traceback
            traceback.print_exc()
            result['message'] = str(err)
            return HttpResponse(json.dumps(result, cls=ComplexEncoder))

