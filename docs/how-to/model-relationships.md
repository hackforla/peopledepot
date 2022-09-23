# How model relationships work

## Discussion

This is

## What do I declare for on_delete?

Here are the [on_delete options](https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey.on_delete). On_delete always acts on the model it's declared in and is triggered by an associated model's corresponding row being deleted. For example, `user` has a foreign key(FK) relation to `user_status_type`. When a user_status_type row is deleted, we don't want all the associated users with that status to be deleted as well, so we use have several options:

   1. PROTECT - don't allow the user_status_type row to be deleted as long as there are users using that status.
   1. RESTRICT - see the documetation for this more complex case
   1. SET_NULL - if the FK field is nullable
   1. SET_DEFAULT - set to the defined default value
   1. SET() - set it to a value
   1. DO_NOTHING - not recommended
