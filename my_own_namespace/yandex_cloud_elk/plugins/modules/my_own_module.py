#!/usr/bin/python

# Copyright: (c) 2026, Aleksey Karamyshev <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
import os

DOCUMENTATION = '''
---
module: create_file
short_description: Create a text file with specified content
description:
  - Creates a text file on the remote host at the given path with provided content.
options:
  path:
    description:
      - Path to the file on the remote host.
    type: str
    required: true
  content:
    description:
      - Content to write to the file.
    type: str
    required: true
'''

EXAMPLES = '''
- name: Create example file
  create_file:
    path: /tmp/example.txt
    content: "Hello from Ansible!"
'''

RETURN = '''
path:
  description: Path of the created file
  type: str
  returned: always
changed:
  description: Whether the file was created or updated
  type: bool
  returned: always
'''

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    changed = False
    if module.check_mode:
        changed = not os.path.exists(path)
    else:
        try:
            old_content = ""
            if os.path.exists(path):
                with open(path, 'r') as f:
                    old_content = f.read()
            if old_content != content:
                with open(path, 'w') as f:
                    f.write(content)
                changed = True
        except IOError as e:
            module.fail_json(msg=f"Failed to write file: {str(e)}")

    module.exit_json(
        changed=changed,
        path=path
    )

if __name__ == '__main__':
    run_module()
