import allure
import pytest

import helpers
from element_objects.header import HeaderElement
from page_objects.catalog_page import CatalogPage
from page_objects.main_page import MainPage
from page_objects.registration_page import RegistrationPage


@allure.title("Регистрация нового пользователя")
def test_registration_new_user(browser, customer_deletion, url):
    user_information = helpers.user_registration_information()
    user_email = user_information[2]

    customer_deletion.append(
        user_email
    )  # передаем в фикстуру значение email для удаления

    registration_url = url + "/index.php?route=account/register"

    registration_page = RegistrationPage(browser, url=registration_url)
    registration_page.open_page()
    registration_page.registration_add_user(*user_information)
    assert registration_page.wait_title("Your Account Has Been Created!")


@allure.title("Тест добавления продукта в корзину с главной страницы")
def test_main_page_add_to_cart(browser, url):
    main_page = MainPage(browser, url)

    main_page.open_page()
    text_added_product = main_page.main_page_get_description_product()
    text_product_in_cart = main_page.main_page_add_product_to_cart()

    assert text_product_in_cart == text_added_product, (
        f"{text_product_in_cart} should be {text_added_product}"
    )


@allure.title("Тест изменения цены при изменении валюты с главной страницы")
def test_main_page_change_currency(browser, url):
    main_page = MainPage(browser, url)

    main_page.open_page()
    first_price = main_page.main_get_price()
    main_page.main_change_currency()
    second_price = main_page.main_get_price()
    assert first_price != second_price, (
        f"price should be changed, initial price {first_price}, price after changing {second_price}"
    )


@allure.title("Тест изменения цены при изменении валюты на странице каталога")
def test_catalog_page_change_currency(browser, url):
    catalog_url = url + "/catalog/desktops"
    catalog_page = CatalogPage(browser, url=catalog_url)

    catalog_page.open_page()
    first_price = catalog_page.catalog_get_price()
    catalog_page.catalog_change_currency()
    second_price = catalog_page.catalog_get_price()
    assert first_price != second_price, (
        f"price should be changed, initial price {first_price}, price after changing {second_price}"
    )


@allure.title("Тест переключение валют из верхнего меню opencart")
def test_change_currency(browser, url):
    header_element = HeaderElement(browser, url)
    header_element.open_page()
    assert header_element.header_change_currency_eur() == "€", (
        f"{header_element.header_change_currency_eur()} should be €"
    )
    assert header_element.header_change_currency_gbp() == "£", (
        f"{header_element.header_change_currency_gbp()} should be £"
    )
    assert header_element.header_change_currency_usd() == "$", (
        f"{header_element.header_change_currency_usd()} should be $"
    )
