import pytest

from constants import admin_global
from constants import admin_project
from constants import member_project
from core.api.permission_check import PermissionCheck
from core.models import PermissionType
from core.models import Project
from core.models import UserPermission
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_practice_lead
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
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
    return PermissionCheck.get_lowest_ranked_permission_type(
        requesting_user, target_user
    )


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestGetLowestRankedPermissionType:

    def test_admin_lowest_min(self):
        """Test that lowest rank for Garry, a global admin user, to Valerie, who
        has no assignments, is admin_global.  Set up:
        - Garry is a global admin user.
        - Valerie has no assignments
        - Expected: global admin
        """
        # Setup
        garry_user = SeedUser.get_user(garry_name)
        website_project = Project.objects.get(name=website_project_name)
        admin_project_permision_type = PermissionType.objects.get(name=admin_project)
        UserPermission.objects.create(
            user=garry_user,
            project=website_project,
            permission_type=admin_project_permision_type,
        )
        # Test
        rank = _get_lowest_ranked_permission_type(garry_name, valerie_name)
        assert rank == admin_global

    def test_team_member_lowest_rank_for_two_project_members_1(self):
        """
        Tests that lowest rank of Winona to Wally, both project members on
        the same site, is project member.  Set up:
        - Wally is a team member on website project
        - Winona is also a team member on website project
        - Expected result: project member
        """
        rank = _get_lowest_ranked_permission_type(wally_name, winona_name)
        assert rank == member_project

    def test_team_member_lowest_rank_for_two_team_members_2(self):
        """
        Tests that lowest rank of a team member (member_team) relative to a project admin
        is team member. Set up:
        - Wally is a team member on website project
        - Wanda is a project admin on website project
        - Expected result: website project
        """
        rank = _get_lowest_ranked_permission_type(wally_name, wanda_admin_project)
        assert rank == member_project

    def test_lowest_rank_blank_of_two_non_team_member(self):
        """Test that lowest rank is blank for Wally relative to Patrick,
        who are project members on different projects, is blank.  Setup:
        - Wally is a project member on Website project.
        - Patrick is a project member on People Depot project
        - Expected result: blank
        """
        rank = _get_lowest_ranked_permission_type(wally_name, patrick_practice_lead)
        assert rank == ""

    def test_two_team_members_lowest_for_multiple_user_permissions_1(self):
        """Test that lowest rank for Zani, assigned to multiple projects, relative to Winona
        who are both project members on Website project, is project member.  Setup:
        - Zani, project member of Website project and project admin on People Depot project
        - Winona, project member on Website project
        - Expected: project admin
        """
        rank = _get_lowest_ranked_permission_type(zani_name, winona_name)
        assert rank == member_project

    def test_team_member_lowest_rank_for_multiple_user_permissions_1(self):
        """
        Test that lowest rank for Zani, assigned to multiple projects and a
        project admin on Website project, relative to Winona, is project admin.  Setup:
        - Zani, project member of Website project and project admin on People Depot project
        - Winona, project member on Website project
        - Expected: project admin
        """
        rank = _get_lowest_ranked_permission_type(zani_name, patti_name)
        assert rank == admin_project
