┌───────────────────────────┐
│ Incoming DRF Request │
└─────────────-─────────────┘

GET REQUEST
┌───────────────────────┐
│ ViewSet.get_queryset │
└─────────────┬─────────┘
│
▼
UserRelatedRequest.filter_queryset_by_allowed_users(view)
→ restricts queryset to users the requester is allowed to see

POST and PATCH requests
┌───────────────────────────────┐
│ Permission Checks (ViewSet) │
└─────────────┬─────────────────┘
│
├── POST request:
│ UserRelatedPostPatchPermission.has_permission
│ → UserRelatedRequest.validate_post_fields(view, request)
│
└── PATCH request:
UserRelatedPostPatchPermission.has_object_permission
→ UserRelatedRequest.validate_patch_fields(view, request, obj)

RESPONSE TO CLIENT

┌─────────────────────────┐
│ Serializer Execution │
└─────────────┬───────────┘
│
▼
UserSerializer.to_representation(instance)
→ UserRelatedRequest.get_serializer_representation(self, instance, original_representation)
→ filters serializer output to allowed fields

```
          │
          ▼
```

┌───────────────────────────┐
│ Response to the Client │
└───────────────────────────┘
