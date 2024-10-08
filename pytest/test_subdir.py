# Copyright (c) 2023 VMware, Inc.  All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the “License”); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an “AS IS” BASIS, without warranties or
# conditions of any kind, EITHER EXPRESS OR IMPLIED.  See the License for the
# specific language governing permissions and limitations under the License.

import glob
import os
import pytest
import shutil
import subprocess
import yaml
import xmltodict


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OVA_COMPOSE = os.path.join(THIS_DIR, "..", "ova-compose", "ova-compose.py")

VMDK_CONVERT=os.path.join(THIS_DIR, "..", "build", "vmdk", "vmdk-convert")

CONFIG_DIR=os.path.join(THIS_DIR, "configs")

WORK_DIR=os.path.join(os.getcwd(), "pytest-configs")
SUB_DIR=os.path.join(WORK_DIR, "subdir")


@pytest.mark.parametrize("setup_test", [SUB_DIR], indirect=True)
def test_subdir(setup_test):
    in_yaml = os.path.join(CONFIG_DIR, "basic_param.yaml")

    basename = os.path.basename(in_yaml.rsplit(".", 1)[0])
    out_ovf = os.path.join(WORK_DIR, f"{basename}.ovf")

    process = subprocess.run([OVA_COMPOSE, "-i", in_yaml, "-o", out_ovf, "--param", f"rootdisk={SUB_DIR}/dummy.vmdk", "--vmdk-convert", VMDK_CONVERT], cwd=WORK_DIR)
    assert process.returncode == 0
