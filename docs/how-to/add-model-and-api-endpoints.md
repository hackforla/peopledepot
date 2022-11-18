# Add new model and API endpoints

## Add the model in django

https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/models.py#L150-L172

1. We inherit all models from AbstractBaseModel, which provides a uuid primary key, created_at, and updated_at timestamps.
1. Most fields should be nullable. Text fields should be blank=True, data fields should be null=True.
1. The data types in the github issue may be given in database column types such as `INTEGER`, `VARCHAR`, and `TEXT`, but we need to convert them into [Django field types](https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types) when defining the model.
1. CharField cooresponds to `VARCHAR`, which can be text up to a maximum length. We're going default to giving them `max_length=255` unless there's a better value like `max_length=2` for state abbreviation.
1. Try to add the relationships to non-existent models, but comment them out. Another dev will complete them when they go to implement those models. See [relationships guide](model-relationships.md) for explanations of how to define relationships.
1. Always define the `__str__` function. It lets us do a quick test of the model by calling `str([model])`. It's also useful for the admin site model list view.

### Run migrations to generate database migration files

```bash
./scripts/migrate.sh
```

### Write a simple test

Since we defined the `__str__` function, we need to write a test for it.

1. Add a fixture for the model

   Fixtures are reusable code that can be used in multiple tests by declaring them as parameters of the test case. In this example, we show both defining a fixture (recurring_event) and using another fixture (project).

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/conftest.py#L40-L42

   1. We name the fixture after the model name.
   1. This model makes use of a project model as a foreign key relation, so we pass in the project fixture, which creates a project model.
   1. We create an object of the new model, passing in at least the required fields.

1. Add a test case

   When creating Django models, there's no need to test the CRUD functionality since Django itself is well-tested and we can expect it to generate the correct CRUD functionality. Feel free to write some tests for practice. What really needs testing are any custom code that's not part of Django. Sometimes we need to override the default Django behavior and that should be tested.

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_models.py#L17-L18

   1. Pass in our fixture so that the model object is created for us
   1. The `__str__` method should be tested since it's an override of the default Django method.
   1. Write assertion(s) to check that what's passed into the model is what it contains. The simplest thing to check is the `__str__` method

1. Running the test script should show it passing

   ```bash
   ./scripts/test.sh
   ```

## Register the model with admin site

Django comes with an admin site interface that allows admin users to view and change the data in the models. It's essentially a database viewer.

1. Import the new model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/admin.py#L8

1. Register the model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/admin.py#L110-L116

   1. We declare a [ModelAdmin](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin) class so we can customize the fields that we expose to the admin interface.
   1. We use the [register decorator](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.register) to register the class with the admin site.
   1. [list_display](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) controls what's shown in the list view
   1. [list_filter](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) adds filter controls to declared fields (useful, but not showin in this example)

### View the admin site to see everything's working and there are no issues, which should be fine unless there's custom input fields

1. See the [contributing doc](https://github.com/fyliu/peopledepot/blob/development/docs/contributing.md#:~:text=Browse%20to%20the%20web%20admin%20interface%20at%20http%3A//localhost%3A8000/admin/) for how to view the admin interface.

1. Example of a custom field

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/models.py#L95

   1. Having this field could cause the admin site to crash and the developer will need to look at the debug message and resolve it

### Tests

1. Feel free to write tests for the admin. There's no example for it yet.
1. The reason there's no tests is that the admin site is independent of the API functionality, and we're mostly interested in the API part.

## Work on the API endpoints

There's several steps for adding API endpoints.

### Add serializer

This is code that serializes objects into strings for the API endpoints, and deserializes strings into object when we receive data from the client.

1. Import the new model

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L4

1. Add a serializer class

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L78-L96

   1. We inherit from [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer). It knows how to serialize/deserialize the Django built-in data fields so we don't have to write the code to do it.
   1. We do need to pass in the model, the fields we want to expose to the API, and any read-only fields.
   1. uuid, created_at, and updated_at are automatic and always read-only.

1. Custom data fields may need extra code in the serializer.

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/serializers.py#L10

   1. This non-built-in model field provides a serializer so we just point to it

1. Custom validators if we need them

   We will need to write custom validators here if we want custom behavior, such as validating URL strings and limit them to the github user profile pattern using regular expression, for example.

   ```text
   Example here when we have one
   ```

### Add viewset

Viewset defines the set of CRUD API endpoints for the model.

1. Import the serializer

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L16

1. Add the [viewset](https://www.django-rest-framework.org/api-guide/viewsets/) and CRUD API endpoint descriptions.

   https://github.com/fyliu/peopledepot/blob/ee0506ddaf8ca7f09fbbadceb35d2fa361fb0a32/app/core/api/views.py#L107-L118

   1. We inherit from [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset), which provides a default view implementation of all 5 CRUD actions: create, retrieve, partial_update, update, destroy, list.
   1. We use the extend_schema_view decorator to attach the API doc strings to the viewset. They are usually defined as docstrings of the corresponding function definitions inside the viewset. Since we use ModelViewSet, there's nowhere to put the docstrings but above the viewset.
   1. The minimum code we need with ModelViewSet are the queryset, and the serializer_class.
   1. Permissions
      1. For now use permission_classes = [IsAuthenticated]
      1. It doesn't limit access enough, but we will fix it later.

1. Here's a more complex API doc example

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/views.py#L35-L75

   1. Define strings for all 5 actions: create, retrieve, partial_update, update, destroy, list.
   1. This one is fancy and provides example of data to pass into the query params. Most of the time we won't need it.
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

1. [Register](https://www.django-rest-framework.org/api-guide/routers/#usage) the viewset to the [router](https://www.django-rest-framework.org/api-guide/routers/)

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/api/urls.py#L14

   1. First param is the URL prefix use in the API routes. It is, by convention, plural
      - This would show up in the URL like this: `http://localhost/api/v2/recuring-events/` and `http://localhost/api/v2/recuring-events/<uuid>`
   1. Second param is the viewset class which defines the API actions
   1. basename is the name used for generating the endpoint names, such as [basename]-list, [basename]-detail, etc. It's in the singular form. This is automatically generated if the viewset definition contains a `queryset` attribute, but it's required if the viewset overrides that with the `get_queryset` function
      - reverse("recurring-event") would return `http://localhost/api/v2/recuring-events/`

### Add API tests

For the CRUD operations, since we're using `ModelViewSet` where all the actions are provided by `rest_framework` and well-tested, it's not necessary to have test cases for them. But here's an example of one

1. Import API URL

   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_api.py#L11

1. Add test case
   https://github.com/fyliu/peopledepot/blob/acd8898e7b0364913cc8ae3f9973dfd846adedcc/app/core/tests/test_api.py#L70-L81

   1. Use `auth_client` instead of `admin_client`
   1. Given
      1. Pass in the necessary fixtures
      1. Construct the payload
   1. When
      1. Create the object
   1. Then
      1. Check that it's created via [status code](https://www.django-rest-framework.org/api-guide/status-codes/#client-error-4xx)
      1. Maybe also check the data


### Create initial data migration

See page on create initial data migrations
