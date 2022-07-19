from pytest import raises

from core.models import User


def test_good_choice():
    assert User.objects.filter(is_staff=True).count() == 1


def test_bad_choice():
    with raises(User.DoesNoteExist):
        User.objects.filter(is_staff=False)
