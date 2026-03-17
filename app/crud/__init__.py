from app.crud.user import (
    create_user_crud,
    get_user_by_email_crud,
    get_user_by_id_crud,
    update_user_crud,
    deactivate_user_crud,
)
from app.crud.dep_views import (
    get_user_by_id_with_role_and_permission,
    validate_permission,
)
from app.crud.acess_rule import get_access_rule_by_id_crud, update_access_rule_crud
