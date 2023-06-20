from typing import Any

from fastapi import APIRouter, BackgroundTasks, Request

from app import schemas
from app.chain.webhook import WebhookChain
from app.core.config import settings

router = APIRouter()


async def start_webhook_chain(body: Any, form: Any, args: Any):
    """
    启动链式任务
    """
    WebhookChain().message(body=body, form=form, args=args)


@router.post("/", summary="Webhook消息响应", response_model=schemas.Response)
async def webhook_message(background_tasks: BackgroundTasks,
                          token: str, request: Request) -> Any:
    """
    Webhook响应
    """
    if token != settings.API_TOKEN:
        return schemas.Response(success=False, message="token认证不通过")
    body = await request.body()
    form = await request.form()
    args = request.query_params
    background_tasks.add_task(start_webhook_chain, body, form, args)
    return schemas.Response(success=True)
