from fastapi import HTTPException


def query_multiple_items(database, model):
    return database.query(model).all()


def query_single_item(
    database,
    model,
    identifier,
    model_name: str,
    primary_key_field: str = 'id'
):
    pk_column = getattr(model, primary_key_field)
    item = database.query(model).filter(pk_column == identifier).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    return item


def update_record(
    database,
    model,
    update_data,
    identifier: int,
    controller_name: str,
    primary_key_field: str = 'id'
):
    item = query_single_item(database, model, identifier, controller_name, primary_key_field)
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    database.commit()
    database.refresh(item)
    return item


def safe_delete_check(database, checked_controller_model, identifier: int, param_checked: str, controller_name: str,
                      checked_controller_name: str):
    column = getattr(checked_controller_model, param_checked)
    item = database.query(checked_controller_model).filter(column == identifier).first()

    if item is not None:
        primary_key_attr = f"{checked_controller_name.lower()}Id" if hasattr(item,
                                                                             f"{checked_controller_name.lower()}Id") else "id"
        item_id = getattr(item, primary_key_attr, None)

        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete {controller_name} with id {identifier} because it is referenced by {checked_controller_name} with id {item_id}. [409]"
        )


def add_and_commit(database, item):
    database.add(item)
    database.commit()
    database.refresh(item)
    return item


def delete_and_commit(database, item):
    database.delete(item)
    database.commit()
    return None
