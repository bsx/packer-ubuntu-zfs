#!/usr/bin/env python3
# -*- coding: utf8 -*-

import boto3
import json
import subprocess

region = subprocess.check_output(['/usr/bin/ec2metadata', '--availability-zone'], encoding='utf8').strip()[:-1]

ec2 = boto3.resource('ec2', region_name=region)

instance_id = subprocess.check_output(['/usr/bin/ec2metadata', '--instance-id'], encoding='utf8').strip()

instance = ec2.Instance(instance_id)

root_device = instance.root_device_name

volume_id = ''

for device in instance.block_device_mappings:
    if device['DeviceName'] != root_device:
        volume_id = device['Ebs']['VolumeId'].replace('-', '')

nvme_mapping = json.loads(subprocess.check_output(['/usr/sbin/nvme', 'list', '-o', 'json'], encoding='utf8'))

for device in nvme_mapping['Devices']:
    if device['SerialNumber'] == volume_id:
        print(device['DevicePath'])
