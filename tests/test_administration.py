import allure
import pytest

from page_objects.administration_page import AdministrationPage
from page_objects.administration_products_page import ProductsPage


@allure.title("Страница 'Administration'. Тест логин и выход из аккаунта")
def test_administration_login_logout(browser, url):
    administration_url = url + "/administration"
    administration_page = AdministrationPage(browser, url=administration_url)
    administration_page.open_page()
    assert administration_page.administration_login(), (
        f"login should be successful - logout button should be present"
    )

    assert administration_page.administration_logout(), (
        f"Expected action: after logout - go to Administration page"
    )


test_product = "test_1"


@allure.title("Страница 'Administration'. Тест добавление нового продукта")
@pytest.mark.order(1)
# @pytest.mark.dependency()
def test_administration_add_new_product(browser, product_creation, url):
    administration_url = url + "/administration"
    administration_page = AdministrationPage(browser, url=administration_url)
    administration_page.open_page()
    administration_page.administration_login()
    administration_page.administration_go_to_product_page()

    products = ProductsPage(browser, url)
    assert "Add Product" in products.products_click_add_new_item(), (
        f"'Add Product' form should be shown"
    )

    products.products_add_new_product(test_product)

    administration_page.administration_go_to_product_page()

    assert test_product in products.products_find_by_name(test_product), (
        f"{test_product} product can be founded"
    )


@allure.title("Страница 'Administration'. Тест удаление добавленного продукта")
@pytest.mark.order(2)
# @pytest.mark.dependency(depends=["test_administration_add_new_product"])
def test_administration_delete_product(browser, product_deletion, url):
    administration_url = url + "/administration"
    administration_page = AdministrationPage(browser, url=administration_url)
    administration_page.open_page()
    administration_page.administration_login()
    administration_page.administration_go_to_product_page()

    products = ProductsPage(browser, url)
    products.products_find_by_name(test_product)
    products.products_select_check_box()
    assert products.products_delete_product() == "No results!"
