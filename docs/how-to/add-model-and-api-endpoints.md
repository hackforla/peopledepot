## Add the model

https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdminhttps://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/models.py#L150-L172

1. We inherit from AbstractBaseModel, which provides a uuid primary key, created_at, and updated_at timestamps.
1. Most fields should be nullable. Text fields should be blank=True, data fields should be null=True and maybe also blank=True.
1. CharFields are Varchar. Just give them max_length=255 unless there's a better value.
1. Try to add the relationships to non-existant models, but comment them out. Another dev will complete them when they go to implement those models.
1. Always define the `__str__` function. It lets us do a quick test of the model by calling `str([model])`.

### run migrations

```bash
./scripts/migrate.sh
```

### Write a simple test

1. Add a fixture for the model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/conftest.py#L40-L42

   1. We name the fixture after the model name.
   1. This model makes use of a project model as a foreign key relation, so we pass in the project fixture which defines a project model.
   1. We create an object of the new model, passing in at least the required fields.

1. Add a test case

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_models.py#L17-L18

   1. pass in our fixture so that the model object is created for us
   1. Write assertion(s) to check that what's passed into the model is what it contains. The simplest thing to check is the `str()` method

## Register with admin site

1. Import the new model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/admin.py#L8

1. Register the model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/admin.py#L110-L116

   1. We declare a [ModelAdmin](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin) class so we can customize the fields that we expose to the admin interface.
   1. We use the [register decorator](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.register) to register the class with the admin site.
   1. [list_display](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) controls what's shown in the list view
   1. [list_filter](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) adds filter controls to declared fields

### Use the admin site to see everything's working and there are no issues, which should be fine unless there's custom input fields

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/models.py#L95

## Work on the API endpoints

### Add serializer

This is code that serializes objects into strings for the API endpoint, and deserializes strings into object when we receive data from the client.

1. Import the model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L4

1. Add a serializer class

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L78-L96

   1. We inherit from ModelSerializer, which provides a lot of functionality and reduces the amount of code we need to write for built-in data fields.
   1. We do need to pass in the model, the fields we want to expose to the API, and any read-only fields.
   1. uuid, created_at, and updated_at are automatic and always read-only.

1. Custom data fields may need extra code in the serializer.

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L10

1. Custom validators

   We will need to write custom validators here if we want custom behavior, such as validating URL strings and limit them to the github user profile pattern using regular expression, for example.

   ```text
   Example here when we have one
   ```

### Add viewset

Viewset defines the set of endpoints for the API.

1. Import the serializer

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L16

1. Add the [viewset](https://www.django-rest-framework.org/api-guide/viewsets/)

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L121-L138

   1. We inherit from ModelViewSet which provides a default view implementation of all 5 actions: list, create, retrieve, destroy, update, partial_update.
   1. We use the extend_schema_view decorator to attach the API doc strings to the viewset. They are usually defined as docstrings of the corresponding function definitions inside the viewset. Since we use ModelViewSet, there's nowhere to put the docstrings but above the viewset.
   1. The minimum code we need with ModelViewSet are permission_classes, queryset, and serializer_class. Here, we defined custom permissions.
   1. **Don't do this custom get_permissions function**
      1. For now use permission_classes = (IsAuthenticated,) and not the get_permissions function.
      1. It doesn't limit access enough, but we will fix it later.

1. Here's a more complete API doc example

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L35-L75

   1. Define strings for all 5 actions: list, create, retrieve, destroy, update, partial_update.
   1. This one is fancy and provides example of data to pass into the query params. Most of the time we probably won't need it.
      1. The examples array can hold multiple examples.
         1. Example ID string has to be unique but is not displayed
         1. summary string appears as an option in the dropdown
         1. description is displayed in the example

1. Add any query params

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L75-L98

   1. The get_queryset function overrides the default and lets us filter the objects returned to the client if they pass in a query param.
   1. Notice the queryset property is now the get_queryset function which returns the queryset.
   1. Start with all the model objects and filter them based on any available query params.

### Register API endpoints to the router

1. Import the viewset

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/urls.py#L4-L9

1. Register the viewset to the [router](https://www.django-rest-framework.org/api-guide/routers/)

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/urls.py#L14

   1. First param is the URL prefix
   1. Second param is the viewset
   1. basename is the name used for generating the endpoint names, such as [basename]-list, [basename]-detail, etc.

### Add API tests

1. Import API URL

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_api.py#L11

1. Add test case
   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_api.py#L70-L81

   1. Pass in the necessary fixtures
   1. Construct data
   1. Create the object
   1. Check that it's created
   1. Maybe also check the data
