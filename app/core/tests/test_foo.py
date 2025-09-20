import pytest
from core.models import Project
from core.tests.utils.load_data import load_data  # adjust path if needed
from core.tests.utils.seed_constants import website_project_name, people_depot_project

@pytest.mark.load_user_data_required
@pytest.mark.django_db
def test_project_count():
    # At this point, your autouse fixture should already have run load_data()
    projects = Project.objects.all()
    assert projects.count() == 2

    # Optional: verify project names
    names = {p.name for p in projects}
    assert names == {website_project_name, people_depot_project}
