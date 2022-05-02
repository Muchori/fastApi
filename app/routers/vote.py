from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2


router = APIRouter(
  prefix="/vote",
  tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(
  vote: schemas.VoteResponse, 
  db: Session = Depends(database.get_db), 
  current_user: str = Depends(oauth2.get_current_user)):

  ## checking if post exists first
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

  ## vote query to check for vote in db
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()
  
  if(vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Cannot perform the action again') ## checking if vote has been sent in the db
    new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
    db.add(new_vote) ## adds vote to the db
    db.commit()

    return {
      "message": "vote success"
    }

  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
    vote_query.delete(synchronize_session=False) ## deleting vote in the db
    db.commit()

    return {
      "message": "vote deleted successfully"
    }

