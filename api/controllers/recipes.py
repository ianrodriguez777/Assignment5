
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        name=recipe.name,
        ingredients=recipe.ingredients
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    update_data = recipe.model_dump(exclude_unset=True)
    db_recipe.update(update_data, synchronize_session=False)
    db.commit()
    return db_recipe.first()

def delete(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    db_recipe.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
