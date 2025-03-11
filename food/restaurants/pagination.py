from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            
                'next_pagenumbr': self.page.next_page_number() if self.page.has_next() else None,
                'previous_number':self.page.previous_page_number() if self.page.has_previous()else None,
                'count': self.page.pagnator.count,
                'current_page':self.page.number,
                'results': data
            
             })