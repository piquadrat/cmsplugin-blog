from django.conf import settings
try:
    from django.views.generic import DateDetailView
except ImportError:
    from cbv import DateDetailView

from menus.utils import set_language_changer
from cmsplugin_blog.models import Entry

if 'threadedcomments' in settings.INSTALLED_APPS:
    template_name_suffix = '_detail_threadedcomments'
else:
    template_name_suffix = '_detail'

class EntryDateDetailView(DateDetailView):
    
    slug_field = 'entrytitle__slug'
    date_field = 'pub_date'
    month_format = '%m'
    queryset = Entry.objects.all()
    template_name_suffix = template_name_suffix
    
    def get_object(self):
        obj = super(EntryDateDetailView, self).get_object()
        set_language_changer(self.request, obj.language_changer)
        return obj
        
    def get_queryset(self):
        queryset = super(EntryDateDetailView, self).get_queryset()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.published()
