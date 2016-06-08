from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from apps.html_builder.models import *
from BeautifulSoup import BeautifulSoup
from django.shortcuts import render_to_response

import string
import mechanize
import time
import yaml
import os
import urllib

APP_ROOT_CONFIG = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
config_file = open(os.path.join(APP_ROOT_CONFIG,'structure.yml'), 'r')
config = yaml.load(config_file)

class index(TemplateView):
    model = Main
    template_name = 'html_builder/index.html'

    def __init__(self, **kwargs):
        super(index, self).__init__(**kwargs)
        self.method = None
        self.POST = None

    def get(self, request, *args, **kwargs):
        data = Main(campaign = None, category = None)
        data.save()
        d = Main.objects.latest('id_html_builder_main')
        return render(request, self.template_name, { 'id_html_builder_main': d.id_html_builder_main })

class list(TemplateView):
    template_name = 'html_builder/list.html'

def get_type(request):
   if request.is_ajax():
       type = request.GET['type']
       html = render_to_string('html_builder/partials/' + type + '.html', {'type': type})
   else:
       html = "Error!"
   return HttpResponse(html)

def save_structure(request):
    y = 1
    num_results2 = Structure.objects.filter(fk_html_builder_main=request.GET['fk_html_builder_main']).count()
    if request.is_ajax():
        content_main = Main.objects.filter(id_html_builder_main=request.GET['fk_html_builder_main']).values()
        country = content_main[0]['country']
        campaign = content_main[0]['campaign']
        category = content_main[0]['category']
        j = 0;
        if request.GET['name'] == 'i_jetlore1fila':
            num_results = Structure.objects.filter(fk_html_builder_main=request.GET['fk_html_builder_main'], name='i_jetlore1fila').count()
            order = num_results2 + 1
            r1 = num_results * 5
            r2 = r1 + 5
            j = +1;
            dic_data = {}
            dic_data['order'] = '%s' % order
            dic_data['filter'] = request.GET['filter']
            dic_data['tile'] = request.GET['tile']
            z = 1
            for k in range(r1, r2):
                url_jetlore = config['jetlore']['structure']['url']
                url_jetlore = url_jetlore.replace('[jetlore_code]', config['jetlore'][country])
                url_jetlore = url_jetlore.replace('[tile]', request.GET['tile'])
                url_jetlore = url_jetlore.replace('[filter]', request.GET['filter'])
                x = int(str(k))
                if x <= 4:
                    url_jetlore = url_jetlore.replace('[i]', str(k+1))
                else :
                    url_jetlore = url_jetlore.replace('[i]', str(k))

                code_n = 'code_1'
                url_jetlore = url_jetlore.replace('[country]', country)

                img_jetlore = config['jetlore']['structure']['img']
                if x <= 4:
                    url_jetlore = url_jetlore.replace('[i]', str(k+1))
                else :
                    url_jetlore = url_jetlore.replace('[i]', str(k))
                img_jetlore = url_jetlore.replace('[jetlore_code]', config['jetlore'][country])
                img_jetlore = url_jetlore.replace('[tile]', request.GET['tile'])
                img_jetlore = url_jetlore.replace('[filter]', request.GET['filter'])
                img_jetlore = url_jetlore.replace('[code]', request.GET[code_n])

                data_url = 'url_link_%s' % z
                data_img = 'url_img_%s' % z
                z += 1

                dic_data[data_url] = url_jetlore
                dic_data[data_img] = img_jetlore
                dic_data[code_n] = request.GET[code_n]
                dic_data['name'] = 'i_jetlore1fila'
                dic_data['is_deeplink'] = 0
                dic_data['fk_html_builder_main'] = request.GET['fk_html_builder_main']
        else:
            utm = config['structure']['utms']
            utm = utm.replace('[campaign]', campaign)
            utm = utm.replace('[category]', category)
            utm = utm.replace('[country]', country)
            utm = utm.replace('[name]', request.GET['name'])
            order = num_results2 + 1

            dic_data = request.GET.dict()
            dic_data['order'] = '%s' % order

            j = 0
            adjust_dl = 'https://app.adjust.com/egxlce_om9uev?deep_link=linio://%s' % country
            campaign_dl = '[campaign_dl]'
            category_dl = None
            creative_dl = None
            dl = None
            for key, value in request.GET.iteritems():
                if 'url_link' in key:
                    url = request.GET[key]
                    s = value.find('?')
                    s += 1
                    if s != 0:
                        utm = string.replace(utm, '?wt', '&wt', 1)
                    url_plus_utm = str(url + utm)
                    if key == 'url_link_1':
                        code_n = 'code_1'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 1
                    elif key == 'url_link_2':
                        code_n = 'code_2'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 2
                    elif key == 'url_link_3':
                        code_n = 'code_3'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 3
                    elif key == 'url_link_4':
                        code_n = 'code_4'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 4
                    elif key == 'url_link_5':
                        code_n = 'code_5'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 5
                    elif key == 'url_link_6':
                        code_n = 'code_6'
                        url_plus_utm= url_plus_utm.replace('[code]', request.GET[code_n])
                        j = 6
                    dic_data[key] = url_plus_utm
                    deeplink = "url_deeplink_%s" % j
                    r = value.find('?')
                    r += 1
                    if r == 0:
                        if '.html' or '/p/' in value:
                            m = mechanize.Browser()
                            try :
                                page = m.open(url)
                                html = page.read()
                                soup = BeautifulSoup(html)
                                table = soup.find("td")
                                if table != None:
                                    for a in table:
                                        sku = a
                                    if sku == "SKU":
                                        table = soup.find('td', itemprop="sku")
                                        for a in table:
                                            sku = a
                                    dl = '/d/%s' % sku
                                else :
                                    url_dl_split = url.split('/')
                                    if len(url_dl_split) == 4:
                                        dl = ''
                                    if len(url_dl_split) == 5:
                                        dl = '/c/%s' % url_dl_split[3]
                                    elif len(url_dl_split) == 6:
                                        dl = '/sc/%s' % url_dl_split[4]
                                    elif len(url_dl_split) == 7:
                                        dl = '/sc/%s' % url_dl_split[5]
                            except (mechanize.HTTPError,mechanize.URLError) as e:
                                if isinstance(e,mechanize.HTTPError):
                                    url_dl_split = url.split('/')
                                    if len(url_dl_split) == 4:
                                        dl = ''
                                    if len(url_dl_split) == 5:
                                        dl = '/c/%s' % url_dl_split[3]
                                    elif len(url_dl_split) == 6:
                                        dl = '/sc/%s' % url_dl_split[4]
                                    elif len(url_dl_split) == 7:
                                        dl = '/sc/%s' % url_dl_split[5]
                    else:
                        url_dl_split = url.split('/')
                        if len(url_dl_split) == 4:
                            dl = ''
                        if len(url_dl_split) == 5:
                            dl = '/c/%s' % url_dl_split[3]
                        elif len(url_dl_split) == 6:
                            dl = '/sc/%s' % url_dl_split[4]
                        elif len(url_dl_split) == 7:
                            dl = '/sc/%s' % url_dl_split[5]
                    encode = urllib.quote(url_plus_utm.encode("utf-8")).replace('%25', '%')
                    encode = encode.replace('/', '%2F').replace('%5Bcode%5D', request.GET[code_n])
                    deep_link = adjust_dl + dl + "&redirect=" + encode + "&campaign=Postal&adgroup=CRM&creative=" + campaign_dl.replace('[campaign_dl]', request.GET[code_n])
                    dic_data[deeplink] = deep_link

        print(dic_data)
        Structure.objects.create(**dic_data).save()
        i = Structure.objects.filter(fk_html_builder_main=request.GET['fk_html_builder_main']).values()

    return render(request, 'html_builder/partials/preview.html', { "i": i })

def delete_structure(request):
    if request.is_ajax():
        data = request.GET
        d = Structure.objects.get(id_html_builder_structure=data['id'])
        d.delete()

        return HttpResponse('Success!')

def edit_structure(request):
    dic_data = request.GET.dict()
    Structure.objects.filter(id_html_builder_structure=request.GET['id_html_builder_structure']).update(**dic_data)
    i = Structure.objects.filter(fk_html_builder_main=request.GET['fk_html_builder_main']).values()
    return render(request, 'html_builder/partials/preview.html', { "i": i })

def full_structure(request):
    consulta = ''
    consulta = Structure.objects.filter(id_html_builder_structure=request.GET['id_html_builder_structure']).values()
    id_html_builder_structure = consulta[0]['id_html_builder_structure']
    fk_html_builder_main = consulta[0]['fk_html_builder_main']
    type = consulta[0]['name']
    filter = consulta[0]['filter']
    tile = consulta[0]['tile']
    created_at = consulta[0]['created_at']
    is_deeplink = consulta[0]['is_deeplink']
    order = consulta[0]['order']
    code_1 = consulta[0]['code_1']
    code_2 = consulta[0]['code_2']
    code_3 = consulta[0]['code_3']
    code_4 = consulta[0]['code_4']
    code_5 = consulta[0]['code_5']
    code_6 = consulta[0]['code_6']
    url_img_1 = consulta[0]['url_img_1']
    url_img_2 = consulta[0]['url_img_2']
    url_img_3 = consulta[0]['url_img_3']
    url_img_4 = consulta[0]['url_img_4']
    url_img_5 = consulta[0]['url_img_5']
    url_img_6 = consulta[0]['url_img_6']
    url_img_mobile_1 = consulta[0]['url_img_mobile_1']
    url_link_1 = consulta[0]['url_link_1']
    url_link_2 = consulta[0]['url_link_2']
    url_link_3 = consulta[0]['url_link_3']
    url_link_4 = consulta[0]['url_link_4']
    url_link_5 = consulta[0]['url_link_5']
    url_link_6 = consulta[0]['url_link_6']
    url_deeplink_1 = consulta[0]['url_deeplink_1']
    url_deeplink_2 = consulta[0]['url_deeplink_2']
    url_deeplink_3 = consulta[0]['url_deeplink_3']
    url_deeplink_4 = consulta[0]['url_deeplink_4']
    url_deeplink_5 = consulta[0]['url_deeplink_5']
    url_deeplink_6 = consulta[0]['url_deeplink_6']
    alt_title_1 = consulta[0]['alt_title_1']
    alt_title_2 = consulta[0]['alt_title_2']
    alt_title_3 = consulta[0]['alt_title_3']
    alt_title_4 = consulta[0]['alt_title_4']
    alt_title_5 = consulta[0]['alt_title_5']
    alt_title_6 = consulta[0]['alt_title_6']

    if request.is_ajax():
        html = render_to_string('html_builder/partials/' + type + '.html', {'type': type, 'id_html_builder_structure': request.GET['id_html_builder_structure'], 'fk_html_builder_main': fk_html_builder_main})
        html2 = html
    else:
       html = "Error!"
    return HttpResponse(html)

def build_html(request):
    if request.method == 'POST':

        content_main = Main.objects.filter(id_html_builder_main=request.POST['id_html_builder_main']).values()

        country = content_main[0]['country']
        campaign = content_main[0]['campaign']
        category = content_main[0]['category']

        html_doc = config['html_doc'][country]
        header = config['header'][country]
        style = config['style']
        menu = config['menu'][country]
        footer = config['footer'][country]

        header = header.replace('[campaign]', campaign)
        header = header.replace('[category]', category)
        header = header.replace('[country]', country)

        menu = menu.replace('[campaign]', campaign)
        menu = menu.replace('[category]', category)
        menu = menu.replace('[country]', country)

        footer = footer.replace('[campaign]', campaign)
        footer = footer.replace('[category]', category)
        footer = footer.replace('[country]', country)

        content_all = Structure.objects.filter(fk_html_builder_main=request.POST['id_html_builder_main']).order_by('order').values()
        content = ''
        order = 0
        for i in content_all:
            content += config[i['name']]

            # TODO: Revisar caso de jetlore con if y crear for dependiendo el tipo de banner para quitar codigo
            if i['name'] == 'i_bigbanner':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link = i['url_deeplink_1']
                else:
                    link = i['url_link_1']
                content = content.replace('[url_link_1]', link)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                style = style.replace('%%url_img_mobile_1%%', i['url_img_mobile_1'])
            elif i['name'] == 'i_medvertical' or i['name'] == 'i_medhorizontal' or i['name'] == 'i_teaser2imagenes' or i['name'] == 'i_voucher' or i['name'] == 'i_smallfull':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
            elif i['name'] == 'i_4verticales':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
            elif i['name'] == 'i_bb_4':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                    link5 = i['url_deeplink_5']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                    link5 = i['url_link_5']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
                content = content.replace('[url_link_5]', link5)
                content = content.replace('[url_img_5]', i['url_img_5'])
                content = content.replace('[alt_title_5]', i['alt_title_5'])
            elif i['name'] == 'i_6verticales':
                order = '1'
                content = content.replace('[order]', order)
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                    link5 = i['url_deeplink_5']
                    link6 = i['url_deeplink_6']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                    link5 = i['url_link_5']
                    link6 = i['url_link_6']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
                content = content.replace('[url_link_5]', link5)
                content = content.replace('[url_img_5]', i['url_img_5'])
                content = content.replace('[alt_title_5]', i['alt_title_5'])
                content = content.replace('[url_link_6]', link6)
                content = content.replace('[url_img_6]', i['url_img_6'])
                content = content.replace('[alt_title_6]', i['alt_title_6'])
            elif i['name'] == 'i_jetlore1fila':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])

        html = html_doc + style + header + menu + content + footer

        file_name = time.strftime("%d%m%Y__%H%M%S") + '__html_builder_beta_1.html'
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
        return response

def update_general_information(request):
    Main.objects.filter(id_html_builder_main=request.GET['id_html_builder_main']).update(campaign=request.GET['campaign'], category=request.GET['category'], country=request.GET['country'])

def update_order(request):
    Structure.objects.filter(id_html_builder_structure=request.GET['id_html_builder_structure']).update(order=request.GET['order'])

def build_html_preview(request):
    if request.method == 'POST':

        content_main = Main.objects.filter(id_html_builder_main=request.POST['id_html_builder_main']).values()

        country = content_main[0]['country']
        campaign = content_main[0]['campaign']
        category = content_main[0]['category']

        html_doc = config['html_doc'][country]
        header = config['header'][country]
        style = config['style']
        menu = config['menu'][country]
        footer = config['footer'][country]

        header = header.replace('[campaign]', campaign)
        header = header.replace('[category]', category)
        header = header.replace('[country]', country)

        menu = menu.replace('[campaign]', campaign)
        menu = menu.replace('[category]', category)
        menu = menu.replace('[country]', country)

        footer = footer.replace('[campaign]', campaign)
        footer = footer.replace('[category]', category)
        footer = footer.replace('[country]', country)

        content_all = Structure.objects.filter(fk_html_builder_main=request.POST['id_html_builder_main']).order_by('order').values()
        content = ''
        order = 0
        for i in content_all:
            content += config[i['name']]

            # TODO: Revisar caso de jetlore con if y crear for dependiendo el tipo de banner para quitar codigo
            if i['name'] == 'i_bigbanner':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link = i['url_deeplink_1']
                else:
                    link = i['url_link_1']
                content = content.replace('[url_link_1]', link)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                style = style.replace('%%url_img_mobile_1%%', i['url_img_mobile_1'])
            elif i['name'] == 'i_medvertical' or i['name'] == 'i_medhorizontal' or i['name'] == 'i_teaser2imagenes' or i['name'] == 'i_voucher' or i['name'] == 'i_smallfull':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
            elif i['name'] == 'i_4verticales':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
            elif i['name'] == 'i_bb_4':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                    link5 = i['url_deeplink_5']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                    link5 = i['url_link_5']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
                content = content.replace('[url_link_5]', link5)
                content = content.replace('[url_img_5]', i['url_img_5'])
                content = content.replace('[alt_title_5]', i['alt_title_5'])
            elif i['name'] == 'i_6verticales':
                order = '1'
                content = content.replace('[order]', order)
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                    link5 = i['url_deeplink_5']
                    link6 = i['url_deeplink_6']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                    link5 = i['url_link_5']
                    link6 = i['url_link_6']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[alt_title_1]', i['alt_title_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[alt_title_2]', i['alt_title_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[alt_title_3]', i['alt_title_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])
                content = content.replace('[alt_title_4]', i['alt_title_4'])
                content = content.replace('[url_link_5]', link5)
                content = content.replace('[url_img_5]', i['url_img_5'])
                content = content.replace('[alt_title_5]', i['alt_title_5'])
                content = content.replace('[url_link_6]', link6)
                content = content.replace('[url_img_6]', i['url_img_6'])
                content = content.replace('[alt_title_6]', i['alt_title_6'])
            elif i['name'] == 'i_jetlore1fila':
                i['order'] = '1'
                if i['is_deeplink'] == '1':
                    link1 = i['url_deeplink_1']
                    link2 = i['url_deeplink_2']
                    link3 = i['url_deeplink_3']
                    link4 = i['url_deeplink_4']
                else:
                    link1 = i['url_link_1']
                    link2 = i['url_link_2']
                    link3 = i['url_link_3']
                    link4 = i['url_link_4']
                content = content.replace('[url_link_1]', link1)
                content = content.replace('[url_img_1]', i['url_img_1'])
                content = content.replace('[url_link_2]', link2)
                content = content.replace('[url_img_2]', i['url_img_2'])
                content = content.replace('[url_link_3]', link3)
                content = content.replace('[url_img_3]', i['url_img_3'])
                content = content.replace('[url_link_4]', link4)
                content = content.replace('[url_img_4]', i['url_img_4'])

        html = html_doc + style + header + menu + content + footer

        return HttpResponse(html)

