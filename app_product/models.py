from django.db import models


class Category(models.Model):
    # Explain relations from category (Category model) to the product review
    # (Review model).
    # Category has multi Brand
    #     - Relation: (Category) 1-n (Brand)
    # Brand has multi Product
    #     - Relation: (Brand) 1-n (Product)
    # Product has multi Review
    #     - Relation: (Product) 1-n (Review)

    PHONES = 'ph'
    GAMING = 'ga'
    COMPUTING = 'co'
    CATEGORIES = [
        (PHONES, 'Phones'),
        (GAMING, 'Gaming'),
        (COMPUTING, 'Computing')
    ]
    name = models.CharField(max_length=2, choices=CATEGORIES)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Return readable name instead of the database name, .e.g ph to Phone.
        """
        categories = enumerate(self.CATEGORIES)
        for count, item in categories:  # pylint: disable=unused-variable
            if self.name == item[0]:
                return item[1]
            else:
                continue
        return 'Unknown'


class Brand(models.Model):
    SAMSUNG = 'sa'
    OPPO = 'op'
    KONAMI = 'ko'
    SONY = 'so'
    DELL = 'de'
    HP = 'hp'
    BRANDS = [
        (SAMSUNG, 'SAMSUNG'),
        (OPPO, 'OPPO'),
        (KONAMI, 'KONAMI'),
        (SONY, 'SONY'),
        (DELL, 'DELL'),
        (HP, 'HP'),
    ]
    # Relation attribute
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    # Regular Attributes
    name = models.CharField(max_length=2, choices=BRANDS)

    def __str__(self):
        """
        Return readable name instead of the database name, .e.g ph to Phone.
        """
        brands = enumerate(self.BRANDS)
        for count, item in brands:  # pylint: disable=unused-variable
            if self.name == item[0]:
                return item[1]
            else:
                continue
        return 'Unknown'


class Product(models.Model):
    # Relation attributes
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    # Regular attributes
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='app_product/images')

    def __str__(self):
        return f'{self.title}'[:20].capitalize()

    def get_count_total_reviews(self):
        """
        Count total reviews related to product.
        """
        return self.review_set.count()

    def get_review_percentage(self):
        """
        Return percentage of total review rate related to the product,
        presented by stars.

        NOTE: Google "How to calculate the percentage", and refer to
        rate_percentage_explain.png image included with the files.
        """

        # Get total rate
        total_rate = self.review_set.count() * 5

        # Get addition of different rate
        # NOTE: The multiplied number is (How many stars).
        rate_1 = self.review_set.filter(rate__exact=1).count() * 1
        rate_2 = self.review_set.filter(rate__exact=2).count() * 2
        rate_3 = self.review_set.filter(rate__exact=3).count() * 3
        rate_4 = self.review_set.filter(rate__exact=4).count() * 4
        rate_5 = self.review_set.filter(rate__exact=5).count() * 5
        different_rate = rate_1 + rate_2 + rate_3 + rate_4 + rate_5

        # Convert to percentage
        try:
            decimal = different_rate / total_rate
        except ZeroDivisionError:
            return 0
        percentage = decimal * 100

        # Convert to stars
        stars = percentage / 20

        return round(stars, 1)


class Review(models.Model):
    """
    Reviews by users who purchased the product.
    """
    # Relation Attribute
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    # Regular attributes
    title = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.PositiveSmallIntegerField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.rate} out of 5, at {self.timestamp}'

    # Trigger for full_clean() in case of calling save() directly, for example
    # using Django shell.
    is_cleaned = False

    def clean(self, *args, **kwargs):
        """
        Make sure the rate input will always fall between 1 and 5:
            If, input smaller than 1 save rate field as 1,
            if, input greater than 5 save rate field as 5,
            else, save the input.
        """
        # is_cleaned must be True to pass the if condition within save().
        self.is_cleaned = True
        # None is set by PositiveSmallIntegerField if value is smaller than 0.
        if self.rate is None or self.rate < 1:
            self.rate = 1
        elif self.rate > 5:
            self.rate = 5
        else:
            super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Clean fields in case of calling save() directly, for example using
        Django shell.
        """
        # Ignore full_clean() call on values in range 1 and 5.
        if self.is_cleaned is False and (self.rate < 1 or self.rate > 5):
            self.full_clean()
        else:
            super().save(*args, **kwargs)
