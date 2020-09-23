from pprint import pprint
import re


def add_role_change_instance(line, role):
    # change resource name
    if 'resource "aws_instance"' in line:
        print([re.sub(r'(?<=")\S+(?=")', r'\g<0>_' + role, line) if re.search(r'(?<=")\S+(?=")', line) != 'aws_instance' else ''][0])

    if 'vpc_security_group_ids ' in line:
        # chercher le dernier de la liste puis y ajouter le role
        # print((?<=data\.aws_security_group\.)\S+(?=\.id))


page = []

f = open("D:\\pxmt\\Ops_5_export\\Fleet\\live-region\\modules\\region-dynamic\\main.tf", "r")
for line in f:
    page.append(line.strip())

order = input("what did you wan't to do: ")
if order == 'add role':
    parameter = input('select instance: ')
    current_lime = ''  # check the past line
    result = []  # store the result
    flag = 0  # get the last line of the code block
    for counter, line in enumerate(page):
        # search for the instance only
        if parameter in line and 'resource "aws_instance"' in line:
            result.append(line)
            add_role_change_instance(line, 'partner')
            flag = counter  # add the counter in the flag
        if current_lime == '}' and line == '}' and flag != 0:
            # take the block code form first to last line
            for c in range(flag, counter+1):
                print(page[c])
                add_role_change_instance(page[c], 'partner')

            flag = 0
        current_lime = line

