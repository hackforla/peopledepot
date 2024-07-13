import pytest

from constants import global_admin
from constants import project_lead
from constants import project_member
from core.models import PermissionType
from core.models import Project
from core.models import UserPermissions
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_project_lead
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_project_lead
from core.tests.utils.seed_constants import website_project_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser


def fields_match_for_get_user(username, response_data, fields):
    for user in response_data:
        if user["username"] == username:
            return set(user.keys()) == set(fields)
    return False


def _get_lowest_ranked_permission_type(requesting_username, target_username):
    requesting_user = SeedUser.get_user(requesting_username)
    target_user = SeedUser.get_user(target_username)
    return PermissionUtil.get_lowest_ranked_permission_type(
        requesting_user, target_user
    )


@pytest.mark.django_db
class TestGetLowestRankedPermissionType:
    def test_admin_lowest_for_admin(self):
        """Test that lowest rank for Garry, a global admin user, is global_admin,
        even if a user permission is assigned.
        """
        # Setup
        garry_user = SeedUser.get_user(garry_name)
        website_project = Project.objects.get(name=website_project_name)
        project_lead_permision_type = PermissionType.objects.get(name=project_lead)
        UserPermissions.objects.create(
            user=garry_user,
            project=website_project,
            permission_type=project_lead_permision_type,
        )
        # Test
        rank = _get_lowest_ranked_permission_type(garry_name, valerie_name)
        assert rank == global_admin

    def test_team_member_lowest_rank_for_two_team_members(self):
        """Test that lowest rank for Wally relative tp Wanda, a project lead,
        or Winona, a team member, is project_member
        """
        rank = _get_lowest_ranked_permission_type(wally_name, winona_name)
        assert rank == project_member

        rank = _get_lowest_ranked_permission_type(wally_name, wanda_project_lead)
        assert rank == project_member

    def test_lowest_rank_blank_of_two_non_team_member(self):
        """Test that lowest rank is blank for Wally relative to Patrick,
        who are team members on different projects, is blank."""
        rank = _get_lowest_ranked_permission_type(wally_name, patrick_project_lead)
        assert rank == ""

    def test_team_member_lowest_rank_for_multiple_user_permissions(self):
        """Test that lowest rank for Zani, a team member on Winona's project, is team member
        and lowest rank for Zani, a project lead on Patti's project, is project lead
        """
        rank = _get_lowest_ranked_permission_type(zani_name, winona_name)
        assert rank == project_member

        rank = _get_lowest_ranked_permission_type(zani_name, patti_name)
        assert rank == project_lead
