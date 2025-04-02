from fastapi import HTTPException


def query_multiple_items(database, model):
    return database.query(model).all()

def query_single_item(database, model, identifier, controller_name: str):
    item = database.query(model).filter(model.id == identifier).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"{controller_name} with id {identifier} not found [404]")
    return item

def update_record(database, model, update_data, identifier: int, controller_name: str):
    item = query_single_item(database, model, identifier, controller_name)
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    database.commit()
    database.refresh(item)
    return item


def safe_delete_check(database, checked_controller_model, identifier: int, param_checked:str, controller_name: str, checked_controller_name: str):
    item = database.query(checked_controller_model).filter(getattr(checked_controller_model, param_checked) == identifier).first()
    if item is not None:
        raise HTTPException(status_code=409,
                            detail=f"{checked_controller_name} id {item.id} has a {controller_name} with id {identifier} assigned to it. [409]")


def add_and_commit(database, item):
    database.add(item)
    database.commit()
    database.refresh(item)
    return item

def delete_and_commit(database, item):
    database.delete(item)
    database.commit()
    return None