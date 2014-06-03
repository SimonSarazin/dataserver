from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentTypeManager
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView

from cms.models import Page
from cms.api import create_page, add_plugin, assign_user_to_page
from cms.models.permissionmodels import PagePermission
from guardian.shortcuts import assign_perm

from dataserver import settings

class CMSRedirectView(RedirectView):
  """
    a view aimed at redirecting to base CMS views after some checks
    - 1st time : create a home page with all plugins 
    - Then: redirect to cms user home page
  """
  def get_redirect_url(self, **kwargs):
        url = self.page.get_absolute_url()
        url += "?edit"
        return url

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    """
    GUP specific 
    1/ get current user first group
        u.groups.all()[0]
    2a/ get page associated to group
        g.pagepermission_set.all()[0].page
    OR
    2b/ create page
    3/ bind plugins
    4/ associate to group
        assign_perm("cms.view_page", user_or_group=g, obj=self.page)
        assign_perm("cms.change_page", user_or_group=g, obj=self.page)
        assign_perm("cms.publish_page", user_or_group=g, obj=self.page)
    """
    # FIXME : should implement multi-groups management
    user_group = request.user.groups.all()[0]

    # check if logged in user has already created a page 
    try:
        #self.page = Page.objects.get(created_by=request.user, in_navigation=True, publisher_is_draft=True, is_home = False, template=settings.PROJECT_PAGE_TEMPLATE)
        pp = PagePermission.objects.filter(group=user_group)[0]
        self.page = pp.page
    except:      
        # else, create page and hook plugins to placeholders :      
        page_name = 'home-%s' % (user_group)
        self.page = create_page(page_name, settings.PROJECT_PAGE_TEMPLATE, 'fr', created_by=request.user, published=True, in_navigation=True)
        # assign group to created page
        perm_data = {
               'can_change': True,
               'can_add': False,
               'can_move_page':False,
               'can_delete':False,
               'can_change_advanced_settings': True,
               'can_publish': True,
               'can_change_permissions': True,
               'can_view': False,
           }
        page_permission = PagePermission(page=self.page, group=user_group, **perm_data)
        page_permission.save()

        # logo 
        logo_ph = self.page.placeholders.get(slot='logo')
        add_plugin(logo_ph, 'PicturePlugin', 'fr')
        # project_description
        descr_ph = self.page.placeholders.get(slot='project_description')
        add_plugin(descr_ph, 'TextPlugin', 'fr', body='Cliquez pour ajouter la description du projet')
        # project_pictures
        pic_ph = self.page.placeholders.get(slot='project_pictures')
        add_plugin(pic_ph, 'BackgroundImagesPlugin', 'fr')
        # news_block
        news_ph = self.page.placeholders.get(slot='news_block')
        add_plugin(news_ph, 'CMSNewsPlugin', 'fr')
        # carto
        carto_ph = self.page.placeholders.get(slot='carto')
        add_plugin(carto_ph, 'CartoPlugin', 'fr')


    return super(CMSRedirectView, self).dispatch(request, *args, **kwargs)
  
  
  
  
