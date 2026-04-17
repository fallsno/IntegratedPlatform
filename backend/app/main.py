from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path          # ← 必须导入
import importlib                   # ← 新增
import pkgutil                     # ← 新增
import app.routers as routers_pkg  # ← 新增

app = FastAPI(title="型号版本管理系统 API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传目录配置
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------- 动态导入所有路由模块 ----------
for _, module_name, _ in pkgutil.iter_modules(routers_pkg.__path__):
    try:
        module = importlib.import_module(f"app.routers.{module_name}")
        if hasattr(module, "router"):
            prefix = f"/api/{module_name}"
            app.include_router(module.router, prefix=prefix, tags=[module_name])
            print(f"✅ 已注册路由: {prefix}")
        else:
            print(f"⚠️ 模块 {module_name} 未定义 router，跳过")
    except Exception as e:
        print(f"❌ 导入模块 {module_name} 失败: {e}")

@app.get("/")
def root():
    return {"message": "Model Management System API"}