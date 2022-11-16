# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import DataError
from django.test import TestCase
# Local apps
from app_product.models import Category
# Third party
from mixer.backend.django import Mixer

#   fake argument: Randomize generated values that allows covering unexpected
# test cases.
mixer = Mixer(fake=False)


class CategoryAttributeTests(TestCase):
    """
    Tests for Brand.category.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.brand = mixer.blend('app_product.Brand')
        self.brand_meta = self.brand._meta  # pylint: disable=protected-access
        self.category_field = self.brand_meta.get_field('category')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.category_field  # pylint: disable=pointless-statement

    def test_attribute_has_relation(self):
        self.assertTrue(self.category_field.is_relation)

    def test_attribute_relation_is_ForeignKey(self):
        self.assertIsInstance(
            self.category_field,
            models.ForeignKey
        )

    def test_attribute_is_related_to_Category_model(self):
        self.assertIs(
            self.category_field.related_model,
            Category
        )

    def test_attribute_set_to_null_on_related_Category_deletion(self):
        # Create new brand instance.
        category = mixer.blend('app_product.Category')
        self.brand.category = category
        self.brand.save()
        # Delete created Brand instance.
        category.delete()
        self.brand.refresh_from_db()
        self.assertIsNone(self.brand.category)


class NameAttributeTests(TestCase):
    """
    Tests for Brand.name.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.brand = mixer.blend('app_product.Brand')
        self.brand_meta = self.brand._meta  # pylint: disable=protected-access
        self.brand_field = self.brand_meta.get_field('name')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.brand_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_CharField(self):
        self.assertIsInstance(
            self.brand_field,
            models.CharField
        )

    def test_attribute_has_2_as_max_length(self):
        self.assertEqual(
            self.brand_field.max_length,
            2
        )

    def test_attribute_raises_if_input_pass_max_length(self):
        """
        max_length is 2.
        """
        # NOTE: I'm using PostgreSQL as database, if you are using SQLite
        # instead, it will ignore assigned max_length, and the test will not
        # pass, that's because SQLite uses TEXT to store strings.
        self.brand.name = 'test'
        with self.assertRaises(DataError):
            self.brand.save()

    def test_attribute_has_correct_choices(self):
        """
        Correct choices are
        [
            ('sa', 'SAMSUNG'), ('op', 'OPPO'), ('ko', 'KONAMI'),
            ('so', 'SONY'), ('de', 'DELL'), ('hp', 'HP')
        ]
        """
        self.assertEqual(
            self.brand_meta.get_field('name').choices,
            [
                ('sa', 'SAMSUNG'), ('op', 'OPPO'), ('ko', 'KONAMI'),
                ('so', 'SONY'), ('de', 'DELL'), ('hp', 'HP')
            ]
        )

    def test_attribute_accepts_value_from_assigned_choices_only(self):
        """
        Attribute should not accept any value out of
        [
            ('sa', 'SAMSUNG'), ('op', 'OPPO'), ('ko', 'KONAMI'),
            ('so', 'SONY'), ('de', 'DELL'), ('hp', 'HP')
        ]
        """
        self.brand.name = 'xz'
        with self.assertRaises(ValidationError):
            self.brand.full_clean()


class __str__MethodTests(TestCase):
    """
    Tests for Brand.__str__().
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.brand = mixer.blend('app_product.Brand')

    def test_method_will_not_return_default_value(self):
        """
        Default is Brand object (1) (model_name + 'object' + model.id)
        """
        self.assertNotEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            f'{self.brand._meta.model_name} object ({self.brand.id})'\
                .capitalize()  # pylint: disable=protected-access
        )

    def test_method_will_return_SAMSUNG_if_name_is_sa(self):
        self.brand.name = 'sa'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'SAMSUNG'
        )

    def test_method_will_return_OPPO_if_name_is_op(self):
        self.brand.name = 'op'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'OPPO'
        )

    def test_method_will_return_KONAMI_if_name_is_co(self):
        self.brand.name = 'ko'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'KONAMI'
        )

    def test_method_will_return_SONY_if_name_is_so(self):
        self.brand.name = 'so'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'SONY'
        )

    def test_method_will_return_DELL_if_name_is_de(self):
        self.brand.name = 'de'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'DELL'
        )

    def test_method_will_return_HP_if_name_is_hp(self):
        self.brand.name = 'hp'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'HP'
        )

    def test_method_will_return_Unknown_if_name_value_is_not_in_choices(self):
        self.brand.name = 'xz'
        self.assertEqual(
            self.brand.__str__(),  # pylint: disable=unnecessary-dunder-call
            'Unknown'
        )
