# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import DataError
from django.test import TestCase
# Third party
from mixer.backend.django import Mixer

#   fake argument: Randomize generated values that allows covering unexpected
# test cases.
mixer = Mixer(fake=False)


class NameAttributeTests(TestCase):
    """
    Tests for Category.name.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.category = mixer.blend('app_product.Category')
        self.category_meta = self.category._meta  # pylint: disable=protected-access
        self.name_field = self.category_meta.get_field('name')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.name_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_CharField(self):
        self.assertIsInstance(
            self.name_field,
            models.CharField
        )

    def test_attribute_has_2_as_max_length(self):
        self.assertEqual(
            self.name_field.max_length,
            2
        )

    def test_attribute_raises_if_input_pass_max_length(self):
        """
        max_length is 2.
        """
        # NOTE: I'm using PostgreSQL as database, if you are using SQLite
        # instead, it will ignore assigned max_length, and the test will not
        # pass, that's because SQLite uses TEXT to store strings.
        self.category.name = 'test'
        with self.assertRaises(DataError):
            self.category.save()

    def test_name_attribute_has_correct_choices(self):
        """
        Correct choices are
        [('ph', 'Phones'), ('ga', 'Gaming'), ('co', 'Computing')]
        """
        self.assertEqual(
            self.category_meta.get_field('name').choices,
            [('ph', 'Phones'), ('ga', 'Gaming'), ('co', 'Computing')]
        )

    def test_name_attribute_accepts_value_from_assigned_choices_only(self):
        """
        Attribute should not accept any value out of
        [('ph', 'Phones'), ('ga', 'Gaming'), ('co', 'Computing')]
        """
        self.category.name = 'xz'
        with self.assertRaises(ValidationError):
            self.category.full_clean()


class MetaClassTests(TestCase):
    """
    Tests for Category.Meta.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        category = mixer.blend('app_product.Category')
        self.category_meta = category._meta  # pylint: disable=protected-access

    def test_verbose_name_plural_is_not_assigned_to_Categorys(self):
        """
        Default is Categorys (model_name + s).
        """
        self.assertNotEqual(
            f'{self.category_meta.model_name}s',
            self.category_meta.verbose_name_plural
        )

    def test_verbose_name_plural_is_str(self):
        field_type = self.category_meta.verbose_name_plural
        self.assertIsInstance(field_type, str)

    def test_verbose_name_plural_is_assigned_to_Categories(self):
        self.assertEqual(
            self.category_meta.verbose_name_plural,
            'Categories'
        )


class __str__MethodTests(TestCase):
    """
    Tests for Category.__str__().
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.category = mixer.blend('app_product.Category')

    def test_str_will_not_return_default_value(self):
        """
        Default is Category object (1) (model_name + 'object' + model.id)
        """
        self.assertNotEqual(
            self.category.__str__(),  # pylint: disable=unnecessary-dunder-call
            f'{self.category._meta.model_name} object ({self.category.id})'\
                .capitalize()  # pylint: disable=protected-access
        )

    def test_str_will_return_Gaming_if_name_is_ga(self):
        self.category.name = 'ga'
        self.assertEqual(
            self.category.__str__(),  # pylint: disable=unnecessary-dunder-call
            'Gaming'
        )

    def test_str_will_return_Phones_if_name_is_ph(self):
        self.category.name = 'ph'
        self.assertEqual(
            self.category.__str__(),  # pylint: disable=unnecessary-dunder-call
            'Phones'
        )

    def test_str_will_return_Computing_if_name_is_co(self):
        self.category.name = 'co'
        self.assertEqual(
            self.category.__str__(),  # pylint: disable=unnecessary-dunder-call
            'Computing'
        )

    def test_str_will_return_Unknown_if_name_value_is_not_in_choices(self):
        self.category.name = 'xz'
        self.assertEqual(
            self.category.__str__(),  # pylint: disable=unnecessary-dunder-call
            'Unknown'
        )
