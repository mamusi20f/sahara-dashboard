# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

from django.core.urlresolvers import reverse_lazy
from horizon import forms
from horizon import tables

from savannadashboard.api import client as savannaclient
from savannadashboard.image_registry.forms import EditTagsForm
from savannadashboard.image_registry.forms import RegisterImageForm
from savannadashboard.image_registry.tables import ImageRegistryTable


LOG = logging.getLogger(__name__)


class EditTagsView(forms.ModalFormView):
    form_class = EditTagsForm
    template_name = 'image_registry/edit_tags.html'
    success_url = reverse_lazy('horizon:savanna:image_registry:index')

    def get_context_data(self, **kwargs):
        context = super(EditTagsView, self).get_context_data(**kwargs)
        context['image'] = self.get_object()
        return context

    def get_object(self):
        savanna = savannaclient.Client(self.request)
        return savanna.images.get(self.kwargs["image_id"])

    def get_initial(self):
        image = self.get_object()

        return {"image_id": image.id,
                "tags_list": json.dumps(image.tags),
                "user_name": image.username,
                "description": image.description}


class ImageRegistryView(tables.DataTableView):
    table_class = ImageRegistryTable
    template_name = 'image_registry/image_registry.html'

    def get_data(self):
        savanna = savannaclient.Client(self.request)

        return savanna.images.list()


class RegisterImageView(forms.ModalFormView):
    form_class = RegisterImageForm
    template_name = 'image_registry/register_image.html'
    success_url = reverse_lazy('horizon:savanna:image_registry:index')

    def get_initial(self):
        # need this initialization to allow registration
        # of images without tags
        return {"tags_list": json.dumps([])}
