"""Endpoint TEMPORAIRE d'import des challenges CTF. À SUPPRIMER après usage."""
import os
import subprocess
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

router = APIRouter(prefix="/_import_ctf", tags=["_import_ctf"])

SECRET = os.environ.get("IMPORT_CTF_SECRET", "blackhawk-ctf-import-2026")


class ImportRequest(BaseModel):
    mode: str = "dry-run"  # "dry-run" ou "apply"
    publish: bool = True


def _run_import(mode: str, publish: bool):
    cmd = ["python", "-m", "scripts.import_ctf_bulk", f"--{mode}"]
    if not publish and mode == "apply":
        cmd.append("--no-publish")
    log_path = "/tmp/import_ctf.log"
    with open(log_path, "w") as f:
        subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)


@router.post("/run")
async def import_ctf(secret: str, background: BackgroundTasks, payload: ImportRequest):
    if secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    background.add_task(_run_import, payload.mode, payload.publish)
    return {"status": "started", "mode": payload.mode, "publish": payload.publish}


@router.get("/logs")
async def get_logs(secret: str):
    if secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    log_path = "/tmp/import_ctf.log"
    if not os.path.exists(log_path):
        return {"logs": "Aucun log disponible."}
    with open(log_path, "r") as f:
        return {"logs": f.read()[-10000:]}
