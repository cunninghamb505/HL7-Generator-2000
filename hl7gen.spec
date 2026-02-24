# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for HL7 Generator 2000."""

import os
from pathlib import Path

block_cipher = None
ROOT = os.path.abspath(".")

# All data directories that must ship with the frozen app.
# Each tuple is (source_path, dest_relative_to_bundle_root).
datas = [
    (os.path.join(ROOT, "src", "templates"), os.path.join("src", "templates")),
    (os.path.join(ROOT, "static"), "static"),
    (os.path.join(ROOT, "config"), "config"),
    (os.path.join(ROOT, ".env.example"), "."),
]

# Dynamically-loaded modules that PyInstaller cannot detect via static analysis.
hiddenimports = [
    # --- message type generators ---
    "src.generators.message_types.adt",
    "src.generators.message_types.orm",
    "src.generators.message_types.oru",
    "src.generators.message_types.rde",
    "src.generators.message_types.rds",
    "src.generators.message_types.mdm",
    "src.generators.message_types.dft",
    "src.generators.message_types.vxu",
    "src.generators.message_types.bar",
    "src.generators.message_types.siu",
    "src.generators.message_types.mfn",
    "src.generators.message_types.ack",
    # --- segment builders ---
    "src.generators.segment_builders.msh",
    "src.generators.segment_builders.pid",
    "src.generators.segment_builders.pv1",
    "src.generators.segment_builders.evn",
    "src.generators.segment_builders.nk1",
    "src.generators.segment_builders.al1",
    "src.generators.segment_builders.dg1",
    "src.generators.segment_builders.gt1",
    "src.generators.segment_builders.orc",
    "src.generators.segment_builders.obr",
    "src.generators.segment_builders.obx",
    "src.generators.segment_builders.pv2",
    "src.generators.segment_builders.mrg",
    "src.generators.segment_builders.rxe",
    "src.generators.segment_builders.rxd",
    "src.generators.segment_builders.rxa",
    "src.generators.segment_builders.rxg",
    "src.generators.segment_builders.txa",
    "src.generators.segment_builders.ft1",
    "src.generators.segment_builders.sch",
    "src.generators.segment_builders.mfi",
    "src.generators.segment_builders.mfe",
    "src.generators.segment_builders.aig",
    "src.generators.segment_builders.ail",
    "src.generators.segment_builders.aip",
    "src.generators.segment_builders.in1",
    "src.generators.segment_builders.in2",
    "src.generators.segment_builders.in3",
    # --- workflow step handlers ---
    "src.workflows.step_handlers.admission",
    "src.workflows.step_handlers.discharge",
    "src.workflows.step_handlers.transfer",
    "src.workflows.step_handlers.lab_order",
    "src.workflows.step_handlers.lab_result",
    "src.workflows.step_handlers.pharmacy_order",
    "src.workflows.step_handlers.pharmacy_dispense",
    "src.workflows.step_handlers.vaccination",
    "src.workflows.step_handlers.document",
    "src.workflows.step_handlers.billing",
    "src.workflows.step_handlers.bar",
    "src.workflows.step_handlers.scheduling",
    "src.workflows.step_handlers.master_file",
    # --- validators ---
    "src.validators.rules",
    "src.validators.message_validator",
    # --- z-segment engine ---
    "src.generators.z_segment_engine",
    # --- web routes (imported dynamically in create_app) ---
    "src.web.routes.control",
    "src.web.routes.dashboard",
    "src.web.routes.destinations",
    "src.web.routes.messages",
    "src.web.routes.metrics",
    "src.web.routes.workflows",
    "src.web.routes.patients",
    # --- third-party libs that PyInstaller sometimes misses ---
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "multipart",
    "pydantic_settings",
    "hl7apy",
    "hl7apy.core",
    "hl7apy.consts",
    "hl7apy.parser",
    "aiofiles",
    "structlog",
    "rich",
]

a = Analysis(
    [os.path.join(ROOT, "src", "__main__.py")],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "PIL",
    ],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="hl7gen",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="hl7gen",
)
