# Django
from django.test import TestCase
from django.db import models
from django.db.utils import DataError
# Local apps
from app_product.models import Brand
# Third party
from mixer.backend.django import Mixer


#   fake argument: Randomize generated values that allows covering unexpected
# test cases.
mixer = Mixer(fake=False)


class BrandAttributeTests(TestCase):
    """
    Tests for Product.brand.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.product = mixer.blend('app_product.product')
        self.product_meta = self.product._meta  # pylint: disable=protected-access
        self.brand_field = self.product_meta.get_field('brand')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.brand_field  # pylint: disable=pointless-statement

    def test_attribute_has_relation(self):
        self.assertTrue(self.brand_field.is_relation)

    def test_attribute_relation_is_ForeignKey(self):
        self.assertIsInstance(
            self.brand_field,
            models.ForeignKey
        )

    def test_attribute_is_related_to_Brand_model(self):
        self.assertIs(
            self.brand_field.related_model,
            Brand
        )

    def test_attribute_set_to_null_on_related_Brand_deletion(self):
        # Create new Brand instance.
        brand = mixer.blend('app_product.Brand')
        self.product.brand = brand
        self.product.save()
        # Delete created Brand instance.
        brand.delete()
        self.product.refresh_from_db()
        self.assertIsNone(self.product.brand)


class TitleAttributeTests(TestCase):
    """
    Tests for Product.title.
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.product = mixer.blend('app_product.Product')
        self.product_meta = self.product._meta  # pylint: disable=protected-access
        self.product_field = self.product_meta.get_field('title')

    def test_attribute_is_created(self):
        """
        If no attribute, FieldDoesNotExist will raise by default.
        """
        self.product_field  # pylint: disable=pointless-statement

    def test_attribute_is_assigned_to_CharField(self):
        self.assertIsInstance(
            self.product_field,
            models.CharField
        )

    def test_attribute_has_100_as_max_length(self):
        self.assertEqual(
            self.product_meta.get_field('title').max_length,
            100
        )

    def test_attribute_raises_if_input_pass_max_length(self):
        """
        max_length is 100.
        """
        # NOTE: I'm using PostgreSQL as database, if you are using SQLite
        # instead, it will ignore assigned max_length, and the test will not
        # pass, that's because SQLite uses TEXT to store strings.
        self.product.title = 'tests' * 21
        with self.assertRaises(DataError):
            self.product.save()


class __str__MethodTests(TestCase):
    """
    Tests for Product.__str__().
    """

    def setUp(self):
        # NOTE: Mixer sets models.field(default) if no value assigned.
        self.product = mixer.blend('app_product.Product')

    def test_method_will_not_return_default_value(self):
        """
        Default is Product object (1) (model_name + 'object' + model.id)
        """
        self.assertNotEqual(
            self.product.__str__(),  # pylint: disable=unnecessary-dunder-call
            f'{self.product._meta.model_name} object ({self.product.id})'\
                .capitalize()  # pylint: disable=protected-access
        )

    def test_method_will_return_title(self):
        text = 'title'
        self.product.title = text
        self.assertEqual(
            self.product.__str__(),  # pylint: disable=unnecessary-dunder-call
            text.capitalize()
        )

    def test_method_will_return_title_sliced_by_20(self):
        text = 'title title title...extra'[:20]
        self.product.title = text
        self.assertEqual(
            self.product.__str__(),  # pylint: disable=unnecessary-dunder-call
            text.capitalize()
        )


class GetCountTotalReviewsMethodTests(TestCase):
    """
    Tests for Product.get_count_total_reviews().
    """

    def setUp(self):
        # Assigned title argument to differ this product instance from mixer product
        # instance.
        self.product = mixer.blend('app_product.product', title='test')

    def test_method_will_return_int(self):
        self.assertIsInstance(
            self.product.get_count_total_reviews(),
            int
        )

    def test_method_will_return_correct_number(self):
        """
        Correct number is 6.
        """
        reviews = mixer.cycle(6).blend(
            'app_product.Review', product=self.product
        )
        # Calling save() is a must to update the test temporary database.
        for r in reviews:
            r.save()

        self.assertEqual(
            self.product.get_count_total_reviews(),
            6
        )


class GetReviewPercentageMethodTest(TestCase):
    """
    Tests for Product.get_review_percentage().
    """

    def setUp(self):
        # Assigned title argument to differ this product instance from mixer product
        # instance.
        self.product = mixer.blend('app_product.product', title='test')

    def test_method_will_return_int(self):
        self.assertIsInstance(
            self.product.get_review_percentage(),
            int
        )

    def test_method_will_return_correct_number(self):
        """
        Correct number is 1.5.
        """
        # NOTE: Refer to test_rate_percentage_explain image for better
        # understanding, along with rate_percentage_example image.

        rate_1 = mixer.cycle(26).blend(
            'app_product.Review', product=self.product, rate=1
        )
        for r in rate_1:
            r.save()

        rate_2 = mixer.cycle(6).blend(
            'app_product.Review', product=self.product, rate=2
        )
        for r in rate_2:
            r.save()

        rate_3 = mixer.cycle(34).blend(
            'app_product.Review', product=self.product, rate=3
        )
        for r in rate_3:
            r.save()

        rate_4 = mixer.cycle(70).blend(
            'app_product.Review', product=self.product, rate=4
        )
        for r in rate_4:
            r.save()

        rate_5 = mixer.cycle(296).blend(
            'app_product.Review', product=self.product, rate=5
        )
        for r in rate_5:
            r.save()

        self.assertEqual(
            self.product.get_review_percentage(),
            4.4
        )
