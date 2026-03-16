from app.crud.user import (
    create_user_crud,
    get_user_by_email_crud,
    get_user_by_id_crud,
    update_user_crud,
    deactivate_user_crud,
)
from app.crud.dep_views import (
    get_user_by_id_with_role_and_permission,
    check_read_permission_for_user,
    all_read_permission_checker,
    check_update_permission_for_user,
)
