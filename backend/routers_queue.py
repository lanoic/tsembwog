from fastapi import APIRouter, Depends, HTTPException
from .deps import get_current_user
from .tasks import retrain_rego_model_task

router = APIRouter(prefix="/queue", tags=["queue"])

@router.post("/train-now")
def queue_train_now(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    res = retrain_rego_model_task.delay()
    return {"enqueued": True, "task_id": res.id}
