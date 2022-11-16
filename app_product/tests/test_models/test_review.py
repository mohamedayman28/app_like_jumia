# Django
from django.test import TestCase
from django.db import models
from django.db.utils import DataError
# Local apps
from app_product.models import Product
# Third party
from mixer.backend.django import Mixer


#   fake argument: Randomize generated values that allows covering unexpected
# test cases.
mixer = Mixer(fake=False)


class ProductAttributeTests(TestCase):
    """
    Tests for Review.product.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.review = mixer.blend('app_product.Review')
        self.review_meta = self.review._meta  # pylint: disable=protected-access
        self.product_field = self.review_meta.get_field('product')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.review_meta.get_field('product')

    def test_attribute_has_relation(self):
        self.assertTrue(self.product_field.is_relation)

    def test_attribute_relation_is_ForeignKey(self):
        self.assertIsInstance(
            self.product_field,
            models.ForeignKey
        )

    def test_attribute_is_related_to_Product_model(self):
        self.assertIs(
            self.product_field.related_model,
            Product
        )

    def test_attribute_is_CASCADE_on_related_Product_deletion(self):
        # Create new Product instance.
        product = mixer.blend('app_product.Product')
        self.review.product = product
        self.review.save()
        # Delete created Product instance.
        product.delete()

        with self.assertRaises(self.review.DoesNotExist):
            self.review.refresh_from_db()


class TitleAttributeTests(TestCase):
    """
    Tests for Review.title.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.review = mixer.blend('app_product.Review')
        self.review_meta = self.review._meta  # pylint: disable=protected-access
        self.title_field = self.review_meta.get_field('title')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.title_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_CharField(self):
        self.assertIsInstance(
            self.title_field,
            models.CharField
        )

    def test_attribute_has_50_as_max_length(self):
        self.assertEqual(
            self.title_field.max_length,
            50
        )

    def test_attribute_raises_if_input_pass_max_length(self):
        """
        max_length is 50.
        """
        # NOTE: I'm using PostgreSQL as database, if you are using SQLite
        # instead, it will ignore assigned max_length, and the test will not
        # pass, that's because SQLite uses TEXT to store strings.
        self.review.title = 'test' * 13
        with self.assertRaises(DataError):
            self.review.save()


class DescriptionAttributeTests(TestCase):
    """
    Tests for Review.description.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.review = mixer.blend('app_product.Review')
        self.review_meta = self.review._meta  # pylint: disable=protected-access
        self.description_field = self.review_meta.get_field('description')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.description_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_TextField(self):
        self.assertIsInstance(
            self.description_field,
            models.TextField
        )


class RateAttributeTests(TestCase):
    """
    Tests for Review.rate.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.review = mixer.blend('app_product.Review')
        self.review_meta = self.review._meta  # pylint: disable=protected-access
        self.rate_field = self.review_meta.get_field('rate')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.rate_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_PositiveSmallIntegerField(self):
        self.assertIsInstance(
            self.rate_field,
            models.PositiveSmallIntegerField
        )


class TimestampAttributeTests(TestCase):
    """
    Tests for Review.timestamp.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.review = mixer.blend('app_product.Review')
        self.review_meta = self.review._meta  # pylint: disable=protected-access
        self.timestamp_field = self.review_meta.get_field('timestamp')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.timestamp_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_DateField(self):
        self.assertIsInstance(
            self.timestamp_field,
            models.DateField
        )

    def test_attribute_auto_now_add_is_True(self):
        self.assertTrue(self.timestamp_field.auto_now_add)


class __str__MethodTests(TestCase):
    """
    Tests for Review.__str__().
    """

    def setUp(self):
        self.review = mixer.blend('app_product.Review')

    def test_method_will_not_return_default_value(self):
        """
        Default is Review object (1) (model_name + 'object' + model.id)
        """
        self.assertNotEqual(
            self.review.__str__(),  # pylint: disable=unnecessary-dunder-call
            f'{self.review._meta.model_name} object ({self.review.id})'\
                .capitalize()  # pylint: disable=protected-access
        )

    def test_method_will_return_correct_value(self):
        timestamp = self.review.timestamp
        rate = self.review.rate
        self.assertEqual(
            self.review.__str__(),  # pylint: disable=unnecessary-dunder-call
            f'{rate} out of 5, at {timestamp}'
        )


class SaveMethodTests(TestCase):
    # def setUp(self):
    #     # NOTE: Mixer sets models.field(default) if no value assigned.
    #     self.review = mixer.blend('app_product.Review')
    #     self.review.is_cleaned = False
    #     self.review_meta = self.review._meta  # pylint: disable=protected-access
    #     self.rate_field = self.review_meta.get_field('rate')

    def test_method_will_behave_default_if_is_clean_is_True_and_input_is_greater_than_5(self):
        """
        Default is, to save any int value to the field (Review.rate).
        """
        review = mixer.blend('app_product.Review')
        # Make sure review.is_cleaned is True be able to modify review.rate.
        if review.is_cleaned is False:
            review.is_cleaned = True
        review.rate = 10
        review.save()
        self.assertEqual(
            review.rate,
            10
        )

    def test_method_will_save_rate_as_1_if_is_clean_is_False_and_input_smaller_than_1(self):
        review = mixer.blend('app_product.Review')
        # Make sure review.is_cleaned is False be able to modify review.rate.
        if review.is_cleaned is True:
            review.is_cleaned = False
        review.rate = 0
        review.save()
        self.assertEqual(
            review.rate,
            1
        )

    def test_method_will_save_rate_as_5_if_input_greater_than_5(self):
        review = mixer.blend('app_product.Review', rate=10)
        self.assertEqual(
            review.rate,
            5
        )

    def test_method_will_save_rate_as_1_if_input_is_1(self):
        review = mixer.blend('app_product.Review', rate=1)
        self.assertEqual(
            review.rate,
            1
        )

    def test_method_will_save_rate_as_2_if_input_is_2(self):
        review = mixer.blend('app_product.Review', rate=2)
        self.assertEqual(
            review.rate,
            2
        )

    def test_method_will_save_rate_as_3_if_input_is_3(self):
        review = mixer.blend('app_product.Review', rate=3)
        self.assertEqual(
            review.rate,
            3
        )

    def test_method_will_save_rate_as_4_if_input_is_4(self):
        review = mixer.blend('app_product.Review', rate=4)
        self.assertEqual(
            review.rate,
            4
        )

    def test_method_will_save_rate_as_5_if_input_is_5(self):
        review = mixer.blend('app_product.Review', rate=5)
        self.assertEqual(
            review.rate,
            5
        )
