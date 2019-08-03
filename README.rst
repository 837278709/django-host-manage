====================================
Host Management
====================================

Quick start
--------------------------------------------

1. Add "host_management" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'host_management',
        'rest_framework',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^host_management/', include('host_management.urls')),

3. Run `python manage.py migrate` to create the `host_management` models.

4. Run `python setup.py bdist_wheel`

5. Run `pip install django_host_management-0.8-py3-none-any.whl`
