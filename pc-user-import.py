from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'import_file_name',
    type=str,
    help='Import (CSV) file name for the Users.')
parser.add_argument(
    'role_name',
    type=str,
    help='Role to assign to the imported Users.')
args = parser.parse_args()

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args)
pc_settings = pc_lib_general.pc_settings_get(args)
pc_api.configure(pc_settings)

# --Main-- #

print('API - Getting the current list of Users ...', end='')
user_list_current = pc_api.user_list_get_v2()
print(' done.')
print()

user_list_to_import = pc_lib_general.pc_file_load_csv_text(args.import_file_name)

print('API - Getting the Roles list ...', end='')
user_role_list = pc_api.user_role_list_get()
print(' done.')

user_role_id = None
for user_role in user_role_list:
    if user_role['name'].lower() == args.role_name.lower():
        user_role_id = user_role['id']
        break
if user_role_id is None:
    pc_lib_general.pc_exit_error(400, 'Role not found. Please verify the Role name.')

users_duplicate_current_count = 0
users_duplicate_file_count = 0
user_list_to_import_validated = []

for user_new in user_list_to_import:
    user_exists = False
    # Remove duplicates from the import file list.
    for user_to_import in user_list_to_import_validated:
        if user_to_import['email'].lower() == user_new['email'].lower():
            users_duplicate_file_count = users_duplicate_file_count + 1
            user_exists = True
            break
    if not user_exists:
        # Remove duplicates based upon the current user list.
        for user_current in user_list_current:
            if user_new['email'].lower() == user_current['email'].lower():
                users_duplicate_current_count = users_duplicate_current_count + 1
                user_exists = True
                break
        if not user_exists:
            user_validated = {}
            user_validated['email']     = user_new['email']
            user_validated['firstName'] = user_new['firstName']
            user_validated['lastName']  = user_new['lastName']
            user_validated['timeZone']  = 'America/Los_Angeles'
            user_validated['roleId']    = user_role_id
            user_list_to_import_validated.append(user_validated)

print('Users to add: %s' % len(user_list_to_import_validated))
print('Users skipped (duplicates in Prisma Cloud): %s' % users_duplicate_current_count)
print('Users skipped (duplicates in Import File): %s' % users_duplicate_file_count)

print('API - Creating Users ...')
for new_user in user_list_to_import_validated:
    print('Adding User: %s' % new_user['email'])
    pc_api.user_add(new_user)
print('Done.')
