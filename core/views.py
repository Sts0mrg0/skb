import random

from photolog.models import PhotoObject
from django.views import generic, View
from django import http
from . import models

from django.shortcuts import render_to_response
from django.template import RequestContext


def unpack_catalogs(catalogs):
    """Распаковка содержимого каталогов в один список
    Возвращает список фотообъектов
    """

    photoobjects = []
    for cat in catalogs:
        photoobjects.extend(cat.photoobject_set.all())
    return photoobjects


class IndexView(generic.ListView):

    queryset = models.Partitions.published.all()
    template_name = 'core/index.html'
    context_object_name = 'partitions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = models.HomePage.published.first()
        if data:
            context['data'] = data
            catalogs = data.catalog.all()
            photoobjects = unpack_catalogs(catalogs)
            if len(photoobjects) > 3:
                context['randphobj'] = random.sample(photoobjects, k = 4)
            else:
                context['randphobj'] = photoobjects
            context['url_type'] = 'ajax'
            context['url_get'] = '/works/'
            phobj_id = []
            for obj in context['randphobj']:
                phobj_id.append(obj.pk)
            context['context_list'] = phobj_id
            context['current_photoobj'] = phobj_id[0] if phobj_id else None

        return context


class PartitionsView(generic.base.TemplateView):

    def get_obj(self):
        try:
            path = self.request.path
            obj = models.Partitions.objects.get(url = path)
            return obj
        except Exception as e:
            raise

    def get_template_names(self):
        try:
            template_name = self.get_obj().template_name
            return template_name
        except Exception as e:
            return 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['partition'] = self.get_obj()
            return context
        except Exception as e:
            return context


class BasicView(PartitionsView):
    """Вывод базовых модулей"""

    def get_context_data(self, **kwargs):

        filter = self.kwargs.get('prodtype', '')
        try:
            bases = models.StandardModel.objects.all().filter(prod_type=filter)
            context = super().get_context_data(**kwargs)
            context['bases'] = bases
            return context
        except Exception as e:
            raise


class BasicItemView(generic.DetailView):
    """Вывод подробностей базового модуля"""
    
    model = models.StandardModel
    template_name = 'core/basic_item.html'
    context_object_name = 'item'

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter = self.kwargs.get('prodtype', '')
        try:
            bases = models.StandardModel.objects.all().filter(prod_type=filter)
            phobj_id = []
            for obj in bases:
                phobj_id.append(obj.pk)

            id = self.kwargs.get('pk')
            context['images'] = models.StandardModel.objects.get(pk=id).phobj.images_set.all()
            context['bases'] = bases
            context['context_list'] = phobj_id
            context['url_type'] = 'noajax'
            context['url_get'] = '/base/{}/'.format(filter)
            context['current_photoobj'] = id
            return context
        except:
            raise


class WorksView(PartitionsView):
    """Вывод альбома работ"""

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        try:
            obj = self.get_obj()
            catalogs = obj.catalog.all()
            phobj_id = []
            photoobjects = unpack_catalogs(catalogs)
            
            for obj in photoobjects:
                phobj_id.append(obj.pk)

            context['phobj'] = photoobjects
            context['context_list'] = phobj_id
            context['url_type'] = 'ajax'
            context['url_get'] = '/works/'
            context['current_photoobj'] = phobj_id[0] if phobj_id else None
            return context
        except:
            pass



class WorksItemView(generic.DetailView):
    """Формируем окно просмотра картинки
        из каталога с описанием
    """
    model = PhotoObject
    template_name = 'core/gallery_item_view_ajax.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.is_ajax():
            self.template_name = 'core/gallery_item_view.html'
        
        id = self.kwargs.get('pk')
        context['images'] = PhotoObject.objects.get(pk=id).images_set.all()
        # import pdb; pdb.set_trace()
        return context


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response