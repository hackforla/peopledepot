# Add new model and API endpoints

This guide aims to enable developers with little or no django experience to add django models and API endpoints to the project. Most code examples are followed by detailed explanations.

The developer will have exposure to the following in this document:

- python
- django
- django rest framework
- relational database through the Django ORM (object-relational mapper)
- data types
- object-oriented concepts (object, inheritance, composition)
- unit testing
- API design
- command line

This guide assumes the developer has followed the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md#310-push-to-upstream-origin-aka-your-fork) up to section 3.2 and have created a local branch to work on this. The development server would be already running in the background and will automatically apply the changes when we save the files.

We will choose the [recurring_event issue](https://github.com/hackforla/peopledepot/issues/14) as an example. Our goal is to create a database table and an API that a client can use to work with the data. The work is split into 3 testable components: the model, the admin site, and the API

Let's start!

## The model

### Add the model in django

Add the following to app/core/models.py

```python
class RecurringEvent(AbstractBaseModel):
    """
    Recurring Events
    """

    name = models.CharField(max_length=255)
    start_time = models.TimeField("Start", null=True, blank=True)
    duration_in_min = models.IntegerField(null=True, blank=True)
    video_conference_url = models.URLField(blank=True)
    additional_info = models.TextField(blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # location_id = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    # event_type_id = models.ForeignKey("EventType", on_delete=models.DO_NOTHING)
    # brigade_id = models.ForeignKey("Brigade", on_delete=models.DO_NOTHING)
    # day_of_week = models.ForeignKey("DayOfWeek", on_delete=models.DO_NOTHING)
    # must_roles = models.ManyToManyField("Role")
    # should_roles = models.ManyToManyField("Role")
    # could_roles = models.ManyToManyField("Role")
    # frequency_id = models.ForeignKey("Frequency", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"
```

[link to code](https://github.com/hackforla/peopledepot/blob/aad76446fc9ce3942d4f6290322ca1f73279703e/app/core/models.py#L154-L176)

1. We inherit all models from AbstractBaseModel, which provides a `uuid` primary key, `created_at`, and `updated_at` timestamps. In the Github issue, these fields might be called `id`, `created`, and `updated`. There's no need to add those.
1. Most fields should not be required. Text fields should be `blank=True`, data fields should be `null=True`.
1. The data types in the github issue may be given in database column types such as `INTEGER`, `VARCHAR`, but we need to convert them into [Django field types](https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types) when defining the model.
1. `VARCHAR` can be either `CharField` or `TextField`.
   1. `CharField` has a `max_length`, which makes it useful for finite length text data. We're going default to giving them `max_length=255` unless there's a better value like `max_length=2` for state abbreviation.
   1. `TextField` doesn't have a maximum length, which makes it ideal for large text fields such as `description`.
1. Try to add the relationships to non-existent models, but comment them out. Another developer will complete them when they go to implement those models. See [relationships guide](model-relationships.md) for explanations of how to define relationships.
1. Always override the `__str__` function to output something more meaningful than the default. It lets us do a quick test of the model by calling `str([model])`. It's also useful for the admin site model list view.

### Run migrations to generate database migration files

```bash
./scripts/migrate.sh
```

### Write a simple test

Since we overrode the `__str__` function, we need to write a test for it.

1. Add a fixture for the model

   Fixtures are reusable code that can be used in multiple tests by declaring them as parameters of the test case. In this example, we show both defining a fixture (recurring_event) and using another fixture (project).

   Note: The conftest file is meant to hold shared test fixtures, among other things. The fixtures have directory scope.

   Add the following to app/core/tests/conftest.py

   ```python
   @pytest.fixture
   def recurring_event(project):
       return RecurringEvent.objects.create(name="Test Recurring Event", project=project)
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/aad76446fc9ce3942d4f6290322ca1f73279703e/app/core/tests/conftest.py#L43-L45)

   1. We name the fixture after the model name (`recurring_event`).
   1. This model makes use of the `project` model as a foreign key relation, so we pass in the `project` fixture, which creates a `project` model.
   1. We create an object of the new model, passing in at least the required fields. In this case, we passed in enough arguments to use the `__str__` method in a test.

1. Add a test case

   When creating Django models, there's no need to test the CRUD functionality since Django itself is well-tested and we can expect it to generate the correct CRUD functionality. Feel free to write some tests for practice. What really needs testing are any custom code that's not part of Django. Sometimes we need to override the default Django behavior and that should be tested.

   Here's a basic test to see that the model stores its name.

   Add the following to app/core/tests/test_models.py

   ```python
   def test_recurring_event(recurring_event):
       assert str(recurring_event) == "Test Recurring Event"
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/aad76446fc9ce3942d4f6290322ca1f73279703e/app/core/tests/test_models.py#L17-L18)

   1. Pass in our fixture so that the model object is created for us.
   1. The `__str__` method should be tested since it's an override of the default Django method.
   1. Write assertion(s) to check that what's passed into the model is what it contains. The simplest thing to check is the `__str__` method.

1. Run the test script to show it passing

   ```bash
   ./scripts/test.sh
   ```

### Check point 1

This is a good place to pause, check, and save. Refer to the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md) sections 3.4-3.9 for details.

1. Run pre-commit checks

   ```bash
   ./scripts/precommit-check.sh
   ```

1. Add and commit changes

   ```bash
   git add -A
   git commit -m "feat: add model: recurring_event"
   ```

## The admin site

Django comes with an admin site interface that allows admin users to view and change the data in the models. It's essentially a database viewer.

### Register the model with the admin site

1. Import the new model

   ```python
   from .models import RecurringEvent
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/admin.py#L10)

1. Register the model

   ```python
   @admin.register(RecurringEvent)
   class RecurringEventAdmin(admin.ModelAdmin):
       list_display = (
           "name",
           "start_time",
           "duration_in_min",
       )
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/admin.py#L115-L121)

   1. We declare a [ModelAdmin](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin) class so we can customize the fields that we expose to the admin interface.
   1. We use the [register decorator](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.register) to register the class with the admin site.
   1. [list_display](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) controls what's shown in the list view
   1. [list_filter](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) adds filter controls to declared fields (useful, but not shown in this example).

### View the admin site to see that everything's working and there are no issues, which should be the case unless there's custom input fields creating problems

1. See the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md#:~:text=Browse%20to%20the%20web%20admin%20interface%20at%20http%3A//localhost%3A8000/admin/) for how to view the admin interface.

1. Example of a custom field (as opposed to the built-in ones)

   ```python
   time_zone = TimeZoneField(blank=True, use_pytz=False, default="America/Los_Angeles")
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/models.py#L96)

   1. Having a misconfigured or buggy custom field could cause the admin site to crash and the developer will need to look at the debug message and resolve it.

### Tests

1. Feel free to write tests for the admin. There's no example for it yet.
1. The reason there's no tests is that the admin site is independent of the API functionality, and we're mainly interested in the API part.
1. When the time comes that we depend on the admin interface, we will need to have tests for the needed functionalities.

### Check point 2

This is a good place to pause, check, and save. Refer to the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md) sections 3.4-3.9 for details.

1. Run pre-commit checks

   ```bash
   ./scripts/precommit-check.sh
   ```

1. Add and commit changes

   ```bash
   git add -A
   git commit -m "feat: register admin: recurring_event"
   ```

## The API

There's several components to adding API endpoints: Model(already done), Serializer, View, and Router.

### Add serializer

This is code that serializes objects into strings for the API endpoints, and deserializes strings into object when we receive data from the client.

1. Import the new model

   ```python
   from core.models import RecurringEvent
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/serializers.py#L6)

1. Add a serializer class

   ```python
   class RecurringEventSerializer(serializers.ModelSerializer):
       """Used to retrieve recurring_event info"""

       class Meta:
           model = RecurringEvent
           fields = (
               "uuid",
               "name",
               "start_time",
               "duration_in_min",
               "video_conference_url",
               "additional_info",
               "project",
           )
           read_only_fields = (
               "uuid",
               "created_at",
               "updated_at",
           )
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/serializers.py#L82-L100)

   1. We inherit from [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer). It knows how to serialize/deserialize the Django built-in data fields so we don't have to write the code to do it.
   1. We do need to pass in the `model`, the `fields` we want to expose through the API, and any `read_only_fields`.
   1. `uuid`, `created_at`, and `updated_at` are managed by automations and are always read-only.

1. Custom data fields may need extra code in the serializer

   ```python
   time_zone = TimeZoneSerializerField(use_pytz=False)
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/serializers.py#L14)

   1. This non-built-in model field provides a serializer so we just point to it.

1. Custom validators if we need them

   We will need to write custom validators here if we want custom behavior, such as validating URL strings and limit them to the github user profile pattern using regular expression, for example.

   ```text
   Example here when we have one
   ```

### Add viewset

Viewset defines the set of API endpoints for the model.

1. Import the serializer

   ```python
   from .serializers import RecurringEventSerializer
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/views.py#L14)

1. Add the [viewset](https://www.django-rest-framework.org/api-guide/viewsets/) and CRUD API endpoint descriptions

   ```python
   @extend_schema_view(
       list=extend_schema(description="Return a list of all the recurring events"),
       create=extend_schema(description="Create a new recurring event"),
       retrieve=extend_schema(description="Return the details of a recurring event"),
       destroy=extend_schema(description="Delete a recurring event"),
       update=extend_schema(description="Update a recurring event"),
       partial_update=extend_schema(description="Patch a recurring event"),
   )
   class RecurringEventViewSet(viewsets.ModelViewSet):
       permission_classes = [IsAuthenticated]
       queryset = RecurringEvent.objects.all()
       serializer_class = RecurringEventSerializer
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/views.py#L112-L123)

   1. We inherit from [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset), which provides a default view implementation of all 6 CRUD actions: `create`, `retrieve`, `partial_update`, `update`, `destroy`, `list`.
   1. We use the `extend_schema_view` decorator to attach the API doc strings to the viewset. They are usually defined as docstrings of the corresponding function definitions inside the viewset. Since we use `ModelViewSet`, there's nowhere to put the docstrings but above the viewset.
   1. The minimum code we need with `ModelViewSet` are the `queryset`, and the `serializer_class`.
   1. Permissions
      1. For now use `permission_classes = [IsAuthenticated]`
      1. It doesn't control permissions the way we want, but we will fix it later.

### Extended example

This example shows how to add a filter params. It's done for the [user model](https://github.com/hackforla/peopledepot/issues/15) as a [requirement](https://github.com/hackforla/peopledepot/issues/10) from VRMS.

1. Here's a more complex API doc example (this example is using the User model's ViewSet)

   ```python
   @extend_schema_view(
       list=extend_schema(
           summary="Users List",
           description="Return a list of all the existing users",
           parameters=[
               OpenApiParameter(
                   name="email",
                   type=str,
                   description="Filter by email address",
                   examples=[
                       OpenApiExample(
                           "Example 1",
                           summary="Demo email",
                           description="get the demo user",
                           value="demo-email@email.com,",
                       ),
                   ],
               ),
               OpenApiParameter(
                   name="username",
                   type=OpenApiTypes.STR,
                   location=OpenApiParameter.QUERY,
                   description="Filter by username",
                   examples=[
                       OpenApiExample(
                           "Example 1",
                           summary="Demo username",
                           description="get the demo user",
                           value="demo-user",
                       ),
                   ],
               ),
           ],
       ),
       create=extend_schema(description="Create a new user"),
       retrieve=extend_schema(description="Return the given user"),
       destroy=extend_schema(description="Delete the given user"),
       update=extend_schema(description="Update the given user"),
       partial_update=extend_schema(description="Partially update the given user"),
   )
   class UserViewSet(viewsets.ModelViewSet):
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/views.py#L39-L79)

   1. Define strings for all 6 actions: `create`, `retrieve`, `partial_update`, `update`, `destroy`, `list`.
   1. This one is fancy and provides examples of data to pass into the query params. It's probably more than we need right now.
      1. The examples array can hold multiple examples.
         1. Example ID string has to be unique but is not displayed.
         1. `summary` string appears as an option in the dropdown.
         1. `description` is displayed in the example.

1. Add any query params according to the requirements (this example is using the User model's ViewSet)

   ```python
   class UserViewSet(viewsets.ModelViewSet):
       ...

       def get_queryset(self):
           """
           Optionally filter users by an 'email' and/or 'username' query paramerter in the URL
           """
           queryset = get_user_model().objects.all()
           email = self.request.query_params.get("email")
           if email is not None:
               queryset = queryset.filter(email=email)
           username = self.request.query_params.get("username")
           if username is not None:
               queryset = queryset.filter(username=username)
           return queryset
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/views.py#L84-L95)

   1. Notice the `queryset` property is now the `get_queryset(()` function which returns the queryset.
   1. The `get_queryset()` function overrides the default and lets us filter the objects returned to the client if they pass in a query param.
   1. Start with all the model objects and filter them based on any available query params.

### Register API endpoints to the router

1. Import the viewset.

   ```python
   from .views import RecurringEventViewSet
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/urls.py#L6)

1. [Register](https://www.django-rest-framework.org/api-guide/routers/#usage) the viewset to the [router](https://www.django-rest-framework.org/api-guide/routers/)

   ```python
   router.register(r"recurring-events", RecurringEventViewSet, basename="recurring-event")
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/api/urls.py#L14)

   1. First param is the URL prefix use in the API routes. It is, by convention, plural
      - This would show up in the URL like this: `http://localhost/api/v1/recuring-events/` and `http://localhost/api/v1/recuring-events/<uuid>`
   1. Second param is the viewset class which defines the API actions
   1. `basename` is the name used for generating the endpoint names, such as [basename]-list, [basename]-detail, etc. It's in the singular form. This is automatically generated if the viewset definition contains a `queryset` attribute, but it's required if the viewset overrides that with the `get_queryset` function
      - `reverse("recurring-event-list")` would return `http://localhost/api/v1/recuring-events/`

### Add API tests

For the CRUD operations, since we're using `ModelViewSet` where all the actions are provided by `rest_framework` and well-tested, it's not necessary to have test cases for them. But here's an example of one.

1. Import API URL

   ```python
   RECURRING_EVENTS_URL = reverse("recurring-event-list")
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/09e2856b6dd8038aedbbc9b42c3a44009be1fd2f/app/core/tests/test_api.py#L11)

1. Add test case

   ```python
   def test_create_recurring_event(auth_client, project):
       """Test that we can create a recurring event"""

       payload = {
           "name": "Test Weekly team meeting",
           "start_time": "18:00:00",
           "duration_in_min": 60,
           "video_conference_url": "https://zoom.com/link",
           "additional_info": "Test description",
           "project": project.uuid,
       }
       res = auth_client.post(RECURRING_EVENTS_URL, payload)
       assert res.status_code == status.HTTP_201_CREATED
       assert res.data["name"] == payload["name"]
   ```

   [link to code](https://github.com/hackforla/peopledepot/blob/097f8f254534c1e53bc23f14ef71afbed0b70fa0/app/core/tests/test_api.py#L150-L163)

   1. Given
      1. Pass in the necessary fixtures
      1. Construct the payload
   1. When
      1. Create the object
   1. Then
      1. Check that it's created via [status code](https://www.django-rest-framework.org/api-guide/status-codes/#client-error-4xx)
      1. Maybe also check the data. A real test should check all the data, but we're kind of relying on django to have already tested this.

1. Run the test script to show it passing

   ```bash
   ./scripts/test.sh
   ```

### Check point 3

This is a good place to pause, check, and save. Refer to the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md) sections 3.4-3.9 for details.

1. Run pre-commit checks

   ```bash
   ./scripts/precommit-check.sh
   ```

1. Add and commit changes

   ```bash
   git add -A
   git commit -m "feat: add endpoints: recurring_event"
   ```

### Push the code and start a PR

Refer to the [contributing doc](https://github.com/hackforla/peopledepot/blob/main/docs/CONTRIBUTING.md#310-push-to-upstream-origin-aka-your-fork) section 3.10 onward.
