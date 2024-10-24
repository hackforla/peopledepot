is_admin
clear
validate_user_fields_patchable(requesting_user, target_user, request_fields)
    => get_most_privileged_ranked_permissio(requesting_user: User, target_user: User)
    =

field_permissions
permission_type_rank_dict()
csv_field_permissions()
   => parse_csv_field_permissions()
get_field_permission_dict_from_rows
    # @classmethod
    # def get_field_permission_dict_from_rows(
    #     cls, rows: List[Dict[str, Any]]
    # ) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    #     """Convert CSV rows into a structured dictionary."""
    #     result = defaultdict(lambda: defaultdict(list))
    #     for row in rows:
    #         result[row["operation"]][row["table"]].append(
    #             {key: row[key] for key in ["field_name", "read", "update", "create"]}
    #         )
    #     return dict(result)
