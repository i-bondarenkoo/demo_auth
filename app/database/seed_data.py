from app.models.user import User
from app.models.role import Role
from app.models.business_element import BusinessElement
from app.models.access_role import AccessRole
from app.utils.helpers import hash_passwd

from app.database.db_constructor import db_constructor
import asyncio


async def seed_data():
    async with db_constructor.session_factory() as session:
        admin = Role(name="admin")
        user = Role(name="user")
        manager = Role(name="manager")
        session.add_all(
            [
                admin,
                user,
                manager,
            ]
        )
        await session.flush()

        john = User(
            email="john@mail.ru",
            first_name="John",
            last_name="Backer",
            password_hash=hash_passwd("secret123"),
            role_id=admin.id,
        )
        margaret = User(
            email="margo@mail.ru",
            first_name="Margo",
            last_name="White",
            password_hash=hash_passwd("qwerty443"),
            role_id=manager.id,
        )
        andy = User(
            email="andy@mail.ru",
            first_name="Andy",
            last_name="Orton",
            password_hash=hash_passwd("supersecret21"),
            role_id=manager.id,
            is_active=False,
        )
        sofia = User(
            email="sofia@mail.ru",
            first_name="Sofia",
            last_name="Bradley",
            password_hash=hash_passwd("qqq21"),
            role_id=user.id,
        )
        session.add_all(
            [
                andy,
                margaret,
                john,
                sofia,
            ]
        )
        await session.flush()

        products_element = BusinessElement(name="products")
        category_element = BusinessElement(name="category")
        session.add_all(
            [
                products_element,
                category_element,
            ]
        )
        await session.flush()

        rule1 = AccessRole(
            role_id=admin.id,
            element_id=products_element.id,
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )
        rule2 = AccessRole(
            role_id=manager.id,
            element_id=products_element.id,
            read_permission=True,
            create_permission=True,
            update_permission=True,
            delete_permission=True,
        )
        rule3 = AccessRole(
            role_id=user.id,
            element_id=category_element.id,
            read_permission=True,
            create_permission=True,
            update_permission=True,
            delete_all_permission=True,
        )
        rule4 = AccessRole(
            role_id=manager.id,
            element_id=category_element.id,
            read_permission=True,
            create_permission=True,
        )
        rule5 = AccessRole(
            role_id=admin.id,
            element_id=category_element.id,
            read_permission=True,
            create_permission=True,
            update_permission=True,
            delete_permission=True,
        )
        session.add_all(
            [
                rule1,
                rule2,
                rule3,
                rule4,
                rule5,
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
