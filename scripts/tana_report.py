import os

import ppt.models
from ppt import models
from shared_models import models as shared_models

import csv

""" ---- to run --------------------------------------- """
""" > python manage.py shell                            """
""" >>> from scripts import tana_report                 """
""" >>> tana_report.generate_susan_report()             """
"""---------------------------------------------------- """

"""---------------------------------------------------- """
""" ---- handy to know if you make changes to the script"""
""" ---- and want to reload it without having to exit   """
""" ---- the shell ------------------------------------ """
""" >>> from importlib import reload                    """
""" >>> reload(tana_report)                             """
""" >>> tana_report.generate_susan_report()             """
"""---------------------------------------------------- """


def generate_susan_report():

    year = 2023
    branch = 3

    """ for this report we're using the fiscal year, the section name **and** if the ProjectYear has_field_component """
    project_years = models.ProjectYear.objects.filter(has_field_component=True, fiscal_year_id=year,
                                                      project__section__division__branch_id=branch)

    pro = ppt.models.Project.objects.filter(years__in=project_years)
    sect = shared_models.Section.objects.filter(ppt__in=pro)
    div = shared_models.Division.objects.filter(sections__in=sect)

    for d in div:

        pro_div = project_years.filter(project__section__division=d)

        """ The project year has a list of numbers for its status_choices, we'll create a 'dictionary' to use to replace """
        """ the id values with the proper text values from the ProjectYear.status_choice list """
        status_list = models.ProjectYear.status_choices
        status = {status_list[i][0]: status_list[i][1] for i in range(0, len(status_list))}

        """ We're going to dump our output into the dm_apps/dm_apps/scripts/fixtures/ directory """
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

        """ if the directory doesn't exist create it or we'll get an error when trying to create a file in the next step """
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        """ create the file, the f'report_name...' is a fancy way to *format* strings, you can put variables between the """
        """ brackets to append variables on to the string """
        f = open(os.path.join(output_path, f'susan_report_{d}_{year}.csv'), 'w', newline='', encoding='utf-8')

        """ create a Comma Separated Value file writer because we're writing csv files and this makes it easier to format"""
        writer = csv.writer(f)
        writer.writerow([
            'ID',
            'Status',
            'Title',
            'Division',
            'Section',
            'Functional group',
            'Start date of project',
            'End date of project',
            'Project years',
            'Project leads',
            'Project overview',

            'Des. Need for Vehicle',
            'Ship',
            'COIP number',
            'Insturments',

            'Requires Field Support Staff',
            'Support Details',

            'Requires Lab Work',
            'Is Lab Space Required',
            'Specialized Support',
            'Other Lab Requirements',

        ])

        for p in pro_div:
            years = ", ".join([y.fiscal_year.full for y in p.project.years.all()])
            leads_as_users = p.get_project_leads_as_users()
            leads = ""
            if leads_as_users:
                leads = ", ".join([u.first_name + " " + u.last_name for u in leads_as_users])

            writer.writerow([p.project.pk, status.get(p.status), p.project.title, p.project.section.division, p.project.section, p.project.functional_group,
                             p.start_date, p.end_date, years, leads, p.project.overview,

                             p.vehicle_needs, p.ship_needs, p.coip_reference_id, p.instrumentation,
                             p.requires_field_staff, p.field_staff_needs,
                             p.has_lab_component, p.requires_lab_space,
                             p.requires_other_lab_support, p.other_lab_support_needs
                             ])

        f.close()