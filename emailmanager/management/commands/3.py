from django.core.management import BaseCommand

# def dupl(data_2):##Ubiraem duplikati v otsortirovannom spiske data_
#             index = 0
#             a=[]
#             while len(data_2) >index and data_2[index] not in a:
#                    a.append(data_2[index])
#                    index += 1
#             index += 1
#             # print(a)
#             return a
def get_variants(a):
    print(a[0][1][0])
    for i in a[0]:
        print(i[0])
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        # dupl(['a','d','g', 'a', 'd'])
        get_variants([((1,2,3),(4,5,6))])