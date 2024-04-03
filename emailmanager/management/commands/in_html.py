import datetime
from django.core.management import BaseCommand
import jinja2
from worktimeprivate.management.commands.chek import num_days
from tabulate import tabulate

# def in_html_table():
#     data = tabulate(num_days('2021-03-10', datetime.date.today()[0]), tablefmt='html')
#     print(data)   
    # with open('worktimeprivate/templates/worktimeprivate/employee_calendar.html', 'wb+') as my_file:
    #     my_file.write(tabulate(num_days('2021-03-10', datetime.date.today()[0]), tablefmt='html'))

        #
# table = [['one','two','three'],['four','five','six'],['seven','eight','nine']]
####################################################################################################
# def tuple_to_html_join(data_tuple):
#     list_items = [f"<li>{item}</li>" for item in data_tuple]
#     html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
#     return html

# data = ("Apple", "Banana", "Orange", "Grapes")
# html_output = tuple_to_html_join(data)
# print(html_output)
########################################################################################
# f'<table> <tbody> <tr><td style="text-align: right;"> { (tabulate(i[2], tablefmt='html')[1])} </td><td style="text-align: right;">3</td></tr></tbody></table>'



class Command(BaseCommand):
   
    def handle(self, *args, **options):

        data_month = num_days(datetime.datetime.strptime('2023-11-10', "%Y-%m-%d").date(), datetime.date.today())
        # print(data_month)
        for i in data_month:

            for ii in i[2]:
                print(f"<table> <thead><tr> <th>Год: {i[0]}</th><th>Месяц: {i[1]}</th></tr></thead><tbody>{{ % for row in num_days % }} <tr>{{ % for col_value in row % }} <td> {{{{ col_value }}}} 
                </td></tr> </tbody></table>")
                
# >>> print(f"{{")
# {
# >>> print(f"}}")
# }
# >>> print(f"{{}}")
# {}
# >>> print(f"{{foo}}")
# {foo}
#####################################
#         <table>
#   {# если нужен хедер #}
#   <thead>
#     <tr>
#       <th>#</th>
#       {# здесь можно добавить имена колонок #}
#     </tr>
#   </thead>
#   <tbody>
#     {% for row in array %}
#     <tr>
#       {% for col_value in row %}
#       <td>{{ col_value }}</td>
#       {% endfor %}
#     </tr>
#     {% endfor %}
#   </tbody>
# </table>
        
        ###################################################################
#         template = jinja2.Template('''
# <table cellspacing="2" border="1" cellpadding="5">
                                     
#     {% for row in relations_table %}
#         <thead>
#     <tr>
#       <th>{{row[0]}}</th>
     
#     </tr>
#         </thead>                        
#     <tr>
#         {% for value in row %}
#         <td>{{ value }}</td>
#         {% endfor %}    
#     </tr>
#     {% endfor %}
# </table>
# ''')
#         relations_table = [[25, 98, 40, 17, 66, 65, 41, 11, 70, 58], [89, 93, 35, 89, 40, 17, 66, 65, 41, 99]]
        
        
#         # for i in data_month:
#         # html = template.render(relations_table=relations_table)
#         html = template.render(relations_table=data_month)
#         print(html)    
        ######################################################################################################
            # print(tabulate (i[2], tablefmt='html'))
            # (tabulate(i[2], tablefmt='html')
            # print(f'<table> <tbody> <tr><td style="text-align: right;"> {i [2]} </td><td style="text-align: right;">3</td></tr></tbody></table>')
            # if isinstance(i, list):
                # print(tabulate(i, tablefmt='html'))
        # print(tabulate(data), tablefmt='html')
        # in_html_table()
