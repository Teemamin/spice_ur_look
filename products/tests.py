from django.test import TestCase, Client
from .forms import AddProductForm, ReviewForm
from .models import Product, Review, Wishlist
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.models import User



# Create your tests here.


class TestProductForms(TestCase):
    def test_form_isvalid(self):
        form_data = {
            'name': 'item',
            'gender': "man",
            'description': 'test',
            'price': 22.99,
            'quantity': 1,
        }
        form = AddProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_required_fields(self):
        form_data = {
            'name': 'item',
            'gender': "man",
            'quantity': 1,
        }
        form = AddProductForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestReviewForms(TestCase):
    def test_form_valid(self):
        form_data = {
            'review': 'test fields',
            'rate': 2,
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rate_required(self):
        form_data = {
            'review': 'test fields',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestProductViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        self.products_url = reverse('products')

    def test_all_product(self):
        response = self.client.get(self.products_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_single_product_path(self):
        product = Product.objects.create(
            name='testing edit',
            gender='man',
            description='test desc',
            price=20.2,
            quantity=1
        )
        response = self.client.get(f'/products/{product.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/single_product.html')

    def test_add_product(self):
        form = AddProductForm({
            'name': 'added',
            'gender': 'man',
            'description': 'test desc',
            'price': 20.2,
            'quantity': 1,
        })
        self.client.post('/add_product/')
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        form.save()
        new_product = get_object_or_404(Product, name='added')
        self.assertTrue(new_product)

    def test_revise_product(self):
        form = AddProductForm({
            'name': 'edit',
            'gender': 'woman',
            'description': 'test edit',
            'price': 40.2,
            'quantity': 1,
        })
        self.client.post('/revise/')
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        form.save()
        updated_product = get_object_or_404(Product, name='edit')
        self.assertTrue(updated_product)
        response = self.client.get(
            f'/products/{updated_product.id}/', follow=True
        )
        self.assertEqual(response.status_code, 200)
        response.context['product']
        self.assertTemplateUsed(
            response, 'products/single_product.html'
        )

    def test_can_delete_product(self):
        product = Product.objects.create(
            name='testing delete',
            gender='man',
            description='test delete',
            price=20.2,
            quantity=1
        )
        response = self.client.get(f'/delete_product/{product.id}/')
        product.delete()
        self.assertEqual(response.status_code, 404)
        existing_item = Product.objects.filter(id=product.id)
        self.assertEqual(len(existing_item), 0)

    # def test_product_review(self):
    #     product = Product.objects.create(
    #         name='testing review',
    #         gender='man',
    #         description='test delete',
    #         price=20.2,
    #         quantity=1
    #     )
    #     product_obj = Product.objects.get(pk=product.id)
    #     form = ReviewForm({
    #         'rate': 2,
    #     })
    #     response = self.client.post(f'products/add_review/{product_obj.id}/')
    #     form.product = product_obj
    #     form.user = self.user
    #     self.assertTrue(form.is_valid())
    #     self.assertTrue(form.save())
    #     form.save()
    #     self.assertRedirects(response, f'/products/{product_obj.id}/', follow=True)

    def test_wishlist_view(self):
        product = Product.objects.create(
            name='testing wishlist',
            gender='man',
            description='test wishlist',
            price=20.2,
            quantity=1
        )

        Wishlist.objects.create(
            user_id=self.user.pk,
            wished_product_id=product.id
        )
        wishlist = Wishlist.objects.filter(user_id=self.user.pk)
        self.assertTrue(wishlist)
        response = self.client.get(
            '/products/wishlist_view/', follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_call_view_deny_anonymous(self):
        response = self.client.get('/products/wishlist_view/', follow=True)
        self.assertRedirects(
            response, '/accounts/login/?next=/products/wishlist_view/'
        )