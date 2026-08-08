from blog.forms import CategoryAdminForm

from .base import BaseBlogTest


class CategoryAdminFormTest(BaseBlogTest):

    def test_rejects_category_depth_greater_than_3(self):
        child3 = self.create_category_depth_3()["child3"]

        form = CategoryAdminForm(
            data={
                "name": "test category",
                "treebeard_ref_node": child3.pk,
                "treebeard_position": "sorted-child",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_register_category_depth_to_3(self):
        child2 = self.create_category_depth_3()["child2"]
        
        form = CategoryAdminForm(
            data={
                "name": "test category",
                "treebeard_ref_node": child2.pk,
                "treebeard_position": "sorted-child",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertNotIn("__all__", form.errors)

    def test_register_category_as_sibling_of_category_depth_3(self):
        child3 = self.create_category_depth_3()["child3"]

        form = CategoryAdminForm(
            data={
                "name": "test category",
                "treebeard_ref_node": child3.pk,
                "treebeard_position": "sorted-sibling",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertNotIn("__all__", form.errors)
               
